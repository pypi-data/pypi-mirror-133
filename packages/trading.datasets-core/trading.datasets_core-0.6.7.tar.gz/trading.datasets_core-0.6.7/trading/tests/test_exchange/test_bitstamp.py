"""Tests for trading.datasets_core.exchange.bitstamp."""
# pylint: disable=missing-class-docstring,missing-function-docstring,line-too-long

import ccxt
import pytest

from trading.datasets_core.errors import UnknownSymbolError
from trading.datasets_core.exchange import BitstampExchange
from trading.datasets_core.exchange import Exchange
from trading.datasets_core.metadata.timeframe import Timeframe
from trading.datasets_core.utils.datetime_utils import to_datetime


@pytest.fixture(name="exchange", scope="class")
def fixture_exchange():
    return BitstampExchange()


class TestExchangeBitstamp:

    def test_initialization(self, exchange):
        assert issubclass(type(exchange), Exchange)
        assert isinstance(exchange, BitstampExchange)

    def test_generate_fetch_ohlcv_params(self, exchange):
        expected_output = {"start": 1293836400, "end": 1294196400}
        assert exchange._generate_fetch_ohlcv_params(
            timeframe=Timeframe("1h"),
            start=to_datetime("2011-01-01"),
            limit=100) == expected_output

        expected_output = {"start": 946598400, "end": 947635200}
        assert exchange._generate_fetch_ohlcv_params(
            timeframe=Timeframe("1d"),
            start=to_datetime("2000-01-01"),
            limit=12) == expected_output

    def test_validating_symbol(self, exchange):
        assert exchange.get_valid_symbol("BTC/USDT") == "BTC/USDT"

        with pytest.raises(UnknownSymbolError):
            exchange.get_valid_symbol("BKAHDBLAJDHunknwonExchange")

    def test_unsuccessful_fetch_ohlcv(self, exchange, mocker):
        """Separate unsuccessful case so it can be mock patched."""
        mocker.patch("ccxt.bitstamp.fetch_ohlcv", side_effect=ccxt.ExchangeError)
        mocker.patch("time.sleep", return_value=None)

        with pytest.raises(ccxt.ExchangeError):
            exchange.fetch_ohlcv(
                symbol="btcusd",
                timeframe="1d",
                start="JAN 1 2021",
                end="JAN 4 2021")

    def test_successful_fetch_ohlcv(self, exchange):
        expected_output = [
            (1609459200000, 28999.63, 29022.01, 28999.14, 29006.31, 0.86157958),
            (1609459260000, 29007.31, 29086.9, 29007.31, 29083.47, 14.56195084),
            (1609459320000, 29069.8, 29073.02, 29028.14, 29035.89, 3.03030144),
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
            symbol="ethusd",
            timeframe="1d",
            start="JAN 1 1995",
            end="JAN 4 1995") == []

        expected_count = 8_785
        ohlcvs = exchange.fetch_ohlcv(
            symbol="ethbtc", timeframe="1h", start="2020", end="2021")

        assert len(ohlcvs) == expected_count

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
        assert ohlcvs[0].open == 28999.63
        assert ohlcvs[0].high == 29022.01
        assert ohlcvs[0].low == 28999.14
        assert ohlcvs[0].close == 29006.31
        assert ohlcvs[0].volume == 0.86157958

        assert ohlcvs[1].timestamp == 1609459260000
        assert ohlcvs[1].open == 29007.31
        assert ohlcvs[1].high == 29086.9
        assert ohlcvs[1].low == 29007.31
        assert ohlcvs[1].close == 29083.47
        assert ohlcvs[1].volume == 14.56195084

        assert ohlcvs[2].timestamp == 1609459320000
        assert ohlcvs[2].open == 29069.8
        assert ohlcvs[2].high == 29073.02
        assert ohlcvs[2].low == 29028.14
        assert ohlcvs[2].close == 29035.89
        assert ohlcvs[2].volume == 3.03030144

    def test_successful_fetch_reverse_ohlcv(self, exchange):
        expected_output = [
            (1609459320000, 29069.8, 29073.02, 29028.14, 29035.89, 3.03030144),
            (1609459260000, 29007.31, 29086.9, 29007.31, 29083.47, 14.56195084),
            (1609459200000, 28999.63, 29022.01, 28999.14, 29006.31, 0.86157958),
        ]
        assert exchange.fetch_ohlcv(
            symbol="btcusd",
            timeframe="1m",
            start="JAN 1 2021 00:00:00+00:00",
            end="JAN 1 2021 00:02:00+00:00",
            reverse_return=True) == expected_output
