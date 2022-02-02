from datetime import datetime

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Maryland raw data for consolidation."""

    postal_code = "MD"
    fields = dict(
        company="Company",
        location="Location",
        date="Notice Date",
        jobs="Total Employees",
    )
    date_format = "%m/%d/%Y"
    date_corrections = {
        "4/1/2020 (REVISED) 10/22/2020": datetime(2020, 4, 1),
        "3/3020/17": datetime(2017, 3, 20),
        "5/62011": datetime(2011, 5, 6),
        "2/1/2010 to 2/28/2010": datetime(2010, 2, 1),
        "NOTE: possible event 10/22/2010": datetime(2010, 10, 22),
    }
