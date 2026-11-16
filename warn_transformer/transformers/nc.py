import typing

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform North Carolina raw data for consolidation."""

    postal_code = "NC"
    fields = dict(
        company="WARN Notice: WARN Notice Name",
        location="City",
        notice_date="Date of Notice",
        effective_date="Effective Date",
        jobs="Number affected at this location",
    )
    date_format = "%m/%d/%Y"
    # Closures are announced well ahead. 2026 has notices effective 16 months out.
    max_future_days = 365 * 2

    def check_if_temporary(self, row: typing.Dict) -> typing.Optional[bool]:
        """Determine whether a row is a temporary or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean or null
        """
        value = row["Type of layoff or closure"].lower().strip()
        if value == "temporary":
            return True
        elif value == "permanent":
            return False
        else:
            return None

    def check_if_closure(self, row: typing.Dict) -> typing.Optional[bool]:
        """Determine whether a row is a closure or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean or null
        """
        value = row["WARN notice type"].lower().strip()
        if value == "closure":
            return True
        elif value == "layoff":
            return False
        else:
            return None
