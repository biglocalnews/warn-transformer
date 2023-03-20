from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform South Dakota raw data for consolidation."""

    postal_code = "SD"
    fields = dict(
        company="Company",
        location="Location",
        notice_date="Date Received",
        jobs="Employees Affected",
    )
    date_format = "%m/%d/%Y"
    jobs_corrections = {
        "1-5": 1,
    }
