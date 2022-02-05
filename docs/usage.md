---
hide-toc: true
---

# Usage Examples

```{eval-rst}
.. currentmodule:: epiweeks
```

## Week Instance and Methods

You can create an instance of {obj}`Week` object by only providing the year and
week number:

```pycon
>>> from epiweeks import Week

>>> Week(2019, 1)
Week(2019, 1, CDC)
```

It is also possible to create an instance of {obj}`Week` object from a date,
formatted string, or current date:

```pycon
>>> from datetime import date
>>> from epiweeks import Week

>>> my_date = date(2018, 12, 30)
>>> Week.fromdate(my_date)
Week(2019, 1, CDC)

>>> Week.fromstring("2019W01")
Week(2019, 1, CDC)

>>> Week.thisweek()
Week(2019, 26, CDC)
```

By default, the US CDC system is assumed when creating the {obj}`Week` object
instance. To use the ISO system instead:

```pycon
>>> from epiweeks import Week

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
```

The instance of {obj}`Week` object has also some other useful methods:

```pycon
>>> from epiweeks import Week

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
```

## Year Instance and Methods

You can create an instance of {obj}`Year` object by only providing the year, or
from current date:

```pycon
>>> from epiweeks import Year

>>> Year(2018)
Year(2018, CDC)

>>> Year.thisyear()
Year(2019, CDC)
```

By default, the US CDC system is assumed when creating the {obj}`Year` object
instance. To use the ISO system instead:

```pycon
>>> from epiweeks import Year

>>> Year(2018, system="iso")
Year(2018, ISO)

>>> Year.thisyear(system="iso")
Year(2019, ISO)
```

To get a list of {obj}`Week` objects for all weeks of a year:

```pycon
>>> from epiweeks import Year

>>> list(Year(2019).iterweeks())
[(Week(2019, 1, CDC), ..., Week(2019, 52, CDC))]
```

The instance of {obj}`Year` object has also some other useful methods:

```pycon
>>> from epiweeks import Year

>>> year = Year(2019)

>>> year.totalweeks()
52

>>> year.startdate()
datetime.date(2018, 12, 30)

>>> year.enddate()
datetime.date(2019, 12, 28)
```

## Generating Epidemiological Calendars

The epidemiological calendar can be easily generated using this package as
demonstrated in the following two examples.

To generate a week endings calendar for a year as in
[this document](https://wwwn.cdc.gov/nndss/document/W2018-19.pdf) by US CDC:

```python
from epiweeks import Year

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
```

To generate a full epidemiological calendar for a year as in
[this document](https://www.paho.org/hq/dmdocuments/2016/2016-cha-epidemiological-calendar.pdf)
by PAHO:

```python
from epiweeks import Year

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
```

## Rich Comparison and Logical Operations

Rich comparison (==, !=, >, >=, <, <=) between {obj}`Week` objects is supported.
Adding or subtracting (+, -) an integer to/from a {obj}`Week` object is also
supported and results in a new {obj}`Week` with that number of weeks added or
subtracted. Containment operator (in) allows testing membership of a
{obj}`datetime.date` to the {obj}`Week` object. Using these operators with an
unexpected type of object raises a `TypeError` exception that can be caught and
handled in `try` and `except` blocks:

```pycon
>>> from datetime import date
>>> from epiweeks import Week

>>> week1 = Week(2019, 1)
>>> week2 = Week(2018, 52)

>>> week1 > week2
True

>>> (week1 - 1) == week2
True

>>> week1 + 3
Week(2019, 4, CDC)

>>> date(2019, 1, 2) in week1
True

>>> week1 == "2019W01"
Traceback (most recent call last):
    ...
TypeError: "Can't compare 'Week' to 'str'"
```

## Validation of Input data

Input values validation is enabled by default ({obj}`Week` validation can be
disabled to improve performance). Invalid values raises `ValueError` exception
that can be caught and handled in `try` and `except` blocks:

```pycon
>>> from epiweeks import Week, Year

>>> Week(2018, 53)
Traceback (most recent call last):
    ...
ValueError: Week must be in 1..52 for year: 53

>>> Week.fromstring("2019W01", system="mmwr")
Traceback (most recent call last):
    ...
ValueError: "System must be in ('cdc', 'iso'): 'mmwr'"

>>> Year(22019)
Traceback (most recent call last):
    ...
ValueError: "Year must be in 1..9999: 22019"
```
