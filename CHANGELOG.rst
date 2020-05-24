Change Log
----------

**2.1.2**

- Improved exception messages by including the type or value used.
- Improved PyPI packaging by removing unnecessary files.
- Updated related tests and documentations.

**2.1.1**

- Fixed some typos.
- Improved documentation.

**2.1.0**

- Changed the parameter ``method``, which sets how the weeks are
  numbered, to ``system`` for better clarity and intuitive usage.
- Updated documentation and unit tests.
- Other minor fixes and enhancements.

**2.0.0**

- Dropped support for Python 3.5.
- Added ``fromstring()`` classmethod to allow constructing the ``Week`` object
  from a formatted string, for example '2019W08' or '201908'.
- Added ``cdcformat()`` method to return a formatted string like the one used
  by US CDC for epi weeks, for example for week 8 of 2019 it returns '201908'.
- Added ``daydate()`` method to return the date of specific weekday for a week.
- Changed the optional value 'WHO' of the parameter ``method`` to 'ISO'.
- Changed the ``fromdate()`` classmethod of ``Week`` object to accept a date
  object as an argument instead of year, month, and day.
- Made the ``Week`` and ``Year`` objects hashable.
- Improved rich comparison methods.
- Improved input data validation.
- Updated and improved documentation examples.
- Updated unit tests.
- Other minor fixes and enhancements.

**1.0.0**

- First release.
