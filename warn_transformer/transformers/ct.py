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

    def transform_date(self, value: str) -> typing.Optional[str]:
        """Transform a raw date string into a date object.

        Args:
            value (str): The raw date string provided by the source

        Returns: A date object ready for consolidation. Or, if the date string is invalid, a None.
        """
        value = value.strip().split()[-1].strip()
        return super().transform_date(value)
