from datetime import datetime

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Washington D.C. raw data for consolidation."""

    postal_code = "DC"
    fields = dict(
        company="Organization Name",
        location=lambda x: "Washington D.C.",  # Hardcode in the city name
        notice_date="Notice Date",
        effective_date="Effective Layoff Date",
        jobs="Number toEmployees Affected",
    )
    date_format = ("%B %d, %Y", "%m/%d/%y", "%B, %d, %Y", "%B %d,%Y")
    date_corrections = {
        "May 2 and 5, 2020": datetime(2020, 5, 2),
        "March, 20, 2020": datetime(2020, 3, 20),
        "31, 2019": datetime(2019, 12, 31),
        "August 2013": datetime(2013, 8, 1),
        "October 2013": datetime(2013, 10, 1),
        "May 7,14 & 31, 2012": datetime(2012, 5, 7),
        "February 28, 2022 March 31, 2022": datetime(2020, 2, 28),
        "December 25, and Feb - Jun 2021": datetime(2020, 12, 25),
        "TBD": None,
        "September 15, 2020 and March 18, 2020": datetime(2020, 9, 15),
        "May 31, 2012 June 15, 2012": datetime(2012, 5, 31),
        "June 29, 2012 & August 3, 2012": datetime(2012, 6, 29),
        "November 15 - December 16, 2022": datetime(2022, 11, 15),
        "December 3 - December 17, 2022": datetime(2022, 12, 3),
        "Februart 14, 2025": datetime(2025, 2, 14),
        "December 20 & 31, 2024": datetime(2024, 12, 20),
        "Februart 20, 2025": datetime(2025, 2, 20),
        "Various Dates through September 30, 2025": datetime(2025, 9, 30),
        "February 28 and March 7 & 14, 2025": datetime(2025, 2, 28),
        "Various Dates through May 30, 2025": datetime(2025, 5, 30),
        "March 28 through May 31, 2025": datetime(2025, 3, 28),
        "March 14, 2025 through April30, 2025": datetime(2025, 3, 14),
        "Various Dates through May 16, 2026": datetime(2025, 5, 16),
        "Various Dates through May 16, 2025": datetime(2025, 5, 16),
        "May 2, 2025 through May 16, 2026": datetime(2025, 5, 2),
        "May 9 through September 30, 2025": datetime(2025, 5, 9),
        "Various dates through June 30, 2025": datetime(2025, 6, 30),
        "July 31 through August 28, 2025": datetime(2025, 7, 31),
        "September 30 through December 30, 2025": datetime(2025, 9, 30),
        "Various Dates through June 29, 2025": datetime(2025, 6, 29),
        "Various Dates through September 28, 2025": datetime(2025, 9, 28),
        "Various Dates through November2, 2025": datetime(2025, 11, 2),
        "Various Dates through November 2, 2025": datetime(2025, 11, 2),
        "September 30 through September 28, 2025": datetime(2025, 9, 30),  # What?
        "March 14, 2025 through April 30, 2025": datetime(2025, 3, 14),
    }
    jobs_corrections = {
        "All": None,
        "TBD": None,
        "45 (amended)": 45,
        "63 (amended)": 63,
        "54 (amended)": 54,
        "46 (amended)": 46,
    }
