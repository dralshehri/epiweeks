# Changelog

The versioning scheme is compliant with the [PEP 440] specification.

[PEP 440]: https://peps.python.org/pep-0440/#public-version-identifiers

## 2.3.0 (2023-12-18)

- Dropped support for Python 3.7 and added support for Python 3.12.
- Changed documentation theme along with other enhancements.

## 2.2.0 (2023-04-24)

- Dropped support for Python 3.6 and added support for Python 3.11.
- Fixed location of type-checking marker file.
- Added more classifiers to package configuration.
- Updated documentation and removed badges from the package description.
- Updated development configurations and GitHub actions.
- Changed GitHub username back to @dralshehri and updated related links.

## 2.1.4 (2022-02-12)

- Changed package docstrings to Google style and updated documentation.
- Updated development workflows and configurations.
- Other minor fixes and enhancements.
- Changed GitHub username to @mhalshehri and updated related links.

## 2.1.3 (2021-09-24)

- Added `__version__` attribute to the package.
- Changed `Week` rich comparison to return `NotImplemented` when the second
  operand is not a `Week` object.
- Changed the project structure by converting the`epiweeks` module into a
  package.
- Updated packaging configuration files and local development workflow.
- Updated documentation structure and theme.
- Other minor fixes and enhancements.

## 2.1.2 (2020-05-24)

- Improved exception messages by including the type or value used.
- Improved PyPI packaging by removing unnecessary files.
- Updated related tests and documentations.

## 2.1.1 (2019-06-27)

- Fixed some typos.
- Improved documentation.

## 2.1.0 (2019-06-26)

- Changed the parameter `method`, which sets how the weeks are numbered, to
  `system` for better clarity and intuitive usage.
- Updated documentation and unit tests.
- Other minor fixes and enhancements.

## 2.0.0 (2019-06-25)

- Dropped support for Python 3.5.
- Added `fromstring()` classmethod to allow constructing the `Week` object from
  a formatted string, for example '2019W08' or '201908'.
- Added `cdcformat()` method to return a formatted string like the one used by
  US CDC for epi weeks, for example for week 8 of 2019 it returns '201908'.
- Added `daydate()` method to return the date of specific weekday for a week.
- Changed the optional value 'WHO' of the parameter `method` to 'ISO'.
- Changed the `fromdate()` classmethod of `Week` object to accept a date object
  as an argument instead of year, month, and day.
- Made the `Week` and `Year` objects hashable.
- Improved rich comparison methods.
- Improved input data validation.
- Updated and improved documentation examples.
- Updated unit tests.
- Other minor fixes and enhancements.

## 1.0.0 (2018-11-28)

- First release.
