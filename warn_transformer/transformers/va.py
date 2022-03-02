import typing

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Virginia raw data for consolidation."""

    postal_code = "VA"
    fields = dict(
        company="Company Name",
        location="Location City",
        date="Notice Date",
        jobs="Employees Affected",
    )
    date_format = "%m/%d/%Y"

    def check_if_closure(self, row: typing.Dict) -> typing.Optional[bool]:
        """Determine whether a row is a closure or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean or null
        """
        return "yes" in row["Closure"].lower() or None
