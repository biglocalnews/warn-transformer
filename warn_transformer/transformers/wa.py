import typing

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Washington raw data for consolidation."""

    postal_code = "WA"
    fields = dict(
        company="Company",
        location="Location",
        notice_date="Layoff Start Date",
        effective_date="Layoff Start Date",
        jobs="# of Workers",
    )
    date_format = "%m/%d/%Y"

    def check_if_temporary(self, row: typing.Dict) -> typing.Optional[bool]:
        """Determine whether a row is a temporary or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean or null
        """
        return row["Type of Layoff"].lower() == "temporary"

    def check_if_closure(self, row: typing.Dict) -> typing.Optional[bool]:
        """Determine whether a row is a closure or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean or null
        """
        temporary = row["Type of Layoff"].lower() == "temporary"
        if temporary:
            return False
        return row["Closure Layoff"].lower() == "closure"
