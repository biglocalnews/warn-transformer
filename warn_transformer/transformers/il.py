import typing

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Illinois raw data for consolidation."""

    postal_code = "IL"
    fields = dict(
        company="COMPANY NAME",
        location=lambda row: f"{row['COMPANY ADDRESS']} {row['CITY, STATE, ZIP']}".strip(),
        date=lambda row: row["NOTICE DATE"] or row["SUPP NOTICE DATE"],
        jobs="WORKERS AFFECTED",
    )
    date_format = ("%Y-%m-%d %H:%M:%S", "%m/%d/%Y")
    jobs_corrections = {
        "N/A": None,
        "Not Provided": None,
        "Not reported": None,
    }

    def transform_jobs(self, value: str) -> typing.Optional[int]:
        """Transform a raw jobs number into an integer.

        Args:
            value (str): A raw jobs number provided by the source

        Returns: An integer number ready for consolidation. Or, if the value is invalid, a None.
        """
        # Split on new lines
        values = value.split("\n")
        # Do the normal stuff
        return super().transform_jobs(values[0])
