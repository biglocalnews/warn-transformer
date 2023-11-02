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
        "TBD": None,
        "Temp layoff": None,
        "-": None,
        "3030-08-23 00:00:00": datetime(2020, 8, 23),
        "04/22/2022, 09/30/2022, 12/21/22": datetime(2022, 4, 22),
        "08/15/2023, 8/22/2023": datetime(2024, 8, 15),
        "7/7/23 - 08/23": datetime(2023, 7, 7),
        "7/723 -  08/23": datetime(2023, 7, 7),
        "7/7/23 - 8/2023": datetime(2023, 7, 7),
        "7/723 -  8/2023": datetime(2023, 7, 7),
        "10/23/2023 - 12/15/2023": datetime(2023, 10, 23),
        "09/15/2023 - 12/06/2023": datetime(2023, 9, 15),
        "09/30/2023 - 12/31/2023": datetime(2023, 9, 30),
        "9/15/2023 - 12/06/2023": datetime(2023, 9, 15),
        "9/30/2023 - 12/31/2023": datetime(2023, 9, 30),
        "11/17/2023 - 12/01/2023": datetime(2023, 11, 17),
        "11/15/2023 - 12/31/2023": datetime(2023, 11, 15),
        "10/1/2023,10/31/2023,11/05/2023, 1/31/2024,1/1/2024,3/1/2024, 4/1/2024": datetime(
            2023, 10, 1
        ),
        "12/31/24, 9/27/24, 8/30/24, 5/31/24, 1/31/24, 12/13/2023, 10/25/2023, 9/27/2023, 9/20/2023, 9/18/2023,9/7/2023, 4/13/23, 3/30/23": None,
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
