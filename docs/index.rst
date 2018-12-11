Epi Weeks
=========

A Python package to calculate epidemiological weeks using US CDC (MMWR) and
WHO (ISO) calculation methods.

`Source Code <https://github.com/dralshehri/hijri-converter>`__

|travis| |codecov| |docs| |supported| |version|

.. |travis|
   image:: https://travis-ci.org/dralshehri/epi-weeks.svg?branch=master
   :alt: Travis-CI Build Status
   :target: https://travis-ci.org/dralshehri/epi-weeks

.. |codecov|
   image:: https://codecov.io/github/dralshehri/epi-weeks/coverage.svg?branch=master
   :alt: Coverage Status
   :target: https://codecov.io/github/dralshehri/epi-weeks

.. |docs|
   image:: https://readthedocs.org/projects/epiweeks/badge/?version=latest
   :alt: Docs Status
   :target: https://epiweeks.readthedocs.io/en/latest

.. |supported|
   image:: https://img.shields.io/pypi/pyversions/epiweeks.svg
   :alt: Supported versions
   :target: https://pypi.python.org/pypi/epiweeks

.. |version|
   image:: https://img.shields.io/pypi/v/epiweeks.svg
   :alt: PyPI Package latest release
   :target: https://pypi.python.org/pypi/epiweeks

.. contents::
   :local:
   :backlinks: none

Background
----------

Epidemiological weeks, commonly referred to as "epi weeks", are simply
a standardized method of counting weeks to allow for the comparison of
reported public health data.
Epidemiological weeks are used by the US CDC, WHO, and many other health
organizations.

The US CDC defines epidemiological week (known as `MMWR week`_) as seven days
beginning with Sunday and ending with Saturday.
The WHO defines epidemiological week, based on `ISO week`_, as seven days
beginning with Monday and ending with Sunday.
In either case, the end of the first epidemiological
week of the year by definition must fall at least four days into the year.
Most years have 52 epidemiological weeks, but some have 53.

.. _`MMWR week`: https://wwwn.cdc.gov/nndss/document/MMWR_Week_overview.pdf
.. _`ISO week`: https://en.wikipedia.org/wiki/ISO_week_date

Features
--------

- Support for both US CDC (MMWR) and WHO (ISO) calculation methods.
- Accurate and reliable calculation.
- Fully tested against multiple original references.
- Calculation of start and end dates of week.
- Iteration of year's weeks or week's dates.
- Rich comparison between weeks.
- Logical operations for weeks (addition, subtraction and containment).
- Validation of input data.
- ...and more.

Installation
------------

.. code-block:: bash

   $ pip install epiweeks

Usage Examples
--------------

To import the package:

.. code-block:: pycon

   >>> import epiweeks as epi

To calculate epidemiological week from a Gregorian date or today date:

.. code-block:: pycon

   >>> epi.Week(2019, 1)
   Week(2019, 1, cdc)

   >>> epi.Week.fromdate(2018, 12, 30)
   Week(2019, 1, cdc)

   >>> epi.Week.thisweek()
   Week(2018, 48, cdc)

By default, US CDC calculation method is assumed. To use WHO method instead:

.. code-block:: pycon

   >>> epi.Week(2019, 1, 'who')
   Week(2019, 1, who)

   >>> epi.Week.fromdate(2018, 12, 30, 'who')
   Week(2018, 52, who)

   >>> epi.Week.thisweek('who')
   Week(2018, 48, who)

To get an iterator of :obj:`epiweeks.Week` objects for an epidemiological year:

.. code-block:: pycon

   >>> list(epi.Year(2018).iterweeks())
   [(Week(2018, 1, cdc), ..., Week(2018, 52, cdc))]

The instance of :obj:`epiweeks.Week` object has some other useful methods:

.. code-block:: pycon

   >>> week = epi.Week(2019, 1)

   >>> week.weektuple()
   (2019, 1)

   >>> week.isoformat()
   '2019W01'

   >>> week.startdate()
   datetime.date(2018, 12, 30)

   >>> week.enddate()
   datetime.date(2019, 1, 5)

   >>> list(week.iterdates())
   [(datetime.date(2018, 12, 30), ..., datetime.date(2019, 1, 5))]

Rich comparison, addition, subtracting and containment operators for
:obj:`epiweeks.Week` object are supported:

.. code-block:: pycon

   >>> week1 = epi.Week(2019, 1)
   >>> week2 = epi.Week(2018, 52)

   >>> week1 > week2
   True

   >>> (week1 - 1) == week2
   True

   >>> week1 + 3
   Week(2019, 4, cdc)

   >>> from datetime import date
   >>> date(2019, 1, 2) in week1
   True

Input values are by default checked if valid. Invalid input will raise
``TypeError`` or ``ValueError`` exception that can be caught and handled
in try and except blocks:

.. code-block:: pycon

   >>> epi.Week(2018, 53)
   Traceback...
   ValueError: week must be in 1..52 for year

   >>> epi.Year(2019, 'mmwr')
   Traceback...
   ValueError: method must be 'who' or 'cdc'

Licence
-------

This package is distributed under an MIT licence.
The licence is as follows (from ``LICENSE.txt`` file):

.. literalinclude:: ../LICENSE.txt
   :language: text

API Reference
-------------

This section documents the API of `epiweeks` module, which is the main module
of Epi Weeks package.

.. automodule:: epiweeks
