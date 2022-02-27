from datetime import datetime

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Washington D.C. raw data for consolidation."""

    postal_code = "DC"
    fields = dict(
        company="Organization Name",
        location=lambda x: "Washington D.C.",  # Hardcode in the city name
        date="Notice Date",
        jobs="Number toEmployees Affected",
    )
    date_format = ("%B %d, %Y", "%m/%d/%y")
    date_corrections = {
        "May 2 and 5, 2020": datetime(2020, 5, 2),
        "March, 20, 2020": datetime(2020, 3, 20),
        "31, 2019": datetime(2019, 12, 31),
        "August 2013": datetime(2013, 8, 1),
        "October 2013": datetime(2013, 10, 1),
        "May 7,14 & 31, 2012": datetime(2012, 5, 7),
    }
    jobs_corrections = {
        "All": None,
    }
