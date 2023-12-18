"""Epidemiological weeks calculation based on the US CDC (MMWR) and ISO week
numbering systems.

https://github.com/dralshehri/epiweeks
"""

__version__ = "2.3.0"

from datetime import date, timedelta
from typing import Iterator, Tuple


class Week:
    """A Week object represents a week in epidemiological week calendar."""

    __slots__ = "_year", "_week", "_system"

    def __init__(
        self, year: int, week: int, system: str = "cdc", validate: bool = True
    ):
        """
        Args:
            year: Epidemiological year.
            week: Epidemiological week.
            system: Week numbering system, which may be ``cdc`` where the
                week starts on Sunday or ``iso`` where the week starts on
                Monday.
            validate: Whether to validate year, week and system or not.

        Raises:
            ValueError: When ``year`` is out of supported range.
            ValueError: When ``week`` is out of weeks range for year.
            ValueError: When ``system`` is not within supported systems.
        """

        if validate:
            _check_year(year)
            _check_system(system)
            _check_week(year, week, system)

        self._year = year
        self._week = week
        self._system = system.upper()

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}({self._year}, {self._week}, {self._system})"

    def __str__(self) -> str:
        return self.cdcformat() if self._system == "CDC" else self.isoformat()

    def __hash__(self) -> int:
        return hash((self._year, self._week, self._system))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._compare(other) == 0

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._compare(other) > 0

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._compare(other) >= 0

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._compare(other) < 0

    def __le__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._compare(other) <= 0

    def _compare(self, other: "Week") -> int:
        """Compare two Week objects after checking if they are comparable."""
        class_name = self.__class__.__name__
        if self._system != other.system:
            raise TypeError(
                f"Can not compare '{class_name}' objects with different "
                f"numbering systems: '{self._system}' and '{other.system}'"
            )
        self_week = self.weektuple()
        other_week = other.weektuple()
        return (
            0
            if self_week == other_week
            else 1
            if self_week > other_week
            else -1
        )

    def __add__(self, other: int) -> "Week":
        if not isinstance(other, int):
            other_type = type(other).__name__
            raise TypeError(f"Second operand must be 'int': {other_type}")
        new_date = self.startdate() + timedelta(weeks=other)
        return self.__class__.fromdate(new_date, self._system)

    def __sub__(self, other: int) -> "Week":
        if not isinstance(other, int):
            other_type = type(other).__name__
            raise TypeError(f"Second operand must be 'int': {other_type}")
        return self.__add__(-other)

    def __contains__(self, other: date) -> bool:
        if not isinstance(other, date):
            other_type = type(other).__name__
            raise TypeError(
                f"Tested operand must be 'datetime.date' object: {other_type}"
            )
        return other in self.iterdates()

    @classmethod
    def fromdate(cls, date_object: date, system: str = "cdc") -> "Week":
        """Construct Week object from a date.

        Args:
            date_object: Python date object.
            system: Week numbering system, which may be ``cdc`` where the
                week starts on Sunday or ``iso`` where the week starts on
                Monday.
        """

        _check_system(system)
        year = date_object.year
        date_ordinal = date_object.toordinal()
        year_start_ordinal = _year_start(year, system)
        week = (date_ordinal - year_start_ordinal) // 7
        if week < 0:
            year -= 1
            year_start_ordinal = _year_start(year, system)
            week = (date_ordinal - year_start_ordinal) // 7
        elif week >= 52:
            year_start_ordinal = _year_start(year + 1, system)
            if date_ordinal >= year_start_ordinal:
                year += 1
                week = 0
        week += 1
        return cls(year, week, system, validate=False)

    @classmethod
    def fromstring(
        cls, week_string: str, system: str = "cdc", validate: bool = True
    ) -> "Week":
        """Construct Week object from a formatted string.

        Args:
            week_string: Week string formatted as ``YYYYww``, ``YYYYWww``,
                or ``YYYY-Www``. If the string ends with weekday as in ISO
                formats, weekday will be ignored.
            system: Week numbering system, which may be ``cdc`` where the
                week starts on Sunday or ``iso`` where the week starts on
                Monday.
            validate: Whether to validate year, week and system or not.
        """

        week_string = week_string.replace("-", "").replace("W", "")
        year = int(week_string[0:4])
        week = int(week_string[4:6])
        return cls(year, week, system, validate)

    @classmethod
    def thisweek(cls, system: str = "cdc") -> "Week":
        """Construct Week object from current date.

        Args:
            system: Week numbering system, which may be ``cdc`` where the
                week starts on Sunday or ``iso`` where the week starts on
                Monday.
        """

        return cls.fromdate(date.today(), system)

    @property
    def year(self) -> int:
        """Return year as an integer"""
        return self._year

    @property
    def week(self) -> int:
        """Return week number as an integer"""
        return self._week

    @property
    def system(self) -> str:
        """Return week numbering system as a string"""
        return self._system

    def weektuple(self) -> Tuple[int, int]:
        """Return week as a tuple of (year, week)."""
        return self._year, self._week

    def cdcformat(self) -> str:
        """Return a string representing the week in CDC format ``YYYYww``."""
        return f"{self._year:04}{self._week:02}"

    def isoformat(self) -> str:
        """Return a string representing the week in ISO compact format
        ``YYYYWww``.
        """
        return f"{self._year:04}W{self._week:02}"

    def startdate(self) -> date:
        """Return date for first day of week."""
        year_start_ordinal = _year_start(self._year, self._system)
        week_start_ordinal = year_start_ordinal + ((self._week - 1) * 7)
        startdate = date.fromordinal(week_start_ordinal)
        return startdate

    def enddate(self) -> date:
        """Return date for last day of week."""
        enddate = self.startdate() + timedelta(days=6)
        return enddate

    def iterdates(self) -> Iterator[date]:
        """Return an iterator that yield date objects for all days of week."""
        startdate = self.startdate()
        for day in range(0, 7):
            yield startdate + timedelta(days=day)

    def daydate(self, weekday: int = 6) -> date:
        """Return date for specific weekday of week.

        Args:
            weekday: Week day, which may be ``0..6`` where Monday is 0 and
                Sunday is 6.
        """

        diff = (_system_adjustment(self._system) + weekday) % 7
        return self.startdate() + timedelta(days=diff)


class Year:
    """A Year object represents a year in epidemiological week calendar."""

    __slots__ = "_year", "_system"

    def __init__(self, year: int, system: str = "cdc"):
        """
        Args:
            year: Epidemiological year.
            system: Week numbering system, which may be ``cdc`` where the
                week starts on Sunday or ``iso`` where the week starts on
                Monday.

        Raises:
            ValueError: When ``year`` is out of supported range.
            ValueError: When ``system`` is not within supported systems.
        """

        _check_year(year)
        _check_system(system)
        self._year = year
        self._system = system.upper()

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}({self._year}, {self._system})"

    def __str__(self) -> str:
        return f"{self._year:04}"

    def __hash__(self) -> int:
        return hash((self._year, self._system))

    @classmethod
    def thisyear(cls, system: str = "cdc") -> "Year":
        """Construct Year object from current date.

        Args:
            system: Week numbering system, which may be ``cdc`` where the
                week starts on Sunday or ``iso`` where the week starts on
                Monday.
        """

        return cls(date.today().year, system)

    @property
    def year(self) -> int:
        """Return year as an integer"""
        return self._year

    @property
    def system(self) -> str:
        """Return week numbering system as a string"""
        return self._system

    def totalweeks(self) -> int:
        """Return number of weeks in year."""
        return _year_total_weeks(self._year, self._system)

    def startdate(self) -> date:
        """Return date for first day of first week of year."""
        year_start_ordinal = _year_start(self._year, self._system)
        return date.fromordinal(year_start_ordinal)

    def enddate(self) -> date:
        """Return date for last day of last week of year."""
        year_end_ordinal = _year_start(self._year + 1, self._system) - 1
        return date.fromordinal(year_end_ordinal)

    def iterweeks(self) -> Iterator[Week]:
        """Return an iterator that yield Week objects for all weeks of year."""
        for week in range(1, self.totalweeks() + 1):
            yield Week(self._year, week, self._system, validate=False)


def _check_year(year: int) -> None:
    """Check value of year."""
    max_years = 9999
    if not 1 <= year <= max_years:
        raise ValueError(f"Year must be in 1..{max_years}")


def _check_week(year: int, week: int, system: str) -> None:
    """Check value of week."""
    max_weeks = _year_total_weeks(year, system)
    if not 1 <= week <= max_weeks:
        raise ValueError(f"Week must be in 1..{max_weeks} for year")


def _check_system(system: str) -> None:
    """Check value of week numbering system."""
    systems = ("cdc", "iso")
    if system.lower() not in systems:
        raise ValueError(f"System must be in {systems}")


def _system_adjustment(system: str) -> int:
    """Return needed adjustment based on week numbering system."""
    systems = ("iso", "cdc")  # Monday, Sunday
    return systems.index(system.lower())


def _year_start(year: int, system: str) -> int:
    """Return ordinal for first day of first week for year."""
    adjustment = _system_adjustment(system)
    mid_weekday = 3 - adjustment  # Sun is 6 .. Mon is 0
    jan1 = date(year, 1, 1)
    jan1_ordinal = jan1.toordinal()
    jan1_weekday = jan1.weekday()
    week1_start_ordinal = jan1_ordinal - jan1_weekday - adjustment
    if jan1_weekday > mid_weekday:
        week1_start_ordinal += 7
    return week1_start_ordinal


def _year_total_weeks(year: int, system: str) -> int:
    """Return number of weeks in year."""
    year_start_ordinal = _year_start(year, system)
    next_year_start_ordinal = _year_start(year + 1, system)
    weeks = (next_year_start_ordinal - year_start_ordinal) // 7
    return weeks
