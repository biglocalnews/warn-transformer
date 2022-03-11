import typing

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Florida raw data for consolidation."""

    postal_code = "FL"
    fields = dict(
        company="Company Name",
        location="Company Name",
        notice_date="State Notification Date",
        effective_date="Layoff Date",
        jobs="Employees Affected",
    )
    date_format = ("%m-%d-%y", "%m/%d/%Y")
    jobs_corrections = {
        # This Disney layoff notice is large but legit
        # https://www.usatoday.com/story/travel/2020/10/30/disney-world-live-entertainment-shows-dark-covid-19-pandemic/6088586002/
        10903: 10903,
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
            value = value.replace("\n", "").strip()
            value = value.split(" thru")[0].strip()
            value = value.split("thru")[0].strip()
            return super().transform_date(value)

    def transform_company(self, value: str) -> str:
        """Transform a raw company name.

        Args:
            value (str): The raw company string provided by the source

        Returns: A string object ready for consolidation.
        """
        return value.split("\n")[0].strip()

    def transform_location(self, value: str) -> str:
        """Transform a raw location.

        Args:
            value (str): The raw location string provided by the source

        Returns: A string object ready for consolidation.
        """
        return value.split("\n")[-1].split(",")[0].strip()
