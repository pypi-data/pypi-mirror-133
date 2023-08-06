""" int_date contains utilities for an int representation of a date

An int date is an integer that represents a date, such as:

20101215 stands for Dec. 15th, 2015

The package allows the users to retrieve these int numbers from ``str``,
``datetime``, ``date`` or ``float``.

It supplies some utilities such as ``get_interval``, ``get_workdays``, etc.
"""
from datetime import datetime, timedelta, date

import six
from dateutil import rrule

__author__ = 'Cedric Zhuang'


def int_date(value):
    """ Convert the input into a date

    Convert the value to an int date.  It accepts numbers, string,
    ``datetime.datetime`` or ``datetime.date``

    If the input is string, it could be:
    2015-01-30
    2015/01/30
    20150130

    :param value: int, float or string representation of a date
    :exception: ValueError if input could not be converted
    :return: int date
    """
    if value is None:
        ret = None
    else:
        if isinstance(value, six.string_types):
            value = _convert_date(value)
        if value is None:
            raise ValueError("cannot process {}".format(value))

        if isinstance(value, (datetime, date)):
            ret = value.year * 10000 + value.month * 100 + value.day
        else:
            ret = int(value)
            # check if it's a valid date
            _ = _to_date(ret)
    return ret


def to_date(value):
    """Convert a ``int`` date to a :class:`datetime` instance

    :param value: a representation of the int date
    :return: datetime instance of the date
    """
    date_str = "%s" % int_date(value)
    return _str_to_date(date_str)


def get_interval(left, right):
    """ get interval (in day) between two int dates

    :param left: first int date
    :param right:  second int date
    :return: difference (in day), negative if second date is earlier
             than the first one.
    """
    left_date = to_date(left)
    right_date = to_date(right)
    delta = right_date - left_date
    return delta.days


def get_workdays(left, right):
    """get the number of business days between two int dates.

    :param left: first date in string or int
    :param right:  second date in string or int
    :return: business days, negative if second date is earlier
             than the first one.
    """
    int_left = int_date(left)
    int_right = int_date(right)
    reverse = False
    if int_left > int_right:
        reverse = True
        int_left, int_right = int_right, int_left
    date_start_obj = _to_date(int_left)
    date_end_obj = _to_date(int_right)
    weekdays = rrule.rrule(rrule.DAILY,
                           byweekday=range(0, 5),
                           dtstart=date_start_obj,
                           until=date_end_obj)
    weekdays = len(list(weekdays))
    if reverse:
        weekdays = -weekdays
    return weekdays


def from_diff(i_date, delta_day):
    """calculate new int date with a start date and a diff (in days)

    :param i_date: the starting date
    :param delta_day: diff (in days), negative means past
    :return: result date
    """
    value = to_date(i_date)
    value += timedelta(delta_day)
    return int_date(value)


def today():
    """Get the today of int date

    :return: int date of today
    """
    the_day = date.today()
    return int_date(the_day)


def in_year(day, *years):
    """check if day is in years list or year

    :param day: date
    :param years: list of years or year
    :return: true if in, otherwise false
    """
    year = int(int_date(day) / 1e4)
    return _in_range_or_equal(year, years)


def in_month(day, *months):
    """check if day is in months list or month

    :param day: date
    :param months: list of months or month
    :return: true if in, otherwise false
    """
    month = int(int_date(day) % 10000 / 100)
    return _in_range_or_equal(month, months)


def in_date(day, *dates):
    """check if day is in dates list or date

    :param day: date
    :param dates: list of dates or date
    :return: true if in, otherwise false
    """
    the_date = int(int_date(day) % 100)
    return _in_range_or_equal(the_date, dates)


def _in_range_or_equal(value, to_compare):
    return value in to_compare


def _str_to_date(date_str, format_str=None):
    """ Convert a string to a date object

    :param date_str: the input date string
    :param format_str: format of the date string
    :exception: ValueError if string is not a valid date
    :return: the date object
    """
    if format_str is None:
        format_str = "%Y%m%d"
    try:
        ret = datetime.strptime(date_str, format_str).date()
    except ValueError:
        raise ValueError("input is not a valid date: {}".format(date_str))
    return ret


def _convert_date(date_str):
    """convert a *date_str* to int date

    convert string '2015-01-30' to int 20150130
    convert string '2015/01/30' to int 20150130
    :return: int format of date
    """
    ret = None

    if '-' in date_str:
        ret = _str_to_date(date_str, "%Y-%m-%d")
    elif '/' in date_str:
        ret = _str_to_date(date_str, "%Y/%m/%d")
    elif len(date_str) == 8:
        ret = _str_to_date(date_str, "%Y%m%d")
    return ret


def _to_date(day):
    """ Convert an integer to a date object

    :param day: an integer represents the date
    :exception: ValueError if input is not a valid date
    :return: the date object
    """
    int_day = day
    day = int_day % 100
    month = (int_day % 10000 - day) / 100
    year = int_day / 10000

    return date(int(year), int(month), int(day))
