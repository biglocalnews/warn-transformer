from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Iowa raw data for consolidation."""

    state = "IA"
    fields = dict(
        company="Company",
        date="Notice Date",
        jobs="Emp #",
    )
    date_format = "%m/%d/%Y"
