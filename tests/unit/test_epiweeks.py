import pytest
from datetime import date, timedelta
import epiweeks as epi


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ((date(2014, 12, 28), "cdc"), (2014, 53)),
        ((date(2014, 12, 28), "iso"), (2014, 52)),
        ((date(2015, 1, 2), "cdc"), (2014, 53)),
        ((date(2015, 1, 2), "iso"), (2015, 1)),
        ((date(2016, 2, 14), "cdc"), (2016, 7)),
        ((date(2016, 2, 14), "iso"), (2016, 6)),
        ((date(2017, 12, 31), "cdc"), (2018, 1)),
        ((date(2017, 12, 31), "iso"), (2017, 52)),
    ],
)
def test_week_fromdate(test_input, expected):
    week = epi.Week.fromdate(*test_input)
    assert week.weektuple() == expected


def test_thisweek_cdc():
    week = epi.Week.thisweek("cdc")
    today_weekday = date.today().isoweekday()
    startdate = date.today() - timedelta(days=(today_weekday % 7))
    assert week.startdate() == startdate


def test_thisweek_iso():
    week = epi.Week.thisweek("iso")
    today_weekday = date.today().isoweekday()
    startdate = date.today() - timedelta(days=today_weekday - 1)
    assert week.startdate() == startdate


@pytest.fixture(scope="module")
def week_cdc():
    return epi.Week(2015, 1, "cdc")


@pytest.fixture(scope="module")
def week_iso():
    return epi.Week(2015, 1, "iso")


def test_representation_of_week(week_cdc, week_iso):
    assert week_cdc.__repr__() == "Week(2015, 1, cdc)"
    assert week_iso.__repr__() == "Week(2015, 1, iso)"


def test_string_representation_of_week(week_cdc):
    assert week_cdc.__str__() == "2015W01"


def test_week_equality(week_cdc):
    assert week_cdc == epi.Week(2015, 1)
    assert week_cdc != epi.Week(2014, 1)


def test_week_ordering(week_cdc):
    assert week_cdc > epi.Week(2014, 53)
    assert week_cdc >= epi.Week(2015, 1)
    assert week_cdc < epi.Week(2015, 2)
    assert week_cdc <= epi.Week(2015, 1)


def test_week_addition(week_cdc):
    assert (week_cdc + 1) == epi.Week(2015, 2)


def test_week_subtracting(week_cdc):
    assert (week_cdc - 1) == epi.Week(2014, 53)


def test_week_containment(week_cdc, week_iso):
    assert date(2015, 1, 5) in week_cdc
    assert date(2015, 1, 1) in week_iso


def test_week_year(week_cdc):
    assert week_cdc.year == 2015


def test_week_number(week_cdc):
    assert week_cdc.week == 1


def test_week_method(week_cdc, week_iso):
    assert week_cdc.method == "CDC"
    assert week_iso.method == "ISO"


def test_weektuple(week_cdc):
    assert week_cdc.weektuple() == (2015, 1)


def test_week_isoformat(week_cdc):
    assert week_cdc.isoformat() == "2015W01"


def test_week_startdate(week_cdc, week_iso):
    assert week_cdc.startdate() == date(2015, 1, 4)
    assert week_iso.startdate() == date(2014, 12, 29)


def test_week_enddate(week_cdc, week_iso):
    assert week_cdc.enddate() == date(2015, 1, 10)
    assert week_iso.enddate() == date(2015, 1, 4)


def test_week_dates(week_cdc, week_iso):
    dates_cdc = [
        date(2015, 1, 4),
        date(2015, 1, 5),
        date(2015, 1, 6),
        date(2015, 1, 7),
        date(2015, 1, 8),
        date(2015, 1, 9),
        date(2015, 1, 10),
    ]
    dates_iso = [
        date(2014, 12, 29),
        date(2014, 12, 30),
        date(2014, 12, 31),
        date(2015, 1, 1),
        date(2015, 1, 2),
        date(2015, 1, 3),
        date(2015, 1, 4),
    ]
    assert list(week_cdc.iterdates()) == dates_cdc
    assert list(week_iso.iterdates()) == dates_iso


@pytest.mark.parametrize(
    "test_input", ["__eq__", "__gt__", "__ge__", "__lt__", "__le__"]
)
def test_test_week_comparison_exception(week_cdc, test_input):
    with pytest.raises(TypeError) as e:
        getattr(week_cdc, test_input)("w")
    assert str(e.value) == "second operand must be 'Week' object"


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("__add__", "second operand must be 'int'"),
        ("__sub__", "second operand must be 'int'"),
        ("__contains__", "tested operand must be 'date' object"),
    ],
)
def test_test_week_operator_exception(week_cdc, test_input, expected):
    with pytest.raises(TypeError) as e:
        getattr(week_cdc, test_input)("w")
    assert str(e.value) == expected


def test_thisyear_cdc():
    year = epi.Year.thisyear("cdc")
    today_year = date.today().year
    assert year.startdate().toordinal() == epi._year_start(today_year, "cdc")


def test_thisyear_iso():
    year = epi.Year.thisyear("iso")
    today_year = date.today().year
    assert year.startdate().toordinal() == epi._year_start(today_year, "iso")


@pytest.fixture(scope="module")
def year_cdc():
    return epi.Year(2015, "cdc")


@pytest.fixture(scope="module")
def year_iso():
    return epi.Year(2015, "iso")


def test_representation_of_year(year_cdc, year_iso):
    assert year_cdc.__repr__() == "Year(2015, cdc)"
    assert year_iso.__repr__() == "Year(2015, iso)"


def test_string_representation_of_year(year_cdc):
    assert year_cdc.__str__() == "2015"


def test_year_number(year_cdc):
    assert year_cdc.year == 2015


def test_year_method(year_cdc, year_iso):
    assert year_cdc.method == "CDC"
    assert year_iso.method == "ISO"


def test_year_totalweeks(year_cdc, year_iso):
    assert year_cdc.totalweeks == 52
    assert year_iso.totalweeks == 53


def test_year_startdate(year_cdc, year_iso):
    assert year_cdc.startdate() == date(2015, 1, 4)
    assert year_iso.startdate() == date(2014, 12, 29)


def test_year_enddate(year_cdc, year_iso):
    assert year_cdc.enddate() == date(2016, 1, 2)
    assert year_iso.enddate() == date(2016, 1, 3)


def test_year_weeks(year_cdc, year_iso):
    cdc_weeks = []
    for w in range(1, 53):
        cdc_weeks.append(epi.Week(2015, w))
    assert list(year_cdc.iterweeks()) == cdc_weeks
    iso_weeks = []
    for w in range(1, 54):
        iso_weeks.append(epi.Week(2015, w, "iso"))
    assert list(year_iso.iterweeks()) == iso_weeks


def test_check_valid_week():
    try:
        epi._check_week(2018, 1, "cdc")
    except (TypeError or ValueError):
        pytest.fail("week should be valid")


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ((2015, "w", "cdc"), "week must be an integer"),
        ((2015, 0, "cdc"), "week must be in 1..52 for year"),
        ((2015, 53, "cdc"), "week must be in 1..52 for year"),
    ],
)
def test_check_invalid_week(test_input, expected):
    with pytest.raises((TypeError, ValueError)) as e:
        epi._check_week(*test_input)
    assert str(e.value) == expected


def test_check_valid_year():
    try:
        epi._check_year(2018)
    except (TypeError or ValueError):
        pytest.fail("year should be valid")


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("y", "year must be an integer"),
        (0, "year must be in 1..9999"),
        (20155, "year must be in 1..9999"),
    ],
)
def test_check_invalid_year(test_input, expected):
    with pytest.raises((TypeError, ValueError)) as e:
        epi._check_year(test_input)
    assert str(e.value) == expected


def test_check_valid_method():
    try:
        epi._check_method("CDC")
        epi._check_method("iso")
    except (TypeError or ValueError):
        pytest.fail("method should be valid")


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (0, "method must be a string"),
        ("mmwr", "method must be 'cdc' or 'iso'"),
    ],
)
def test_check_invalid_method(test_input, expected):
    with pytest.raises((TypeError, ValueError)) as e:
        epi._check_method(test_input)
    assert str(e.value) == expected


@pytest.mark.parametrize("test_input, expected", [("cdc", 1), ("iso", 0)])
def test_method_adjustment(test_input, expected):
    assert epi._method_adjustment(test_input) == expected


@pytest.mark.parametrize(
    "test_input, expected", [((2015, "cdc"), 735602), ((2015, "iso"), 735596)]
)
def test_year_start_ordinal(test_input, expected):
    assert epi._year_start(*test_input) == expected


@pytest.mark.parametrize(
    "test_input, expected", [((2015, "cdc"), 52), ((2015, "iso"), 53)]
)
def test_year_total_weeks(test_input, expected):
    assert epi._year_total_weeks(*test_input) == expected
