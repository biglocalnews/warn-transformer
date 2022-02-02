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
