from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Oklahoma raw data for consolidation."""

    postal_code = "OK"
    fields = dict(
        company="employer",
        location=lambda row: row["city"] or row["address"] or row["lwib_area"],
        notice_date="notice_date",
        jobs="number_of_employees_affected",
    )
    date_format = "%b %d, %Y"
