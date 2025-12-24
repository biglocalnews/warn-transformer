import typing

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Georgia raw data for consolidation."""

    postal_code = "GA"
    fields = dict(
        company="Company Name",
        location=lambda row: row["First Location Address"] or row["County"],
        effective_date="First Date of Separation",
        jobs="Total Number of Affected Employees",
    )
    date_format = "%m/%d/%Y"

    # This needs to be checked -- no temporary data to test against
    def check_if_temporary(self, row: typing.Dict) -> typing.Optional[bool]:
        """Determine whether a row is a temporary or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean or null
        """
        return "temporary" in row["Type of Layoff or Closure"].lower() or None

    def check_if_closure(self, row: typing.Dict) -> typing.Optional[bool]:
        """Determine whether a row is a closure or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean or null
        """
        return "closure" in row["Type of Layoff or Closure"].lower() or None
