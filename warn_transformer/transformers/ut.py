from datetime import datetime

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Utah raw data for consolidation."""

    postal_code = "UT"
    fields = dict(
        company="Company Name",
        location="Location",
        notice_date="Date of Notice",
        jobs="Affected Workers",
    )
    date_format = ("%m/%d/%Y", "%m/%d/%y")
    date_corrections = {
        "03/09/2020&": datetime(2020, 3, 9),
        "01/05/18/": datetime(2018, 1, 5),
        "03/05/14 Updated": datetime(2014, 3, 5),
        "09/31/10": datetime(2010, 9, 30),
        "05/2009": datetime(2009, 5, 1),
        "01/07//09": datetime(2009, 1, 7),
        "08/31//2022": datetime(2022, 8, 31),
    }
    jobs_corrections = {
        "645 Revised": 645,
    }
