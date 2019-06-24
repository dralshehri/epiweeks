from datetime import date, timedelta
from typing import Tuple, Iterator


class Week:
    """A Week object represents a week in epidemiological week calendar."""

    __slots__ = "_year", "_week", "_method"

    def __init__(
        self, year: int, week: int, method: str = "CDC", validate: bool = True
    ) -> None:
        """
        :param year: Epidemiological year
        :type year: int
        :param week: Epidemiological week
        :type week: int
        :param method: Calculation method, which may be ``CDC`` where the week
            starts on Sunday or ``ISO`` where the week starts on Monday
            (default is ``CDC``)
        :type method: str
        :param validate: Whether to validate year, week and method or not
            (default is ``True``)
        :type validate: bool
        """

        if validate:
            _check_year(year)
            _check_method(method)
            _check_week(year, week, method)

        self._year = year
        self._week = week
        self._method = method.upper()

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}({self._year}, {self._week}, {self._method})"

    def __str__(self) -> str:
        return self.cdcformat() if self._method == "CDC" else self.isoformat()

    def __hash__(self) -> int:
        return hash((self._year, self._week, self._method))

    def __eq__(self, other: "Week") -> bool:
        return self._compare(other) == 0

    def __gt__(self, other: "Week") -> bool:
        return self._compare(other) > 0

    def __ge__(self, other: "Week") -> bool:
        return self._compare(other) >= 0

    def __lt__(self, other: "Week") -> bool:
        return self._compare(other) < 0

    def __le__(self, other: "Week") -> bool:
        return self._compare(other) <= 0

    def _compare(self, other: "Week") -> int:
        """Compare two Week objects after checking if they are comparable."""
        class_name = self.__class__.__name__
        other_name = type(other).__name__
        if not isinstance(other, self.__class__):
            raise TypeError(f"can't compare '{class_name}' to '{other_name}'")
        if self._method != other._method:
            raise TypeError(
                f"can't compare '{class_name}' objects with different "
                f"calculation methods"
            )
        x = self.weektuple()
        y = other.weektuple()
        return 0 if x == y else 1 if x > y else -1

    def __add__(self, other: int) -> "Week":
        if not isinstance(other, int):
            raise TypeError("second operand must be 'int'")
        new_date = self.startdate() + timedelta(weeks=other)
        return self.__class__.fromdate(new_date, self._method)

    def __sub__(self, other: int) -> "Week":
        if not isinstance(other, int):
            raise TypeError("second operand must be 'int'")
        return self.__add__(-other)

    def __contains__(self, other: date) -> bool:
        if not isinstance(other, date):
            raise TypeError("tested operand must be 'datetime.date' object")
        return other in self.iterdates()

    @classmethod
    def fromdate(cls, date_object: date, method: str = "CDC") -> "Week":
        """Construct Week object from a date.

        :param date_object: Gregorian date object
        :type date_object: datetime.date
        :param method: Calculation method, which may be ``CDC`` where the week
            starts on Sunday or ``ISO`` where the week starts on Monday
            (default is ``CDC``)
        :type method: str
        """

        _check_method(method)
        year = date_object.year
        date_ordinal = date_object.toordinal()
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
    def fromstring(
        cls, week_string: str, method: str = "CDC", validate: bool = True
    ) -> "Week":
        """Construct Week object from a formatted string.

        :param week_string: Week string formatted as ‘YYYYww’, ‘YYYYWww’,
            or ‘YYYY-Www’ for example ‘201908’, ‘2019W08’, or ‘2019-W08’.
            If the string ends with weekday as in ISO formats, weekday will
            be ignored.
        :type week_string: str
        :param method: Calculation method, which may be ``CDC`` where the week
            starts on Sunday or ``ISO`` where the week starts on Monday
            (default is ``CDC``)
        :type method: str
        :param validate: Whether to validate year, week and method or not
            (default is ``True``)
        :type validate: bool
        """

        week_string = week_string.replace("-", "").replace("W", "")
        year = int(week_string[:4])
        week = int(week_string[4:6])
        return cls(year, week, method, validate)

    @classmethod
    def thisweek(cls, method: str = "CDC") -> "Week":
        """Construct Week object from current date.

        :param method: Calculation method, which may be ``CDC`` where the week
            starts on Sunday or ``ISO`` where the week starts on Monday
            (default is ``CDC``)
        :type method: str
        """

        return cls.fromdate(date.today(), method)

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

    def cdcformat(self) -> str:
        """Return a string representing the week in CDC format ‘YYYYww’ for
        example ‘201908’.
        """

        return f"{self._year:04}{self._week:02}"

    def isoformat(self) -> str:
        """Return a string representing the week in ISO compact format
        ‘YYYYWww’ for example ‘2019W08’.
        """

        return f"{self._year:04}W{self._week:02}"

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

    def iterdates(self) -> Iterator[date]:
        """Return an iterator that yield date objects for all days of week."""
        startdate = self.startdate()
        for day in range(0, 7):
            yield startdate + timedelta(days=day)

    def daydate(self, weekday: int = 6) -> date:
        """Return date for specific weekday of week.

        :param weekday: Week day, which may be ``0..6`` where Monday is 0 and
            Sunday is 6 (default is ``6``)
        :type weekday: int
        """

        diff = (_method_adjustment(self._method) + weekday) % 7
        return self.startdate() + timedelta(days=diff)


class Year:
    """A Year object represents a year in epidemiological week calendar."""

    __slots__ = "_year", "_method"

    def __init__(self, year: int, method: str = "CDC") -> None:
        """
        :param year: Epidemiological year
        :type year: int
        :param method: Calculation method, which may be ``CDC`` where the week
            starts on Sunday or ``ISO`` where the week starts on Monday
            (default is ``CDC``)
        :type method: str
        """

        _check_year(year)
        _check_method(method)
        self._year = year
        self._method = method.upper()

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}({self._year}, {self._method})"

    def __str__(self) -> str:
        return f"{self._year:04}"

    def __hash__(self) -> int:
        return hash((self._year, self._method))

    @classmethod
    def thisyear(cls, method: str = "CDC") -> "Year":
        """Construct Year object from current date.

        :param method: Calculation method, which may be ``CDC`` where the week
            starts on Sunday or ``ISO`` where the week starts on Monday
            (default is ``CDC``)
        :type method: str
        """

        return cls(date.today().year, method)

    @property
    def year(self) -> int:
        """Return year as an integer"""
        return self._year

    @property
    def method(self) -> str:
        """Return calculation method as a string"""
        return self._method

    def totalweeks(self) -> int:
        """Return number of weeks in year."""
        return _year_total_weeks(self._year, self._method)

    def startdate(self) -> date:
        """Return date for first day of first week of year."""
        year_start_ordinal = _year_start(self._year, self._method)
        return date.fromordinal(year_start_ordinal)

    def enddate(self) -> date:
        """Return date for last day of last week of year."""
        year_end_ordinal = _year_start(self._year + 1, self._method) - 1
        return date.fromordinal(year_end_ordinal)

    def iterweeks(self) -> Iterator[Week]:
        """Return an iterator that yield Week objects for all weeks of year."""
        for week in range(1, self.totalweeks() + 1):
            yield Week(self._year, week, self._method, validate=False)


def _check_year(year: int) -> None:
    """Check value of year."""
    if not 1 <= year <= 9999:
        raise ValueError("year must be in 1..9999")


def _check_week(year: int, week: int, method: str) -> None:
    """Check value of week."""
    weeks = _year_total_weeks(year, method)
    if not 1 <= week <= weeks:
        raise ValueError(f"week must be in 1..{weeks} for year")


def _check_method(method: str) -> None:
    """Check value of calculation method."""
    methods = ["CDC", "ISO"]
    if method.upper() not in methods:
        raise ValueError(f"method must be '{methods[0]}' or '{methods[1]}'")


def _method_adjustment(method: str) -> int:
    """Return needed adjustment based on first day of week."""
    first_day = ("Mon", "Sun")
    if method.upper() == "CDC":
        return first_day.index("Sun")
    return first_day.index("Mon")


def _year_start(year: int, method: str) -> int:
    """Return ordinal for first day of first week for year."""
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
    """Return number of weeks in year."""
    year_start_ordinal = _year_start(year, method)
    next_year_start_ordinal = _year_start(year + 1, method)
    weeks = (next_year_start_ordinal - year_start_ordinal) // 7
    return weeks
