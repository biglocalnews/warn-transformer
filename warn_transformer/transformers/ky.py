import re
import typing

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Kentucky raw data for consolidation."""

    postal_code = "KY"
    fields = dict(
        company="Company Name",
        location=lambda row: row["Location"]
        or row["County: Local  Name"]
        or row["County"],
        notice_date="Date Received",
        effective_date="Projected Date",
        jobs="Employees",
    )
    date_format = "%Y-%m-%d %H:%M:%S"
    minimum_year = 1997
    date_corrections = {
        "43490.0": None,
        "N/A": None,
        "November": None,
        "43735.0": None,
    }
    jobs_corrections = {
        "?": None,
        "N/A": None,
        "See W.A.R.N.": None,
        "74 fulltime and 184 parttime": 74,
        "Reduction from 13 to 1": 12,
        "See WARN": None,
        "in WARN": None,
        "Unknown": None,
        "TBD": None,
    }

    def transform_jobs(self, value: str) -> typing.Optional[int]:
        """Transform a raw jobs number into an integer.

        Args:
            value (str): A raw jobs number provided by the source

        Returns: An integer number ready for consolidation. Or, if the value is invalid, a None.
        """
        value = value.split("-")[0].strip()
        value = value.replace("+/-", "")
        value = value.replace("+/", "").strip()
        value = value.replace("+", "").strip()
        value = re.split(" {5,}", value)[0].strip()
        return super().transform_jobs(value)

    def check_if_closure(self, row: typing.Dict) -> typing.Optional[bool]:
        """Determine whether a row is a closure or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean or null
        """
        if "closure" in row["Closure or Layoff?"].lower():
            return True
        elif "closure" in row["Closure/Layoff"].lower():
            return True
        else:
            return None
