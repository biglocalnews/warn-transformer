import logging
import typing
from datetime import datetime

from ..schema import BaseTransformer

logger = logging.getLogger(__name__)


class Transformer(BaseTransformer):
    """Transform Iowa raw data for consolidation."""

    postal_code = "IA"
    fields = dict(
        company="Company",
        location="City",
        notice_date="Notice Date",
        effective_date="Layoff Date",
        jobs="Emp #",
    )
    date_format = ("%m/%d/%Y", "%Y-%m-%d %H:%M:%S")
    date_corrections = {
        "9/1/8/2020": datetime(2020, 1, 8),
        "4/26/21": datetime(2021, 4, 26),
        "2021-04-30 00:00:00": datetime(2021, 4, 30),
        "7/14/21": datetime(2021, 7, 14),
        "7/12/21": datetime(2021, 7, 12),
        "2027-07-27 00:00:00": datetime(2024, 7, 27),
    }

    def check_if_amendment(self, row: typing.Dict) -> bool:
        """Determine whether a row is an amendment or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean
        """
        return "amendment" in row["Notice Type"].lower().strip()

    def check_if_closure(self, row: typing.Dict) -> typing.Optional[bool]:
        """Determine whether a row is a closure or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean or null
        """
        return "closing" in row["Notice Type"].lower() or None

    def handle_amendments(
        self, row_list: typing.List[typing.Dict]
    ) -> typing.List[typing.Dict]:
        """Remove amended filings from the provided list of records.

        Args:
            row_list (list): A list of clean rows of data.

        Returns: A list of cleaned data, minus amended records.
        """
        amendments_count = len([r for r in row_list if r["is_amendment"] is True])
        logger.debug(f"{amendments_count} amendments in {self.postal_code}")
        logger.debug(
            "No action has been taken because it does not appear to be necessary to remove ancestor filings."
        )
        return row_list
