from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Iowa raw data for consolidation."""

    state = "IA"
    fields = dict(
        company="Company",
        date="Notice Date",
        jobs="Emp #",
    )
    date_format = "%m/%d/%Y"

    def prep_row_list(self, row_list):
        """Make necessary transformations to the raw row list prior to transformation.

        Useful for filter out empty rows.
        """
        # Loop through the full row list
        prepped_list = []
        for row in row_list:
            # Skip empty rows
            if not row["Company"]:
                continue

            # Keep what's left
            prepped_list.append(row)

        # Return what we got
        return prepped_list
