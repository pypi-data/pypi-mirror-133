"""Module containing trading-datasets-core's custom errors."""


__all__ = [
    # Class exports
    "InvalidTimeframeError",
    "UnknownExchangeError",
    "UnknownSymbolError",
    "UnknownTimeframeUnitError",
]


class InvalidTimeframeError(ValueError):
    """This error is raised when the input timeframe is invalid.

    This error is also raised if the `Timeframe` class can't
    automagically extrapolate the values from the input.
    """


class UnknownExchangeError(ValueError):
    """This error is raised when the exchange requested is unknown."""


class UnknownSymbolError(ValueError):
    """This error is raised when we don't recognize a given symbol."""


class UnknownTimeframeUnitError(ValueError):
    """This error is raised when the input timeframe unit is unknown."""
