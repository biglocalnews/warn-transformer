from datetime import datetime

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    # class Transformer:
    """Transform North Dakota raw data for consolidation."""

    postal_code = "ND"
    fields = dict(
        company="Company Name",
        location="Location",
        notice_date="WARN Dated",
        effective_date="Date of Layoff/Closure",
        jobs="Number Laid Off/Affected",
    )
    date_format = ["%m/%d/%Y", "%m/%d/%y"]  # , "%B %d, %Y", "%B %d, %y
    date_corrections = {
        "4/25/2025 6/28/2025": datetime(2025, 4, 25),
        "1/15/2026 1/28/2026": datetime(2026, 1, 15),
        "10/21/2025 12/21/2025": datetime(2025, 10, 21),
        "Not stated": None,
        "3/1/2032 - 4/30/2023": datetime(2023, 3, 1),
        "3/3/2025 5/2/2025": datetime(2025, 3, 3),
        "9/23/2024 11/22/2024": datetime(2024, 9, 23),
        "7/21/2025beginning 9/26/2025": datetime(2025, 7, 21),
        "Starts 3/25/2020": datetime(2020, 3, 25),
        "Began 1/10/17": datetime(2017, 1, 10),
        "12/20/2024 2/19/2025": datetime(2024, 12, 20),
        "starts 10/29/2017": datetime(2017, 10, 29),
        "5/28/2024 7/27/2024": datetime(2024, 5, 28),
        "starts 10/11/2017": datetime(2017, 10, 11),
        "starts 8/30/2022": datetime(2022, 8, 30),
    }
    jobs_corrections = {
        "approx. 22,00 nationwide (14 reported in ND)": 14,
    }
