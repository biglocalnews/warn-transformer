from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Illinois raw data for consolidation."""

    postal_code = "IL"
    fields = dict(
        company="Location Name",
        location=lambda row: f"{row['Location Address']} {row['Location City']}, {row['Location State']} {row['Location Zipcode']}".strip(),
        date=lambda row: row["Initial Date Reported"] or row["Notify Date"],
        jobs="Revised Layoff",
    )
    date_format = "%Y-%m-%d %H:%M:%S"
    minimum_year = 1987
    maximum_jobs = 100000
