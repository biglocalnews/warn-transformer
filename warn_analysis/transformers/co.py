from datetime import datetime
import typing

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Colorado raw data for consolidation."""

    postal_code = "CO"
    fields = dict(
        company="company",
        location="local area",
        date="warn date",
        jobs="layoffs",
    )
    date_format = "%m/%d/%Y"
    date_corrections = {
        "1/7/19 & 4/6/2020": datetime(2019, 1, 7),
        "3/1/19 (received on 3/22/19)": datetime(2019, 3, 1),
        "3/21/19 (received  3/22/19)": datetime(2019, 3, 21),
        "7/6/19-7/31/19": datetime(2019, 7, 6),
        "7/15/19 (received 7/16/19)": datetime(2019, 7, 15),
        "11-1-19 received 11/19/19 via Local Area/Suthers office": datetime(2019, 11, 1),
        "05/24/19 - 3/20/2020": datetime(2019, 5, 24),
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

        # Cut rows with only one value
        prepped_list = []
        for row in row_list:
            # Skip rows with only one or two values
            value_list = [v for v in row.values() if v.strip()]
            if len(value_list) > 2:
                prepped_list.append(row)

        # Return the result
        return prepped_list

    def transform_date(self, value: str) -> str:
        """Transform a raw date string into a date object.

        Args:
            value (str): The raw date string provided by the source

        Returns: A date object ready for consolidation. Or, if the date string is invalid, a None.
        """
        try:
            dt = datetime.strptime(value.strip(), "%m/%d/%y")
        except ValueError:
            return super().transform_date(value)
        return str(dt.date())
