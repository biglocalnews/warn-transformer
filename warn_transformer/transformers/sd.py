from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform South Dakota raw data for consolidation."""

    postal_code = "SD"
    fields = dict(
        company="Company",
        location="Location",
        date="Date",
        jobs="Employees Affected",
    )
    date_format = "%m/%d/%Y"
