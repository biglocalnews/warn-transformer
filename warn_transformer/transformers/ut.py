from datetime import datetime

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Utah raw data for consolidation."""

    postal_code = "UT"
    fields = dict(
        company="Company Name",
        location="Location",
        date="Date of Notice",
        jobs="Affected Workers",
    )
    date_format = ("%m/%d/%Y", "%m/%d/%y")
    date_corrections = {
        "03/09/2020&": datetime(2020, 3, 9),
    }
