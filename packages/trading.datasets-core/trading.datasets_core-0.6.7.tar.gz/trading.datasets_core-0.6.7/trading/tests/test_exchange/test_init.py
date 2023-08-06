"""Tests for trading.datasets_core.exchange."""
# pylint: disable=missing-class-docstring,missing-function-docstring

import pytest

from trading.datasets_core.errors import UnknownExchangeError
from trading.datasets_core import exchange


class TestExchange:

    def test_getting_exchange_object(self):
        assert isinstance(
            exchange.get(exchange.BINANCE), exchange.BinanceExchange)

        # Test out caching
        assert isinstance(
            exchange.get(exchange.BINANCE), exchange.BinanceExchange)

        with pytest.raises(UnknownExchangeError):
            exchange.get("SomeCompletelyUnknownExchange")
