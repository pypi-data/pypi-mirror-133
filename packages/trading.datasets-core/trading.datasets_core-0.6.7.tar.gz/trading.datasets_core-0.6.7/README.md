![Trading Datasets](external/images/trading-datasets-core.png)

![Python](https://img.shields.io/badge/Python-3.7-blue)
![Version](https://img.shields.io/badge/Version-0.6.4-brightgreen)
![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen)

## What is it?
----------

**Trading Datasets Core** is the Quant Team's wrapper library for CCXT
and is an essential part of our data-retrieval libraries for crypto assets. This library shouldn't be used publicly by general users, this is imported by
**Trading Datasets**, which is the correct public interface.

## Where to get it?
----------

The source code is currently hosted on Bitbucket: [https://bitbucket.org/swapooquantitativedevelopment/trading-datasets-core/](https://bitbucket.org/swapooquantitativedevelopment/trading-datasets-core/)

Binary installer for the latest released version is available at the Python Package Index (PyPI)

```shell
$ pip install trading.datasets_core
```

## Dependencies
--------------------------

- [CCXT - A JavaScript / Python / PHP cryptocurrency trading API with support for more than 120 bitcoin/altcoin exchanges](https://ccxt.readthedocs.io/en/latest/index.html)
- [TheFuzz - Provides fuzzy string matching like a boss in a simple-to-use package](https://github.com/seatgeek/thefuzz)
- [python-dateutil - An extension to the standard datetime Python Library](https://github.com/dateutil/dateutil)
- [python-Levenshtein - Provides functions for fast computation of Levenshtein distance and string similarity](https://github.com/ztane/python-Levenshtein/)
- [DateTimeRange - Provides a simpler interface for datetime range objects](https://github.com/thombashi/DateTimeRange)

## Installation from sources
--------------------------

To install `trading.datasets_core` from source, locate and go in the **trading-datasets-core** directory (same one where you found this file after cloning the git repository), execute:

```shell
$ pip install .
```

or for installing in [development mode](https://pip.pypa.io/en/latest/cli/pip_install/#install-editable):

```shell
$ pip install -e .
```

## Contribution guidelines
--------------------------

If you want to contribute to **Trading Datasets Core**, be sure to review the [contribution guidelines](CONTRIBUTING.md). By participating, you are expected to uphold this guidelines.
