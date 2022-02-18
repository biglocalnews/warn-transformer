from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform New Mexico raw data for consolidation."""

    postal_code = "NM"
    fields = dict(
        company="JOB SITE NAME",
        location="CITY NAME",
        date="NOTICE DATE",
        jobs="TOTAL LAYOFF NUMBER",
    )
    date_format = ("%d-%b-%Y", "%d-%b-%y", "%m/%d/%Y")
    jobs_corrections = {
        "Not Disclosed": None,
        "?": None,
    }
