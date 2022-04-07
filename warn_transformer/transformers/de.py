from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Deleware raw data for consolidation."""

    postal_code = "DE"
    fields = dict(
        company="employer",
        location="city",
        notice_date="notice_date",
        jobs="number_of_employees_affected",
    )
    date_format = "%b %d, %Y"
