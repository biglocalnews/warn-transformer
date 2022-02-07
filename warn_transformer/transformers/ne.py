from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Nebraska raw data for consolidation."""

    postal_code = "NE"
    fields = dict(
        company="Company",
        location="City",
        date="Date",
        jobs="Jobs Affected",
    )
    date_format = "%m/%d/%Y"
    jobs_corrections = {
        "100+": 100,
        "5-9": 5,
        "3-5": 3,
        "a few": 1,
    }
