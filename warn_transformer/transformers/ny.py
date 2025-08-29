import typing
from datetime import datetime

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform New York raw data for consolidation."""

    postal_code = "NY"
    fields = dict(
        company=lambda row: row["Business Legal Name"] or row["Company"] or None,
        location="Impacted Site County",
        notice_date=lambda row: row["Date of WARN Notice "]
        or row["Date of WARN Notice"]
        or None,
        effective_date="Date Layoff/Closure Starts",
        jobs="Number of Affected Workers ",
    )
    date_format = ("%Y-%m-%d %H:%M:%S", "%m/%d/%Y", "%Y-%m-%d")
    date_corrections = {
        "929/2022": datetime(2022, 9, 29),
        "3/6/3023": datetime(2023, 3, 6),
        "2": datetime(2021, 2, 12),
        "2/2/2024`": datetime(2024, 2, 2),
        "7/29/24": datetime(2024, 7, 29),
        "7/31/24": datetime(2024, 7, 31),
        "8/2/24": datetime(2024, 8, 2),
        "9/24/24": datetime(2024, 9, 24),
        "2/12/24": datetime(2024, 12, 12),  # Note date shift
        "2026-12-31": datetime(
            2026, 12, 31
        ),  # Everything on the state web site begins 2026 and ends 2026.
    }

    def transform_date(self, value: str) -> typing.Optional[str]:
        """Transform a raw date string into a date object.

        Args:
            value (str): The raw date string provided by the source

        Returns: A date object ready for consolidation. Or, if the date string is invalid, a None.
        """
        if not value:
            return None
        value = value.split()[0].replace(",", "").replace(";", "")
        return super().transform_date(value)

    def check_if_temporary(self, row: typing.Dict) -> typing.Optional[bool]:
        """Determine whether a row is a temporary or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean or null
        """
        value = row["Permanent or Temporary Layoff?"].lower()
        if "permanent" in value:
            return False
        elif "temporary" in value:
            return True
        else:
            return None

    def check_if_closure(self, row: typing.Dict) -> typing.Optional[bool]:
        """Determine whether a row is a closure or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean or null
        """
        value = row["Layoff or Closure?"].lower()
        if "closure" in value:
            return True
        elif "layoff" in value:
            return False
        else:
            return None
