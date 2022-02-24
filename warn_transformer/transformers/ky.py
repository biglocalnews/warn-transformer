from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Kentucky raw data for consolidation."""

    postal_code = "KY"
    fields = dict(
        company="Company Name",
        location=lambda row: row["Location"]
        or row["County: Local  Name"]
        or row["County"],
        date="Date Received",
        jobs="Employees",
    )
    date_format = "%Y-%m-%d %H:%M:%S"
    date_corrections = {
        "43490.0": None,
    }
