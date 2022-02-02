from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform New York raw data for consolidation."""

    postal_code = "NY"
    fields = dict(
        company="Company",
        location="City",
        date="Notice Date",
        jobs="Number Affected",
    )
    date_format = "%Y-%m-%d %H:%M:%S"
