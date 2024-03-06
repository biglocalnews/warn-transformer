import typing
from datetime import datetime

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Rhode Island raw data for consolidation."""

    postal_code = "RI"
    fields = dict(
        company="Company Name",
        location="Location of Layoffs",
        date="WARN Date",
        effective_date="Effective Date",
        jobs="Number Affected",
    )
    date_format = ("%Y-%m-%d %H:%M:%S", "%m/%d/%Y", "%m/%d/%y", "%m/%Y")
    date_corrections = {
        "2108-10-23 00:00:00": datetime(2018, 10, 23),
        "2108-11-01 00:00:00": datetime(2018, 11, 1),
        "Staggered": None,
    }
    jobs_corrections = {
        "---": None,
        "54 Union 3 Non Union": 57,
        "190 company with an additional 100 contracted": 290,
        "60-80": 60,
        "additional 16": 16,
        "1900-03-17 00:00:00": None,
        "309 *updated 10/26/23": 309,
        "1900-01-01 00:00:00": 1,
    }

    def transform_company(self, value: str) -> str:
        """Transform a raw company name.

        Args:
            value (str): The raw company string provided by the source

        Returns: A string object ready for consolidation.
        """
        return value.strip().replace("*", "")

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
        return "yes" in row["Closing Yes/No"].lower() or None
