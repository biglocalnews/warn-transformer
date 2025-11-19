from datetime import datetime

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Montana raw data for consolidation."""

    postal_code = "MT"
    fields = dict(
        company="Name of Company",
        location="County",
        notice_date="Date of Notice",
        effective_date="Date of Impact",
        jobs="Number of Employees Affected",
    )
    date_format = ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d")
    date_corrections = {
        "3/1620 to 4/30/20": datetime(2020, 3, 16),
        "Sept-April": None,
        "5/22/2025, 5/29/2025, 6/5/2025": datetime(2025, 5, 22),
        "12/31/202": datetime(2025, 12, 31),
        "11/17/225": datetime(2025, 11, 17),
    }
    jobs_corrections = {
        "Not noted": None,
        "MT # unknown": None,
        "up to 300": 1,
        "Over 100": 100,
    }
