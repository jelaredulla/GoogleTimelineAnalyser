import calendar
from collections import defaultdict
import datetime
import json
import os
import pandas
from re import search
import pytz
from typing import List

import tax_utils
import dt_utils

CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

HOME = 'home'
WORK = 'the office'

SEMANTIC_TYPE_HOME = 'TYPE_HOME'
SEMANTIC_TYPE_WORK = 'TYPE_WORK'


def is_similar_address(address, substrings):
    for substring in substrings:
        similar = search(substring, address)
        if similar:
            return True

    return False


def summarise(
        filepath: str,
        home_substrings: List[str],
        work_substrings: List[str],
        tz_info: datetime.tzinfo):
    """
    Creates a summary for all the data in the specified file

    @param filepath: full path to a timeline JSON
    @returns list of timeline activities, each summarised by START_DATE, START_TIME, END_DATE, END_TIME, DURATION, TIMELINE_address_type, SEMANTIC_TYPE, ADDRESS
    """
    summary_data = []

    with open(filepath, 'r', encoding='utf8') as opened_file:
        file_contents = json.load(opened_file)

        timeline = file_contents.get('timelineObjects', [])

        for activity in timeline:
            timeline_categories = list(activity.keys())

            if len(timeline_categories) != 1:
                raise RuntimeError('Uh oh, timeline address_type ambiguous: {}'.format(', '.join(timeline_categories)))

            timeline_address_type = timeline_categories[0]

            activity_data = activity[timeline_address_type]

            start_datetime = dt_utils.as_datetime(activity_data['duration']['startTimestamp'], tz_info)
            end_datetime = dt_utils.as_datetime(activity_data['duration']['endTimestamp'], tz_info)

            activity_summary = {
                'START_DATETIME': start_datetime,
                'END_DATETIME': end_datetime,
                'START_DATE': start_datetime.strftime('%Y-%m-%d'),
                'START_TIME': start_datetime.strftime('%H:%M'),
                'END_DATE': end_datetime.strftime('%Y-%m-%d'),
                'END_TIME': end_datetime.strftime('%H:%M'),
                'DURATION (hrs)': dt_utils.get_duration_in_hours(end_datetime - start_datetime),
                'TIMELINE_address_type': timeline_address_type,
            }

            location_data = activity_data.get('location', {})

            semantic_type = location_data.get('semanticType', '')
            if not semantic_type:
                semantic_type = location_data.get('name', '')

            address = location_data.get('address', '')
            if address:
                address = address.replace('\n', ', ')

            address_type = ''
            if semantic_type == SEMANTIC_TYPE_HOME:
                address_type = HOME
            elif semantic_type == SEMANTIC_TYPE_WORK:
                address_type = WORK
            elif is_similar_address(address, home_substrings):
                address_type = HOME
            elif is_similar_address(address, work_substrings):
                address_type = WORK
            elif address:
                address_type = address
            else:
                address_type = 'Unknown'

            activity_summary.update({
                'SEMANTIC_TYPE': semantic_type,
                'ADDRESS': address,
                'ADDRESS_TYPE': address_type
            })

            summary_data.append(activity_summary)

    return summary_data


def analyze_location_during_work_hours(
        location_data: pandas.DataFrame,
        work_dates: List[datetime.datetime],
        work_start_time: datetime.time,
        work_end_time: datetime.time,
        tz_info: datetime.tzinfo):
    """
    TODO: this comment
    """
    all_work_day_summaries = []
    no_data_dates = 0
    for date in work_dates:
        work_start_datetime = datetime.datetime.combine(
            date=date,
            time=work_start_time,
            tzinfo=tz_info
        )
        work_end_datetime = datetime.datetime.combine(
            date=date,
            time=work_end_time,
            tzinfo=tz_info
        )

        activities = location_data[(location_data['END_DATETIME'] >= work_start_datetime)
                                  & (location_data['START_DATETIME'] <= work_end_datetime)]

        work_day_summary = defaultdict(float)
        if len(activities):
            for _, activity in activities.iterrows():
                address_type = activity['ADDRESS_TYPE']

                if address_type == WORK:
                    duration = activity['END_DATETIME'] - activity['START_DATETIME']
                else:
                    # Calculate time spent at this address during work hours
                    work_hours_activity_start = max(work_start_datetime, activity['START_DATETIME'])
                    work_hours_activity_end = min(work_end_datetime, activity['END_DATETIME'])
                    duration =  work_hours_activity_end - work_hours_activity_start

                work_day_summary[address_type] += dt_utils.get_duration_in_hours(duration)
        else:
            no_data_dates += 1

        work_day_summary['date'] = date
        work_day_summary['day'] = calendar.day_name[date.weekday()]
        all_work_day_summaries.append(work_day_summary)

    result = pandas.DataFrame(data=all_work_day_summaries)

    # Order the columns so that date, day, HOME & WORK are first
    existing_columns = list(result.columns)
    ordered_columns = []
    for column in ['date', 'day', HOME, WORK]:
        if column in existing_columns:
            ordered_columns.append(column)
            existing_columns.remove(column)
    ordered_columns.extend(existing_columns)

    return result[ordered_columns], no_data_dates


def prompt_for_substrings(address_type):
    print()

    substrings = []
    while True:
        substring = input('Enter substring for {} (e.g. suburb or postcode): '.format(address_type))
        if not substring:
            break

        substrings.append(substring)
        print('Addresses with any of the substrings {} will be identified as {}'.format(substrings, address_type))
        print('If these are all the substrings to use, hit Enter to continue')

    return substrings


if __name__ == '__main__':
    # Prompt the user for the tax year
    tax_year = input('Tax year (e.g. 2021): ')
    if not tax_year.isdigit():
        print('Tax year {} is invalid - aborting'.format(tax_year))
        exit(1)
    tax_year = int(tax_year)

    # Prompt the user for the full path to their Google location history
    input_dir = input('\nPath to Google location history (should end in "Semantic Location History"): ')
    input_dir = input_dir.rstrip('\\/')
    if not os.path.isdir(input_dir) or os.path.basename(input_dir) != 'Semantic Location History':
        print('\nPlease specify the full path to the "Semantic Location History" folder'
              ' from your Google Takeout download; it should end with "\\Semantic Location History"')
        exit(1)

    # Prompt the user for the full path to the output directory
    default_output_dir = os.path.join(CURRENT_DIRECTORY, 'GoogleTimelineAnalyser Output')
    output_dir = input('\nDirectory where results will be written (defaults to "{}"): '.format(default_output_dir))
    if output_dir and not os.path.isdir(output_dir):
        print('Output directory "{}" is invalid. Using default directory instead.'.format(output_dir))
        output_dir = ''
    if not output_dir:
        output_dir = default_output_dir
    print('Summary data will be written to:', output_dir)

    # Prompt the user for substrings to identify home addresses
    home_substrings = prompt_for_substrings(HOME)

    # Prompt the user for substring to identify work addresses
    work_substrings = prompt_for_substrings(WORK)

    # Prompt the user for their work start time
    raw_start_time = input('\nWhat time do you start work usually (HH:MM)? ')
    try:
        work_start_time = datetime.time.fromisoformat(raw_start_time)
    except:
        print('Start time of "{}" was invalid - aborting'.format(raw_start_time))
        exit(1)

    # Prompt the user for their work end time
    raw_end_time = input('What time do you end work usually (HH:MM)? ')
    try:
        work_end_time = datetime.time.fromisoformat(raw_end_time)
    except:
        print('End time of "{}" was invalid - aborting'.format(raw_end_time))
        exit(1)

    # Prompt the user for their timezone
    default_timezone_name = 'Australia/Sydney'
    timezone_name = input('\nWhat timezone are you in (defaults to "{}")? '.format(default_timezone_name))
    if timezone_name:
        try:
            local_tz =  pytz.timezone(timezone_name)
        except:
            print('Timezone "{}" was invalid - aborting'.format(timezone_name))
            exit(1)
    else:
        timezone_name = default_timezone_name
        local_tz = pytz.timezone(timezone_name)
    print('Using timezone:', timezone_name)

    print('\nAnalysing timeline for the {}-{} tax_year...'.format(tax_year, tax_year + 1))

    # Get the tax month / year combinations
    tax_months = tax_utils.get_tax_months(tax_year)

    # Construct the relevant timeline JSON files based on the month / year combinations
    relevant_filepaths = []
    for tax_month in tax_months:
        year, month_name = tax_month
        filepath = os.path.join(input_dir,
                                str(year),
                                '{}_{}.json'.format(year, month_name.upper()))
        relevant_filepaths.append(filepath)

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        print('\nOutput directory does not exist, so making it...')
        os.makedirs(output_dir)

    print()

    # Parse each month's timeline JSON and add it to the year summary
    year_summary = []
    for filepath in relevant_filepaths:
        print('Attempting to parse file "{}" (full path is "{}")'.format(os.path.basename(filepath), filepath), end='')

        # Check whether the constructed filepath actually exists
        if os.path.isfile(filepath):
            print('    - file exists so parsing it...')
            month_summary = summarise(
                filepath=filepath,
                home_substrings=home_substrings,
                work_substrings=work_substrings,
                tz_info=local_tz
            )
            year_summary.extend(month_summary)
        else:
            print('    - not found.')
    print()

    # Check that the summary isn't empty
    if len(year_summary) == 0:
        print('\nCould not find any activities to summarise')
        exit(1)

    # Make a year summary dataframe and sort it chronologically
    year_summary = pandas.DataFrame(year_summary)
    year_summary.sort_values(by=['START_DATE', 'START_TIME'], inplace=True)

    # Write the year summary to file, so maybe a human can sanity-check this intermediate step
    year_summary_filepath = os.path.join(output_dir, '{}-{}_location_summary.csv'.format(tax_year, tax_year + 1))
    year_summary.to_csv(year_summary_filepath, index=False)

    work_dates = tax_utils.get_work_dates(tax_year=tax_year)
    work_days_summary, no_data_dates = analyze_location_during_work_hours(
        location_data=year_summary,
        work_dates=work_dates,
        work_start_time=work_start_time,
        work_end_time=work_end_time,
        tz_info=local_tz
    )

    # Write the work days summary to file, so maybe a human can sanity-check it
    work_days_filepath = os.path.join(output_dir, '{}-{}_work_days.csv'.format(tax_year, tax_year + 1))
    work_days_summary.to_csv(work_days_filepath, index=False)

    print('\nThere were {} work dates with no location data whatsoever'.format(no_data_dates))

    # Hours in the office
    office_hours = work_days_summary[WORK].sum()
    print('Spent {:.2f} hours in the office'.format(office_hours))

    # Hours working from home
    wfh_hours = work_days_summary[HOME].sum()
    print('Spent {:.2f} hours at home during working hours'.format(wfh_hours))
    shortcut_rate = 0.8
    shortcut_method = shortcut_rate * wfh_hours
    print('${:.2f} * {:.2f} = {:.2f}'.format(shortcut_rate, wfh_hours, shortcut_method))
    print('So you can claim approximately ${:.2f} for working from home'.format(shortcut_method))
