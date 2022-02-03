from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Oregon raw data for consolidation."""

    postal_code = "OR"
    fields = dict(
        company="Employer",
        location="City",
        date="Notification Date",
        jobs="Count",
    )
    date_format = "%m/%d/%Y"
