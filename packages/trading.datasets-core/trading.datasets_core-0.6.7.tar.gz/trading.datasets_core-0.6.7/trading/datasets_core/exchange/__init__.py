"""Package for exchange-related components in Trading Datasets Core."""

import re

from thefuzz.process import extractOne as fuzzy_match

from trading.datasets_core.errors import UnknownExchangeError

from trading.datasets_core.exchange.base import Exchange
from trading.datasets_core.exchange.binance import BinanceExchange
from trading.datasets_core.exchange.bitmex import BitMEXExchange
from trading.datasets_core.exchange.bitstamp import BitstampExchange
from trading.datasets_core.exchange.ftx import FTXExchange


__all__ = [
    # Class exports
    "Exchange",
    "BinanceExchange",
    "BitMEXExchange",
    "BitstampExchange",
    "FTXExchange",

    # Function exports
    "get",
]

_EXCHANGE_NAME_CLASS_MAPPING = {
    "Binance": BinanceExchange,
    "BitMEX": BitMEXExchange,
    "Bitstamp": BitstampExchange,
    "FTX": FTXExchange,
}


# Caching of exchange instances
_instances = {}


def get(exchange_name: str, config: bool = {}) -> Exchange:  # pylint: disable=redefined-outer-name
    """Returns the proper exchange class given its name."""
    global _instances
    if exchange_name in _instances:
        return _instances[exchange_name]

    valid_exchange_name, match_score = fuzzy_match(
        str(exchange_name), _EXCHANGE_NAME_CLASS_MAPPING.keys())

    # Raise an error if the exchange name is unrecognized or invalid
    if not exchange_name or match_score < 55:
        raise UnknownExchangeError(exchange_name)

    # Save the instance in the cache
    instance = _EXCHANGE_NAME_CLASS_MAPPING.get(valid_exchange_name, Exchange)(
        config=config,
    )
    _instances[exchange_name] = instance

    return instance


# Dynamic export of exchange name constants
for exchange_name in _EXCHANGE_NAME_CLASS_MAPPING.keys():  # pylint: disable=consider-iterating-dictionary
    # Replace any special character with underscore
    # and convert exchange names to uppercase
    constant_name = re.sub("[^A-Za-z0-9]+", "_", exchange_name).upper()
    globals()[constant_name] = exchange_name


__all__ += [key.upper() for key in _EXCHANGE_NAME_CLASS_MAPPING.keys()]
