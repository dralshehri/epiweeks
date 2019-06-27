Epi Weeks
=========

A Python package to calculate epidemiological weeks using the CDC (MMWR) and
ISO week numbering systems.

|travis| |codecov| |docs| |supported| |version| |license|

.. |travis|
   image:: https://img.shields.io/travis/com/dralshehri/epiweeks.svg
   :alt: Build Status
   :target: https://travis-ci.com/dralshehri/epiweeks
.. |codecov|
   image:: https://img.shields.io/codecov/c/github/dralshehri/epiweeks.svg
   :alt: Coverage Status
   :target: https://codecov.io/github/dralshehri/epiweeks
.. |docs|
   image:: https://img.shields.io/readthedocs/epiweeks/stable.svg
   :alt: Docs Status
   :target: https://epiweeks.readthedocs.io/
.. |supported|
   image:: https://img.shields.io/pypi/pyversions/epiweeks.svg
   :alt: Python version support
   :target: https://pypi.python.org/pypi/epiweeks
.. |version|
   image:: https://img.shields.io/pypi/v/epiweeks.svg
   :alt: PyPI Package version
   :target: https://pypi.python.org/pypi/epiweeks
.. |license|
   image:: https://img.shields.io/github/license/dralshehri/epiweeks.svg
   :alt: License
   :target: https://github.com/dralshehri/epiweeks/blob/master/LICENSE

Features
--------

- Support for both the CDC (MMWR) and ISO week numbering systems.
- Accurate and tested calculations.
- Intuitive, clean, and easy-to-use interface.
- Calculation of the start and end dates of weeks.
- Iteration of year's weeks or week's dates.
- Rich comparison between weeks.
- Logical operations for weeks (addition, subtraction and containment).
- Validation of input data.
- Works on Python 3.6+ with zero dependencies.
- Thoroughly tested on all supported Python versions.

Installation
------------

.. code-block:: bash

   $ pip install -U epiweeks

Basic Usage
-----------

.. code-block:: python

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

Online Tool
-----------

The following is a simple online tool that was developed to calculate
epidemiological weeks (CDC system only) using the latest version of
this package:

https://www.dralshehri.com/epiweeks/

Documentation
-------------

Please see https://epiweeks.readthedocs.io/ for full documentation of
this package, including overview, more usage examples and API reference.

Contributing
------------

Contributions are welcome! See
`CONTRIBUTING.rst <https://github.com/dralshehri/epiweeks/blob/master/CONTRIBUTING.rst>`__
for more info.

Authors
-------

The main author is Mohammed Alshehri —
`@dralshehri <https://github.com/dralshehri>`__.

License
-------

This package is distributed under an MIT license.
See `LICENSE <https://github.com/dralshehri/epiweeks/blob/master/LICENSE>`__.
