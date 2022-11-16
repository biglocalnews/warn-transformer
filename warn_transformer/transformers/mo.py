import typing
from datetime import datetime

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Missouri raw data for consolidation."""

    postal_code = "MO"
    fields = dict(
        company="Title",
        location="Location(s)",
        notice_date="Received Sort descending",
        effective_date="Layoff date(s)",
        jobs="# affected",
    )
    date_format = ("%m/%d/%Y", "%m/%d/%y", "%B %Y", "%B %d, %Y")
    date_corrections = {
        "04/-9/2020": datetime(2020, 4, 9),
        "March 2020": datetime(2020, 3, 1),
        "": None,
        "11/08/2109": datetime(2019, 11, 8),
    }
    jobs_corrections = {
        "330 remote workers (18 located in Missouri)": 18,
        "Unknown": None,
    }

    def transform_date(self, value: str) -> typing.Optional[str]:
        """Transform a raw date string into a date object.

        Args:
            value (str): The raw date string provided by the source

        Returns: A date object ready for consolidation. Or, if the date string is invalid, a None.
        """
        try:
            return super().transform_date(value)
        except Exception:
            value = value.strip().split()[0].strip()
            value = value.strip().split("-")[0].strip()
            value = value.replace("–", "")
            value = value.replace(",", "")
            return super().transform_date(value)

    def check_if_closure(self, row: typing.Dict) -> typing.Optional[bool]:
        """Determine whether a row is a closure or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean or null
        """
        return "clos" in row["Type"].lower() or None
