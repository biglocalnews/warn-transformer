from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Vermont raw data for consolidation."""

    postal_code = "VT"
    fields = dict(
        company="employer",
        location="city",
        date="notice_date",
        jobs="number_of_employees_affected",
    )
    date_format = "%b %d, %Y"
