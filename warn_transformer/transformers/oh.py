import re
import typing
from datetime import datetime

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Ohio raw data for consolidation."""

    postal_code = "OH"
    fields = dict(
        company="Company",
        location="City/County",
        notice_date="Date Received",
        effective_date="Layoff Date(s)",
        jobs="Potential Number Affected",
    )
    date_format = "%m/%d/%Y"
    date_corrections = {
        "08/14/02018": datetime(2018, 8, 14),
        "01/30/201 7": datetime(2017, 1, 30),
        "10/30/20015": datetime(2015, 10, 30),
        "None": None,
        "Unknown": None,
        "10/2015": datetime(2015, 10, 1),
        "Various": None,
        "Mar‐16": None,
        "12/23/2015â": datetime(2015, 12, 23),
        "01/152024": datetime(2024, 1, 15),
        "3/5/202403/19/2024": datetime(2024, 3, 5),
        "3/5/2024-03/19/2024": datetime(2024, 3, 5),
        "10/31/2024;": datetime(2024, 10, 31),
        "07/1309/12/2024": datetime(2024, 7, 13),
        "07/13-09/12/2024": datetime(2024, 7, 13),
        "10/1/2024;": datetime(2024, 10, 1),
        "10/1/2024; 10/31/2024; 12/31/2024": datetime(2024, 10, 1),
        "(9/17/202": datetime(2024, 9, 17),
        "(9/17/2024-9/30/2024": datetime(2024, 9, 17),
        "(9/17/2024-9/30/2024)": datetime(2024, 9, 17),
        "11/4/202404/1/2025": datetime(2024, 11, 4),
    }
    jobs_corrections = {
        "13 FT": 13,
        "58 94 97 35": 58,
        "Unknown": None,
        "unknown": None,
        "242 80": 242,
        "323‐500": 323,
    }

    def transform_date(self, value: str) -> typing.Optional[str]:
        """Transform a raw date string into a date object.

        Args:
            value (str): The raw date string provided by the source

        Returns: A date object ready for consolidation. Or, if the date string is invalid, a None.
        """
        # Cut out cruft
        value = value.replace("Updated", "")
        value = value.replace("Revised", "")
        value = value.replace("-", "").strip()

        # Split double dates
        if len(value) == 20:
            value = value[:10]
        elif len(value) == 19:
            value = value[:9]
        value = re.split(r"\s{2,}", value)[0].strip()
        value = value.split("Originated")[0].strip()
        # print(value)

        try:
            return super().transform_date(value)
        except Exception:
            value = value.split(" to ")[0].strip()
            value = value.split()[0].strip()
            value = value.replace("‐", "")
            return super().transform_date(value)
