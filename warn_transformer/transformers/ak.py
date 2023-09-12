import typing
from datetime import datetime

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Alaska raw data for consolidation."""

    postal_code = "AK"
    fields = dict(
        company="Company",
        location="Location",
        notice_date="Notice Date",
        effective_date="Layoff Date",
        jobs="Employees Affected",
    )
    date_format = "%m/%d/%y"
    date_corrections = {
        "9/30/20*": datetime(2020, 9, 30),
        "August-November 2021": datetime(2021, 8, 1),
        "4/1/20 5/31/20": datetime(2020, 4, 1),
        "Varied": None,
        "March to May 2016": datetime(2016, 3, 1),
        "various": None,
        "June-August 2023": datetime(2023, 6, 1),
        "9/6/2023": datetime(2023, 9, 6),
        "9/5/2023": datetime(2023, 9, 5),
    }
    jobs_corrections = {
        "Up to 300": 300,
        "TBA": None,
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
        value = value.strip()
        value = value.split(" to ")[0].strip()
        value = value.replace("Starting ", "").strip()
        return super().transform_date(value)

    def check_if_temporary(self, row: typing.Dict) -> typing.Optional[bool]:
        """Determine whether a row is a temporary or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean or null
        """
        return "temporary" in row["Notes"].lower() or None

    def check_if_closure(self, row: typing.Dict) -> typing.Optional[bool]:
        """Determine whether a row is a closure or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean or null
        """
        return "closure" in row["Notes"].lower() or None
