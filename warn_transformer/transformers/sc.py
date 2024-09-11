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
        "5/19/2023 - 7/14/2023": datetime(2023, 5, 19),
        "9/3/2023 - 10/30/2023": datetime(2023, 9, 3),
        "12/15/2023 - 07/31/2024": datetime(2023, 12, 15),
        "4/6/2024 - 4/19/2024": datetime(2024, 4, 6),
        "5/10/2024 - 12/31/2024": datetime(2024, 5, 10),
        "05/24/2024 - 12/31/2024": datetime(2024, 5, 24),
        "5/24/2024 - 12/31/2024": datetime(2024, 5, 24),
        "6/19/2024 - 7/3/2024": datetime(2024, 6, 19),
        "6/23/2024 - 7/7/2024": datetime(2024, 6, 23),
        "8/9/2024 - 9/30/2024": datetime(2024, 8, 9),
        "9/28/2024 - 1/14/2025": datetime(2024, 9, 28),
        "9/1/2024 - 3/1/2025": datetime(2024, 9, 1),
        "8/19/24 - 9/20/24": datetime(2024, 8, 19),
        "11/11/24 - 12/20/24": datetime(2024, 11, 11),
    }
