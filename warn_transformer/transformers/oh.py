from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Ohio raw data for consolidation."""

    postal_code = "OH"
    fields = dict(
        company="Company",
        location="City/County",
        date="DateReceived",
        jobs="Potential NumberAffected",
    )
    date_format = "%m/%d/%Y"
