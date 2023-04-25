---
hide-toc: true
---

# Background

**EpiWeeks** is a Python package to calculate epidemiological weeks using the US
CDC (MMWR) and ISO week numbering systems. Epidemiological weeks, commonly
referred to as "epi weeks", are simply a standardized method for numbering weeks
as a period of time to group epidemiological events. This method allows for the
comparison of reported events for a given year, or period of a year, with those
of previous years. It also facilitates similar comparison between countries.

There are several systems for numbering weeks. The most common systems when it
comes to epidemiological weeks are the US CDC and ISO systems. The US CDC system
is used in countries such as the United States, Canada, Australia, India, Egypt,
and Saudi Arabia. The ISO system is used in all European countries and most of
Asian ones.

The US CDC defines the week ([MMWR week]) as seven days, beginning with Sunday
and ending with Saturday. The ISO defines the week ([ISO week]) as seven days,
beginning with Monday and ending with Sunday. In either case, the end of the
first week of the year, by definition, must fall at least four days into the
year. Week numbers range from 1 to 53 for year, although most years consist of
52 weeks.

Public health professionals, analysts, researchers, and developers need to have
a tested and reliable tool for calculating epidemiological weeks. The
**EpiWeeks** package provides that functionality using both the US CDC and ISO
week numbering systems. It has been carefully tested against original resources,
including the [MMWR Weeks Calendars] published by the US CDC, to ensure its
accuracy and reliability. The **EpiWeeks** package can be used in many ways,
from identifying the week of a date or the ending date for a week, to generating
a full epidemiological calendar.

[mmwr week]:
  https://ndc.services.cdc.gov/wp-content/uploads/MMWR_Week_overview.pdf
[iso week]: https://en.wikipedia.org/wiki/ISO_week_date
[mmwr weeks calendars]:
  https://ndc.services.cdc.gov/event-codes-other-surveillance-resources/
