import logging
import typing

from ..schema import BaseTransformer

logger = logging.getLogger(__name__)


class Transformer(BaseTransformer):
    """Transform Wisconsin raw data for consolidation."""

    postal_code = "WI"
    fields = dict(
        company="Company",
        location="City",
        notice_date="Notice Received",
        effective_date="Layoff Begin Date",
        jobs="Affected Workers",
    )
    date_format = (
        "%m/%d/%Y",
        "%Y%m%d",
        "%m/%d/%y",
    )
    date_corrections = {
        "11/03": None,
        "Unknown": None,
    }
    jobs_corrections = {
        "Unknown": None,
    }

    def transform_company(self, value: str) -> str:
        """Transform a raw company name.

        Args:
            value (str): The raw company string provided by the source

        Returns: A string object ready for consolidation.
        """
        # Cut revision notices
        value = value.split("- Revision")[0]
        # Do the typical stuff
        return super().transform_company(value)

    def check_if_amendment(self, row: typing.Dict) -> bool:
        """Determine whether a row is an amendment or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean
        """
        return "revision" in row["Company"].lower()

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

        # Loop through all the rows
        ancestor_list = []
        for i, row in enumerate(row_list):
            # If the current row is amended ...
            if row["is_amendment"]:
                # Get the previous record
                previous_index = i - 1
                previous_record = row_list[previous_index]

                # Are the first five characters of the company name found?
                similar_name = (
                    row["company"][:5].lower() in previous_record["company"].lower()
                )

                # If not, it's not an obvious ancestor
                if not similar_name:
                    logger.debug(f"No ancestor found for {row['company']}")
                    continue

                # If the name is similar, the previous record should be struck
                # We'll mark it by adding its hash_id to our list
                ancestor_list.append(previous_record["hash_id"])

        # Cut all of the ancestor records
        logger.debug(f"{len(ancestor_list)} ancestors removed")
        amended_list = [r for r in row_list if r["hash_id"] not in ancestor_list]

        # Return the rows we want to keep
        return amended_list
