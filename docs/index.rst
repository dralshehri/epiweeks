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

.. contents::
   :local:
   :backlinks: none

.. module:: epiweeks

Overview
--------

Epidemiological weeks, commonly referred to as "epi weeks", are simply
a standardized method for numbering weeks as a period of time to group
epidemiological events. This method allows for the comparison of reported
events for a given year, or period of a year, with those of previous years.
It also facilitates similar comparison between countries.

There are several systems for numbering weeks. The most common systems when it
comes to epidemiological weeks are the CDC and ISO systems. The CDC system is
used in countries such as the United States, Canada, Australia, India, Egypt,
and Saudi Arabia. The ISO system is used in all European countries and most of
Asian ones.

The CDC defines the week (`MMWR week`_) as seven days, beginning with Sunday
and ending with Saturday. The ISO defines the week (`ISO week`_) as seven days,
beginning with Monday and ending with Sunday. In either case, the end of the
first week of the year, by definition, must fall at least four days into the
year. Week numbers range from 1 to 53 for year, although most years consist
of 52 weeks.

Public health professionals, analysts, researchers, and developers need to
have a tested and reliable tool for calculating epidemiological weeks.
The `Epi Weeks`_ package provides that functionality using both the CDC and
ISO week numbering systems. It has been carefully tested against original
resources, including the `MMWR Weeks Calendars`_ published by the CDC, to
ensure its accuracy and reliability. *Epi Weeks* package can be used in many
ways, from identifying the week of a date or the ending date for a week, to
generating a full epidemiological calendar.

.. _`MMWR week`: https://wwwn.cdc.gov/nndss/document/MMWR_Week_overview.pdf
.. _`ISO week`: https://en.wikipedia.org/wiki/ISO_week_date
.. _`Epi Weeks`: https://pypi.org/project/epiweeks/
.. _`MMWR Weeks Calendars`: https://wwwn.cdc.gov/nndss/downloads.html

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

Usage Examples
--------------

Importing the Package
~~~~~~~~~~~~~~~~~~~~~

To import the package:

.. code-block:: pycon

   >>> from epiweeks import Week, Year

Week Instance and Methods
~~~~~~~~~~~~~~~~~~~~~~~~~

You can create an instance of :obj:`Week` object by only providing the year
and week number:

.. code-block:: pycon

   >>> Week(2019, 1)
   Week(2019, 1, CDC)

It is also possible to create an instance of :obj:`Week` object from a date,
formatted string, or current date:

.. code-block:: pycon

   >>> from datetime import date
   >>> my_date = date(2018, 12, 30)
   >>> Week.fromdate(my_date)
   Week(2019, 1, CDC)

   >>> Week.fromstring("2019W01")
   Week(2019, 1, CDC)

   >>> Week.thisweek()
   Week(2019, 26, CDC)

By default, the CDC system is assumed when creating the :obj:`Week` object
instance. To use the ISO system instead:

.. code-block:: pycon

   >>> Week(2019, 1, system="iso")
   Week(2019, 1, ISO)

   >>> from datetime import date
   >>> my_date = date(2018, 12, 30)
   >>> Week.fromdate(my_date, system="iso")
   Week(2018, 52, ISO)

   >>> Week.fromstring("2019W01", system="iso")
   Week(2019, 1, ISO)

   >>> Week.thisweek(system="iso")
   Week(2019, 26, ISO)

The instance of :obj:`Week` object has also some other useful methods:

.. code-block:: pycon

   >>> week = Week(2019, 2)

   >>> week.weektuple()
   (2019, 2)

   >>> week.cdcformat()
   '201902'

   >>> week.isoformat()
   '2019W02'

   >>> week.startdate()
   datetime.date(2019, 1, 6)

   >>> week.enddate()
   datetime.date(2019, 1, 12)

   >>> list(week.iterdates())
   [(datetime.date(2019, 1, 6), ..., datetime.date(2019, 1, 12))]

   >>> week.daydate(3)  # Thursday
   datetime.date(2019, 1, 10)

Year Instance and Methods
~~~~~~~~~~~~~~~~~~~~~~~~~

You can create an instance of :obj:`Year` object by only providing the year,
or from current date:

.. code-block:: pycon

   >>> Year(2018)
   Year(2018, CDC)

   >>> Year.thisyear()
   Year(2019, CDC)

By default, the CDC system is assumed when creating the :obj:`Year` object
instance. To use the ISO system instead:

.. code-block:: pycon

   >>> Year(2018, system="iso")
   Year(2018, ISO)

   >>> Year.thisyear(system="iso")
   Year(2019, ISO)

To get a list of :obj:`Week` objects for all weeks of a year:

.. code-block:: pycon

   >>> list(Year(2019).iterweeks())
   [(Week(2019, 1, CDC), ..., Week(2019, 52, CDC))]

The instance of :obj:`Year` object has also some other useful methods:

.. code-block:: pycon

   >>> year = Year(2019)

   >>> year.totalweeks()
   52

   >>> year.startdate()
   datetime.date(2018, 12, 30)

   >>> year.enddate()
   datetime.date(2019, 12, 28)

Generating Epidemiological Calendars
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The epidemiological calendar can be easily generated using this package as
demonstrated in the following two examples.

To generate a week endings calendar for a year as in
`this document <https://wwwn.cdc.gov/nndss/document/W2018-19.pdf>`__ by CDC:

.. code-block:: python

   for week in Year(2018).iterweeks():
       day = week.enddate().day
       month_name = week.enddate().strftime("%b")
       row = [
           week.week,
           day if day // 8 else " ".join([month_name, str(day)])
       ]
       print(row)

   # [1, 'Jan 6']
   # [2, 13]
   # [3, 20]
   # [4, 27]
   # [5, 'Feb 3']
   # [6, 10]
   # ...
   # [47, 24]
   # [48, 'Dec 1']
   # [49, 8]
   # [50, 15]
   # [51, 22]
   # [52, 29]

To generate a full epidemiological calendar for a year as in
`this document <https://www.paho.org/hq/dmdocuments/2016/2016-cha-epidemiological-calendar.pdf>`__
by PAHO:

.. code-block:: python

   for week in Year(2016).iterweeks():
       row = [
           week.week,
           week.startdate().strftime("%b"),
           *[d.day for d in week.iterdates()],
           week.enddate().strftime("%b")
       ]
       print(row)

   # [1, 'Jan', 3, 4, 5, 6, 7, 8, 9, 'Jan']
   # [2, 'Jan', 10, 11, 12, 13, 14, 15, 16, 'Jan']
   # [3, 'Jan', 17, 18, 19, 20, 21, 22, 23, 'Jan']
   # [4, 'Jan', 24, 25, 26, 27, 28, 29, 30, 'Jan']
   # [5, 'Jan', 31, 1, 2, 3, 4, 5, 6, 'Feb']
   # [6, 'Feb', 7, 8, 9, 10, 11, 12, 13, 'Feb']
   # ...
   # [47, 'Nov', 20, 21, 22, 23, 24, 25, 26, 'Nov']
   # [48, 'Nov', 27, 28, 29, 30, 1, 2, 3, 'Dec']
   # [49, 'Dec', 4, 5, 6, 7, 8, 9, 10, 'Dec']
   # [50, 'Dec', 11, 12, 13, 14, 15, 16, 17, 'Dec']
   # [51, 'Dec', 18, 19, 20, 21, 22, 23, 24, 'Dec']
   # [52, 'Dec', 25, 26, 27, 28, 29, 30, 31, 'Dec']

Rich Comparison and Logical Operations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Rich comparison (==, !=, >, >=, <, <=) between :obj:`Week` objects is
supported. Adding or subtracting (+, -) an integer to/from a :obj:`Week` object
is also supported and results in a new :obj:`Week` with that number of weeks
added or subtracted. Containment operator (in) allows testing membership of a
:obj:`datetime.date` to the :obj:`Week` object. Using these operators with
an unexpected type of object raises a ``TypeError`` exception that can be
caught and handled in ``try`` and ``except`` blocks:

.. code-block:: pycon

   >>> week1 = Week(2019, 1)
   >>> week2 = Week(2018, 52)

   >>> week1 > week2
   True

   >>> (week1 - 1) == week2
   True

   >>> week1 + 3
   Week(2019, 4, CDC)

   >>> from datetime import date
   >>> date(2019, 1, 2) in week1
   True

   >>> week1 == "2019W01"
   Traceback...
   TypeError: Can't compare 'Week' to 'str'

Validation of Input data
~~~~~~~~~~~~~~~~~~~~~~~~

Input values validation is enabled by default (:obj:`Week` validation can be
disabled to improve performance). Invalid values raises ``ValueError``
exception that can be caught and handled in ``try`` and ``except`` blocks:

.. code-block:: pycon

   >>> Week(2018, 53)
   Traceback...
   ValueError: Week must be in 1..52 for year: 53

   >>> Week.fromstring("2019W01", system="mmwr")
   Traceback...
   ValueError: System must be in ('cdc', 'iso'): 'mmwr'

   >>> Year(22019)
   Traceback...
   ValueError: Year must be in 1..9999: 22019

Online Tool
-----------

The following is a simple online tool that was developed to calculate
epidemiological weeks (CDC system only) using the latest version of
this package:

https://www.dralshehri.com/epiweeks/

Source Code
-----------

The source code of this package is available on
`GitHub <https://github.com/dralshehri/epiweeks>`__ where you can
contribute and report issues.

Authors
-------

The main author is Mohammed Alshehri —
`@dralshehri <https://github.com/dralshehri>`__.

License
-------

This package is distributed under an MIT license.
The license is as follows:

.. literalinclude:: ../LICENSE
   :language: text

API Reference
-------------

This section documents the API of `epiweeks` module, which is the main module
of this package.

.. autoclass:: Week
.. autoclass:: Year
