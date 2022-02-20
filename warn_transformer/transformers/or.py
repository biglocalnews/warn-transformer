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
        # This is a nationwide Northwest Airlines layoff that is large and legit.
        # https://www.nytimes.com/1998/09/03/us/northwest-lays-off-27000-increasing-pressure-on-strike.html
        27500: 27500,
    }
