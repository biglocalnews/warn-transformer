from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Oregon raw data for consolidation."""

    postal_code = "OR"
    fields = dict(
        company="Company Name",
        location="Location",
        date="Received Date",
        jobs="Laid Off",
    )
    date_format = "%Y-%m-%d %H:%M:%S"
    minimum_year = 1988
    jobs_corrections = {
        27500: None,
    }
