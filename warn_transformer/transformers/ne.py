import typing
from datetime import datetime

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Nebraska raw data for consolidation."""

    postal_code = "NE"
    fields = dict(
        company="Company",
        location="City",
        notice_date="Date",
        jobs="Jobs Affected",
    )
    date_format = "%m/%d/%Y"
    date_corrections = {
        "12/19/2022\xa0\xa0\n\xa0 11/2/2022": datetime(2022, 11, 2),
        "12/19/2022\xa0\xa0\n\xa0 11/02/2022": datetime(2022, 11, 2),
    }
    jobs_corrections = {
        "100+": 100,
        "5-9": 5,
        "3-5": 3,
        "a few": 1,
    }

    def check_if_closure(self, row: typing.Dict) -> typing.Optional[bool]:
        """Determine whether a row is a closure or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean or null
        """
        return "closure" in row["Type"].lower() or None
