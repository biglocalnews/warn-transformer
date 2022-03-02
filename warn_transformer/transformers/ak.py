import typing
from datetime import datetime

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Alaska raw data for consolidation."""

    postal_code = "AK"
    fields = dict(
        company="Company",
        location="Location",
        date="Notice Date",
        jobs="Employees Affected",
    )
    date_format = "%m/%d/%y"
    date_corrections = {"9/30/20*": datetime(2020, 9, 30)}
    jobs_corrections = {
        "Up to 300": 300,
    }

    def check_if_temporary(self, row: typing.Dict) -> typing.Optional[bool]:
        """Determine whether a row is a temporary or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean or null
        """
        return "temporary" in row["Notes"].lower() or None

    def check_if_closure(self, row: typing.Dict) -> typing.Optional[bool]:
        """Determine whether a row is a closure or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean or null
        """
        return "closure" in row["Notes"].lower() or None
