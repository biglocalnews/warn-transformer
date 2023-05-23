from datetime import datetime

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform South Carolina raw data for consolidation."""

    postal_code = "SC"
    fields = dict(
        company="company",
        location="location",
        notice_date="date",
        jobs="jobs",
    )
    date_format = "%m/%d/%Y"
    date_corrections = {
        "4/8/20/20": datetime(2020, 4, 8),
        "12/31//2015": datetime(2015, 12, 31),
        "4/1/2023 - 12/31/2023": datetime(2023, 4, 1),
        "5/4/2023 - 12/31/2023": datetime(2023, 5, 4),
        "5/19/2023 - 11/10/2023": datetime(2023, 5, 19),
        "5/26/2023 - 6/1/2023": datetime(2023, 5, 26),
        "5/19/2023 - 7/7/2023": datetime(2023, 5, 19),
    }
