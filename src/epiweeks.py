from datetime import date, timedelta
from typing import Tuple, Generator


class Week:
    """A Week object represents a week in epidemiological week calendar
    using CDC or WHO calculation method.
    """

    def __init__(
        self, year: int, week: int, method: str = "cdc", validate: bool = True
    ) -> None:
        """
        :param year: epidemiological year
        :type year: int
        :param week: epidemiological week
        :type week: int
        :param method: calculation method, which may be ``cdc`` for MMWR weeks
            or ``who`` for ISO weeks (default is ``cdc``)
        :type method: str
        :param validate: check if values of year, week and method are valid
            or not (default is ``True``), and you may change it to ``False``
            only when these values are already validated.
        :type validate: bool
        """

        if validate:
            self._year = _check_year(year)
            self._method = _check_method(method)
            self._week = _check_week(self._year, week, self._method)
        else:
            self._year = year
            self._week = week
            self._method = method

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return "{}({}, {}, {})".format(
            class_name, self._year, self._week, self._method
        )

    def __str__(self) -> str:
        return self.isoformat()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Week):
            raise TypeError("second operand must be 'Week' object")
        return self.weektuple() == other.weektuple()

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Week):
            raise TypeError("second operand must be 'Week' object")
        return self.weektuple() > other.weektuple()

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, Week):
            raise TypeError("second operand must be 'Week' object")
        return self.weektuple() >= other.weektuple()

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Week):
            raise TypeError("second operand must be 'Week' object")
        return self.weektuple() < other.weektuple()

    def __le__(self, other: object) -> bool:
        if not isinstance(other, Week):
            raise TypeError("second operand must be 'Week' object")
        return self.weektuple() <= other.weektuple()

    def __add__(self, other: int) -> "Week":
        if not isinstance(other, int):
            raise TypeError("second operand must be 'int'")
        new_date = self.startdate() + timedelta(weeks=other)
        year, month, day = new_date.timetuple()[:3]
        return Week.fromdate(year, month, day, self._method)

    def __sub__(self, other: int) -> "Week":
        if not isinstance(other, int):
            raise TypeError("second operand must be 'int'")
        return self + (-other)

    def __contains__(self, other: date) -> bool:
        if not isinstance(other, date):
            raise TypeError("tested operand must be 'date' object")
        return other in self.iterdates()

    @classmethod
    def fromdate(
        cls, year: int, month: int, day: int, method: str = "cdc"
    ) -> "Week":
        """Construct Week object from a Gregorian date (year, month and day).

        :param year: Gregorian year
        :type year: int
        :param month: Gregorian month
        :type month: int
        :param day: Gregorian day
        :type day: int
        :param method: calculation method, which may be ``cdc`` for MMWR weeks
            or ``who`` for ISO weeks (default is ``cdc``)
        :type method: str
        """

        method = _check_method(method)
        date_ordinal = date(year, month, day).toordinal()
        year_start_ordinal = _year_start(year, method)
        week = (date_ordinal - year_start_ordinal) // 7
        if week < 0:
            year -= 1
            year_start_ordinal = _year_start(year, method)
            week = (date_ordinal - year_start_ordinal) // 7
        elif week >= 52:
            year_start_ordinal = _year_start(year + 1, method)
            if date_ordinal >= year_start_ordinal:
                year += 1
                week = 0
        week += 1
        return cls(year, week, method, validate=False)

    @classmethod
    def thisweek(cls, method: str = "cdc") -> "Week":
        """Construct Week object from current Gregorian date.

        :param method: calculation method, which may be ``cdc`` for MMWR weeks
            or ``who`` for ISO weeks (default is ``cdc``)
        :type method: str
        """

        year, month, day = date.today().timetuple()[:3]
        return cls.fromdate(year, month, day, method)

    @property
    def year(self) -> int:
        """Return year as an integer"""
        return self._year

    @property
    def week(self) -> int:
        """Return week number as an integer"""
        return self._week

    @property
    def method(self) -> str:
        """Return calculation method as a string"""
        return self._method

    def weektuple(self) -> Tuple[int, int]:
        """Return week as a tuple of (year, week)."""
        return self._year, self._week

    def isoformat(self) -> str:
        """Return a string representing the week in compact form of ISO format
        ‘YYYYWww’.
        """

        return "{:04}W{:02}".format(self._year, self._week)

    def startdate(self) -> date:
        """Return date for first day of week."""
        year_start_ordinal = _year_start(self._year, self._method)
        week_start_ordinal = year_start_ordinal + ((self._week - 1) * 7)
        startdate = date.fromordinal(week_start_ordinal)
        return startdate

    def enddate(self) -> date:
        """Return date for last day of week."""
        enddate = self.startdate() + timedelta(days=6)
        return enddate

    def iterdates(self) -> Generator[date, None, None]:
        """Return an iterator that yield datetime.date objects for all days of
        week."""

        startdate = self.startdate()
        for day in range(0, 7):
            yield startdate + timedelta(days=day)


class Year:
    """A Year object represents a year in epidemiological week calendar
    using US CDC or WHO calculation method.
    """

    def __init__(self, year: int, method: str = "cdc") -> None:
        """
        :param year: epidemiological year
        :type year: int
        :param method: calculation method, which may be ``cdc`` for MMWR weeks
            or ``who`` for ISO weeks (default is ``cdc``)
        :type method: str
        """

        self._year = _check_year(year)
        self._method = _check_method(method)

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return "{}({}, {})".format(class_name, self._year, self._method)

    def __str__(self) -> str:
        return "{:04}".format(self._year)

    @property
    def year(self) -> int:
        """Return year as an integer"""
        return self._year

    @property
    def method(self) -> str:
        """Return calculation method as a string"""
        return self._method

    @property
    def totalweeks(self) -> int:
        """Return number of weeks in year as an integer"""
        return _year_total_weeks(self._year, self._method)

    def startdate(self) -> date:
        """Return date for first day of first week of year."""
        year_start_ordinal = _year_start(self._year, self._method)
        return date.fromordinal(year_start_ordinal)

    def enddate(self) -> date:
        """Return date for last day of last week of year."""
        year_end_ordinal = _year_start(self._year + 1, self._method) - 1
        return date.fromordinal(year_end_ordinal)

    def iterweeks(self) -> Generator[Week, None, None]:
        """Return an iterator that yield Week objects for all weeks of year."""
        for week in range(1, self.totalweeks + 1):
            yield Week(self._year, week, self._method, validate=False)


def _check_year(year: int) -> int:
    """Check type and value of year."""
    if not isinstance(year, int):
        raise TypeError("year must be an integer")
    if not 1 <= year <= 9999:
        raise ValueError("year must be in 1..9999")
    return year


def _check_week(year: int, week: int, method: str) -> int:
    """Check type and value of week."""
    if not isinstance(week, int):
        raise TypeError("week must be an integer")
    weeks = _year_total_weeks(year, method)
    if not 1 <= week <= weeks:
        raise ValueError("week must be in 1..{} for year".format(weeks))
    return week


def _check_method(method: str) -> str:
    """Check type and value of calculation method."""
    if not isinstance(method, str):
        raise TypeError("method must be a string")
    method = method.lower()
    methods = ["cdc", "who"]
    if method not in methods:
        raise ValueError("method must be '{}' or '{}'".format(*methods))
    return method


def _method_adjustment(method: str) -> int:
    """Return needed adjustment based on first day of week using given
    calculation method.
    """

    first_day = ("Mon", "Sun")
    if method.lower() == "cdc":
        return first_day.index("Sun")
    return first_day.index("Mon")


def _year_start(year: int, method: str) -> int:
    """Return proleptic Gregorian ordinal for first day of first week for
    given year using given calculation method.
    """

    adjustment = _method_adjustment(method)
    mid_weekday = 3 - adjustment  # Sun is 6 .. Mon is 0
    jan1 = date(year, 1, 1)
    jan1_ordinal = jan1.toordinal()
    jan1_weekday = jan1.weekday()
    week1_start_ordinal = jan1_ordinal - jan1_weekday - adjustment
    if jan1_weekday > mid_weekday:
        week1_start_ordinal += 7
    return week1_start_ordinal


def _year_total_weeks(year: int, method: str) -> int:
    """Return number of weeks in year for given year using given calculation
    method.
    """

    year_start_ordinal = _year_start(year, method)
    next_year_start_ordinal = _year_start(year + 1, method)
    weeks = (next_year_start_ordinal - year_start_ordinal) // 7
    return weeks
