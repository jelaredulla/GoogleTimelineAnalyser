import datetime
import pytz


def as_datetime(value: str, tz_info: datetime.tzinfo):
    formatted_value = value.split('.')[0].split('Z')[0]
    dt_value = datetime.datetime.fromisoformat(formatted_value)

    # To get the time in local timezone
    utc_value = dt_value.replace(tzinfo=pytz.utc)
    return utc_value.astimezone(tz_info)


def get_duration_in_hours(duration: datetime.timedelta) -> float:
    return duration.seconds / (60 * 60)


def sum_duration(durations):
    """
    Helper function to sum time strings

    @param durations <list>: duration time strings in the format HH:MM
    @returns the summation of the durations in the same format HH:MM
    """
    total_minutes = 0

    for duration in durations:
        hours, minutes = duration.split(':')
        total_minutes += int(hours) * 60 + int(minutes)

    total_hours = total_minutes // 60
    total_minutes = (total_minutes % 60)
    total_duration = '{}:{}'.format(str(total_hours).zfill(2), str(total_minutes).zfill(2))

    return total_duration