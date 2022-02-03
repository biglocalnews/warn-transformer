from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Wisconsin raw data for consolidation."""

    postal_code = "WI"
    fields = dict(
        company="Company",
        location="City",
        date="NoticeRcvd",
        jobs="AffectedWorkers",
    )
    date_format = ("%m/%d/%Y", "%Y%m%d")
