"""Module containing the Bitstamp Exchange class."""

from __future__ import annotations

import datetime as dtlib

import ccxt

from trading.datasets_core.exchange.base import Exchange
from trading.datasets_core.metadata.timeframe import Timeframe
from trading.datasets_core.utils.datetime_utils import to_seconds


__all__ = [
    # Class exports
    "BitstampExchange",
]


class BitstampExchange(Exchange, ccxt.bitstamp):
    """Improved class implementation of the CCXT Bitstamp Exchange."""

    FETCH_LIMIT = 999

    def _generate_fetch_ohlcv_params(
        self,
        timeframe: Timeframe,
        start: dtlib.datetime,
        limit: int,
    ) -> dict:

        # FTX needs the starting and ending timestamp in seconds
        end = start + (timeframe.to_timedelta() * (limit - 1))
        start = start - timeframe.to_timedelta()

        return {
            "start": int(to_seconds(start)),
            "end": int(to_seconds(end)),
        }
