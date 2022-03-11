import typing

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform New York raw data for consolidation."""

    postal_code = "NY"
    fields = dict(
        company="Company",
        location="City",
        notice_date="Notice Date",
        effective_date="Layoff Date",
        jobs="Number Affected",
    )
    date_format = "%Y-%m-%d %H:%M:%S"

    def check_if_temporary(self, row: typing.Dict) -> typing.Optional[bool]:
        """Determine whether a row is a temporary or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean or null
        """
        value = row["Dislocation Type"].lower()
        if "possible" in value or "potential" in value:
            return None
        return "temp" in value or None

    def check_if_closure(self, row: typing.Dict) -> typing.Optional[bool]:
        """Determine whether a row is a closure or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean or null
        """
        value = row["Dislocation Type"].lower()
        if "possible" in value or "potential" in value or "temp" in value:
            return None
        return "clos" in value or None
