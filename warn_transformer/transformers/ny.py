import typing
from datetime import datetime

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform New York raw data for consolidation."""

    postal_code = "NY"
    fields = dict(
        company=lambda row: row["company_name"] or row["Company"] or None,
        location="City",
        notice_date=lambda row: row["notice_dated"] or row["Notice Date"] or None,
        effective_date="Layoff Date",
        jobs="Number Affected",
    )
    date_format = ("%Y-%m-%d %H:%M:%S", "%m/%d/%Y", "%Y-%m-%d")
    date_corrections = {
        "929/2022": datetime(2022, 9, 29),
        "3/6/3023": datetime(2023, 3, 6),
        "2": datetime(2021, 2, 12),
        "2/2/2024`": datetime(2024, 2, 2),
        "7/29/24": datetime(2024, 7, 29),
        "7/31/24": datetime(2024, 7, 31),
        "8/2/24": datetime(2024, 8, 2),
    }

    def prep_row_list(
        self, row_list: typing.List[typing.Dict]
    ) -> typing.List[typing.Dict]:
        """Make necessary transformations to the raw row list prior to transformation.

        Args:
            row_list (list): A list of raw rows of data from the source.

        Returns: The row list minus empty records
        """
        # Do the standard stuff
        row_list = super().prep_row_list(row_list)

        # Split records from scrape from those in the archival set
        scraped_list = [r for r in row_list if r["notice_url"]]
        archival_list = [r for r in row_list if not r["notice_url"]]
        assert len(scraped_list) + len(archival_list) == len(row_list)

        # Remove records from the scrape that are covered by the more detailed archival file
        cutoff = datetime(2021, 6, 30)
        keep_list = []
        for r in scraped_list:
            dt_str = self.transform_date(r["notice_dated"])
            assert isinstance(dt_str, str)
            dt = datetime.strptime(dt_str, "%Y-%m-%d")
            if dt > cutoff:
                keep_list.append(r)

        # Add them back together
        prepped_list = keep_list + archival_list

        # Return it
        return prepped_list

    def transform_date(self, value: str) -> typing.Optional[str]:
        """Transform a raw date string into a date object.

        Args:
            value (str): The raw date string provided by the source

        Returns: A date object ready for consolidation. Or, if the date string is invalid, a None.
        """
        if not value:
            return None
        value = value.split()[0].replace(",", "").replace(";", "")
        return super().transform_date(value)

    def check_if_temporary(self, row: typing.Dict) -> typing.Optional[bool]:
        """Determine whether a row is a temporary or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean or null
        """
        value = row["Dislocation Type"].lower()
        if "possible" in value or "potential" in value:
            return None
        return "temp" in value or None

    def check_if_closure(self, row: typing.Dict) -> typing.Optional[bool]:
        """Determine whether a row is a closure or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean or null
        """
        value = row["Dislocation Type"].lower()
        if "possible" in value or "potential" in value or "temp" in value:
            return None
        return "clos" in value or None
