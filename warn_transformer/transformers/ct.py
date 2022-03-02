import typing

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Connecticut raw data for consolidation."""

    postal_code = "CT"
    fields = dict(
        company="affected_company",
        location="layoff_location",
        date="warn_date",
        jobs="number_workers",
    )
    date_format = ["%m/%d/%Y", "%m/%d/%y"]
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
    }

    def transform_date(self, value: str) -> typing.Optional[str]:
        """Transform a raw date string into a date object.

        Args:
            value (str): The raw date string provided by the source

        Returns: A date object ready for consolidation. Or, if the date string is invalid, a None.
        """
        value = value.strip().split()[-1].strip()
        return super().transform_date(value)

    def check_if_closure(self, row: typing.Dict) -> typing.Optional[bool]:
        """Determine whether a row is a closure or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean or null
        """
        return "yes" in row["closing"].lower() or None
