import typing

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Alabama raw data for consolidation."""

    postal_code = "AL"
    fields = dict(
        company="Company",
        location="City",
        date="Initial Report Date",
        jobs="Planned # Affected Employees",
    )
    date_format = "%m/%d/%Y"

    def check_if_closure(self, row: typing.Dict) -> typing.Optional[bool]:
        """Determine whether a row is a closure or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean or null
        """
        return "closing" in row["Closing or Layoff"].lower() or None
