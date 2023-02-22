from datetime import datetime

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Colorado raw data for consolidation."""

    postal_code = "CO"
    fields = dict(
        company="company",
        location=lambda row: row["workforce_area"] or row["workforce_region"],
        notice_date="notice_date",
        effective_date="begin_date",
        jobs=lambda row: row["permanent_job_losses"] or row["jobs"],
    )
    date_format = ("%m/%d/%y", "%m/%d/%Y", "%m-%d-%y", "%m-%d-%Y")
    max_future_days = 365 * 5
    date_corrections = {
        "N/A": None,
        "": None,
        "12/31/19 (for 265) Not specified for 191": datetime(2019, 12, 31),
        "3/24/20- 4/7/20 in phases": datetime(2020, 3, 24),
        "Downsize 1/26/20": datetime(2020, 1, 26),
        "3/13/20 through 4/24/20": datetime(2020, 3, 13),
        "4/30/20, 5/29/20 and 7/31/20": datetime(2020, 4, 30),
        "3/17/20 - 4/2/20": datetime(2020, 3, 17),
        "3/19/20 to 4/20/20, closing 3/19/20": datetime(2020, 3, 19),
        "3/16/20-3/20/20 and 3/21/20-3/31/20": datetime(2020, 3, 16),
        "3/19/20-4/1/20": datetime(2020, 3, 19),
        "3/29": datetime(2020, 3, 29),
        "6/26/20 & 12/29/20": datetime(2020, 6, 26),
        "3/20/20, 3/24/20, & 3/26/20": datetime(2020, 3, 20),
        "3/24/20, 3/26/20 & 3/30/20": datetime(2020, 3, 24),
        "3/23/20, 3/24/20, & 3/26/20": datetime(2020, 3, 23),
        "4/1/20-4/30/20 for hourly workers and May 2020 for salaried associates": datetime(
            2020, 4, 1
        ),
        "3/3/19, 3/31/19": datetime(2019, 3, 3),
        "3/10/19  (184) & 5/31/19  (19)": datetime(2019, 3, 10),
        "3/25/19, 4/24/19, 5/24/19": datetime(2019, 3, 25),
        "5/24/19 - 3/20/20": datetime(2019, 5, 24),
        "4/13/19 - 5/19/19": datetime(2019, 4, 13),
        "5/18/19 - 6/1/19": datetime(2019, 5, 18),
        "5/25/19 (thru 18 mo following)": datetime(2019, 5, 25),
        "7/6/19 - 7/31/19": datetime(2019, 7, 6),
        "8/2/19 - 3/31/20": datetime(2019, 8, 2),
        "9/7/19 - 12/31/19": datetime(2019, 9, 7),
        "10/5/19-12/31/19": datetime(2019, 10, 5),
        "10/18/19-12/31/19": datetime(2019, 10, 18),
        "11/25/19 - 9/30/20": datetime(2019, 11, 25),
        "11/29/19 - 1/31/2020": datetime(2019, 11, 29),
        "10/30/2019, 11/8/2019, 11/22/2019, 11/29/2019": datetime(2019, 10, 30),
        "12/31/19 to 3/26/20": datetime(2019, 12, 31),
        "1/1/20 to 1/14/20": datetime(2020, 1, 1),
        "Closure 1/10/20- 04/10/20": datetime(2020, 1, 10),
        "3/1/19 (received on 3/22/19)": datetime(2019, 3, 1),
        "3/21/19 (received  3/22/19)": datetime(2019, 3, 21),
        "7/6/19-7/31/19": datetime(2019, 7, 6),
        "7/15/19 (received 7/16/19)": datetime(2019, 7, 15),
        "11-1-19 received 11/19/19 via Local Area/Suthers office": datetime(
            2019, 11, 1
        ),
        "05/24/19 - 3/20/2020": datetime(2019, 5, 24),
        "1/7/19 & 4/6/2020": datetime(2019, 1, 7),
        "WARN Date": None,
        "TOTAL": None,
    }
    jobs_corrections = {
        "-": None,
        "61 total, 4 in CO": 4,
        "61 total 4 in CO": 4,
        "": None,
        "55-59": 59,
        "Unknown": None,
        "Unknown - Previous submission 117": None,
        "Layoff Total": None,
        "N/A": None,
        "40-60": 40,
        "1 (of 72 in CO)": 1,
        "38 (resigned voluntarily)": None,
        "49 (5 in CO)": 5,
    }
