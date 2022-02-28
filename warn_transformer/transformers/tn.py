from datetime import datetime

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Tennessee raw data for consolidation."""

    postal_code = "TN"
    fields = dict(
        company="Company",
        location=lambda row: row["City"] or f"{row['County']} County",
        date="Notice Date",
        jobs="No. Of Employees",
    )
    date_format = ("%Y/%m/%d", "%m/%d/%Y")
    date_corrections = {
        "2018/4/ 27": datetime(2018, 4, 27),
    }
