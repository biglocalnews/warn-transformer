from datetime import datetime

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
    date_format = ("%m/%d/%Y", "%m/%d/%y")
    date_corrections = {
        "1/7/19 & 4/6/2020": datetime(2019, 1, 7),
        "3/1/19 (received on 3/22/19)": datetime(2019, 3, 1),
        "3/21/19 (received  3/22/19)": datetime(2019, 3, 21),
        "7/6/19-7/31/19": datetime(2019, 7, 6),
        "7/15/19 (received 7/16/19)": datetime(2019, 7, 15),
        "11-1-19 received 11/19/19 via Local Area/Suthers office": datetime(
            2019, 11, 1
        ),
        "05/24/19 - 3/20/2020": datetime(2019, 5, 24),
    }
