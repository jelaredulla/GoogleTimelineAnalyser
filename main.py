import argparse
import calendar
import datetime
import json
import math
import os
import pandas


CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))


def validate_filepaths(filepaths):
    for filepath in filepaths:
        if not os.path.isfile(filepath):
            raise ValueError('Filepath "{}" is invalid!'.format(filepath))


def get_tax_months(tax_year):
    tax_months = []

    for i in range(7, 13):
        tax_months.append((tax_year, calendar.month_name[i]))

    for i in range(1, 7):
        tax_months.append((tax_year + 1, calendar.month_name[i]))

    return tax_months


def summarise(filepath):
    summary_data = []

    with open(filepath, 'r') as opened_file:
        file_contents = json.load(opened_file)

        timeline = file_contents.get('timelineObjects', [])

        for activity in timeline:
            timeline_categories = list(activity.keys())

            if len(timeline_categories) != 1:
                raise RuntimeError('Uh oh, timeline category ambiguous: {}'.format(', '.join(timeline_categories)))

            timeline_category = timeline_categories[0]

            activity_data = activity[timeline_category]

            start_timestamp = int(activity_data['duration']['startTimestampMs']) / 1000
            end_timestamp = int(activity_data['duration']['endTimestampMs']) / 1000

            start_datetime = datetime.datetime.fromtimestamp(start_timestamp)
            end_datetime = datetime.datetime.fromtimestamp(end_timestamp)

            duration = end_datetime - start_datetime
            duration_seconds = duration.seconds
            duration_hours = duration_seconds // (60 * 60)
            duration_minutes = math.floor((duration_seconds % (60 * 60)) / 60)
            assert (duration_minutes < 60)

            duration_hours = str(duration_hours).zfill(2)
            duration_minutes = str(duration_minutes).zfill(2)

            activity_summary = {
                'START_DATE': start_datetime.strftime('%Y-%m-%d'),
                'START_TIME': start_datetime.strftime('%H:%M'),
                'END_DATE': end_datetime.strftime('%Y-%m-%d'),
                'END_TIME': end_datetime.strftime('%H:%M'),
                'DURATION': '{}:{}'.format(duration_hours, duration_minutes),
                'TIMELINE_CATEGORY': timeline_category,
            }

            location_data = activity_data.get('location', {})

            semantic_type = location_data.get('semanticType', '')
            if not semantic_type:
                semantic_type = location_data.get('name', '')

            address = location_data.get('address', '')
            if address:
                address = address.replace('\n', ', ')

            activity_summary.update({
                'SEMANTIC_TYPE': semantic_type,
                'ADDRESS': address,
            })

            summary_data.append(activity_summary)

    return summary_data


def get_office_days(year_summary):
    days_at_office = []

    relevant_days = year_summary[year_summary['SEMANTIC_TYPE'] == 'TYPE_WORK']
    assert (relevant_days['START_DATE'].equals(relevant_days['END_DATE']))

    office_dates = relevant_days['START_DATE'].unique()

    for date in office_dates:
        weekday = datetime.date.fromisoformat(date).weekday()
        if weekday > 5:
            print('{} questionable because it was a {}'.format(date, calendar.day_name[weekday]))

        office_day_data = relevant_days[relevant_days['START_DATE'] == date]
        durations = list(office_day_data['DURATION'])

        days_at_office.append({
            'DATE': date,
            'DURATION': sum_duration(durations),
        })

    return pandas.DataFrame(days_at_office)


def sum_duration(durations):
    total_minutes = 0

    for duration in durations:
        hours, minutes = duration.split(':')
        total_minutes += int(hours) * 60 + int(minutes)

    total_hours = total_minutes // 60
    total_minutes = (total_minutes % 60)
    total_duration = '{}:{}'.format(str(total_hours).zfill(2), str(total_minutes).zfill(2))

    return total_duration


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyse your Google timeline to find the time you spent at the office')
    parser.add_argument('input_dir', help='Directory containing your Google Maps timeline data')
    parser.add_argument('--output_dir', default=os.path.join(CURRENT_DIRECTORY, 'output'), help='Directory to write the output')
    parser.add_argument('--tax_year', type=int, default=2020, help='Beginning tax year')
    args = parser.parse_args()

    initials = 'AR'
    input_dir = args.input_dir
    output_dir = args.output_dir
    tax_year = args.tax_year

    print('Google timeline data is in:', input_dir)
    print('Analysing timeline for the {} tax_year...'.format(tax_year))
    print('Summary data will be written to:', output_dir)

    tax_months = get_tax_months(tax_year)

    relevant_filepaths = []
    for tax_month in tax_months:
        year, month_name = tax_month
        filepath = os.path.join(input_dir,
                                'Location History',
                                'Semantic Location History',
                                str(year),
                                '{}_{}.json'.format(year, month_name.upper()))
        relevant_filepaths.append(filepath)

    validate_filepaths(relevant_filepaths)

    if not os.path.exists(output_dir):
        print('Output directory does not exist, so making it...')
        os.makedirs(output_dir)

    year_summary = []
    for filepath in relevant_filepaths:
        print('Parsing file "{}"...'.format(os.path.basename(filepath)))

        month_summary = summarise(filepath)
        year_summary.extend(month_summary)

    year_summary = pandas.DataFrame(year_summary)
    year_summary.sort_values(by=['START_DATE', 'START_TIME'], inplace=True)

    year_summary_filepath = os.path.join(output_dir, '{}-{}_location_summary.csv'.format(tax_year, tax_year + 1))
    year_summary.to_csv(year_summary_filepath, index=False)

    office_days = get_office_days(year_summary)

    office_days_filepath = os.path.join(output_dir, '{}-{}_office_days.csv'.format(tax_year, tax_year + 1))
    office_days.to_csv(office_days_filepath, index=False)


    print('\n\n')
    print('Days in the office:', len(office_days))
    print('Total time in the office:', sum_duration(list(office_days['DURATION'])))