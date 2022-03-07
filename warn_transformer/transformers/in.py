import typing
from datetime import datetime

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Indiana raw data for consolidation."""

    postal_code = "IN"
    fields = dict(
        company="Company",
        location="City",
        date="Notice Date",
        jobs="Affected Workers",
    )
    date_format = ["%m/%d/%Y", "%m/%d/%y"]
    jobs_corrections = {
        "97 (in MI)0 (in IN)": 0,
        "100+": 100,
        "62 MAY be affected": 62,
        "5 in Indiana": 5,
        "Unknown": None,
        "75 in Indiana": 75,
        "40-50": 40,
        "100-130": 100,
        "4 Hoosiers": 4,
        "Undisclosed at this time": None,
        "500 Nationwide": None,
        "NA": None,
        "103 (REVISED) 10/22/2020 108": 103,
    }
    date_corrections = {
        "01/30/1202": datetime(2012, 1, 30),
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

        # Cut rows with data-free revisions
        return [r for r in row_list if r["Affected Workers"] != "N/A"]

    def check_if_closure(self, row: typing.Dict) -> typing.Optional[bool]:
        """Determine whether a row is a closure or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean or null
        """
        whitelist = ["CL", "CL -Relocating", "LO and CL", "LO/CL", "PENDING CL"]
        return row["Notice Type"] in whitelist or None
