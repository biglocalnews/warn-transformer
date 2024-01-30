import datetime

from ..schema import BaseTransformer

# import typing


class Transformer(BaseTransformer):
    """Transform Hawaii raw data for consolidation."""

    postal_code = "HI"
    # Company,Date,PDF url,location,jobs

    fields = dict(
        company="Company",
        notice_date="Date",
        location="location",
        jobs="jobs",
    )

    date_format = "%Y-%m-%d"

    date_corrections = {
        "* Hawaiian Airlines Amended September 16, 2020": datetime.datetime(
            2020, 9, 16
        ),
        "*Hyatt Regency Waikiki Update December 14, 2020": datetime.datetime(
            2020, 12, 14
        ),
        "*Grand Hyatt Kauai Resort & Spa Amendment #2 August 13, 2021": datetime.datetime(
            2021, 8, 13
        ),
        "*American Machinery Update October 21, 2020": datetime.datetime(2020, 10, 21),
        "** Correction to FOH Hospitality Inc.": None,
        "*Hawaiian Airlines Amendment": None,
        "* Correction to Marriott Resort Hospitality Corporation": None,
        "* DFS Update October 30, 2020": datetime.datetime(2020, 10, 30),
        "*Alohilani Resort Amendment": None,
        "*** Correction to HV Global Management Corporation": None,
        "* Princeville Resort updated March 24, 2020": datetime.datetime(2020, 3, 24),
        "*Grand Hyatt Kauai Resort & Spa Amendment October 30, 2020": datetime.datetime(
            2020, 10, 30
        ),
        "* Waikoloa Beach Marriott Resort & Spa Amended June 9, 2020": datetime.datetime(
            2020, 6, 9
        ),
        "*JTB Hawaii, Inc. Supplement October 30, 2020": datetime.datetime(
            2020, 10, 30
        ),
        "*Hawaiian Airlines Second Amended October 14, 2020": datetime.datetime(
            2020, 10, 14
        ),
        "*Flying Food Group, LLC Amended 10/12/2021": datetime.datetime(2021, 10, 12),
        "*Errata to Amended WARN": None,
        "September 10. 2021 He-Man Landscaping, LLC": datetime.datetime(2021, 9, 21),
        "September 10. 2021": datetime.datetime(2021, 9, 21),
    }

    jobs_corrections = {
        "": None,
    }

    def transform_company(self, value: str) -> str:
        """Transform a raw company name.

        Args:
            value (str): The raw company string provided by the source

        Returns: A string object ready for consolidation.
        """
        return value.split("\n")[0].strip()
