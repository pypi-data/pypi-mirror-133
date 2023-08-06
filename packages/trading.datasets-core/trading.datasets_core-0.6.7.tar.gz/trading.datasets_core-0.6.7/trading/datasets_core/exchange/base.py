"""Module containing base exchange classes."""

from __future__ import annotations

from collections import namedtuple
from typing import Callable
import datetime as dtlib
import time

from datetimerange import DateTimeRange
from thefuzz.process import extractOne as fuzzy_match
import ccxt

from trading.datasets_core.errors import UnknownSymbolError
from trading.datasets_core.metadata.timeframe import Timeframe
from trading.datasets_core.utils.datetime_utils import get_valid_start_end
from trading.datasets_core.utils.datetime_utils import to_milliseconds
from trading.datasets_core.utils.threading_utils import PropagatingThread


__all__ = [
    # Class exports
    "Exchange",
]


class Exchange(ccxt.Exchange):
    """Improved class implementation of the CCXT Exchange.

    This is used in conjuction with any of the specific exchanges
    in CCXT. So if we want to use this base Exchange class as a parent
    class, we would also need to add the specific exchange from
    CCXT as a parent class.

    For example:
    ```
    # Create a new exchange class. We need to use two
    # classes as parents, one from CCXT and the other
    # one is our base Exchange class.
    class NewBinanceExchange(Exchange, ccxt.binance):
        ...
    ```
    """

    # Must be overriden by subclasses to
    # maximize each individual exchange's limit
    FETCH_LIMIT = 100

    def __init__(self, config: dict | None = None):
        # Make sure config is an empty dictionary if its invalid
        if not config:
            config = {}

        # Force rate limit into the config
        config.update({"enableRateLimit": True})

        super().__init__(config)

        # Make sure markets are already loaded when instance is created
        # but only do it for subclasses of Exchange, not Exchange itself
        if issubclass(type(self), Exchange) and type(self) != Exchange:
            super().load_markets()

    def fetch_ohlcv(
        self,
        symbol: str,
        timeframe: Timeframe | str,
        start: dtlib.datetime | str | int | None = None,
        end: dtlib.datetime | str | int | None = None,
        include_latest: bool = True,
        named_tuple: bool = False,
        reverse_return: bool = False,
    ) -> list[list[int | float] | namedtuple]:

        """Returns a set of OHLCV data given certain parameters.

        Arguments:
            symbol: Ticker symbol of the crypto asset.
            timeframe: Timeframe of the candlestick data to fetch. Some
                examples of valid timeframe strings are `"2h"` for two
                hour, `"1d"` for one day, and `"1w"` for 1 week.
            start: Starting datetime of the data to be fetched.
                The input argument can be a string indicating a
                valid datetime-like string or a number indicating the
                timestamp in milliseconds.
            end: Ending timestamp of the data to be fetched.
                The input argument can be a string indicating a
                valid datetime-like string or a number indicating the
                timestamp in milliseconds.
            include_latest: If the `include_latest` variable is set to
                `False` the latest date is not included since most
                datasets are constantly changing intraday. If set to
                `True`, then the latest date is included.
            named_tuple: if set to `True`, the the function returns a
                list of named tuples instead of a raw list of list
                version of the OHLCV. The named tuple has the following
                attributes: `timestamp`, `open`, `high`, `low`, `close`,
                and `volume`.
            reverse_return: If set to `True`, the return would be sorted
                from newest to oldest: index 0 would contain the latest
                OHLCV data and index -1 would contain the olders.

        Return:
            A list of list of numbers if `named_tuple` is set to `False`
            or a list of named tuples if `named_tuple` is set to `True`.
        """

        ohlcvs = self._fetch_dataset(
            self._per_thread_fetch_ohlcv, symbol, timeframe, start, end,
            include_latest=include_latest,
            remove_duplicates=True,
            sort_result=True,
        )

        if reverse_return:
            ohlcvs.reverse()

        if named_tuple:
            OHLCV = namedtuple("OHLCV", (
                "timestamp", "open", "high", "low", "close", "volume"))

            ohlcvs = [OHLCV(*x) for x in ohlcvs]

        return ohlcvs

    def fetch_funding_rates(
        self,
        symbol: str,
        start: dtlib.datetime | str | int | None = None,
        end: dtlib.datetime | str | int | None = None,
        include_latest: bool = True,
        named_tuple: bool = False,
        reverse_return: bool = False,
    ) -> list[list[int | float] | namedtuple]:

        """Returns a set of funding rates given certain parameters.

        Arguments:
            symbol: Ticker symbol of the crypto asset.
            timeframe: Timeframe of the candlestick data to fetch. Some
                examples of valid timeframe strings are `"2h"` for two
                hour, `"1d"` for one day, and `"1w"` for 1 week.
            start: Starting datetime of the data to be fetched.
                The input argument can be a string indicating a
                valid datetime-like string or a number indicating the
                timestamp in milliseconds.
            end: Ending timestamp of the data to be fetched.
                The input argument can be a string indicating a
                valid datetime-like string or a number indicating the
                timestamp in milliseconds.
            include_latest: If the `include_latest` variable is set to
                `False` the latest date is not included since most
                datasets are constantly changing intraday. If set to
                `True`, then the latest date is included.
            named_tuple: if set to `True`, the the function returns a
                list of named tuples instead of a raw list of list
                version of the OHLCV. The named tuple has the following
                attributes: `timestamp`, `open`, `high`, `low`, `close`,
                and `volume`.
            reverse_return: If set to `True`, the return would be sorted
                from newest to oldest: index 0 would contain the latest
                OHLCV data and index -1 would contain the olders.

        Return:
            A list of list of numbers if `named_tuple` is set to `False`
            or a list of named tuples if `named_tuple` is set to `True`.
        """

        funding_rates = self._fetch_dataset(
            self._per_thread_fetch_funding_rates, symbol,
            Timeframe("8h"), start, end,
            include_latest=include_latest,
            remove_duplicates=True,
            sort_result=True,
        )

        if reverse_return:
            funding_rates.reverse()

        if named_tuple:
            FundingRate = namedtuple("FundingRate", ("timestamp", "rate"))
            funding_rates = [FundingRate(*x) for x in funding_rates]

        return funding_rates

    def _fetch_dataset(
        self,
        fetch_fn: Callable,
        symbol: str,
        timeframe: Timeframe | str,
        start: dtlib.datetime | str | int | None = None,
        end: dtlib.datetime | str | int | None = None,
        include_latest: bool = True,
        remove_duplicates: bool = True,
        sort_result: bool = True,
    ) -> list[list[int | float]]:

        """Fetch a dataset from an exchange using multiple threads.

        Arguments:
            fetch_fn: An internal function that determines what
                dataset we fetch. The function signature should include
                a symbol, timeframe, start, limit, and result variable.
                Function should return a list of list of ints or floats.
            symbol: Ticker symbol of the crypto asset.
            timeframe: Timeframe of the candlestick data to fetch. Some
                examples of valid timeframe strings are `"2h"` for two
                hour, `"1d"` for one day, and `"1w"` for 1 week.
            start: Starting datetime of the data to be fetched.
                The input argument can be a string indicating a
                valid datetime-like string or a number indicating the
                timestamp in milliseconds.
            end: Ending timestamp of the data to be fetched.
                The input argument can be a string indicating a
                valid datetime-like string or a number indicating the
                timestamp in milliseconds.
            include_latest: If the `include_latest` variable is set to
                `False` the latest date is not included since most
                datasets are constantly changing intraday. If set to
                `True`, then the latest date is included.
            remove_duplicates: If set to `True`, duplicates are removed
                in the resulting dataset.
            sort_result: If set to `True`, the resulting dataset is
                sorted using the first index of the element - usually
                the timestamp of each period in the dataset.

        Return
            A list of list of numbers. The data depends on the fetch
            function passed in the arguments.

        """

        # Validate and standardize the symbol before using it
        symbol = self.get_valid_symbol(symbol)

        # Standardize the timeframe before using it
        timeframe = Timeframe(timeframe)

        # Make sure that the start and end times are valid
        raw_start, raw_end = start, end
        start, end = get_valid_start_end(
            start, end, timeframe,
            timeframe_multiplier=self.FETCH_LIMIT,
            include_latest=include_latest)

        full_range_start = start

        # Create a datetime range from the initial start and end
        # datetimes and create a limit-based timedelta to generate a
        # list of new start and end timedates for the async OHLCV fetch
        time_range = DateTimeRange(start, end)
        time_range_tf = Timeframe(
            interval=(timeframe.interval * self.FETCH_LIMIT),
            unit=timeframe.unit)

        # Progress trackers
        prev_results_count = 0
        newly_added_count = 0

        results = []
        threads = []
        for start in time_range.range(time_range_tf.to_timedelta()):
            # Ignore the last start time given if its greater than
            # or equal to our goal end fetch time
            if start > end:
                break  # pragma: no cover

            threads.append(PropagatingThread(
                target=fetch_fn,
                args=(
                    symbol,
                    timeframe,
                    start,
                    self.FETCH_LIMIT,
                    results,
                )
            ))

        # Start all threads
        for thread in threads:
            # Apply a slowdown if we reach half of the fetch limit
            if newly_added_count >= (self.FETCH_LIMIT / 2):  # pragma: no cover
                time.sleep(0.25)
                newly_added_count = 0

            thread.start()

            # Update progress trackers
            results_count = len(results)
            newly_added_count += (results_count - prev_results_count)
            prev_results_count = results_count

        # Wait for all of them to finish
        for thread in threads:
            thread.join()

        # Remove duplicates in the result, apply a hard-end-time cap
        if remove_duplicates:
            start_ms = to_milliseconds(full_range_start)
            end_ms = to_milliseconds(end)
            results = dict.fromkeys(
                tuple(x) for x in results
                if x[0] <= end_ms and x[0] >= start_ms
            )

        # Sort the resulting dataset
        if sort_result:
            results = sorted(results)

        if not results:
            return results

        # Make sure to cap the result
        if raw_start and raw_end is None:
            return results[:self.FETCH_LIMIT]
        if raw_end and raw_start is None:
            return results[abs(len(results) - self.FETCH_LIMIT):]

        return results

    def _per_thread_fetch_ohlcv(
        self,
        symbol: str,
        timeframe: Timeframe,
        start: dtlib.datetime,
        limit: int,
        results: list[list[int | float]],
    ) -> list[list[int | float]]:

        # Generate parameters for CCXT's original `fetch_ohlcv()` function
        fetch_ohlcv_params = self._generate_fetch_ohlcv_params(
            timeframe, start, limit)

        ohlcv = super().fetch_ohlcv(
            symbol,
            str(timeframe),
            limit=limit,
            params=fetch_ohlcv_params)

        results += ohlcv

    def _generate_fetch_ohlcv_params(
        self,
        timeframe: Timeframe,
        start: dtlib.datetime,
        limit: int,
    ) -> dict:

        raise NotImplementedError

    def get_valid_symbol(self, symbol: str) -> str:
        valid_symbol, match_score = fuzzy_match(
            str(symbol), self.markets.keys())

        # Raise an error if the exchange name is unrecognized or invalid
        if not symbol or match_score < 55:
            raise UnknownSymbolError(symbol)

        return valid_symbol
