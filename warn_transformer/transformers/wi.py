import typing

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Wisconsin raw data for consolidation."""

    postal_code = "WI"
    fields = dict(
        company="Company",
        location="City",
        date="Notice Received",
        jobs="Affected Workers",
    )
    date_format = ("%m/%d/%Y", "%Y%m%d")
    jobs_corrections = {
        "Unknown": None,
    }

    def check_if_amendment(self, row: typing.Dict) -> bool:
        """Determine whether a row is an amendment or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean
        """
        return "revision" in row["Company"].lower()
