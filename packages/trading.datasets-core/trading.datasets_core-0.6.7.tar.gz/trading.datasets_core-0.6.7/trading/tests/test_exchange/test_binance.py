"""Tests for trading.datasets_core.exchange.binance."""
# pylint: disable=missing-class-docstring,missing-function-docstring

import ccxt
import pytest

from trading.datasets_core.errors import UnknownSymbolError
from trading.datasets_core.exchange import BinanceExchange
from trading.datasets_core.exchange import Exchange
from trading.datasets_core.metadata.timeframe import Timeframe
from trading.datasets_core.utils.datetime_utils import to_datetime


@pytest.fixture(name="exchange", scope="class")
def fixture_exchange():
    return BinanceExchange()


class TestExchangeBinance:

    def test_initialization(self, exchange):
        assert issubclass(type(exchange), Exchange)
        assert isinstance(exchange, BinanceExchange)

    def test_generate_fetch_ohlcv_params(self, exchange):
        expected_output = {"startTime": 1293840000000, "limit": 100}
        assert exchange._generate_fetch_ohlcv_params(
            timeframe=Timeframe("1h"),
            start=to_datetime("2011-01-01"),
            limit=100) == expected_output

        expected_output = {"startTime": 946684800000, "limit": 12}
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
        mocker.patch(
            "ccxt.binance.fetch_ohlcv", side_effect=ccxt.ExchangeError)
        mocker.patch("time.sleep", return_value=None)

        with pytest.raises(ccxt.ExchangeError):
            exchange.fetch_ohlcv(
                symbol="btcusd",
                timeframe="1d",
                start="JAN 1 2021",
                end="JAN 4 2021")

    def test_successful_fetch_ohlcv(self, exchange):
        expected_output = [
            (1609459200000, 28923.63, 28961.66, 28913.12, 28961.66, 27.457032),
            (1609459260000, 28961.67, 29017.5, 28961.01, 29009.91, 58.477501),
            (1609459320000, 29009.54, 29016.71, 28973.58, 28989.3, 42.470329),
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

        # Check if the number of datapoints is within the threshold
        # of one year's worth of hourly data. Threshold is -1% and,
        # in the time of writing, the result is 8_768. Test date range
        # is from JAN. 1, 2020 to JAN. 1, 2021 which is 8_785 days.
        upper_limit = 8_785
        lower_limit = upper_limit * 0.99
        ohlcvs = exchange.fetch_ohlcv(
            symbol="btcusd", timeframe="1h", start="2020", end="2021")
        actual_count = len(ohlcvs)

        assert lower_limit <= actual_count
        assert actual_count <= upper_limit

        # List of excluded timestamps, at least for Binance
        excluded_timestamps = (
            1581213600000, 1582113600000, 1582117200000, 1582120800000,
            1582124400000, 1582128000000, 1583316000000, 1587780000000,
            1587783600000, 1593309600000, 1593313200000, 1593316800000,
            1606716000000, 1608562800000, 1608566400000, 1608570000000,
            1608861600000,
        )

        # Loop through all expected timestamps and assert
        downloaded_timestamps = [x[0] for x in ohlcvs]
        for expected_timestamp in range(1577836800000, 1609462800000, 3600000):
            if expected_timestamp not in excluded_timestamps:
                assert expected_timestamp in downloaded_timestamps

        # Check if the number of datapoints is expected for
        # fetch given only the `end` argument
        upper_limit = exchange.FETCH_LIMIT
        lower_limit = upper_limit * 0.99
        ohlcvs = exchange.fetch_ohlcv(
            symbol="btcusd", timeframe="1h", end="2021")
        actual_count = len(ohlcvs)

        assert lower_limit <= actual_count
        assert actual_count <= upper_limit
        assert ohlcvs[-1][0] == 1609459200000

        # Check if the number of datapoints is expected for
        # fetch given only the `start` argument
        ohlcvs = exchange.fetch_ohlcv(
            symbol="btcusd", timeframe="1h", start="2021")
        actual_count = len(ohlcvs)

        assert lower_limit <= actual_count
        assert actual_count <= upper_limit
        assert ohlcvs[0][0] == 1609459200000

    def test_successful_fetch_named_tuple_ohlcv(self, exchange):
        ohlcvs = exchange.fetch_ohlcv(
            symbol="btcusd",
            timeframe="1m",
            start="JAN 1 2021 00:00:00+00:00",
            end="JAN 1 2021 00:02:00+00:00",
            named_tuple=True)

        assert ohlcvs[0].timestamp == 1609459200000
        assert ohlcvs[0].open == 28923.63
        assert ohlcvs[0].high == 28961.66
        assert ohlcvs[0].low == 28913.12
        assert ohlcvs[0].close == 28961.66
        assert ohlcvs[0].volume == 27.457032

        assert ohlcvs[1].timestamp == 1609459260000
        assert ohlcvs[1].open == 28961.67
        assert ohlcvs[1].high == 29017.5
        assert ohlcvs[1].low == 28961.01
        assert ohlcvs[1].close == 29009.91
        assert ohlcvs[1].volume == 58.477501

        assert ohlcvs[2].timestamp == 1609459320000
        assert ohlcvs[2].open == 29009.54
        assert ohlcvs[2].high == 29016.71
        assert ohlcvs[2].low == 28973.58
        assert ohlcvs[2].close == 28989.3
        assert ohlcvs[2].volume == 42.470329

    def test_successful_fetch_reverse_ohlcv(self, exchange):
        expected_output = [
            (1609459320000, 29009.54, 29016.71, 28973.58, 28989.3, 42.470329),
            (1609459260000, 28961.67, 29017.5, 28961.01, 29009.91, 58.477501),
            (1609459200000, 28923.63, 28961.66, 28913.12, 28961.66, 27.457032),
        ]
        assert exchange.fetch_ohlcv(
            symbol="btcusd",
            timeframe="1m",
            start="JAN 1 2021 00:00:00+00:00",
            end="JAN 1 2021 00:02:00+00:00",
            reverse_return=True) == expected_output

    def test_unsuccessful_fetch_funding_rates(self, exchange, mocker):
        """Separate unsuccessful case so it can be mock patched."""
        mocker.patch(
            (
                "trading.datasets_core.BinanceExchange."
                "_per_thread_fetch_funding_rates"
            ),
            side_effect=ccxt.ExchangeError)

        mocker.patch("time.sleep", return_value=None)

        with pytest.raises(ccxt.ExchangeError):
            exchange.fetch_funding_rates(
                symbol="btcusd",
                start="JAN 1 2021",
                end="JAN 4 2021")

    def test_successful_fetch_funding_rates(self, exchange):
        expected_output = [
            (1609459200000, 0.00022753),
            (1609488000000, 0.00026336),
            (1609516800000, 0.00034457),
            (1609545600000, 0.0001),
            (1609574400000, 0.00020151),
            (1609603200000, 0.00115471),
            (1609632000000, 0.00124058),
        ]
        assert exchange.fetch_funding_rates(
            symbol="btcusd",
            start="JAN 1 2021 00:00:00+00:00",
            end="JAN 3 2021 00:00:00+00:00") == expected_output

    def test_successful_fetch_named_tuple_funding_rates(self, exchange):
        funding_rates = exchange.fetch_funding_rates(
            symbol="btcusd",
            start="JAN 1 2021 00:00:00+00:00",
            end="JAN 3 2021 00:00:00+00:00",
            named_tuple=True)

        assert funding_rates[0].timestamp == 1609459200000
        assert funding_rates[0].rate == 0.00022753

        assert funding_rates[2].timestamp == 1609516800000
        assert funding_rates[2].rate == 0.00034457

        assert funding_rates[4].timestamp == 1609574400000
        assert funding_rates[4].rate == 0.00020151

        assert funding_rates[6].timestamp == 1609632000000
        assert funding_rates[6].rate == 0.00124058

    def test_successful_fetch_reverse_funding_rates(self, exchange):
        expected_output = [
            (1609632000000, 0.00124058),
            (1609603200000, 0.00115471),
            (1609574400000, 0.00020151),
            (1609545600000, 0.0001),
            (1609516800000, 0.00034457),
            (1609488000000, 0.00026336),
            (1609459200000, 0.00022753),
        ]
        assert exchange.fetch_funding_rates(
            symbol="btcusd",
            start="JAN 1 2021 00:00:00+00:00",
            end="JAN 3 2021 00:00:00+00:00",
            reverse_return=True) == expected_output
