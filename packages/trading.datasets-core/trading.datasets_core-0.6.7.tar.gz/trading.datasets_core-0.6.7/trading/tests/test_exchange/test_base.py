"""Tests for trading.datasets_core.exchange.base."""
# pylint: disable=missing-class-docstring,missing-function-docstring

import ccxt
import pytest

from trading.datasets_core.exchange.base import Exchange


@pytest.fixture(name="exchange", scope="class")
def fixture_exchange():
    return Exchange()


class TestExchangeBase:

    def test_initialization(self, exchange):
        assert issubclass(type(exchange), ccxt.Exchange)
        assert isinstance(exchange, Exchange)

    def test_unimplemented_generate_fetch_ohlcv_params(self, exchange):
        with pytest.raises(NotImplementedError):
            exchange._generate_fetch_ohlcv_params(None, None, None)
