import typing

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform New Jersey raw data for consolidation."""

    postal_code = "NJ"
    fields = dict(
        company="Company",
        location="City",
        date="Effective Date",
        jobs="Workforce Affected",
    )
    date_format = ["%Y-%m-%d %H:%M:%S", "%M/%d/%Y", "%M/%d/%y"]
    jobs_corrections = {
        "TBA": None,
        "To be Determined": None,
        "-": None,
    }
    date_corrections = {
        "TBA": None,
        "Temp layoff": None,
        "-": None,
    }

    def transform_jobs(self, value: str) -> typing.Optional[int]:
        """Transform a raw jobs number into an integer.

        Args:
            value (str): A raw jobs number provided by the source

        Returns: An integer number ready for consolidation. Or, if the value is invalid, a None.
        """
        # Cut the asterisk they sometimes use
        value = value.replace("*", "")

        # Do the normal stuff
        return super().transform_jobs(value)
