from datetime import date, timedelta

import pytest

import epiweeks


@pytest.fixture(scope="module")
def week_cdc():
    return epiweeks.Week(2015, 1, system="cdc")


@pytest.fixture(scope="module")
def week_iso():
    return epiweeks.Week(2015, 1, system="iso")


def test_week_representation(week_cdc, week_iso):
    assert week_cdc.__repr__() == "Week(2015, 1, CDC)"
    assert week_iso.__repr__() == "Week(2015, 1, ISO)"


def test_week_string(week_cdc, week_iso):
    assert week_cdc.__str__() == "201501"
    assert week_iso.__str__() == "2015W01"


def test_week_hash(week_cdc, week_iso):
    assert week_cdc.__hash__() == hash((2015, 1, "CDC"))
    assert week_iso.__hash__() == hash((2015, 1, "ISO"))


def test_week_equality(week_cdc, week_iso):
    assert week_cdc == epiweeks.Week(2015, 1, system="cdc")
    assert week_cdc != epiweeks.Week(2014, 1, system="cdc")
    assert week_iso == epiweeks.Week(2015, 1, system="iso")
    assert week_iso != epiweeks.Week(2014, 1, system="iso")


def test_week_ordering(week_cdc, week_iso):
    assert week_cdc > epiweeks.Week(2014, 53, system="cdc")
    assert week_cdc >= epiweeks.Week(2015, 1, system="cdc")
    assert week_cdc < epiweeks.Week(2015, 2, system="cdc")
    assert week_cdc <= epiweeks.Week(2015, 1, system="cdc")
    assert week_iso > epiweeks.Week(2014, 52, system="iso")
    assert week_iso >= epiweeks.Week(2015, 1, system="iso")
    assert week_iso < epiweeks.Week(2015, 2, system="iso")
    assert week_iso <= epiweeks.Week(2015, 1, system="iso")


def test_week_addition(week_cdc, week_iso):
    assert (week_cdc + 1) == epiweeks.Week(2015, 2, system="cdc")
    assert (week_iso + 1) == epiweeks.Week(2015, 2, system="iso")


def test_week_subtracting(week_cdc, week_iso):
    assert (week_cdc - 1) == epiweeks.Week(2014, 53, system="cdc")
    assert (week_iso - 1) == epiweeks.Week(2014, 52, system="iso")


def test_week_containment(week_cdc, week_iso):
    assert date(2015, 1, 5) in week_cdc
    assert date(2015, 1, 1) in week_iso


@pytest.mark.parametrize(
    "test_input", ["__eq__", "__gt__", "__ge__", "__lt__", "__le__"]
)
def test_week_comparison_notimplemented(week_cdc, week_iso, test_input):
    assert getattr(week_cdc, test_input)("w") == NotImplemented
    assert getattr(week_iso, test_input)("w") == NotImplemented


@pytest.mark.parametrize(
    "test_input", ["__eq__", "__gt__", "__ge__", "__lt__", "__le__"]
)
def test_week_comparison_exception(week_cdc, week_iso, test_input):
    with pytest.raises(TypeError) as e:
        getattr(week_cdc, test_input)(week_iso)
    assert (
        str(e.value) == "Can't compare 'Week' objects with different "
        "numbering systems: 'CDC' and 'ISO'"
    )


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("__add__", "Second operand must be 'int'"),
        ("__sub__", "Second operand must be 'int'"),
        ("__contains__", "Tested operand must be 'datetime.date' object"),
    ],
)
def test_week_operator_exception(week_cdc, week_iso, test_input, expected):
    with pytest.raises(TypeError) as e:
        getattr(week_cdc, test_input)("w")
        getattr(week_iso, test_input)("w")
    assert str(e.value) == f"{expected}: {type('w').__name__}"


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
    week = epiweeks.Week.fromdate(*test_input)
    assert week.weektuple() == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (("201453", "cdc"), (2014, 53)),
        (("201607", "cdc"), (2016, 7)),
        (("2014W52", "iso"), (2014, 52)),
        (("2015W01", "iso"), (2015, 1)),
        (("2016-W06", "iso"), (2016, 6)),
        (("2018-W01-2", "iso"), (2018, 1)),
        (("2017W527", "iso"), (2017, 52)),
    ],
)
def test_week_fromstring(test_input, expected):
    week = epiweeks.Week.fromstring(*test_input)
    assert week.weektuple() == expected


def test_week_thisweek():
    cdc_week = epiweeks.Week.thisweek(system="cdc")
    cdc_diff = (date.today().weekday() + 1) % 7
    cdc_startdate = date.today() - timedelta(days=cdc_diff)
    assert cdc_week.startdate() == cdc_startdate
    iso_week = epiweeks.Week.thisweek(system="iso")
    iso_diff = date.today().isoweekday() - 1
    iso_startdate = date.today() - timedelta(days=iso_diff)
    assert iso_week.startdate() == iso_startdate


def test_week_year(week_cdc, week_iso):
    assert week_cdc.year == 2015
    assert week_iso.year == 2015


def test_week_number(week_cdc, week_iso):
    assert week_cdc.week == 1
    assert week_iso.week == 1


def test_week_system(week_cdc, week_iso):
    assert week_cdc.system == "CDC"
    assert week_iso.system == "ISO"


def test_weektuple(week_cdc, week_iso):
    assert week_cdc.weektuple() == (2015, 1)
    assert week_iso.weektuple() == (2015, 1)


def test_week_cdcformat(week_cdc):
    assert week_cdc.cdcformat() == "201501"


def test_week_isoformat(week_iso):
    assert week_iso.isoformat() == "2015W01"


def test_week_startdate(week_cdc, week_iso):
    assert week_cdc.startdate() == date(2015, 1, 4)
    assert week_iso.startdate() == date(2014, 12, 29)


def test_week_enddate(week_cdc, week_iso):
    assert week_cdc.enddate() == date(2015, 1, 10)
    assert week_iso.enddate() == date(2015, 1, 4)


def test_week_dates(week_cdc, week_iso):
    cdc_week_dates = [
        date(2015, 1, 4),
        date(2015, 1, 5),
        date(2015, 1, 6),
        date(2015, 1, 7),
        date(2015, 1, 8),
        date(2015, 1, 9),
        date(2015, 1, 10),
    ]
    iso_week_dates = [
        date(2014, 12, 29),
        date(2014, 12, 30),
        date(2014, 12, 31),
        date(2015, 1, 1),
        date(2015, 1, 2),
        date(2015, 1, 3),
        date(2015, 1, 4),
    ]
    assert list(week_cdc.iterdates()) == cdc_week_dates
    assert list(week_iso.iterdates()) == iso_week_dates


def test_week_daydate(week_cdc, week_iso):
    cdc_week_dates = [
        date(2015, 1, 5),
        date(2015, 1, 6),
        date(2015, 1, 7),
        date(2015, 1, 8),
        date(2015, 1, 9),
        date(2015, 1, 10),
        date(2015, 1, 4),
    ]
    iso_week_dates = [
        date(2014, 12, 29),
        date(2014, 12, 30),
        date(2014, 12, 31),
        date(2015, 1, 1),
        date(2015, 1, 2),
        date(2015, 1, 3),
        date(2015, 1, 4),
    ]
    for i, daydate in enumerate(cdc_week_dates):
        assert week_cdc.daydate(i) == daydate
    for i, daydate in enumerate(iso_week_dates):
        assert week_iso.daydate(i) == daydate


@pytest.fixture(scope="module")
def year_cdc():
    return epiweeks.Year(2015, system="cdc")


@pytest.fixture(scope="module")
def year_iso():
    return epiweeks.Year(2015, system="iso")


def test_year_repr(year_cdc, year_iso):
    assert year_cdc.__repr__() == "Year(2015, CDC)"
    assert year_iso.__repr__() == "Year(2015, ISO)"


def test_year_string(year_cdc):
    assert year_cdc.__str__() == "2015"


def test_year_hash(year_cdc, year_iso):
    assert year_cdc.__hash__() == hash((2015, "CDC"))
    assert year_iso.__hash__() == hash((2015, "ISO"))


def test_year_thisyear():
    today_year = date.today().year
    cdc_year = epiweeks.Year.thisyear(system="cdc")
    cdc_year_start = epiweeks._year_start(today_year, system="cdc")
    iso_year = epiweeks.Year.thisyear(system="iso")
    iso_year_start = epiweeks._year_start(today_year, system="iso")
    assert cdc_year.startdate().toordinal() == cdc_year_start
    assert iso_year.startdate().toordinal() == iso_year_start


def test_year_number(year_cdc, year_iso):
    assert year_cdc.year == 2015
    assert year_iso.year == 2015


def test_year_system(year_cdc, year_iso):
    assert year_cdc.system == "CDC"
    assert year_iso.system == "ISO"


def test_year_totalweeks(year_cdc, year_iso):
    assert year_cdc.totalweeks() == 52
    assert year_iso.totalweeks() == 53


def test_year_startdate(year_cdc, year_iso):
    assert year_cdc.startdate() == date(2015, 1, 4)
    assert year_iso.startdate() == date(2014, 12, 29)


def test_year_enddate(year_cdc, year_iso):
    assert year_cdc.enddate() == date(2016, 1, 2)
    assert year_iso.enddate() == date(2016, 1, 3)


def test_year_weeks(year_cdc, year_iso):
    cdc_weeks = []
    for w in range(1, 53):
        cdc_weeks.append(epiweeks.Week(2015, w))
    assert list(year_cdc.iterweeks()) == cdc_weeks
    iso_weeks = []
    for w in range(1, 54):
        iso_weeks.append(epiweeks.Week(2015, w, system="iso"))
    assert list(year_iso.iterweeks()) == iso_weeks


def test_check_valid_week():
    try:
        epiweeks._check_week(2015, 53, system="iso")
    except ValueError:
        pytest.fail("Week should be valid")


def test_check_invalid_week():
    with pytest.raises(ValueError) as e:
        for w in [0, 53]:
            epiweeks._check_week(2015, w, system="cdc")
            assert str(e.value) == f"Week must be in 1..52 for year: {w}"


def test_check_valid_year():
    try:
        epiweeks._check_year(2018)
    except ValueError:
        pytest.fail("Year should be valid")


def test_check_invalid_year():
    with pytest.raises(ValueError) as e:
        for y in [0, 20155]:
            epiweeks._check_year(y)
            assert str(e.value) == f"Year must be in 1..9999: {y}"


def test_check_valid_system():
    try:
        epiweeks._check_system("CDC")
        epiweeks._check_system("cdc")
        epiweeks._check_system("ISO")
        epiweeks._check_system("iso")
    except ValueError:
        pytest.fail("System should be valid")


def test_check_invalid_system():
    with pytest.raises(ValueError) as e:
        epiweeks._check_system("mmwr")
    assert str(e.value) == "System must be in ('cdc', 'iso'): 'mmwr'"


@pytest.mark.parametrize("test_input, expected", [("cdc", 1), ("iso", 0)])
def test_system_adjustment(test_input, expected):
    assert epiweeks._system_adjustment(test_input) == expected


@pytest.mark.parametrize(
    "test_input, expected", [((2015, "cdc"), 735602), ((2015, "iso"), 735596)]
)
def test_year_start_ordinal(test_input, expected):
    assert epiweeks._year_start(*test_input) == expected


@pytest.mark.parametrize(
    "test_input, expected", [((2015, "cdc"), 52), ((2015, "iso"), 53)]
)
def test_year_total_weeks(test_input, expected):
    assert epiweeks._year_total_weeks(*test_input) == expected
