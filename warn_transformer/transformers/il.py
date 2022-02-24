from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Illinois raw data for consolidation."""

    postal_code = "IL"
    fields = dict(
        company="Location Name",
        location=lambda row: f"{row['Location Address']} {row['Location City']}, {row['Location State']} {row['Location Zipcode']}".strip(),
        date=lambda row: row["Initial Date Reported"] or row["Notify Date"],
        jobs="Total # of Employees",
    )
    date_format = "%Y-%m-%d %H:%M:%S"
    minimum_year = 1987
    maximum_jobs = 100000
    # jobs_corrections = {
    #     "N/A": None,
    #     "Not Provided": None,
    #     "Not reported": None,
    # }

    # def transform_jobs(self, value: str) -> typing.Optional[int]:
    #     """Transform a raw jobs number into an integer.

    #     Args:
    #         value (str): A raw jobs number provided by the source

    #     Returns: An integer number ready for consolidation. Or, if the value is invalid, a None.
    #     """
    #     # Split on new lines
    #     values = value.split("\n")
    #     # Do the normal stuff
    #     return super().transform_jobs(values[0])
