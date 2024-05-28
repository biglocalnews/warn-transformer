from datetime import datetime

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Maryland raw data for consolidation."""

    postal_code = "MD"
    fields = dict(
        company="Company",
        location="Location",
        notice_date="Notice Date",
        effective_date="Effective Date",
        jobs="Total Employees",
    )
    date_format = ("%m/%d/%Y", "%m/%d/%y")
    date_corrections = {
        "4/1/2020 (REVISED) 10/22/2020": datetime(2020, 4, 1),
        "3/3020/17": datetime(2017, 3, 20),
        "5/62011": datetime(2011, 5, 6),
        "2/1/2010 to 2/28/2010": datetime(2010, 2, 1),
        "NOTE: possible event 10/22/2010": datetime(2010, 10, 22),
        "3/16/2020 (REVISED) 10/22/2020 11/26/2020": datetime(2020, 3, 16),
        "3/8/19- 6/30/19": datetime(2019, 3, 8),
        "4/13/2018to 5/11/2018": datetime(2018, 4, 13),
        "3/5/2018to 5/4/2018": datetime(2018, 3, 5),
        "3/30/2018 - 6/2018": datetime(2018, 3, 30),
        "7/27/2018 - 8/31/2018": datetime(2018, 7, 27),
        "9/20/18 - 9/30/18": datetime(2018, 9, 20),
        "3/1/19 - 8/31/19": datetime(2019, 3, 1),
        "12/31/18 - 7/31/19": datetime(2018, 12, 31),
        "11/11/18 - 12/31/18": datetime(2018, 11, 11),
        "8/2017-12/2018": datetime(2017, 8, 1),
        "12/2017-8/2018": datetime(2017, 12, 1),
        "3/2018-8/2018": datetime(2018, 3, 1),
        "4/15/2018-4/28/2018": datetime(2018, 4, 15),
        "2/29/2014": datetime(2014, 2, 28),
        "Unknown at this time": None,
        "4/1/2012-11/6/2012": datetime(2012, 4, 1),
        "4th quarter of this year": datetime(2012, 9, 1),
        "4/82011": datetime(2011, 4, 8),
        "7/1/2011-12/2013": datetime(2011, 7, 1),
        "7/62011": datetime(2011, 7, 6),
        "Starting 7/15/2011": datetime(2011, 7, 15),
        "N/A": None,
        "Start 12/1/10 End 9/2011": datetime(2010, 12, 1),
        "09/29/23, 11/30/2023": datetime(2023, 9, 29),
        "10/230/2023": datetime(2023, 10, 23),
        "6/30/204": datetime(2024, 6, 30),
        "7/24/1969": datetime(2024, 7, 24),
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
        "9 50": 59,
    }
