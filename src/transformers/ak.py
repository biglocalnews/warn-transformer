from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Alaska raw data for consolidation."""

    postal_code = "AK"
    fields = dict(
        company="Company",
        date="Notice Date",
        jobs="Employees Affected",
    )
    date_format = "%m/%d/%y"
