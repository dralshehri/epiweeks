# EpiWeeks

<!-- start description -->

A Python package to calculate epidemiological weeks using the US CDC (MMWR) and
ISO week numbering systems.

<!-- end description -->

<!-- start badges -->

[![Release Status](https://img.shields.io/github/actions/workflow/status/dralshehri/epiweeks/release.yml?label=release)][release]
[![Coverage Status](https://img.shields.io/badge/coverage-100%25-success)][coverage]
[![Code Quality](https://img.shields.io/codefactor/grade/github/dralshehri/epiweeks/main?&label=codefactor)][quality]
[![Docs Status](https://img.shields.io/readthedocs/epiweeks/stable)][docs]
[![PyPI Downloads](https://img.shields.io/pypi/dm/epiweeks?color=blue)][downloads]
[![PyPI Version](https://img.shields.io/pypi/v/epiweeks)][pypi-version]
[![Conda Version](https://img.shields.io/conda/vn/bioconda/epiweeks)][conda-version]
[![Package License](https://img.shields.io/github/license/dralshehri/epiweeks)][license]

[release]: https://github.com/dralshehri/epiweeks/actions/workflows/release.yml
[coverage]: https://github.com/dralshehri/epiweeks/actions/workflows/release.yml
[quality]:
  https://www.codefactor.io/repository/github/dralshehri/epiweeks/overview/main
[docs]: https://epiweeks.readthedocs.io
[downloads]: https://pypistats.org/packages/epiweeks
[pypi-version]: https://pypi.python.org/pypi/epiweeks
[conda-version]: https://anaconda.org/bioconda/epiweeks
[license]: https://github.com/dralshehri/epiweeks/blob/main/LICENSE

<!-- end badges -->

<!-- start summary -->

## Features

- Support for both the US CDC (MMWR) and ISO week numbering systems.
- Accurate and tested calculations.
- Intuitive, clean, and easy-to-use interface.
- Calculation of the start and end dates of weeks.
- Iteration of year's weeks or week's dates.
- Rich comparison between weeks.
- Logical operations for weeks (addition, subtraction and containment).
- Validation of input data.
- Works on Python 3.8+ with zero dependencies.
- Thoroughly tested with 100% test coverage.

## Installation

To install using `pip`, run:

```shell
pip install epiweeks
```

To install using `conda`, run:

```shell
conda install -c bioconda epiweeks
```

## Basic Usage

```python
from epiweeks import Week, Year

week = Week(2019, 1)
print(week.enddate())
# 2019-01-05

for week in Year(2019).iterweeks():
    print(week.enddate())
# 2019-01-05
# 2019-01-12
# ...
# 2019-12-21
# 2019-12-28
```

<!-- end summary -->

## Documentation

Please see <https://epiweeks.readthedocs.io> for full documentation of this
package, including background, more usage examples and API reference.

## License

This project is licensed under the terms of the MIT license.
