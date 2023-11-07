import typing
from datetime import datetime

from ..schema import BaseTransformer


def transform_jobs(row):
    """Corrects variations in field names for the number of employees affected."""
    possible_headers = ["No. of EmployeesAffected", "No. of Employees Affected"]
    for field in possible_headers:
        try:
            return row[field]
        except KeyError:
            pass
    raise Exception(
        f"Unable to find the jobs data using these keys: {possible_headers}"
    )


class Transformer(BaseTransformer):
    """Transform Idaho raw data for consolidation."""

    postal_code = "ID"
    fields = dict(
        company="Company",
        location="City",
        notice_date="Date of Letter",
        effective_date="Effective or Commencing Date",
        # jobs="No. of EmployeesAffected",
        jobs=transform_jobs,
    )
    date_format = ("%m/%d/%Y", "%m/%d/%y")
    date_corrections = {
        "2/19/219": datetime(2019, 2, 19),
        "3/7/2010-3/20/2010": datetime(2010, 3, 7),
        "rting": datetime(2015, 2, 16),
        "3/7/2010-3/20/2": datetime(2010, 3, 7),
    }
    jobs_corrections = {
        "8 in ID": 8,
        "17 in ID": 17,
        "80-100": 80,
        "2 5s1ta": 251,
        "120 (2 in ID)": 2,
        "106 (17 in ID)": 17,
        22000: None,
        "22000 (102 in ID)": 102,
        "TBD": None,
        "135 (1 in ID)": 1,
    }

    def transform_date(self, value: str) -> typing.Optional[str]:
        """Transform a raw date string into a date object.

        Args:
            value (str): The raw date string provided by the source

        Returns: A date object ready for consolidation. Or, if the date string is invalid, a None.
        """
        # A little custom clean up based on the weird stuff from this source
        if not value:
            value = ""
        value = value.replace("starting", "")
        value = value.strip().split()[0].replace(",", "").strip()

        # The same old stuff
        return super().transform_date(value)
