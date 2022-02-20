from datetime import datetime

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Rhode Island raw data for consolidation."""

    postal_code = "RI"
    fields = dict(
        company="Company Name (* Denotes Covid 19 Related WARN)",
        location="Location of Layoffs",
        date="WARN Date",
        jobs="Number Affected",
    )
    date_format = "%Y-%m-%d %H:%M:%S"
    date_corrections = {
        "2108-10-23 00:00:00": datetime(2018, 10, 23),
        "2108-11-01 00:00:00": datetime(2018, 11, 1),
    }
    jobs_corrections = {
        "---": None,
        "54 Union 3 Non Union": 57,
        "190 company with an additional 100 contracted": 290,
        "60-80": 60,
        "additional 16": 16,
    }

    def transform_company(self, value: str) -> str:
        """Transform a raw company name.

        Args:
            value (str): The raw company string provided by the source

        Returns: A string object ready for consolidation.
        """
        return value.strip().replace("*", "")
