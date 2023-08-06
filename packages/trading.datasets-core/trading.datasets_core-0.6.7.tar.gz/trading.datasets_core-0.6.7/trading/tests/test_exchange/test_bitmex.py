"""Tests for trading.datasets_core.exchange.bitmex."""
# pylint: disable=missing-class-docstring,missing-function-docstring

import ccxt
import pytest

from trading.datasets_core.errors import UnknownSymbolError
from trading.datasets_core.exchange import BitMEXExchange
from trading.datasets_core.exchange import Exchange
from trading.datasets_core.metadata.timeframe import Timeframe
from trading.datasets_core.utils.datetime_utils import to_datetime


@pytest.fixture(name="exchange", scope="class")
def fixture_exchange():
    return BitMEXExchange()


class TestExchangeBitMEX:

    def test_initialization(self, exchange):
        assert issubclass(type(exchange), Exchange)
        assert isinstance(exchange, BitMEXExchange)

    def test_generate_fetch_ohlcv_params(self, exchange):
        expected_output = {"endTime": "2021-01-01T01:00:00.000Z", "count": 1}
        assert exchange._generate_fetch_ohlcv_params(
            timeframe=Timeframe("1h"),
            start=to_datetime("2021"),
            limit=1) == expected_output

        expected_output = {"endTime": "2004-12-01T10:26:40.000Z", "count": 9}
        assert exchange._generate_fetch_ohlcv_params(
            timeframe=Timeframe("1d"),
            start=to_datetime("2004-11-22 10:26:40+00:00"),
            limit=9) == expected_output

    def test_validating_symbol(self, exchange):
        assert exchange.get_valid_symbol("BTC/USD") == "BTC/USD"

        with pytest.raises(UnknownSymbolError):
            exchange.get_valid_symbol("BKAHDBLAJDHunknwonExchange")

    def test_unsuccessful_fetch_ohlcv(self, exchange, mocker):
        """Separate unsuccessful case so it can be mock patched."""
        mocker.patch("ccxt.bitmex.fetch_ohlcv", side_effect=ccxt.ExchangeError)
        mocker.patch("time.sleep", return_value=None)

        with pytest.raises(ccxt.ExchangeError):
            exchange.fetch_ohlcv(
                symbol="btcusd",
                timeframe="1d",
                start="JAN 1 2021",
                end="JAN 4 2021")

    def test_successful_fetch_ohlcv(self, exchange):
        expected_output = [
            (1609459200000, 28951.0, 29004.0, 28950.5, 29004.0, 995031.0),
            (1609459260000, 29004.0, 29050.0, 29003.5, 29043.5, 3328855.0),
            (1609459320000, 29043.5, 29044.0, 29016.5, 29017.0, 1220460.0),
        ]
        assert exchange.fetch_ohlcv(
            symbol="btcusd",
            timeframe="1m",
            start="JAN 1 2021 00:00:00+00:00",
            end="JAN 1 2021 00:02:00+00:00") == expected_output

        # Reverse start and end, should automagically work
        assert exchange.fetch_ohlcv(
            symbol="btcusd",
            timeframe="1m",
            start="JAN 1 2021 00:02:00+00:00",
            end="JAN 1 2021 00:00:00+00:00") == expected_output

        assert exchange.fetch_ohlcv(
            symbol="btcusd",
            timeframe="1d",
            start="JAN 1 1995",
            end="JAN 4 1995") == []

        expected_count = 8_785
        ohlcvs = exchange.fetch_ohlcv(
            symbol="btcusd", timeframe="1h", start="2020", end="2021")

        assert len(ohlcvs) == expected_count
        assert ohlcvs[-1][0] == 1609459200000

        # Loop through all expected timestamps and assert
        for i, timestamp in enumerate(range(1577836800, 1609462800, 3_600)):
            assert ohlcvs[i][0] == timestamp * 1000

        # Check if the number of datapoints is expected for
        # fetch given only the `end` argument
        expected_count = exchange.FETCH_LIMIT
        ohlcvs = exchange.fetch_ohlcv(
            symbol="btcusd", timeframe="1h", end="2021")

        assert len(ohlcvs) == expected_count
        assert ohlcvs[-1][0] == 1609459200000

        # Check if the number of datapoints is expected for
        # fetch given only the `start` argument
        ohlcvs = exchange.fetch_ohlcv(
            symbol="btcusd", timeframe="1h", start="2021")

        assert len(ohlcvs) == expected_count
        assert ohlcvs[0][0] == 1609459200000

    def test_successful_fetch_named_tuple_ohlcv(self, exchange):
        ohlcvs = exchange.fetch_ohlcv(
            symbol="btcusd",
            timeframe="1m",
            start="JAN 1 2021 00:00:00+00:00",
            end="JAN 1 2021 00:02:00+00:00",
            named_tuple=True)

        assert ohlcvs[0].timestamp == 1609459200000
        assert ohlcvs[0].open == 28951.0
        assert ohlcvs[0].high == 29004.0
        assert ohlcvs[0].low == 28950.5
        assert ohlcvs[0].close == 29004.0
        assert ohlcvs[0].volume == 995031.0

        assert ohlcvs[1].timestamp == 1609459260000
        assert ohlcvs[1].open == 29004.0
        assert ohlcvs[1].high == 29050.0
        assert ohlcvs[1].low == 29003.5
        assert ohlcvs[1].close == 29043.5
        assert ohlcvs[1].volume == 3328855.0

        assert ohlcvs[2].timestamp == 1609459320000
        assert ohlcvs[2].open == 29043.5
        assert ohlcvs[2].high == 29044.0
        assert ohlcvs[2].low == 29016.5
        assert ohlcvs[2].close == 29017.0
        assert ohlcvs[2].volume == 1220460.0

    def test_successful_fetch_reverse_ohlcv(self, exchange):
        expected_output = [
            (1609459320000, 29043.5, 29044.0, 29016.5, 29017.0, 1220460.0),
            (1609459260000, 29004.0, 29050.0, 29003.5, 29043.5, 3328855.0),
            (1609459200000, 28951.0, 29004.0, 28950.5, 29004.0, 995031.0),
        ]
        assert exchange.fetch_ohlcv(
            symbol="btcusd",
            timeframe="1m",
            start="JAN 1 2021 00:00:00+00:00",
            end="JAN 1 2021 00:02:00+00:00",
            reverse_return=True) == expected_output
