"""Module containing the BitMEX Exchange class."""

from __future__ import annotations

import datetime as dtlib

import ccxt

from trading.datasets_core.exchange.base import Exchange
from trading.datasets_core.metadata.timeframe import Timeframe
from trading.datasets_core.utils.datetime_utils import to_iso8601


__all__ = [
    # Class exports
    "BitMEXExchange",
]


class BitMEXExchange(Exchange, ccxt.bitmex):
    """Improved class implementation of the CCXT BitMEX Exchange."""

    FETCH_LIMIT = 999

    def _generate_fetch_ohlcv_params(
        self,
        timeframe: Timeframe,
        start: dtlib.datetime,
        limit: int,
    ) -> dict:

        # BitMEX accepts the ending timestamp in ISO-8601 format
        end = start + (timeframe.to_timedelta() * limit)

        return {
            "endTime": to_iso8601(end),
            "count": limit,
        }
