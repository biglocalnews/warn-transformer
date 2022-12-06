import typing

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Michigan raw data for consolidation."""

    postal_code = "MI"
    fields = dict(
        company="Company Name",
        location="City",
        notice_date="Date Received",
        jobs="Number of Layoffs",
    )
    date_format = "%m/%d/%Y"
    jobs_corrections = {
        "80*": 80,
        "Unreported": None,
    }

    def check_if_closure(self, row: typing.Dict) -> typing.Optional[bool]:
        """Determine whether a row is a closure or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean or null
        """
        return "closing" in row["Incident Type"].lower() or None
