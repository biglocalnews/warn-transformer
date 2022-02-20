from datetime import datetime

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform California raw data for consolidation."""

    postal_code = "CA"
    fields = dict(
        company="company",
        location=lambda row: row["city"] or row["address"],
        date="notice_date",
        jobs="num_employees",
    )
    date_format = "%m/%d/%Y"
    minimum_year = 2014
    jobs_corrections = {
        # This Tesla layoff number large but correct
        # https://www.cnbc.com/2020/05/13/coronavirus-latest-updates.html
        11083: 11083,
    }
    date_corrections = {
        "09/04/2008": datetime(2018, 9, 4),
    }
