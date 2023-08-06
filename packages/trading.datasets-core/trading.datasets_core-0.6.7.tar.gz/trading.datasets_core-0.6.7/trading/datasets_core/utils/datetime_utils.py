"""Module containing datetime-related utility functions."""

from __future__ import annotations

import datetime as dtlib

from dateutil import parser
import pytz

from trading.datasets_core.metadata.timeframe import Timeframe


__all__ = [
    # Function exports
    "get_valid_start_end",
    "to_datetime",
    "to_iso8601",
    "to_milliseconds",
    "to_seconds",
]


def get_valid_start_end(
    start: dtlib.datetime | str | int | None,
    end: dtlib.datetime | str | int | None,
    timeframe: Timeframe,
    timeframe_multiplier: int = 1,
    include_latest: bool = True,
) -> tuple[dtlib.datetime, dtlib.datetime]:

    """Validates and fills up the start and end times.

    Since we want the user to be able to readily use
    the `fetch_ohlcv()` without thinking much about this small detail,
    we automatically fill up the starting and end timestamps
    based on the parameters provided. Here are the different
    fill up cases:

    * If `start` and `end` are not provided, `end` is assigned the
      latest date and `start` is `end` minus the limit of one fetch
      based on the indicated exchange.
    * If either `start` and `end` are not provided but the other one
      is, we just add or subtract the same fetch limit to compute
      for `end` or `start`.
    * Lastly, if both are provided by the user, we use those without
      any other processing.

    Arguments:
        start: Starting datetime of the data to be fetched.
            The input argument can be a string indicating a
            valid datetime-like string or a number indicating the
            timestamp in milliseconds.
        end: Ending timestamp of the data to be fetched.
            The input argument can be a string indicating a
            valid datetime-like string or a number indicating the
            timestamp in milliseconds.
        timeframe: Timeframe of the candlestick data to fetch. Some
            examples of valid timeframe strings are `"2h"` for two
            hour, `"1d"` for one day, and `"1w"` for 1 week.
        include_latest: If the `include_latest` variable is set to
            `True`, the latest OHLCV data is not returned since it
            is not finished yet. If set to `False`, then the
            unfinished data at the time `fetch_ohlcv()` was called
            will be returned.

    Returns:
        A tuple containing the validated start and ending datetimes.
    """

    start = to_datetime(start)
    end = to_datetime(end)
    now = dtlib.datetime.utcnow().replace(tzinfo=pytz.utc)

    # Create a time adjustment variable to dynamically determine
    # the start or end times if ever one of them or both of them
    # are missing or invalid values.
    time_adjustment = timeframe.to_timedelta() * timeframe_multiplier

    if not start and end:
        start = end - time_adjustment
    elif start and not end:
        end = start + time_adjustment
        if end > now:
            end = now
    elif not start and not end:
        end = now
        start = end - time_adjustment

    # Start and end are provided, check if start is less than end
    # if end is earlier than start just swap the values
    elif start > end:
        start, end = (end, start)

    # If the end date is not less than the threshold
    # then don't include it, subtract timeframe from end
    if not include_latest:
        if end >= now:
            end -= timeframe.to_timedelta()

    return start, end


def to_iso8601(value: dtlib.datetime | str | int | None) -> str | None:
    if not value:
        return None

    value_ms = to_milliseconds(value)
    value = to_datetime(value)

    value_iso8601 = value.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-6] + "{:03d}"
    value_iso8601 = value_iso8601.format(int(value_ms) % 1000) + "Z"

    return value_iso8601


def to_milliseconds(value: str | int | None) -> int | None:
    if not value:
        return None

    if isinstance(value, int) and len(str(value)) >= 12:
        return value

    return to_seconds(value) * 1000


def to_seconds(value: str | int | None) -> float | int | None:
    if not value:
        return None

    if isinstance(value, int) and len(str(value)) >= 12:
        return value / 1000

    return to_datetime(value).timestamp()


def to_datetime(value: str | int | None) -> dtlib.datetime | None:
    """Returns the UTC datetime equivalent of the input value.

    Arguments:
        value: The generic input. This can be a string or an integer.
            If its a datetime string, its just parsed automatically.
            If its a number like string or an actual integer,
            we check if its a Unix timestamp and is convert accordingly.

    Return:
        A datetime object.

    """
    if not value:
        return None

    value = str(value)
    if value.isdigit() and len(value) >= 12:
        datetime = dtlib.datetime.utcfromtimestamp(int(value) / 1000.0)
    else:
        first_day_current_yr = dtlib.datetime(dtlib.datetime.now().year, 1, 1)
        datetime = parser.parse(value, default=first_day_current_yr)

    return datetime.replace(tzinfo=datetime.tzinfo or pytz.utc)
