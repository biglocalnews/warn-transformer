import typing

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Oklahoma raw data for consolidation."""

    postal_code = "OK"
    fields = dict(
        company="company_name",
        location=lambda row: row["city"] or row["workforce_board"],
        notice_date="notice_date",
        # jobs="number_of_employees_affected",
        jobs="jobs",
    )

    date_format = "%Y-%m-%d"

    def check_if_closure(self, row: typing.Dict) -> typing.Optional[bool]:
        """Determine whether a row is a closure or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean or null
        """
        return "closing" in row["closure_type"].lower() or None
