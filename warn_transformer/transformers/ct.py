import typing
from datetime import datetime

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Connecticut raw data for consolidation."""

    postal_code = "CT"
    fields = dict(
        company="affected_company",
        location="layoff_location",
        notice_date="warn_date",
        effective_date="layoff_date",
        jobs="number_workers",
    )
    date_format = ["%m/%d/%Y", "%m/%d/%y", "%m-%d-%y", "%Y"]
    date_corrections = {
        "12/31/16-1/13/17": datetime(2016, 12, 31),
        "12/4/15-tbd": datetime(2015, 12, 4),
        "2/29/15": datetime(2015, 2, 28),
        "9/1//15": datetime(2015, 9, 1),
        "Not Indicated": None,
        "# 12 2/13/17 through 2018": datetime(2017, 2, 13),
        "Most 10/29/16": datetime(2016, 10, 29),
        "Several Weeks - Five Months": None,
        "Not Dated Rec'd 6/24/15": datetime(2015, 6, 24),
        "3rd Quarter 2015-4th Quarter 2016": datetime(2015, 6, 1),
        "June 2017 - March 2018": datetime(2017, 6, 1),
        "First quarter 2019 - 2020": datetime(2019, 1, 1),
        "June 2018 - September 2, 2018": datetime(2018, 6, 1),
        "Beginning June 2018": datetime(2018, 6, 1),
        "December 2018 - March 1, 2019": datetime(2018, 12, 1),
        "Possibly 50+": None,
        "N/A": None,
        "Reduction in Hours Since March 2020": datetime(2020, 3, 1),
        "April-June 2020": datetime(2020, 4, 1),
        "": None,
        "7/3/2020- 7/17/2020": datetime(2020, 7, 3),
        "Not Dated Rec'd 4/22/2020": datetime(2020, 4, 22),
        "Not Dated Rec'd 4/13/2020": datetime(2020, 4, 13),
        "3/16 - 12/13/2020": datetime(2020, 3, 16),
        "february": None,
        "potentially": None,
        "not": None,
    }
    jobs_corrections = {
        "up to 703": 703,
        "18; 87": 105,
        "724 across U.S. including 49 from Ridgefield CT location": 49,
        "Not Provided": None,
        "Not Indicated": None,
        "Possibly 50+": 50,
        "Not indicated": None,
        "12; 6; 5": 23,
        "182; additional 21 on reduced hours": 182,
        "78; additional 13 on reduced hours": 78,
        "124; additional 30 on reduced hours": 124,
        "Not reported on WARN notice": None,
        "Not provided": None,
        "489 - total for CT and other locations": 489,
        "158 Stamford 81 Branford": 239,
        "?": None,
        "110 total; 7 CT 103 remote": 7,
        "Not": None,
        "208 (36 of whom work in CT)": 36,
    }

    def transform_date(self, value: str) -> typing.Optional[str]:
        """Transform a raw date string into a date object.

        Args:
            value (str): The raw date string provided by the source

        Returns: A date object ready for consolidation. Or, if the date string is invalid, a None.
        """
        try:
            dt = self.date_corrections[value]
            if dt:
                return str(dt.date())
            else:
                assert dt is None
                return dt
        except KeyError:
            pass
        value = value.lower()
        value = value.replace("beginning", "")
        value = value.replace("after", "")
        value = value.replace("estimated", "")
        value = value.replace(";", "")
        value = value.replace("*", "")
        value = value.strip().split()[0].strip()
        return super().transform_date(value)

    def check_if_closure(self, row: typing.Dict) -> typing.Optional[bool]:
        """Determine whether a row is a closure or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean or null
        """
        return "yes" in row["closing"].lower() or None
