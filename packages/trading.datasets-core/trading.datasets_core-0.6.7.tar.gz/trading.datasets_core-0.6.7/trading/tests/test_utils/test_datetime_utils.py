"""Tests for trading.datasets_core.utils."""
# pylint: disable=missing-class-docstring,missing-function-docstring

import datetime as dtlib

import pytest
import pytz

from trading.datasets_core.metadata.timeframe import Timeframe
from trading.datasets_core.utils.datetime_utils import get_valid_start_end
from trading.datasets_core.utils.datetime_utils import to_datetime
from trading.datasets_core.utils.datetime_utils import to_iso8601
from trading.datasets_core.utils.datetime_utils import to_milliseconds
from trading.datasets_core.utils.datetime_utils import to_seconds


@pytest.fixture(name="datetime", scope="class")
def fixture_datetime():
    return to_datetime("2021-01-01 00:00:00+00:00")


class TestDateTimeUtils:

    def test_iso8601_conversion(self, datetime):
        assert to_iso8601([]) is None
        assert to_iso8601(None) is None
        assert to_iso8601(514862627000) == "1986-04-26T01:23:47.000Z"
        assert to_iso8601(514862627559) == "1986-04-26T01:23:47.559Z"
        assert to_iso8601(514862627062) == "1986-04-26T01:23:47.062Z"
        assert to_iso8601(datetime) == "2021-01-01T00:00:00.000Z"
        assert to_iso8601("2021") == "2021-01-01T00:00:00.000Z"

    def test_seconds_conversion(self, datetime):
        assert to_seconds([]) is None
        assert to_seconds(None) is None
        assert to_seconds(514862627000) == 514862627.000
        assert to_seconds(514862627559) == 514862627.559
        assert to_seconds(514862627062) == 514862627.062
        assert to_seconds(datetime) == 1609459200.000

    def test_milliseconds_conversion(self, datetime):
        assert to_milliseconds([]) is None
        assert to_milliseconds(None) is None
        assert to_milliseconds(514862627000) == 514862627000
        assert to_milliseconds(514862627559) == 514862627559
        assert to_milliseconds(514862627062) == 514862627062
        assert to_milliseconds(datetime) == 1609459200000

    def test_datetime_conversion(self, datetime):
        assert to_datetime([]) is None
        assert to_datetime(None) is None
        assert to_datetime(datetime) == datetime

    def test_validating_start_and_end_datetimes(self):
        timeframe = Timeframe(interval=1, unit="d")
        expected_start = to_datetime("2020-12-31")
        expected_end = to_datetime("2021-01-01")

        assert get_valid_start_end(
            None, "2021-01-01", timeframe) == (expected_start, expected_end)
        assert get_valid_start_end(
            "2020-12-31", None, timeframe) == (expected_start, expected_end)

        # Generate the expected now datetime but add a couple of
        # seconds to account for additional runtime that passed
        now = dtlib.datetime.utcnow().replace(tzinfo=pytz.utc)
        now += dtlib.timedelta(seconds=60)

        result_start, result_end = get_valid_start_end(
            None, None, timeframe)

        assert result_end.year == now.year
        assert result_end.month == now.month
        assert result_end.day == now.day
        assert result_start < now

        # Test if calculated end is over now
        assert get_valid_start_end(now, None, timeframe)[-1] <= now

        test_start = now - dtlib.timedelta(days=1)
        result_start, result_end = get_valid_start_end(
            test_start, None, timeframe)

        assert result_end.year == now.year
        assert result_end.month == now.month
        assert result_end.day == now.day
        assert result_start == test_start

    def test_validating_start_and_end_excluding_latest(self):
        timeframe = Timeframe(interval=1, unit="d")
        now = dtlib.datetime.utcnow().replace(tzinfo=pytz.utc)
        result_start, result_end = get_valid_start_end(
            None, None, timeframe, include_latest=False)

        assert result_end.year == now.year
        assert result_end.day != now.day
        assert result_end < now
