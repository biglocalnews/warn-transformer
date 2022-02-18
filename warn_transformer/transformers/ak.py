from datetime import datetime

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Alaska raw data for consolidation."""

    postal_code = "AK"
    fields = dict(
        company="Company",
        location="Location",
        date="Notice Date",
        jobs="Employees Affected",
    )
    date_format = "%m/%d/%y"
    date_corrections = {"9/30/20*": datetime(2020, 9, 30)}
    jobs_corrections = {
        "Up to 300": 300,
    }
