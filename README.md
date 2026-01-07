# EpiWeeks

<!-- start description -->

A Python package for accurate epidemiological weeks calculation using the US CDC (MMWR) and ISO week numbering systems.

EpiWeeks provides reliable week calculations validated against CDC reference data, essential for disease surveillance, public health reporting, and epidemiological research.

<!-- end description -->

<!-- start badges -->

[![Release Status](https://img.shields.io/badge/release-pass-success)][release] [![Coverage Status](https://img.shields.io/badge/coverage-100%25-success)][coverage] [![PyPI Downloads](https://static.pepy.tech/badge/epiweeks)][downloads] [![PyPI Version](https://img.shields.io/pypi/v/epiweeks)][pypi-version] [![Conda Version](https://img.shields.io/conda/vn/bioconda/epiweeks)][conda-version] [![Package License](https://img.shields.io/github/license/dralshehri/epiweeks)][license] [![Package DOI](https://img.shields.io/badge/doi-10.5281%2Fzenodo.18171641-blue)][doi]

[release]: https://github.com/dralshehri/epiweeks/releases/latest
[coverage]: https://github.com/dralshehri/epiweeks/releases/latest
[downloads]: https://pepy.tech/project/epiweeks
[pypi-version]: https://pypi.python.org/pypi/epiweeks
[conda-version]: https://anaconda.org/bioconda/epiweeks
[license]: https://github.com/dralshehri/epiweeks/blob/main/LICENSE
[doi]: https://doi.org/10.5281/zenodo.18171641

<!-- end badges -->

<!-- start summary -->

## ✨ Features

- Support for both the US CDC (MMWR) and ISO week numbering systems
- Accurate and tested calculations validated against CDC reference data
- Intuitive, clean, and easy-to-use interface
- Calculation of the start and end dates of weeks
- Iteration of year's weeks or week's dates
- Rich comparison between weeks
- Logical operations for weeks (addition, subtraction and containment)
- Comprehensive input validation and error handling
- Full type annotations and 100% test coverage
- Zero runtime dependencies

## 📦 Installation

To install using `uv`, run:

```shell
uv add epiweeks
```

To install using `pip`, run:

```shell
pip install epiweeks
```

To install using `conda`, run:

```shell
conda install -c bioconda epiweeks
```

## 🚀 Basic Usage

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

## 📚 Documentation

Please refer to <https://epiweeks.readthedocs.io> for complete documentation on this package, which includes background information, usage examples, and API reference.

## 🤝 Contributing

If you're interested in contributing, please check out the [Contributing](https://github.com/dralshehri/epiweeks/blob/main/CONTRIBUTING.md) guide for more information on how you can help!

## 📄 License

This project is licensed under the terms of the MIT license.

## 📝 Citation

If you plan to cite this project in your academic publication, please refer to <https://doi.org/10.5281/zenodo.18171641> for citation information.
