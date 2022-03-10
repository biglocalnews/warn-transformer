import typing
from datetime import datetime

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform New Jersey raw data for consolidation."""

    postal_code = "NJ"
    fields = dict(
        company="Company",
        location="City",
        effective_date="Effective Date",
        jobs="Workforce Affected",
    )
    date_format = ["%Y-%m-%d %H:%M:%S", "%M/%d/%Y", "%M/%d/%y"]
    jobs_corrections = {
        "TBA": None,
        "To be Determined": None,
        "-": None,
        "Unknown": None,
        23695: None,
        # The United airlines number is legimate, though nationwide
        # https://abcnews.go.com/Politics/united-airlines-furlough-16000-employees/story?id=72771897
        16000: 16000,
    }
    date_corrections = {
        "TBA": None,
        "Temp layoff": None,
        "-": None,
        "3030-08-23 00:00:00": datetime(2020, 8, 23),
        "04/22/2022, 09/30/2022, 12/21/22": datetime(2022, 4, 22),
    }

    def transform_jobs(self, value: str) -> typing.Optional[int]:
        """Transform a raw jobs number into an integer.

        Args:
            value (str): A raw jobs number provided by the source

        Returns: An integer number ready for consolidation. Or, if the value is invalid, a None.
        """
        # Cut the asterisk they sometimes use
        value = value.replace("*", "")

        # Do the normal stuff
        return super().transform_jobs(value)
