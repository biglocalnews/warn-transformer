import typing
from datetime import datetime

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Pennsylvania raw data for consolidation."""

    postal_code = "PA"
    fields = dict(
        company="company",
        location="county",
        # notice_date="Date Received",
        effective_date="date_effective",
        jobs="jobs",
    )
    date_format = ["%m/%d/%Y", "%m/%d/%y"]
    date_corrections = {
        "Unknown": None,
        "": None,
        "beginning 10/9/25; ending 10/31/25": datetime(2025, 10, 9),
        "beginning 8/26/2025; ending 9/9/2025": datetime(2025, 8, 26),
        "beginning 9/1/2025; ending 9/15/2025": datetime(2025, 9, 1),
        "8/30/2025 - 12/31/2025": datetime(2025, 8, 30),
        "beginning 8/18/2025; ending 12/31/2026": datetime(2025, 8, 18),
        "beginning 8/12/25; ending 10/18/25": datetime(2025, 8, 12),
        "beginning 6/13/25; ending 6/30/25": datetime(2025, 6, 13),
        "beginning 1/17/25; ending 6/30/25": datetime(2025, 1, 17),
        "beginning 7/31/25; ending 8/3/25": datetime(2025, 7, 31),
        "8/25/2025 - 9/8/2025": datetime(2025, 8, 25),
        "5/5/2025 @ Etters location; 6/4/2025 @ Philadelphia location": datetime(
            2025, 5, 5
        ),
        "7/1/2025 - 7/15/2025": datetime(2025, 7, 1),
        "8/1/2025 - 12/31/2025": datetime(2025, 8, 1),
        "beginning 4/25/25; ending 5/2/25": datetime(2025, 4, 25),
        "first wave - 6/9/2025 impacting 192 workers ... second wave - 9/30/2025 impacting 106 workers ... final wave ending  - 11/17/2025 impacting 25 workers": datetime(
            2025, 6, 9
        ),
        "4/22/2025 for Frankford Avenue location ... 4/24/2025 for Castor Avenue location": datetime(
            2025, 4, 22
        ),
        "first wave - 5/9/2025 impacting 124 workers ... second wave - 7/1/2025 impacting 112 workers ... final wave ending  - 12/31/2025 impacting 62 workers": datetime(
            2025, 5, 9
        ),
        "6/27/2025 - 12/31/2025": datetime(2025, 6, 27),
        "beginning:   3/24/2025; ending:   4/12/2025": datetime(2025, 3, 24),
        "May 19, 23, 30 ... June 6, 20, 27 ... July 11, 18 ... August 8, 22, 29 ... September 12": datetime(
            2025, 5, 19
        ),
        "first round -- 5/16 through 5/30; second round -- 6/23 through 7/7; final round -- sometime in 2026": datetime(
            2025, 5, 16
        ),
        "4/23/25; ending:   5/7/25": datetime(2025, 4, 23),
        "4/9/25-10/15/25": datetime(2025, 4, 9),
        "5/26/25-5/30/25": datetime(2025, 1, 31),
        "1/31/25-3/31/25": datetime(2025, 1, 31),
        "beginning:  3/18/25; ending:  3/31/25": datetime(2025, 3, 18),
        "beginning:   1/6/2025; completed:   3/31/2025": datetime(2025, 1, 6),
        "Layoff date:  2/18/2025; Closure date:  2/21/2025": datetime(2025, 2, 18),
        "2/17/2025 through 3/3/2025": datetime(2025, 2, 17),
        "Layoffs:  1/25/2025; Closure:  1/31/2025": datetime(2025, 1, 25),
        "beginning:  1/1/2025; ending:  1/3/2025": datetime(2025, 1, 1),
        "1/3/2025 - 1/31/2026": datetime(2025, 1, 3),
        "1. 1/15/2025 ... 2. 1/22/2025 ... 3. 2/12/2025": datetime(2025, 1, 15),
        "beginning:  12/14/2024; ending:  12/28/2024": datetime(2024, 12, 14),
        "12/9/2024 -- 173 workers ... 12/20/2024 -- 60 workers ... 1/13/2025 -- 2 workers ... 1/27/2025 -- 9 workers ... 2/17/2025 -- 26 workers": datetime(
            2024, 12, 9
        ),
        "beginning:  11/30/24; ending:  12/3/24": datetime(2024, 11, 30),
        "11/27/2024 - 12/31/2024": datetime(2024, 11, 27),
        "11/10/2024 ": datetime(2024, 11, 10),
        "11/22/2024 ": datetime(2024, 11, 22),
        "9/23/2024  ": datetime(2024, 9, 23),
        "11/22  /2024  ": datetime(2024, 11, 22),
        "beginning:  10/26/2024; ending:  11/9/2024 ": datetime(2024, 10, 26),
        "beginning:   10/27/2024; ending:  11/10/2024": datetime(2024, 10, 27),
        "8/30/2024 - 10/4/2024": datetime(2024, 8, 30),
        "beginning:  10/7/2024; ending:  12/31/2024": datetime(2024, 10, 7),
        "6/7 /2024": datetime(2024, 6, 7),
        "8/9 /2024": datetime(2024, 8, 9),
        "8/16 /2024": datetime(2024, 8, 16),
        "8/9/2024 or within a 14-day window ": datetime(2024, 8, 9),
        "beginning:  8/26/2024; E nding:  12/31/2024  ": datetime(2024, 8, 26),
        "beginning:  8/26/2024; E nding:  12/31/2024": datetime(2024, 8, 26),
        "beginning:  8/26/2024; Ending:  12/31/2024": datetime(2024, 8, 26),
        "8/2/2024-8/16/2024": datetime(2024, 8, 2),
        "Beginning 4/20/24; Ending 5/4/2024": datetime(2024, 4, 20),
        "Beginning 4/13/2024; Ending 5/31/2024": datetime(2024, 4, 13),
        "Beginning 2/15/2024; Ending 4/30/2024": datetime(2024, 2, 15),
        "14 day period commencing 4/15/2024": datetime(2024, 4, 15),
        "Beginning 3/8/2024; Ending end of year 2024": datetime(2024, 3, 8),
        "Beginning 1/31/2024; Ending end of year 2024": datetime(2024, 1, 31),
        "3/15/24 - 9/30/24": datetime(2024, 3, 15),
        "Beginning 2/11/2024; Ending 2/25/2024": datetime(2024, 2, 11),
        "Beginning February/March 2024; Ending July 1, 2024": datetime(2024, 2, 1),
        "1/2/2024 and continuing periodically": datetime(2024, 1, 2),
        "1/6/2024 - 3/26/2024": datetime(2024, 1, 6),
        "1/16/2024 - 3/1/2024": datetime(2024, 1, 16),
        "1/18/2024. Additional layoff dates:  2/19/24 & 4/18/24": datetime(2024, 1, 18),
        "beginning:  1/3/2024 (52 employees); ending:  3/31/2024 (128 employees)": datetime(
            2024, 1, 3
        ),
        "Beginning 12/15/2023 - Ending 9/30/2024": datetime(2023, 12, 15),
        "Beginning 11/20/2023 - Ending 12/15/2023": datetime(2023, 11, 20),
        "9/8/23 - 10/1/23": datetime(2023, 9, 8),
        "Beginning 9/29/23; Ending 11/16/23": datetime(2023, 9, 23),
        "Beginning:  October 31, 2023 - ... Ending: April 15, 2024": datetime(
            2023, 10, 31
        ),
        "Beginning:  October 21, 2023 - ... Ending: December 30, 2023": datetime(
            2023, 10, 21
        ),
        "9/8/23 (96 employees) ... 9/15/23 (66 employees) ... 9/22/23 (36 employees) ... 9/29/23 (26 employees) ... 9/30/23 (1 employee) ... 10/6/23 (13 employees) ... 10/13/23 (37 employees) ... 10/20/23 (34 employees) ... 11/10/23 (10 employees) ... 12/1/23 (61 employees) ... 2/2/24 (13 employees) ... ": datetime(
            2023, 9, 8
        ),
        "9/8/23 (96 employees)": datetime(2023, 9, 8),
        "Beginning 8/21/23 - Ending 9/19/23": datetime(2023, 8, 21),
        "beginning 5/10/23 and ending 60-74 days thereafter": datetime(2023, 5, 10),
        "7/14/23 (37 workers); 9/15/23 (125 workers)": datetime(2023, 7, 14),
        "04/14 -- 11 Employees ... 05/05 -- 20 Employees ... 06/17 -- 40 Employees ... 07/07 -- 20 Employees ... 08/04 -- 20 Employees ... 09/08 -- 20 Employees ... 10/06 -- 20 Employees ... 11/03 -- 69 Employees ... 12/29 -- 40 Employees": datetime(
            2023, 4, 14
        ),
        "04/14": datetime(2023, 4, 14),
        "Phase 1: 4/14 ... Phase 2: 5/13 -- 5/27 ... Phase 3: 6/12 -- 8/11": datetime(
            2023, 4, 14
        ),
        "Phase 1: 4/14": datetime(2023, 4, 14),
        "7/3/20223 - 10/16/2023": datetime(2023, 7, 3),
        "6/25/2023 - 7/9/2023": datetime(2023, 6, 25),
        "6/2/23 -- 105 Employees ... 7/7/23 -- 10 Employees ... 10/6/23 -- 70 Employees ... 12/1/23 -- 18 Employees": datetime(
            2023, 6, 2
        ),
        "6/2/23 -- 105 Employees": datetime(2023, 6, 2),
        "6/30/23 -- 50 Employees ... 8/11/23 -- 74 Employees": datetime(2023, 6, 30),
        "6/30/23 -- 50 Employees": datetime(2023, 6, 30),
        "Phase 1: 4/28/23 (67 employees) ... Phase 2: 7/14/23 (9 employees) ... Phase 3: 10/6/23 (4 employees)": datetime(
            2023, 4, 28
        ),
        "Phase 1: 4/28/23 (67 employees)": datetime(2023, 4, 28),
        "February 1, 2023 -- 82 Employees ... March 1, 2023 -- 1 Employee ... April 1, 2023 -- 21 Employees": datetime(
            2023, 2, 1
        ),
        "February 1, 2023 -- 82 Employees": datetime(2023, 2, 1),
        "1st Phase: 1/9/2023 (49 Employees) ... 2nd Phase: 7/31/2023 (15 Employees)": datetime(
            2023, 1, 9
        ),
        "1st Phase: 1/9/2023 (49 Employees)": datetime(2023, 1, 9),
        "Phase 1: 1/11/23 (38 workers) ... Phase 2: 2/10/23 (59 workers) ... Phase 3: 3/31/23 (11 workers) ... Phase 4: TBD (6 workers)": datetime(
            2023, 1, 11
        ),
        "Phase 1: 1/11/23 (38 workers)": datetime(2023, 1, 11),
        "Beginning:  7/15/25; Ending:  7/29/25": datetime(2025, 7, 15),
        "Beginning:   12/9/2024; Ending:   12/21/2024": datetime(2024, 12, 9),
        "beginning:  10/26/2024; ending:  11/9/2024": datetime(2024, 10, 26),
        "beginning:  10/27/2024; ending:  11/10/2024": datetime(2024, 10, 27),
        "Commencing:  5/30/2024; Ending:  7/29/2024": datetime(2024, 5, 30),
        "8/9/2024 or within a 14-day window": datetime(2024, 8, 9),
        "Commencing:  7/6/2024; Ending:  9/1/2024": datetime(2024, 7, 6),
        "Beginning:  6/3/24; Ending:  6/16/24": datetime(2024, 6, 3),
        "Beginning:  2/24/24; Ending:  4/23/24": datetime(2024, 2, 24),
        "Beginning:  5/17/24; Ending:  8/30/24": datetime(2024, 5, 17),
        "Beginning:  1/16/24; Ending:  3/29/24": datetime(2024, 1, 16),
        "Beginning:  1/2/2024 - Ending:  3/31/2024": datetime(2024, 1, 2),
        "November 3, 2023": datetime(2023, 11, 3),
        "9/8/23 (96 employees) ... 9/15/23 (66 employees) ... 9/22/23 (36 employees) ... 9/29/23 (26 employees) ... 9/30/23 (1 employee) ... 10/6/23 (13 employees) ... 10/13/23 (37 employees) ... 10/20/23 (34 employees) ... 11/10/23 (10 employees) ... 12/1/23 (61 employees) ... 2/2/24 (13 employees) ...": datetime(
            2023, 9, 8
        ),
        "Beginning:  2/28/23 - Ending:  12/31/23": datetime(2023, 2, 28),
        "March 3, 2023": datetime(2023, 3, 3),
        "March 31, 2023": datetime(2023, 3, 31),
        "March 5, 2023": datetime(2023, 3, 5),
        "February 28, 2023": datetime(2023, 2, 28),
        "Beginning:  March 15, 2023; Ending:  October 2, 2023": datetime(2023, 3, 15),
        "Beginning:  January 23, 2023; Ending:  March 24, 2023": datetime(2023, 1, 23),
        "Beginning:   12/31/2025; Ending:   6/30/2026": datetime(2025, 12, 31),
        "1/1/2026-12/31/2027": datetime(2026, 1, 1),
        "Beginning 1/31/2026; Ending 2/28/2026": datetime(2026, 1, 31),
        "Beginning 1/12/2026; Ending 1/26/2026": datetime(2026, 1, 12),
        "Beginning 1/12/2026; Ending 5/30/2026": datetime(2026, 1, 12),
        "beginning 2/13/2026; ending 12/31/2026": datetime(2026, 2, 13),
        "beginning 12/4/2025; ending 4/1/2026": datetime(2025, 12, 4),
        "beginning 3/1/2026; ending 6/30/2026": datetime(2026, 3, 1),
        "beginning 1/2/2026; ending 10/31/2026": datetime(2026, 1, 2),
        "beginning 2/27/2026; ending 3/31/2026": datetime(2026, 2, 27),
        "Beginning 3/29/26, ending 9/30/26": datetime(2026, 3, 29),
    }

    jobs_corrections = {
        "Unknown": None,
        "TBD": None,
        "unknown": None,
        "To be determined": None,
        "60 total": 60,
        "72 (54 PA residents impacted)": 54,
        "9 Pennsylvania workers (209 total) ... EFFECTIVE DATE: Beginning: 7/15/25; Ending: 7/29/25": 9,
        "501 @ Etters location; 595 @ Philadelphia location": 1096,
        "14 Pennsylvania residents": 14,
        "430 nationwide; unknown number of PA residents impacted": None,
        "Cooked Plant -- 110 ... Raw Plant - 119": 229,
        "420 ... EFFECTIVE DATE: Beginning:  12/9/2024; Ending:  12/21/2024": 420,
        "124 ... EFFECTIVE DATE: Commencing: 5/30/2024; Ending: 7/29/2024": 124,
        "645 (**ONLY FIVE PA RESIDENTS AFFECTED**)": 5,
        "253 (173 @ Allentown and 80 @ Greensburg)": 253,
        "9 Pennsylvania workers (209 total)": 9,
        "105 (91 Temporary Layoffs and 14 Permanent Layoffs)": 105,
        "60 (all employees work remotely)": None,
        "206 (198 P/T and 8 F/T Employees)": 206,
        "54 (All employees can be relocated to other Amazon Delivery Service Partners)": 54,
        "179 (80 Marsden Employees and 99 Temporary Employees from both Express Labor & Integrated Staffing Agencies)": 179,
        "9236 Nationwide; PA total pending verification": None,
        "81 Total -- 13 of which reside in PA": 81,
    }

    def transform_date(self, value: str) -> typing.Optional[str]:
        """Transform a raw date string into a date object.

        Args:
            value (str): The raw date string provided by the source

        Returns: A date object ready for consolidation. Or, if the date string is invalid, a None.
        """
        # Cut out cruft
        # value = value.replace("Updated", "")
        # value = value.replace("Revised", "")
        # value = value.replace("-", "").strip()

        # Split double dates
        # if len(value) == 20:
        #    value = value[:10]
        # elif len(value) == 19:
        #    value = value[:9]
        # value = re.split(r"\s{2,}", value)[0].strip()
        # value = value.split("Originated")[0].strip()
        # print(value)

        try:
            return super().transform_date(value)
        except Exception:
            # value = value.split(" to ")[0].strip()
            # value = value.split()[0].strip()
            # value = value.replace("‐", "")
            return super().transform_date(value)

    def check_if_closure(self, row: typing.Dict) -> typing.Optional[bool]:
        """Determine whether a row is a closure or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean or null
        """
        return "clos" in row["closure_or_layoff"].lower() or None
