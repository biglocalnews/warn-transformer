from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform New Jersey raw data for consolidation."""

    postal_code = "NJ"
    fields = dict(
        company="COMPANY",
        location="CITY",
        date="EFFECTIVEDATE",
        jobs="WORKFORCEAFFECTED",
    )
    date_format = ["%m/%d/%Y", "%m/%d/%y"]
    date_corrections = {
        "-": None,
    }
