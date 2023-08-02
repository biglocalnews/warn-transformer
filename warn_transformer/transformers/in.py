import typing
from datetime import datetime

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Indiana raw data for consolidation."""

    postal_code = "IN"
    fields = dict(
        company="Company",
        location="City",
        notice_date="Notice Date",
        effective_date="LO/CL Date",
        jobs="Affected Workers",
    )
    date_format = ["%m/%d/%Y", "%m/%d/%y", "%B %Y", "%Y", "%b %Y", "%m/%Y"]
    jobs_corrections = {
        "97 (in MI)0 (in IN)": 0,
        "100+": 100,
        "62 MAY be affected": 62,
        "5 in Indiana": 5,
        "Unknown": None,
        "75 in Indiana": 75,
        "40-50": 40,
        "100-130": 100,
        "4 Hoosiers": 4,
        "Undisclosed at this time": None,
        "500 Nationwide": None,
        "NA": None,
        "103 (REVISED) 10/22/2020 108": 103,
        "Entire Plant": None,
        "All": None,
    }
    date_corrections = {
        "01/30/1202": datetime(2012, 1, 30),
        "April/June 2020": datetime(2020, 4, 1),
        "Unknown": None,
        "Q1 2019": datetime(2019, 1, 1),
        "Q1 2018": datetime(2018, 1, 1),
        "Sept. 2016": datetime(2016, 9, 1),
        "No closure date announced. Layoffs to commence 05/27/2015": datetime(
            2015, 5, 27
        ),
        "TBD": None,
        "09/22/2014-12/07/2014": datetime(2014, 9, 22),
        "08/18/2014-12/31/2014": datetime(2014, 8, 18),
        "End of 2013": datetime(2013, 12, 31),
        "Mid-Year 2014": datetime(2014, 6, 15),
        "02/29/2013": datetime(2013, 2, 28),
        "year end 2014": datetime(2014, 12, 31),
        "4th Qtr 2012": datetime(2012, 9, 1),
        "Mid February 2012": datetime(2012, 2, 14),
        "3rd Qtr 2012": datetime(2012, 6, 1),
        "LO-01/14/2011 CL-End of 2012": datetime(2011, 1, 14),
        "Prior to the end of 2009 (as stated in the WARN notice)": datetime(
            2009, 12, 31
        ),
        "No closure date announced. Layoffs": None,
        "1st Quarter 2009": datetime(2009, 1, 1),
        "02/02/2009\xa0to\xa0\xa012/30/2009": datetime(2009, 2, 2),
        "3rd Quarter of 2009": datetime(2009, 6, 1),
        "August to December 2008": datetime(2008, 8, 1),
        "10/37/2008": datetime(2008, 10, 27),
        "2/29/2013": datetime(2013, 2, 28),
        "LO-1/14/2011 CL-End of 2012": datetime(2011, 1, 14),
        "3rd quarter of 2009": datetime(2009, 6, 1),
    }

    def prep_row_list(
        self, row_list: typing.List[typing.Dict]
    ) -> typing.List[typing.Dict]:
        """Make necessary transformations to the raw row list prior to transformation.

        Args:
            row_list (list): A list of raw rows of data from the source.

        Returns: The row list minus empty records
        """
        # Do the standard stuff
        row_list = super().prep_row_list(row_list)

        # Cut rows with data-free revisions
        return [r for r in row_list if r["Affected Workers"] != "N/A"]

    def transform_date(self, value: str) -> typing.Optional[str]:
        """Transform a raw date string into a date object.

        Args:
            value (str): The raw date string provided by the source

        Returns: A date object ready for consolidation. Or, if the date string is invalid, a None.
        """
        # Try corrections before we edit the string
        try:
            dt = self.date_corrections[value]
            if dt:
                return str(dt.date())
            else:
                assert dt is None
                return dt
        except KeyError:
            pass

        # A little custom clean up based on the weird stuff from this source
        value = value.replace("starting", "")
        value = value.strip().split(" and ")[0].strip()
        value = value.strip().split(" to ")[0].strip()
        value = value.strip().split(" through ")[0].strip()
        value = value.strip().split(" - ")[0].strip()
        value = value.strip().split(" & ")[0].strip()
        value = value.strip().split("\xa0to ")[0].strip()
        value = value.strip().split(" – ")[0].strip()
        value = value.strip().split("-")[0].strip()

        # The same old stuff
        return super().transform_date(value)

    def check_if_closure(self, row: typing.Dict) -> typing.Optional[bool]:
        """Determine whether a row is a closure or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean or null
        """
        whitelist = ["CL", "CL -Relocating", "LO and CL", "LO/CL", "PENDING CL"]
        return row["Notice Type"] in whitelist or None
