from datetime import datetime
import typing

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Indiana raw data for consolidation."""

    postal_code = "IN"
    fields = dict(
        company="Company",
        location="City",
        date="Notice Date",
        jobs="Affected Workers",
    )
    date_format = "%m/%d/%Y"

    def prep_row_list(
        self, row_list: typing.List[typing.Dict]
    ) -> typing.List[typing.Dict]:
        """Make necessary transformations to the raw row list prior to transformation.

        Args:
            row_list (list): A list of raw rows of data from the source.

        Returns: The row list minus empty records
        """
        # Do the standard stuff
        row_list = super().prep_row_list(row_list)

        # Cut rows with data-free revisions
        return [r for r in row_list if r["Affected Workers"] != "N/A"]

    def transform_date(self, value: str) -> str:
        """Transform a raw date string into a date object.

        Args:
            value (str): The raw date string provided by the source

        Returns: A date object ready for consolidation. Or, if the date string is invalid, a None.
        """
        try:
            dt = datetime.strptime(value.strip(), "%m/%d/%y")
        except ValueError:
            return super().transform_date(value)
        return str(dt.date())