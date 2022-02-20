import typing

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Ohio raw data for consolidation."""

    postal_code = "OH"
    fields = dict(
        company="Company",
        location="City/County",
        date="DateReceived",
        jobs="Potential NumberAffected",
    )
    date_format = "%m/%d/%Y"

    def transform_date(self, value: str) -> typing.Optional[str]:
        """Transform a raw date string into a date object.

        Args:
            value (str): The raw date string provided by the source

        Returns: A date object ready for consolidation. Or, if the date string is invalid, a None.
        """
        # Cut out cruft
        value = value.replace("Updated", "")
        value = value.replace("Revised", "")
        # Split double dates
        if len(value) == 20:
            value = value[:10]
        # Do the typical stuff
        return super().transform_date(value)
