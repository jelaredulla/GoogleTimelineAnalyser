import calendar
import datetime

def get_tax_months(tax_year):
    """
    Helper function to get the month+year for all the months of the given tax year

    @param tax_year <int>: the beginning year of the tax year, e.g. 2020 for the 2020-2021 tax year
    @returns list of (year, month name) tuples for the twelve months of the given tax year
    """
    tax_months = []

    for i in range(7, 13):
        tax_months.append((tax_year, calendar.month_name[i]))

    for i in range(1, 7):
        tax_months.append((tax_year + 1, calendar.month_name[i]))

    return tax_months


def get_work_dates(tax_year):
    start_tax_date = datetime.date.fromisoformat('{}-07-01'.format(tax_year))
    end_tax_date = datetime.date.fromisoformat('{}-06-30'.format(tax_year + 1))

    dates = []
    date = start_tax_date
    while date <= end_tax_date:
        # limit to weekdays only by excluding weekends
        if date.weekday() < 5:
            dates.append(date)

        date = date + datetime.timedelta(days=1)

    return dates
