from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform California raw data for consolidation."""

    postal_code = "CA"
    fields = dict(
        company="company",
        location="city",
        date="notice_date",
        jobs="num_employees",
    )
    date_format = "%m/%d/%Y"
