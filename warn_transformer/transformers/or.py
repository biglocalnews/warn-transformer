import typing

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Oregon raw data for consolidation."""

    postal_code = "OR"
    fields = dict(
        company="Company Name",
        location="Location",
        date="Received Date",
        jobs="Laid Off",
    )
    date_format = "%Y-%m-%d %H:%M:%S"
    minimum_year = 1988
    jobs_corrections = {
        # This is a nationwide Northwest Airlines layoff that is large and legit.
        # https://www.nytimes.com/1998/09/03/us/northwest-lays-off-27000-increasing-pressure-on-strike.html
        27500: 27500,
    }

    def check_if_temporary(self, row: typing.Dict) -> typing.Optional[bool]:
        """Determine whether a row is a temporary or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean or null
        """
        return "temporary" in row["Layoff Type"].lower() or None

    def check_if_closure(self, row: typing.Dict) -> typing.Optional[bool]:
        """Determine whether a row is a closure or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean or null
        """
        return "closure" in row["Layoff Type"].lower() or None
