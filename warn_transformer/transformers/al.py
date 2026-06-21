import typing
from datetime import datetime

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Alabama raw data for consolidation."""

    postal_code = "AL"
    fields = dict(
        company="company",
        location="location",
        notice_date="date_notice",
        effective_date="date_action",
        jobs="affected",
    )
    date_format = "%m/%d/%Y"
    date_corrections = {"01/01/0001": datetime(2020, 1, 1)}

    def check_if_closure(self, row: typing.Dict) -> typing.Optional[bool]:
        """Determine whether a row is a closure or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean or null
        """
        if "los" in row["action_type"].lower():
            return True
        elif "ayoff" in row["action_type"].lower():
            return False
        else:
            return None
