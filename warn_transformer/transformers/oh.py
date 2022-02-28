import re
import typing
from datetime import datetime

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Ohio raw data for consolidation."""

    postal_code = "OH"
    fields = dict(
        company="Company",
        location="City/County",
        date="DateReceived",
        jobs="Potential NumberAffected",
    )
    date_format = "%m/%d/%Y"
    date_corrections = {
        "08/14/02018": datetime(2018, 8, 14),
        "01/30/201 7": datetime(2017, 1, 30),
        "10/30/20015": datetime(2015, 10, 30),
    }
    jobs_corrections = {
        "13 FT": 13,
        "58 94 97 35": 58,
        "Unknown": None,
        "unknown": None,
        "242 80": 242,
        "323‐500": 323,
    }

    def transform_date(self, value: str) -> typing.Optional[str]:
        """Transform a raw date string into a date object.

        Args:
            value (str): The raw date string provided by the source

        Returns: A date object ready for consolidation. Or, if the date string is invalid, a None.
        """
        # Cut out cruft
        value = value.replace("Updated", "")
        value = value.replace("Revised", "")
        value = value.replace("-", "").strip()

        # Split double dates
        if len(value) == 20:
            value = value[:10]
        value = re.split(r"\s{2,}", value)[0].strip()
        value = value.split("Originated")[0].strip()

        # Do the typical stuff
        return super().transform_date(value)
