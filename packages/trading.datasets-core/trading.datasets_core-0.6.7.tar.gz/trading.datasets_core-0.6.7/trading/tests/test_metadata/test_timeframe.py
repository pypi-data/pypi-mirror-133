"""Tests for trading.datasets_core.metadata.timeframe_unit."""
# pylint: disable=missing-class-docstring,missing-function-docstring

import pytest

from dateutil.relativedelta import relativedelta

from trading.datasets_core.errors import InvalidTimeframeError
from trading.datasets_core.errors import UnknownTimeframeUnitError
from trading.datasets_core.metadata.timeframe import Timeframe
from trading.datasets_core.metadata.timeframe_unit import TimeframeUnit


@pytest.fixture(name="timeframe", scope="class")
def fixture_timeframe():
    return Timeframe("3d")


class TestTimeframe:

    def test_initialization(self, timeframe):
        timeframe.interval = 3
        timeframe.unit = "d"
        assert isinstance(timeframe, Timeframe)
        assert timeframe.interval == 3
        assert timeframe.unit == "d"

        timeframe = Timeframe(interval="8", unit="h")
        assert timeframe.interval == 8
        assert timeframe.unit == "h"

        timeframe = Timeframe(timeframe)
        assert timeframe.interval == 8
        assert timeframe.unit == "h"

        timeframe = Timeframe()
        assert not timeframe.interval
        assert not timeframe.unit

        timeframe = Timeframe(interval=8.0, unit="h")
        assert timeframe.interval == 8
        assert timeframe.unit == "h"

        timeframe = Timeframe("250ms")
        assert timeframe.interval == 250
        assert timeframe.unit == "ms"

        with pytest.raises(InvalidTimeframeError):
            Timeframe(interval=["invalid", "interval"], unit="h")

        with pytest.raises(InvalidTimeframeError):
            Timeframe(interval={1: 2, 3: 4}, unit="h")

    def test_interval_property(self, timeframe):
        timeframe.interval = 3
        assert isinstance(timeframe.interval, int)
        assert timeframe.interval == 3

        timeframe.interval = 0
        assert isinstance(timeframe.interval, int)
        assert timeframe.interval == 0

        timeframe.interval = -5
        assert isinstance(timeframe.interval, int)
        assert timeframe.interval == -5

        timeframe.interval = "-9.999"
        assert isinstance(timeframe.interval, int)
        assert timeframe.interval == -9

        timeframe.interval = "4.7"
        assert isinstance(timeframe.interval, int)
        assert timeframe.interval == 4

        timeframe.interval = 12.5
        assert isinstance(timeframe.interval, int)
        assert timeframe.interval == 12

        timeframe.interval = "RANDOM VALUE"
        assert timeframe.interval is None

        timeframe.interval = None
        assert timeframe.interval is None

        timeframe.interval = [1, 2, 3]
        assert timeframe.interval is None

        timeframe.interval = ""
        assert timeframe.interval is None

    def test_unit_property(self, timeframe):
        timeframe.unit = "d"
        assert isinstance(timeframe.unit, TimeframeUnit)
        assert str(timeframe.unit) == "d"

        timeframe.unit = "m"
        assert isinstance(timeframe.unit, TimeframeUnit)
        assert str(timeframe.unit) == "m"

        with pytest.raises(UnknownTimeframeUnitError):
            timeframe.unit = "some unknown unit"

        with pytest.raises(UnknownTimeframeUnitError):
            timeframe.unit = "D"

    def test_equality_operation(self, timeframe):
        timeframe.interval = 3
        timeframe.unit = "d"
        assert timeframe == timeframe  # pylint: disable=comparison-with-itself
        assert timeframe == "3d"

        timeframe.interval = 2
        timeframe.unit = "y"
        assert timeframe == timeframe  # pylint: disable=comparison-with-itself
        assert timeframe == "2y"

        assert Timeframe("1d") == Timeframe("24h")
        assert Timeframe() == Timeframe()

    def test_to_repr_conversion(self, timeframe):
        assert repr(timeframe) == (
            f"{timeframe.__class__.__name__}("
            f"interval={timeframe.interval!r}, "
            f"unit={timeframe.unit!r}"
            ")"
        )

    def test_to_str_conversion(self, timeframe):
        timeframe.interval = 3
        timeframe.unit = "d"
        assert str(timeframe) == "3d"

        timeframe.interval = 5.7
        timeframe.unit = "h"
        assert str(timeframe) == "5h"

        timeframe.interval = None
        timeframe.unit = None
        assert str(timeframe) == "0"

    def test_to_duration_conversion(self, timeframe):
        timeframe.interval = 3
        timeframe.unit = "d"
        assert pytest.approx(timeframe.get_duration("y")) == 0.008219178082
        assert pytest.approx(timeframe.get_duration("w")) == 0.428571428571
        assert pytest.approx(timeframe.get_duration("M")) == 0.1
        assert timeframe.get_duration("d") == 3
        assert timeframe.get_duration("h") == 72
        assert timeframe.get_duration("m") == 4320
        assert timeframe.get_duration("s") == 259200
        assert timeframe.get_duration("ms") == 259200000

        assert Timeframe().get_duration() == 0

        with pytest.raises(UnknownTimeframeUnitError):
            timeframe.get_duration("some unknown unit")

    def test_to_pandas_timeframe_conversion(self, timeframe):
        timeframe.interval = 3
        timeframe.unit = "d"
        assert timeframe.to_pandas_timeframe() == "3D"
        assert not Timeframe(0).to_pandas_timeframe()
        assert not Timeframe(
            interval=1, unit=None).to_pandas_timeframe()

    def test_to_offset_timeframe_conversion(self, timeframe):
        timeframe.interval = 3
        timeframe.unit = "d"
        assert timeframe.to_offset_timeframe() == "3d"

        assert not Timeframe(0).to_offset_timeframe()
        assert not Timeframe(
            interval=1, unit=None).to_offset_timeframe()

    def test_to_timedelta_conversion(self, timeframe):
        timeframe.interval = 3
        timeframe.unit = "d"
        assert timeframe.to_timedelta() == relativedelta(days=3)

        assert Timeframe("1d").to_timedelta() == relativedelta(hours=24)
        assert Timeframe("1M").to_timedelta() == relativedelta(days=30.4167)
        assert Timeframe("1y").to_timedelta() == relativedelta(days=365)
        assert Timeframe("3d").to_timedelta() == relativedelta(days=3)
        assert Timeframe("4h").to_timedelta() == relativedelta(hours=4)
        assert Timeframe(
            "69ms").to_timedelta() == relativedelta(microseconds=69000)
