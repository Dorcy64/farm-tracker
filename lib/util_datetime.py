import datetime
from datetime import timedelta
import pytz
import time


def tzware_datetime():
    """
    Return a timezone aware datetime.
    :return: Datetime
    """
    return datetime.datetime.now(pytz.utc)


def timedelta_days(days, compare_date=None):
    """
    Return a new datetime with a month offset applied.
    :param days: Amount of days to offset
    :type days: int
    :param compare_date: Date to compare at
    :type compare_date: date
    :return: datetime
    """
    if compare_date is None:
        compare_date = datetime.datetime.now(pytz.utc)

    return compare_date + datetime.timedelta(days)


def time_now_string():
    return datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_")


def time_now_input():
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")


def format_time(utc_datetime):
    new_dt = str(utc_datetime)[:19]
    dt_object = datetime.datetime.strptime(new_dt, "%Y-%m-%d %H:%M:%S")
    now_timestamp = time.time()
    offset = datetime.datetime.fromtimestamp(now_timestamp) - datetime.datetime.utcfromtimestamp(now_timestamp)
    new_time = dt_object + offset
    return datetime.datetime.strftime(new_time, "%Y-%m-%dT%H:%M")


def current_year():
    """
    Return this year.
    :return: int
    """
    return datetime.datetime.now(pytz.utc).year


def convert_to_utc(time_input, tzname, is_dst=None):
    tz = pytz.timezone(tzname)

    dt = tz.localize(time_input, is_dst=is_dst)
    return dt.astimezone(pytz.utc)
