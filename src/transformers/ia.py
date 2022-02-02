from datetime import datetime


class Transformer:
    """Transform a state's raw data for consolidation."""

    date_format = "%m/%d/%Y"

    def __init__(self, row_list):
        self.row_list = self.prep_row_list(row_list)

    def transform(self):
        """Transform prepared rows into a form that's ready for consolidation."""
        return [self.transform_row(r) for r in self.row_list]

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

    def transform_date(self, value):
        """Transforms a raw date string into a date object.

        Args:
            value (str): The raw date string provided by the source

        Returns: A date object ready for consolidation. Or, if the date string is invalid, a None.
        """
        value = value.strip()
        try:
            dt = datetime.strptime(value, self.date_format)
        except ValueError:
            return None
        return str(dt.date())

    def transform_jobs(self, value):
        """Transforms a raw jobs number into an integer.

        Args:
            value (str): A raw jobs number provided by the source

        Returns: An integer number ready for consolidation. Or, if the value is invalid, a None.
        """
        try:
            return int(value)
        except ValueError:
            return None
