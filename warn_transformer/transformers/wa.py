from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Washington raw data for consolidation."""

    postal_code = "WA"
    fields = dict(
        company="Company",
        location="Location",
        date="Layoff Start Date",
        jobs="# of Workers",
    )
    date_format = "%m/%d/%Y"
