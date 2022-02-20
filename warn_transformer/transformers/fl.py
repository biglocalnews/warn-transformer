from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Florida raw data for consolidation."""

    postal_code = "FL"
    fields = dict(
        company="Company Name",
        location="Company Name",
        date="State Notification Date",
        jobs="Employees Affected",
    )
    date_format = ("%m-%d-%y", "%m/%d/%Y")
    jobs_corrections = {
        # This Disney layoff notice is large but legit
        # https://www.usatoday.com/story/travel/2020/10/30/disney-world-live-entertainment-shows-dark-covid-19-pandemic/6088586002/
        10903: 10903,
    }

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
