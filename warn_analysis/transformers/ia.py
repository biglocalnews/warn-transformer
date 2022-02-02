from datetime import datetime

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Iowa raw data for consolidation."""

    postal_code = "IA"
    fields = dict(
        company="Company",
        location="City",
        date="Notice Date",
        jobs="Emp #",
    )
    date_format = "%m/%d/%Y"
    date_corrections = {
        "9/1/8/2020": datetime(2020, 1, 8),
        "4/26/21": datetime(2021, 4, 26),
        "2021-04-30 00:00:00": datetime(2021, 4, 30),
        "7/14/21": datetime(2021, 7, 14),
        "7/12/21": datetime(2021, 7, 12),
    }
