from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Montana raw data for consolidation."""

    postal_code = "MT"
    fields = dict(
        company="Name of Company",
        location="County",
        date="Date of Notice",
        jobs="Number of Employees Affected",
    )
    date_format = ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d")
    jobs_corrections = {
        "Not noted": None,
        "MT # unknown": None,
    }
