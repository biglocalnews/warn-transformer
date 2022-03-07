import typing

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Missouri raw data for consolidation."""

    postal_code = "MO"
    fields = dict(
        company="COMPANY NAME",
        location="LOCATION",
        date="DATE RECEIVED",
        jobs="# AFFECTED",
    )
    date_format = ("%m/%d/%Y", "%m/%d/%y")
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
        # A little custom clean up based on the weird stuff from this source
        value = value.strip().split()[0].strip()
        return super().transform_date(value)

    def check_if_closure(self, row: typing.Dict) -> typing.Optional[bool]:
        """Determine whether a row is a closure or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean or null
        """
        return "clos" in row["TYPE"].lower() or None
