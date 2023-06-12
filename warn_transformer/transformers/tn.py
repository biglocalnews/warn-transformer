import typing
from datetime import datetime

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Tennessee raw data for consolidation."""

    postal_code = "TN"
    fields = dict(
        company="Company",
        location=lambda row: row["City"] or f"{row['County']} County",
        notice_date="Notice Date",
        effective_date="Effective Date",
        jobs="No. Of Employees",
    )
    date_format = (
        "%Y/%m/%d",
        "%m/%d/%Y",
        "%B %d, %Y",
        "%B %Y",
        "%B%d, %Y",
        "%B %d. %Y",
        "%B %d,%Y",
    )
    date_corrections = {
        "2018/4/ 27": datetime(2018, 4, 27),
        "start of layoff -\xa0March 13, 2020": datetime(2020, 3, 13),
        "December 15-30, 2020": datetime(2020, 12, 15),
        "June 17 - June 30, 2020": datetime(2020, 6, 17),
        "124": None,
        "March 16, 2020 - June 30, 2020": datetime(2020, 3, 16),
        "March 20-24, 2020": datetime(2020, 3, 20),
        "March 4, 2020 - June 4, 2020": datetime(2020, 3, 4),
        "Apri 1, 2020": datetime(2020, 4, 1),
        "Beginning April 14 and ending June 30, 2020": datetime(2020, 4, 14),
        "Beginning February 16 and ending February 29, 2020": datetime(2020, 2, 16),
        "Beginning March 17 and ending March 30, 2020": datetime(2020, 3, 17),
        "Beginning in February 2020": datetime(2020, 2, 1),
        "beginning February 2020": datetime(2020, 2, 1),
        "January 3, 2020 through January 31, 2020": datetime(2020, 1, 3),
        "December 13, 2019 and continue until February 28, 2020": datetime(
            2019, 12, 13
        ),
        "December 1, 2019 until December 31, 2019": datetime(2019, 12, 1),
        "Will begin on November 30, 2019 and will continue to December 31, 2020": datetime(
            2019, 11, 30
        ),
        "Will begin on October 7, 2019 and will continue to November 30, 2019": datetime(
            2019, 10, 7
        ),
        "Initial layoff September 4, 2019 with additional layoffs planned September 13 and September 20": datetime(
            2019, 9, 4
        ),
        "November 9 through November 23, 2019": datetime(2019, 11, 23),
        "September 30, 2019 for 4 employees and October 31, 2019 for 174 employees": datetime(
            2019, 9, 30
        ),
        "Late September 2019": datetime(2019, 9, 15),
        "September 20, 2019 and continuing through December 2019": datetime(
            2019, 9, 20
        ),
        "August 30, 2019 through December 31, 2019": datetime(2019, 8, 30),
        "April 22, 2019, May 4, 2019, and August 7, 2019": datetime(2019, 4, 22),
        "March 3, 2019, March 11, 2019,": datetime(2019, 3, 3),
        "June 15, 2018, July 6, 2018, August 3, 2018": datetime(2018, 6, 15),
        "July 31, 2023; September 30, 2023; December 31, 2023": datetime(2023, 7, 31),
        "June 12, 2023\xa0– August 11, 2023": datetime(2023, 6, 12),
    }

    def transform_date(self, value: str) -> typing.Optional[str]:
        """Transform a raw date string into a date object.

        Args:
            value (str): The raw date string provided by the source

        Returns: A date object ready for consolidation. Or, if the date string is invalid, a None.
        """
        try:
            return super().transform_date(value)
        except Exception:
            value = value.strip().split(" and ")[0].strip()
            value = value.strip().split(" to ")[0].strip()
            value = value.strip().split(" through ")[0].strip()
            value = value.strip().split(" & ")[0].strip()
            value = value.strip().split(" – ")[0].strip()
            return super().transform_date(value)
