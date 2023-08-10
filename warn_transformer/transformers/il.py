import typing

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Illinois raw data for consolidation."""

    postal_code = "IL"
    fields = dict(
        company="Location Name",
        location=lambda row: f"{row['Location Address']} {row['Location City']}, {row['Location State']} {row['Location Zipcode']}".strip(),
        notice_date=lambda row: row["Initial Date Reported"]
        or row["Notification(s) Received"],
        effective_date="Impact Date",
        jobs="Revised Layoff",
    )
    date_format = "%Y-%m-%d %H:%M:%S"
    minimum_year = 1987
    maximum_jobs = 100000

    def check_if_closure(self, row: typing.Dict) -> typing.Optional[bool]:
        """Determine whether a row is a closure or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean or null
        """
        return "closure" in row["Reason"].lower() or None
