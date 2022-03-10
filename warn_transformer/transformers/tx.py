from datetime import datetime

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Texas raw data for consolidation."""

    postal_code = "TX"
    fields = dict(
        company="JOB_SITE_NAME",
        location="CITY_NAME",
        notice_date="NOTICE_DATE",
        effective_date="LayOff_Date",
        jobs="TOTAL_LAYOFF_NUMBER",
    )
    date_format = "%Y-%m-%d %H:%M:%S"
    date_corrections = {
        "1930-03-30 00:00:00": datetime(2020, 3, 30),
        "1930-03-31 00:00:00": datetime(2020, 3, 31),
        "2027-03-01 00:00:00": datetime(2017, 3, 1),
    }
