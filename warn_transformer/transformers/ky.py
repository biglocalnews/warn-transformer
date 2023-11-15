import datetime
import re
import typing

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    """Transform Kentucky raw data for consolidation."""

    postal_code = "KY"
    fields = dict(
        company="Company Name",
        location="County",
        notice_date="Date Received",
        effective_date="Projected Date",
        jobs="Employees",
    )
    date_format = "%Y-%m-%d %H:%M:%S"
    minimum_year = 1997
    date_corrections = {
        "43490.0": None,
        "N/A": None,
        "November": None,
        "43735.0": None,
        "43490": datetime.datetime(2019, 1, 25),
        "43735": datetime.datetime(2019, 9, 27),
        "01/03/2002 - 04/15/2002": datetime.datetime(2002, 1, 3),
        "02/01/2002 - 09/01/2002": datetime.datetime(2002, 2, 1),
        "08/20/2001 - 02/28/2002": datetime.datetime(2001, 8, 20),
        "Unknown": None,
        "12/29/2002 - 01/26/2003": datetime.datetime(2002, 12, 29),
        "11/18/2007 - 12/16/2007": datetime.datetime(2007, 11, 18),
        "12/23/2007 - 02/29/2008": datetime.datetime(2007, 12, 23),
        "11/26/2007 - 12/01/2007": datetime.datetime(2007, 11, 26),
        "Mid-January 2009": None,
        "01/17/2009 - 01/18/2009": datetime.datetime(2009, 1, 17),
        "01/09/2009 - 01/23/2009": datetime.datetime(2009, 1, 9),
        "November and December 2008": None,
        "01/01/2009 - 01/03/2009": datetime.datetime(2009, 1, 1),
        "10/16/2008 - 12/14/2008": datetime.datetime(2008, 10, 16),
        "10/17/2008 - 10/31/2008": datetime.datetime(2008, 10, 17),
        "On or around 11/10/2008": datetime.datetime(2008, 11, 10),
        "On or around 07/27/2009": datetime.datetime(2009, 7, 27),
        "On or around 10/31/2008": datetime.datetime(2008, 10, 31),
        "10/13/2008 - 10/31/2008": datetime.datetime(2008, 10, 13),
        "10/01/2008 - 10/15/2008": datetime.datetime(2008, 10, 1),
        "09/30/2008 - 03/31/2009": datetime.datetime(2008, 9, 30),
        "On or around 07/14/2008 & 07/27/2008": datetime.datetime(2008, 7, 14),
        "10/06/2008, 11/03/2008, 12/03/2008": datetime.datetime(2008, 10, 6),
        "09/10/208": datetime.datetime(2008, 9, 10),
        "?": None,
        "07/28/2008 - 09/30/2008": datetime.datetime(2008, 7, 28),
        "06/14/2008 - 06/28/2008": datetime.datetime(2008, 6, 14),
        "On or around 05/31/2008": datetime.datetime(2008, 5, 31),
        "12/31/2007 - 02/2008": datetime.datetime(2008, 12, 31),
        "01/02/2009 - 05/01/2009": datetime.datetime(2009, 1, 2),
        "01/01/2010 - 09/30/2010": datetime.datetime(2010, 1, 1),
        "12/26/2009 - 01/08/2010": datetime.datetime(2009, 12, 26),
        "06/21/2010 - 07/04/2010": datetime.datetime(2010, 6, 21),
        "11/20/2009 - 11/27/2009": datetime.datetime(2009, 11, 20),
        "11/30/2009 - 12/14/2009": datetime.datetime(2009, 11, 30),
        "07/31/2009 - 09/04/2009": datetime.datetime(2009, 7, 31),
        "08/14/2009 - 10/10/2009": datetime.datetime(2009, 8, 14),
        "09/30/09 +/-": datetime.datetime(2009, 9, 30),
        "07/28/2009 - 08/11/2009": datetime.datetime(2009, 7, 28),
        "07/01/2009 - 09/14/2009": datetime.datetime(2009, 7, 1),
        "05/25/2009 - 06/30/2009": datetime.datetime(2009, 5, 25),
        "04/01/2009 - 09/30/2009": datetime.datetime(2009, 4, 1),
        "05/30/2009 - 06/13/2009": datetime.datetime(2009, 5, 30),
        "05/31/2009 - 10/31/2009": datetime.datetime(2009, 5, 31),
        "04/20/2009 - 07/15/2009": datetime.datetime(2009, 4, 20),
        "01/30/2009 - 02/13/2009": datetime.datetime(2009, 1, 30),
        "01/14/2011 - 04/01/2011": datetime.datetime(2011, 1, 14),
        "11/21/2010 - 03/15/2011": datetime.datetime(2010, 11, 21),
        "11/12/2010 - 05/15/2011": datetime.datetime(2010, 11, 12),
        "10/30/2010 +/-": datetime.datetime(2010, 10, 30),
        "07/02/2010 - 12/17/2010": datetime.datetime(2010, 7, 2),
        "02/03/2010 - 02/17/2010": datetime.datetime(2010, 2, 3),
        "03/27/2010 - 04/16/2010": datetime.datetime(2010, 3, 27),
        "02/05/2010 - 03/12/2010": datetime.datetime(2010, 2, 5),
        "03/12/2010 - 04/15/2010": datetime.datetime(2010, 3, 12),
        "03/06/2010 - 07/01/2010": datetime.datetime(2010, 3, 6),
        "02/03/2012 - 07/13/2012": datetime.datetime(2012, 2, 3),
        "01/20/2012 - 06/30/2012": datetime.datetime(2012, 1, 20),
        "12/23/2011 - 01/31/2012": datetime.datetime(2011, 12, 23),
        "10/01/2011            11/30/2011      12/31/2011": datetime.datetime(
            2011, 10, 1
        ),
        "05/20/2011 - 07/15/2011": datetime.datetime(2011, 5, 20),
        "05/02/2011 - 12/31/2011": datetime.datetime(2011, 5, 2),
        "06/10/2011 - 09/30/2011": datetime.datetime(2011, 6, 10),
        "See WARN": None,
        "02/04/2013, +14 days after": datetime.datetime(2013, 2, 4),
        "45 days, ending 01/28/2013": datetime.datetime(2012, 12, 14),
        "12/31/2012 - 01/14/2013": datetime.datetime(2012, 12, 31),
        "12/28/2012 +/- to ?": datetime.datetime(2012, 12, 28),
        "12/28/2012, or with 2 weeks after.": datetime.datetime(2012, 12, 28),
        "On or before 10/31/2012": datetime.datetime(2012, 10, 31),
        "Within 14 days of 11/12/2012": datetime.datetime(2012, 11, 12),
        "10/31/2012 - 11/13/2012": datetime.datetime(2012, 10, 31),
        "08/31/2012 - 12/31/2012": datetime.datetime(2012, 8, 31),
        "On or before 10/22/2012": datetime.datetime(2012, 10, 22),
        "08/20/2012 - 03/31/2013": datetime.datetime(2012, 8, 20),
        "08/20/2012 & 08/31/2012": datetime.datetime(2012, 8, 20),
        "Mid August 2012 - 12/2013": None,
        "08/20/2012 - 12/31/2013": datetime.datetime(2012, 8, 20),
        "06/16/2012 - 07/13/2012": datetime.datetime(2012, 6, 16),
        "07/20/2012 - late 2013": datetime.datetime(2012, 7, 20),
        "08/07/2012  or within 14 days": datetime.datetime(2012, 8, 7),
        "08/07/2012 or with 2 weeks": datetime.datetime(2012, 8, 7),
        "06/08/2012 - 06/29/2012": datetime.datetime(2012, 6, 8),
        "08/04/2012 - 08/18/2012": datetime.datetime(2012, 8, 4),
        "05/18/2012 - 12/31/2012": datetime.datetime(2012, 5, 18),
        "06/05/2012 - 07/15/2012": datetime.datetime(2012, 6, 5),
        "07/01/2012 - 08/15/2012": datetime.datetime(2012, 7, 1),
        "06/19/2012 - 07/03/2012": datetime.datetime(2012, 6, 19),
        "03/30/2012 - 04/27/2012": datetime.datetime(2012, 3, 30),
        "03/22/2012 +/-": datetime.datetime(2012, 3, 22),
        "03/19/2012 - 04/01/2012 ": datetime.datetime(2019, 3, 19),
        "03/12/2012 - 03/19/2012": datetime.datetime(2012, 3, 12),
        "14th - 28th of February 2014": datetime.datetime(2014, 2, 14),
        "03/31/2014, or during the 14-day period (ending 04/14/2014)": datetime.datetime(
            2014, 3, 31
        ),
        "01/21/2014 - 01/31/2014": datetime.datetime(2014, 1, 21),
        "01/31/2014, or the 14 days period preceeding 01/31/2014": datetime.datetime(
            2014, 1, 31
        ),
        "12/20/2013, or during 14 day period (ending 01/03/2014)": datetime.datetime(
            2013, 12, 20
        ),
        "Decemeber of 2013": datetime.datetime(2013, 12, 1),
        "11/29/2013 - 12/12/2013": datetime.datetime(2013, 11, 29),
        "08/31/2013 - 10/31/2013": datetime.datetime(2013, 8, 31),
        "14th - 25th of October 2013": datetime.datetime(2013, 10, 14),
        "09/27/2013 - 12/27/2013": datetime.datetime(2013, 9, 27),
        "August or September of 2013": None,
        "08/08/2013 - 12/31/2013": datetime.datetime(2013, 8, 8),
        "08/23/2013 - 10/25/2013": datetime.datetime(2013, 8, 23),
        "14-day period following 08/06/2013": datetime.datetime(2013, 8, 6),
        "08/05/2013 - 08/13/2013": datetime.datetime(2013, 8, 5),
        "07/03/2013 - 07/02/2014": datetime.datetime(2013, 7, 3),
        "07/05/2013 - 12/31/2013": datetime.datetime(2013, 7, 5),
        "02/04/2013 - 07/05/2013": datetime.datetime(2013, 2, 4),
        "08/06/2013 - 08/20/2013": datetime.datetime(2013, 8, 6),
        "07/01/2013 - 09/01/2013": datetime.datetime(2013, 7, 1),
        "50/01/2013 - 10/25/2013": None,
        "05/03/2013 - 06/15/2013": datetime.datetime(2013, 5, 3),
        "02/04/2013 - 05/05/2013": datetime.datetime(2013, 2, 4),
        "On or around 03/08/2013": datetime.datetime(2013, 3, 8),
        "03/05/2013 or within the 2-week period afterward": datetime.datetime(
            2013, 3, 5
        ),
        "07/29/2014 thru 09/30/2014": datetime.datetime(2014, 7, 29),
        "Beginning 07/28/2014": datetime.datetime(2014, 7, 28),
        "Beginning 08/22/2014": datetime.datetime(2014, 8, 22),
        "On or shortly after August 18, 2014": datetime.datetime(2014, 8, 18),
        "Between June 30, 2014 and July 11, 2014": datetime.datetime(2014, 6, 30),
        "September 19, 2014, or within the 14-day period after that date": datetime.datetime(
            2014, 9, 19
        ),
        "September 29, 2014, through October 12, 2014": datetime.datetime(2014, 9, 29),
        "Q4, 2014 and are expected to end in Q2, 2015": None,
        "21 jobs beginning December 31, 2014,  See WARN": datetime.datetime(
            2014, 12, 31
        ),
        "September 19, 2014/See WARN": datetime.datetime(2014, 9, 19),
        "On or about January 31, 2015": datetime.datetime(2015, 1, 31),
        "04/03/2015 and  06/30/2015": datetime.datetime(2015, 4, 3),
        " 04/05/2015 ": datetime.datetime(2015, 4, 5),
        "07/31/2015 and 10/30/2015": datetime.datetime(2015, 7, 31),
        "See WARN ": None,
        "03/19/2012 - 04/01/2012": datetime.datetime(2012, 3, 19),
        "2041-06-04 00:00:00": datetime.datetime(2014, 6, 4),
        "04/05/2015": datetime.datetime(2015, 4, 5),
    }
    jobs_corrections = {
        "?": None,
        "N/A": None,
        "See W.A.R.N.": None,
        "74 fulltime and 184 parttime": 74,
        "Reduction from 13 to 1": 12,
        "See WARN": None,
        "in WARN": None,
        "Unknown": None,
        "TBD": None,
        "00:00:00": None,
        "": None,
        "1900-04-08 00:00:00": 99,
        "1901-03-02 00:00:00": 427,
        "1900-04-28 00:00:00": 119,
        "1900-03-28 00:00:00": 88,
        "1900-01-13 00:00:00": 14,
        "1900-02-03 00:00:00": 35,
        "1900-03-01 00:00:00": 61,
        "1900-01-12 00:00:00": 13,
        "1900-08-04 00:00:00": 217,
        "1900-03-13 00:00:00": 73,
        "1900-03-08 00:00:00": 68,
        "1900-04-20 00:00:00": 111,
        "1900-02-23 00:00:00": 55,
        "1900-02-25 00:00:00": 57,
        "1900-11-04 00:00:00": 309,
        "1900-05-06 00:00:00": 127,
        "1900-03-16 00:00:00": 76,
        "1900-04-14 00:00:00": 105,
        "1900-03-22 00:00:00": 82,
        "1900-01-11 00:00:00": 12,
        "1900-01-09 00:00:00": 10,
        "1900-03-03 00:00:00": 63,
        "1900-02-05 00:00:00": 37,
        "1900-03-10 00:00:00": 70,
        "1900-03-02 00:00:00": 62,
        "1900-01-01 00:00:00": 2,
        "1900-03-28 00:00:00": 88,
        "167 -                  197": 167,
        "200 -": 200,
        "79                   10": 89,
        "75 - 100": 75,
        "110 - 145": 110,
        "350 - 756": 350,
        "85 - 90": 85,
        "90 -": 90,
        "290 - 356": 290,
        "200 - 290": 200,
        "48 - 50": 48,
        "250 - 300": 250,
        "118 - 120": 118,
        "154 -": 154,
        "49 -": 49,
        "183 -": 183,
        "450 -": 450,
        "114 -": 114,
        "50 -": 50,
        "220 -": 220,
        "89 -": 89,
        "3 -": 3,
        "121 -": 121,
        "55 -": 55,
        "48 -": 48,
        "316 -": 316,
        "140 -": 140,
        "60 -": 60,
        "150 -": 150,
        "124 -": 124,
        "75 -": 75,
        "157 -": 157,
        "90 -": 90,
        "163 -": 163,
        "156 -": 156,
        "177 -": 177,
        "47                 30": 77,
        "71 -": 71,
        "Â Â  Â Â 124": 124,
        "Â\xa0Â\xa0 Â\xa0Â\xa0124": 124,
    }

    def transform_jobs(self, value: str) -> typing.Optional[int]:
        """Transform a raw jobs number into an integer.

        Args:
            value (str): A raw jobs number provided by the source

        Returns: An integer number ready for consolidation. Or, if the value is invalid, a None.
        """
        value = value.split("-")[0].strip()
        value = value.replace("+/-", "")
        value = value.replace("+/", "").strip()
        value = value.replace("+", "").strip()
        value = re.split(" {5,}", value)[0].strip()
        return super().transform_jobs(value)

    def check_if_closure(self, row: typing.Dict) -> typing.Optional[bool]:
        """Determine whether a row is a closure or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean or null
        """
        if "closure" in row["Closure or Layoff?"].lower():
            return True
        else:
            return None
