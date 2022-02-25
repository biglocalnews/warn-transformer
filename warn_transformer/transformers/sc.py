from datetime import datetime

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform South Carolina raw data for consolidation."""

    postal_code = "SC"
    fields = dict(
        company="company",
        location="location",
        date="date",
        jobs="jobs",
    )
    date_format = "%m/%d/%Y"
    date_corrections = {
        "4/8/20/20": datetime(2020, 4, 8),
        "12/31//2015": datetime(2015, 12, 31),
    }
