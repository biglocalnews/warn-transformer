from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Texas raw data for consolidation."""

    postal_code = "TX"
    fields = dict(
        company="JOB_SITE_NAME",
        location="CITY_NAME",
        date="NOTICE_DATE",
        jobs="TOTAL_LAYOFF_NUMBER",
    )
    date_format = "%Y-%m-%d %H:%M:%S"
