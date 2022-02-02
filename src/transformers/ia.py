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
