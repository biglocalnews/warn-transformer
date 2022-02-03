from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Virginia raw data for consolidation."""

    postal_code = "VA"
    fields = dict(
        company="Company Name",
        location="Location City",
        date="Notice Date",
        jobs="Employees Affected",
    )
    date_format = "%m/%d/%Y"
