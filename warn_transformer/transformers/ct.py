import typing
from datetime import datetime

from ..schema import BaseTransformer


# class Transformer:
class Transformer(BaseTransformer):
    """Transform Connecticut raw data for consolidation."""

    postal_code = "CT"
    fields = dict(
        company="affected_company",
        location="layoff_locations",
        notice_date="warn_document_date",
        effective_date="layoff_dates",
        jobs="number_of_impacted_workers",
    )
    date_format = ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S+00.00", "%m/%d/%Y", "%m-%d-%Y"]
    date_corrections = {
        "12/31/16-1/13/17": datetime(2016, 12, 31),
        "12/4/15-tbd": datetime(2015, 12, 4),
        "2/29/15": datetime(2015, 2, 28),
        "9/1//15": datetime(2015, 9, 1),
        "Not Indicated": None,
        "# 12 2/13/17 through 2018": datetime(2017, 2, 13),
        "Most 10/29/16": datetime(2016, 10, 29),
        "Several Weeks - Five Months": None,
        "Not Dated Rec'd 6/24/15": datetime(2015, 6, 24),
        "3rd Quarter 2015-4th Quarter 2016": datetime(2015, 6, 1),
        "June 2017 - March 2018": datetime(2017, 6, 1),
        "First quarter 2019 - 2020": datetime(2019, 1, 1),
        "June 2018 - September 2, 2018": datetime(2018, 6, 1),
        "Beginning June 2018": datetime(2018, 6, 1),
        "December 2018 - March 1, 2019": datetime(2018, 12, 1),
        "Possibly 50+": None,
        "N/A": None,
        "Reduction in Hours Since March 2020": datetime(2020, 3, 1),
        "April-June 2020": datetime(2020, 4, 1),
        "": None,
        "7/3/2020- 7/17/2020": datetime(2020, 7, 3),
        "Not Dated Rec'd 4/22/2020": datetime(2020, 4, 22),
        "Not Dated Rec'd 4/13/2020": datetime(2020, 4, 13),
        "3/16 - 12/13/2020": datetime(2020, 3, 16),
        "february": None,
        "potentially": None,
        "not": None,
        "9/92024": datetime(2024, 9, 9),
        "4/112025": datetime(2025, 4, 11),
        "3/31/2025,": datetime(2025, 3, 31),
        "11/24/2025 - 4/1/2026": datetime(2025, 11, 24),
        "February 15, 2025, through February 28, 2025": datetime(2025, 2, 15),
        "April 12, 2025": datetime(2025, 4, 12),
        "March 21, 2025": datetime(2025, 3, 21),
        "8/2/2019, 12/13/2029": datetime(2019, 8, 2),
        "June 29, 2025": datetime(2025, 6, 29),
        "6/3/2023, 12/31/2023": datetime(2023, 6, 3),
        "09/15/2020,12/17/2020": datetime(2020, 9, 15),
        "03/28/2020, 04/01/2020": datetime(2020, 3, 28),
        "June 10, 2025": datetime(2025, 6, 10),
        "05/10/2020,05/23/2020": datetime(2020, 5, 10),
        "August 23, 2024": datetime(2024, 8, 23),
        "April 30,  2025. Additional layoffs are scheduled for June 20, 2025 and July 30, 2025": datetime(
            2025, 4, 30
        ),
        "April 25, 2025-July 3 1 , 2025.": datetime(2025, 4, 25),
        "03/20/2020,04/03/2020,04/07/2020": datetime(2020, 3, 20),
        "02/26/2022,03/11/2022": datetime(2022, 2, 26),
        "December 2, 2025": datetime(2025, 12, 2),
        "8/4/23, 9/1/23, 10/6/23, 11/3/23, 12/1/23, 1/5/24, 2/2/24, 2/16/24, 3/1/24, 3/29/24, 5/3/24, 5/31/24, 6/28/24, 9/15/24, 9/20/24, 9/27/24, 9/30/24, 12/6/24": datetime(
            2023, 8, 4
        ),
        "10/10/2020,10/23/2020": datetime(2020, 10, 10),
        "June 7, 2025": datetime(2025, 6, 7),
        "04/01/2020,06/30/2020": datetime(2020, 4, 1),
        "February 10th, 2025 through February 24, 2025": datetime(2025, 2, 10),
        "02 /01/2023 ,03/01/2023": datetime(2023, 2, 1),
        "July 5th, 2024": datetime(2024, 7, 5),
        "02/01/2023,03/01/2023": datetime(2023, 2, 1),
        "7/15/2025, 7/29/2025": datetime(2025, 7, 15),
        "12/8/24 through 12/21/24": datetime(2024, 12, 8),
        "08/20/2023, 09/02/2023": datetime(2023, 8, 20),
        "08/17/2020,08/30/2020": datetime(2020, 8, 17),
        "3/10/2020,4/07/2020": datetime(2020, 3, 10),
        "March 25, 2025": datetime(2025, 3, 25),
        "03/25/2020,03/28/2020": datetime(2020, 3, 25),
        "09/15/2023, 09/23/2023, 11/17/2023, 12/1/2023": datetime(2023, 9, 15),
        "1/13/25, 2/13/25": datetime(2025, 1, 13),
        "01/03/2020,05/30/2020": datetime(2020, 1, 3),
        "05/01/2020,07/06/2020": datetime(2020, 5, 1),
        "03/26/2020, 04/16/2020,05/10/2020": datetime(2020, 3, 26),
        "3/13/2020, 3/20/2020, 4/6/2020,4/19/2020": datetime(2020, 3, 13),
        "September 27, 2024": datetime(2024, 9, 27),
        "09/08/2020,09/22/2020": datetime(2020, 9, 8),
        "09/15/2020,03/17/2021": datetime(2020, 9, 15),
        "03/23/2020, 03/26/2020": datetime(2020, 3, 23),
        "12/20/2024, 1/31/25, 2/14/25, 2/21/25": datetime(2024, 12, 20),
        "04/10/2020,04/22/2020": datetime(2020, 4, 10),
        "10/12/2025 - 10/25/2025": datetime(2025, 10, 12),
        "March, 2025": datetime(2025, 3, 1),
        "5/17/24": datetime(2024, 5, 17),
        "August 24, 2024": datetime(2024, 8, 24),
        "10/21/2023, 10/28/2023, 11/04/2023, 11/18/2023, 11/25/2023, 12/30/2025": datetime(
            2023, 10, 21
        ),
        "04/14/2023, 05/13/2023 - 05/27/2023, 06/12/2023-08/11/2023, 06/12/2023-06/26/2023": datetime(
            2023, 4, 14
        ),
        "8/2/2019-12/31/2019": datetime(2019, 8, 2),
        "9/21/2025 - 10/4/2025": datetime(2025, 9, 21),
        "January 25, 2025 through February 7, 2025": datetime(2025, 1, 25),
        "March 31, 2025, June 30, 2025, and September 30, 2025": datetime(2025, 3, 31),
        "4/2/24": datetime(2024, 4, 2),
        "9/9/24": datetime(2024, 9, 9),
        "5/15/24": datetime(2024, 5, 15),
        "3/22/25": datetime(2025, 3, 22),
        "5/31/24": datetime(2024, 5, 31),
        "10/2/23": datetime(2023, 10, 2),
        "0025-05-16": datetime(2025, 5, 16),
        "0024-05-31": datetime(2024, 5, 31),
        "0005-02-04": datetime(2025, 2, 4),
        "12/28/22025": datetime(2025, 12, 28),
    }
    jobs_corrections = {
        "up to 703": 703,
        "18; 87": 105,
        "724 across U.S. including 49 from Ridgefield CT location": 49,
        "Not Provided": None,
        "Not Indicated": None,
        "Possibly 50+": 50,
        "Not indicated": None,
        "12; 6; 5": 23,
        "182; additional 21 on reduced hours": 182,
        "78; additional 13 on reduced hours": 78,
        "124; additional 30 on reduced hours": 124,
        "Not reported on WARN notice": None,
        "Not provided": None,
        "489 - total for CT and other locations": 489,
        "158 Stamford 81 Branford": 239,
        "?": None,
        "110 total; 7 CT 103 remote": 7,
        "Not": None,
        "208 (36 of whom work in CT)": 36,
        "No CT details provided": 0,
        "416 total; 323 work remotely": 93,
        "42: 30 Remote workers": 12,
        "164 Remote workers": 164,
        "13 total: 2 CT residents": 2,
        "22 total: 10 CT residents": 10,
        "4 total: 0 CT residents": 0,
        "2 (1 remote CT worker)": 1,
        "55 total: 1 CT resident": 1,
        "131 total; 92 CT residents": 92,
        "80 Total; 4 CT": 4,
        "66; #CT workers not indicated": None,
        "": None,
        "113,": 113,
        "Greenwich": None,  # Not my circus, not my monkeys
    }

    def transform_date(self, value: str) -> typing.Optional[str]:
        """Transform a raw date string into a date object.

        Args:
            value (str): The raw date string provided by the source

        Returns: A date object ready for consolidation. Or, if the date string is invalid, a None.
        """
        try:
            dt = self.date_corrections[value]
            if dt:
                return str(dt.date())
            else:
                assert dt is None
                return dt
        except KeyError:
            pass
        value = value.lower()
        value = value.replace("beginning", "")
        value = value.replace("after", "")
        value = value.replace("estimated", "")
        value = value.replace(";", "")
        value = value.replace("*", "")
        value = value.strip().split()[0].strip()
        return super().transform_date(value)


#    def check_if_closure(self, row: typing.Dict) -> typing.Optional[bool]:
#        """Determine whether a row is a closure or not.
#
#        Args:
#            row (dict): The raw row of data.
#
#        Returns: A boolean or null
#        """
#        return "yes" in row["closing"].lower() or None
