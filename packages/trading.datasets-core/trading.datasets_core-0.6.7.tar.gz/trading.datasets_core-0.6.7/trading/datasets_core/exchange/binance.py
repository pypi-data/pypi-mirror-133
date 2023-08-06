"""Module containing the Binance Exchange class."""

from __future__ import annotations

import datetime as dtlib

import ccxt

from trading.datasets_core.exchange.base import Exchange
from trading.datasets_core.metadata.timeframe import Timeframe
from trading.datasets_core.utils.datetime_utils import to_milliseconds


__all__ = [
    # Class exports
    "BinanceExchange",
]


class BinanceExchange(Exchange, ccxt.binance):
    """Improved class implementation of the CCXT Binance Exchange."""

    FETCH_LIMIT = 999

    def _generate_fetch_ohlcv_params(
        self,
        timeframe: Timeframe,
        start: dtlib.datetime,
        limit: int,
    ) -> dict:

        # Binance accepts the start timestamp in millisecond timestamp
        return {
            "startTime": int(to_milliseconds(start)),
            "limit": limit,
        }

    def _per_thread_fetch_funding_rates(
        self,
        symbol: str,
        timeframe: Timeframe,
        start: dtlib.datetime,
        limit: int,
        results: list[list[int | float]],
    ) -> list[list[int | float]]:

        per_thread_funding_rates = self.fapiPublic_get_fundingrate({
            "symbol": self.market(symbol)["id"],
            "startTime": int(to_milliseconds(start)),
            "limit": limit,
        })

        results += [
            [int(int(x["fundingTime"]) / 1000) * 1000, float(x["fundingRate"])]
            for x in per_thread_funding_rates[:]
        ]
