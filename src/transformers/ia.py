from ..schema import BaseTransformer


class Transformer(BaseTransformer):
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

    def transform_row(self, row):
        """Transform a row into a form that's ready for consolidation.

        Args:
            row (dict): One raw row of data from the source

        Returns: A transformed dict that's ready to be loaded into our consolidated schema.
        """
        return dict(
            state="IA",
            company=row["Company"],
            date=self.transform_date(row["Notice Date"]),
            jobs=self.transform_jobs(row["Emp #"]),
        )
