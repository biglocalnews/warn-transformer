import typing
from datetime import datetime

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Idaho raw data for consolidation."""

    postal_code = "ID"
    fields = dict(
        company="Company",
        location="City",
        notice_date="Date of Letter",
        effective_date="Effective or Commencing Date",
        jobs="No. of Employees Affected",
    )
    date_format = ("%m/%d/%Y", "%m/%d/%y")
    date_corrections = {
        "2/19/219": datetime(2019, 2, 19),
        "3/7/2010-3/20/2010": datetime(2010, 3, 7),
    }
    jobs_corrections = {
        "8 in ID": 8,
        "17 in ID": 17,
        "80-100": 80,
    }

    def transform_date(self, value: str) -> typing.Optional[str]:
        """Transform a raw date string into a date object.

        Args:
            value (str): The raw date string provided by the source

        Returns: A date object ready for consolidation. Or, if the date string is invalid, a None.
        """
        # A little custom clean up based on the weird stuff from this source
        value = value.replace("starting", "")
        value = value.strip().split()[0].replace(",", "").strip()

        # The same old stuff
        return super().transform_date(value)
