import typing
from datetime import datetime

from ..schema import BaseTransformer


# class Transformer:
class Transformer(BaseTransformer):
    """Transform Mississippi raw data for consolidation."""

    postal_code = "MS"
    fields = dict(
        company="company",
        location="county",
        notice_date="date_notice",
        effective_date="date_effective",
        jobs="affected",
    )
    date_format = ["%m/%d/%Y", "%m/%d/%y"]
    date_corrections = {
        "08/31/2023 09/01/2023": datetime(2023, 8, 31),
        "6/21/20023": datetime(2023, 6, 21),
        "10/05/202": datetime(2020, 10, 5),
        "1/22/2025 Diamond Comic": datetime(2025, 1, 22),
        "6/11/2025 WARN- Due to": datetime(2025, 6, 11),
        "Management Canceled": None,
        "9/9/2025 WARN – Due to": datetime(2025, 9, 9),
        "10/3/2024 WARN- Due to the": datetime(2024, 10, 3),
        "1/27/2025 MW Components": datetime(2025, 1, 27),
        "4/15/2025 WARN – Due to": datetime(2025, 4, 15),
        "04/2022": datetime(2022, 8, 4),
        "RR-pending": None,
        "08/26/2025 WARN – Due to": datetime(2025, 8, 26),
        "03/23/2023 Sun Air Products": datetime(2023, 3, 23),
        "6/30/2025 Non-WARN – non-": datetime(2025, 6, 30),
        "6/23/2025 WARN – non-renewal": datetime(2025, 6, 23),
        "4/15/2026 WARN -Decline in": datetime(2026, 4, 15),
        "12/03/2024 Cooper Lighting": datetime(2024, 12, 3),
        "No RR event - all employees have left this location": None,
        "4/3.2026": datetime(2026, 4, 3),
        "10/03/2025 WARN- Due to": datetime(2025, 10, 3),
        "3/23/2023 Alliance Healthcare": datetime(2023, 3, 23),
        "7/31/2024 Hartson – Kennedy,": datetime(2024, 7, 31),
        "12/16/2025 Westlake Chemical": datetime(2025, 12, 16),
        "1/18/224": datetime(2024, 1, 18),
        "6/30/2025 Non-WARN – Due to": datetime(2025, 6, 30),
        "03/20/2023 GXO Logistics Supply": datetime(2023, 3, 20),
        "02/07/2025 WARN – Due to": datetime(2025, 2, 7),
        "9/25/2025 WARN – Due to": datetime(2025, 9, 25),
        "TBA": None,
        "4/14/2025 WARN – Due to": datetime(2025, 4, 14),
        "Declined RR event": None,
        "05/30/2026 WARN –": datetime(2026, 5, 30),
        "03/18/2025 Mississippi Polymers": datetime(2025, 3, 18),
        "12-1-2022": datetime(2022, 12, 1),
        "4/15/2025 Non-WARN- Lack of": datetime(2025, 4, 15),
        "10/10/2025 WARN - Declining": datetime(2025, 10, 10),
        "2/2026": datetime(2026, 2, 1),
        "02/18/2025 WWL Vehicle": datetime(2025, 2, 18),
        "07/11/2025 Rex Lumber,": datetime(2025, 7, 11),
        "6/24/2025 Non-WARN- This is a": datetime(2025, 6, 24),
        "02/06/2025 Enviva Pellets": datetime(2025, 2, 6),
        "7/31/ 2023": datetime(2023, 7, 31),
        "Pending": None,
        "4/17/2026 Aramark": datetime(2026, 4, 17),
        "6/15/2026 WARN – Due": datetime(2026, 6, 15),
        "05/11/2026 Leggett &": datetime(2026, 5, 11),
        "6/11/2026 WARN-Plant": datetime(2026, 6, 11),
    }
    jobs_corrections = {
        "1,000": 1000,
        "TBA": None,
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
        return "clos" in row["action_type"].lower() or None
