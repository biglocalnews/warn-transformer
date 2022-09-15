import typing
from datetime import datetime

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform California raw data for consolidation."""

    postal_code = "CA"
    fields = dict(
        company="company",
        location=lambda row: row["city"] or row["address"],
        notice_date="notice_date",
        effective_date="effective_date",
        jobs="num_employees",
    )
    date_format = "%m/%d/%Y"
    max_future_days = 365 * 5
    minimum_year = 2014
    jobs_corrections = {
        # This Tesla layoff number large but correct
        # https://www.cnbc.com/2020/05/13/coronavirus-latest-updates.html
        11083: 11083,
    }
    date_corrections = {
        "09/04/2008": datetime(2018, 9, 4),
        "07/04/2002": datetime(2020, 7, 4),
        "03/09/2121": datetime(2021, 3, 9),
        "03/30/3030": datetime(2020, 3, 30),
    }

    def check_if_temporary(self, row: typing.Dict) -> typing.Optional[bool]:
        """Determine whether a row is a temporary or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean or null
        """
        return "temporary" in row["layoff_or_closure"].lower() or None

    def check_if_closure(self, row: typing.Dict) -> typing.Optional[bool]:
        """Determine whether a row is a closure or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean or null
        """
        return row["layoff_or_closure"].lower().strip() == "closure permanent" or None
