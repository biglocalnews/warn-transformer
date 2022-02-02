from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Alabama raw data for consolidation."""

    postal_code = "AL"
    fields = dict(
        company="Company",
        location="City",
        date="Initial Report Date",
        jobs="Planned # Affected Employees",
    )
    date_format = "%m/%d/%Y"
