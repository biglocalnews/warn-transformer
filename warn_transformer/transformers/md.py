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
    jobs_corrections = {
        "103 (REVISED) 10/22/2020 108": 103,
        "1100-1200 (MDDCVA)": 1100,
        "TBD": None,
        "approx. 150": 150,
        "Initially 110 (Possibly as high as 160)": 110,
        "Unknown": None,
        "Starting with 35 leading up to several hundred by December 2013": 35,
        "Total 106 (at this time number impacted at this location is unknown)": 106,
        "Not sure of the number of impacted workers in MD at this time": None,
        "Unknown at this time": None,
        "60-70 in Maryland": 60,
        "unknown at this time": None,
        "8 additional": 8,
        "Total 35 (At this time number impacted at this location is unknown.)": 35,
        "Not known": None,
        "N/A": None,
    }
