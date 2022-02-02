from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Georgia raw data for consolidation."""

    postal_code = "GA"
    fields = dict(
        company="Company Name",
        location="City",
        date="Separation Date",
        jobs="Est. Impact",
    )
    date_format = "%m/%d/%Y"
