from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Rhode Island raw data for consolidation."""

    postal_code = "RI"
    fields = dict(
        company="Company Name",
        location="Location Of Layoffs",
        date="WARN Date",
        jobs="Number Affected",
    )
    date_format = ("%m/%d/%y", "%m/%d/%Y")
