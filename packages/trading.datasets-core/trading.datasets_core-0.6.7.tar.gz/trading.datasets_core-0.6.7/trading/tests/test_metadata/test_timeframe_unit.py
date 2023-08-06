"""Tests for trading.datasets_core.metadata.timeframe_unit."""
# pylint: disable=missing-class-docstring,missing-function-docstring

import pytest

from trading.datasets_core.errors import UnknownTimeframeUnitError
from trading.datasets_core.metadata.timeframe_unit import TimeframeUnit


@pytest.fixture(name="timeframe_unit", scope="class")
def fixture_timeframe_unit():
    return TimeframeUnit("m")


class TestTimeframeUnit:

    def test_initialization_from_string(self, timeframe_unit):
        assert isinstance(timeframe_unit, TimeframeUnit)

    def test_initialization_from_another_timeframeunit(self):
        inner_timeframe_unit = TimeframeUnit("h")
        outer_timeframe_unit = TimeframeUnit(inner_timeframe_unit)
        assert isinstance(outer_timeframe_unit, TimeframeUnit)
        assert inner_timeframe_unit == "h"
        assert outer_timeframe_unit == "h"

    def test_initialization_from_invalid_value(self):
        assert not TimeframeUnit()
        assert not TimeframeUnit(None)
        assert not TimeframeUnit([])
        assert not TimeframeUnit("")

        with pytest.raises(UnknownTimeframeUnitError):
            TimeframeUnit("some unknown unit")

        with pytest.raises(UnknownTimeframeUnitError):
            TimeframeUnit(8012)

    def test_equality_operation(self, timeframe_unit):
        assert timeframe_unit == "m"

        assert TimeframeUnit(None) != False
        assert TimeframeUnit(None) == None
        assert TimeframeUnit("h") == "h"
        assert TimeframeUnit("y") == "y"
        assert TimeframeUnit("m") == "m"
        assert TimeframeUnit("M") == "M"

    def test_to_repr_conversion(self, timeframe_unit):
        assert repr(TimeframeUnit(None)) == repr(None)
        assert repr(timeframe_unit) == repr("m")

    def test_to_str_conversion(self, timeframe_unit):
        assert str(TimeframeUnit(None)) == str(None)
        assert str(timeframe_unit) == str("m")

    def test_to_seconds_conversion(self):
        assert TimeframeUnit("y").to_seconds() == 31536000
        assert TimeframeUnit("M").to_seconds() == 2592000
        assert TimeframeUnit("w").to_seconds() == 604800
        assert TimeframeUnit("d").to_seconds() == 86400
        assert TimeframeUnit("h").to_seconds() == 3600
        assert TimeframeUnit("m").to_seconds() == 60
        assert TimeframeUnit("s").to_seconds() == 1
        assert TimeframeUnit("ms").to_seconds() == 1 / 1000
        assert TimeframeUnit().to_seconds() == 0

    def test_to_pandas_unit_conversion(self):
        assert TimeframeUnit("y").to_pandas_unit() == "Y"
        assert TimeframeUnit("M").to_pandas_unit() == "MS"
        assert TimeframeUnit("w").to_pandas_unit() == "W"
        assert TimeframeUnit("d").to_pandas_unit() == "D"
        assert TimeframeUnit("h").to_pandas_unit() == "H"
        assert TimeframeUnit("m").to_pandas_unit() == "T"
        assert TimeframeUnit("s").to_pandas_unit() == "S"
        assert TimeframeUnit("ms").to_pandas_unit() == "L"
        assert not TimeframeUnit().to_pandas_unit()

    def test_to_offset_unit_conversion(self):
        assert TimeframeUnit("y").to_offset_unit() == "y"
        assert TimeframeUnit("M").to_offset_unit() == "m"
        assert TimeframeUnit("w").to_offset_unit() == "w"
        assert TimeframeUnit("d").to_offset_unit() == "d"
        assert TimeframeUnit("h").to_offset_unit() == "h"
        assert TimeframeUnit("m").to_offset_unit() == "min"
        assert TimeframeUnit("s").to_offset_unit() == "s"
        assert TimeframeUnit("ms").to_offset_unit() == "ms"
        assert not TimeframeUnit().to_offset_unit()

    def test_to_word_conversion(self):
        assert TimeframeUnit("y").to_word() == "year"
        assert TimeframeUnit("M").to_word() == "month"
        assert TimeframeUnit("w").to_word() == "week"
        assert TimeframeUnit("d").to_word() == "day"
        assert TimeframeUnit("h").to_word() == "hour"
        assert TimeframeUnit("m").to_word() == "minute"
        assert TimeframeUnit("s").to_word() == "second"
        assert TimeframeUnit("ms").to_word() == "millisecond"
        assert not TimeframeUnit().to_word()

    def test_to_adjective_conversion(self):
        assert TimeframeUnit("y").to_adjective() == "yearly"
        assert TimeframeUnit("M").to_adjective() == "monthly"
        assert TimeframeUnit("w").to_adjective() == "weekly"
        assert TimeframeUnit("d").to_adjective() == "daily"
        assert TimeframeUnit("h").to_adjective() == "hourly"
        assert TimeframeUnit("m").to_adjective() == "minute"
        assert TimeframeUnit("s").to_adjective() == "second"
        assert TimeframeUnit("ms").to_adjective() == "millisecond"
        assert not TimeframeUnit().to_adjective()
