import csv
import hashlib
import json
import logging
import typing
from datetime import datetime, timedelta
from pathlib import Path

from marshmallow import Schema, fields

logger = logging.getLogger(__name__)


class WarnNoticeSchema(Schema):
    """An standardized instance of a WARN Act Notice."""

    hash_id = fields.Str(required=True)
    postal_code = fields.Str(max_length=2, required=True)
    company = fields.Str(required=True)
    location = fields.Str(required=True, allow_none=True)
    notice_date = fields.Date(required=True, allow_none=True)
    effective_date = fields.Date(required=True, allow_none=True)
    jobs = fields.Int(required=True, allow_none=True)
    is_temporary = fields.Boolean(required=True, allow_none=True, default=None)
    is_closure = fields.Boolean(required=True, allow_none=True, default=None)
    is_amendment = fields.Boolean(required=True, default=False)


class BaseTransformer:
    """Transform a state's raw data for consolidation."""

    schema = WarnNoticeSchema

    # The base attributes that need to be defined on all subclasses.
    postal_code: str = "xx"
    fields: typing.Dict = dict()

    # The default date format. It will need to be customized by source.
    date_format: typing.Any = "%m/%d/%Y"
    # Manual date corrections for malformed data
    date_corrections: typing.Dict = {}
    # How many days in the future are allowed
    max_future_days: int = 365
    # The minimum year allowed
    minimum_year: int = 1988

    # Manual jobs corrections for malformed data
    jobs_corrections: typing.Dict = {}
    # The max jobs we allow without throwing an error
    maximum_jobs: int = 10000

    def __init__(self, input_dir: Path):
        """Intialize a new instance.

        Args:
            input_dir (Path): A directory where our raw data is stored
        """
        self.input_dir = input_dir
        self.raw_data = self.get_raw_data()

    def get_raw_data(self) -> typing.List[typing.Dict]:
        """Get the raw data from our scraper for this source.

        Returns: A list of raw rows of data from the source.
        """
        # Get downloaded file
        raw_path = self.input_dir / f"{self.postal_code.lower()}.csv"
        # Open the csv
        with open(raw_path) as fh:
            reader = csv.DictReader(fh)
            # Return it as a list
            return list(reader)

    def transform(self) -> typing.List[typing.Dict]:
        """Transform prepared rows into a form that's ready for consolidation.

        Returns: A validated list of dictionaries that conform to our schema
        """
        logger.debug(f"Transforming {self.postal_code}")

        # Prep the row list for transformation
        row_list = self.prep_row_list(self.raw_data)

        # Transform the row list into dicts that are ready to be submitted for validation
        transformed_list = [self.transform_row(r) for r in row_list]

        # Validate each row against our schema
        validated_list = [self.schema().load(r) for r in transformed_list]

        # Deal with amendments
        amended_list = self.handle_amendments(validated_list)

        # Return the result, which should be ready for consolidation
        return amended_list

    def prep_row_list(
        self, row_list: typing.List[typing.Dict]
    ) -> typing.List[typing.Dict]:
        """Make necessary transformations to the raw row list prior to transformation.

        Args:
            row_list (list): A list of raw rows of data from the source.

        Returns: The row list minus empty records
        """
        prepped_list = []
        for row in row_list:
            # Skip empty rows
            try:
                # A list with only empty cells will throw an error
                next(v for v in row.values() if v.strip())
            except StopIteration:
                continue
            prepped_list.append(row)
        return prepped_list

    def transform_row(self, row: typing.Dict) -> typing.Dict:
        """Transform a row into a form that's ready for consolidation.

        Args:
            row (dict): One raw row of data from the source

        Returns: A transformed dict that's ready to be loaded into our consolidated schema.
        """
        # Parse the fields we expect in every transformer
        data = dict(
            postal_code=self.postal_code.upper(),
            company=self.transform_company(
                self.get_raw_value(row, self.fields["company"])
            ),
            location=self.transform_location(
                self.get_raw_value(row, self.fields["location"])
            ),
            jobs=self.transform_jobs(self.get_raw_value(row, self.fields["jobs"])),
            is_temporary=self.check_if_temporary(row),
            is_closure=self.check_if_closure(row),
            is_amendment=self.check_if_amendment(row),
        )

        # Add optional date fields
        if "notice_date" in self.fields:
            data["notice_date"] = self.transform_date(
                self.get_raw_value(row, self.fields["notice_date"])
            )
        else:
            data["notice_date"] = None

        if "effective_date" in self.fields:
            data["effective_date"] = self.transform_date(
                self.get_raw_value(row, self.fields["effective_date"])
            )
        else:
            data["effective_date"] = None

        # Stamp record with a unique ID
        data["hash_id"] = self.get_hash_id(data)

        # Return the results
        return data

    def get_raw_value(self, row, method):
        """Fetch a value from the row that for transformation.

        Args:
            row: One raw row of data from the source
            method: The technique to use to pull data.
                If a strong method is provided,
                it is used to fetch a key of that name from the row. If a callable function is provided, the row is run through it.

        Returns: A value ready for transformation.
        """
        # If a string is provided, pull it from the row dict.
        if isinstance(method, str):
            return row[method]
        # If a function is provided, run the row through it.
        elif isinstance(method, typing.Callable):
            return method(row)
        else:
            raise ValueError("The field method your provided is not valid.")

    def get_hash_id(self, data: typing.Dict) -> str:
        """Convert the row into a unique hexdigest to use as a unique identifier.

        Args:
            data (dict): One raw row of data from the source

        Returns: A unique hexdigest string computed from the source data.
        """
        dict_string = json.dumps(data)
        hash_obj = hashlib.sha224(dict_string.encode("utf-8"))
        return hash_obj.hexdigest()

    def transform_company(self, value: str) -> str:
        """Transform a raw company name.

        Args:
            value (str): The raw company string provided by the source

        Returns: A string object ready for consolidation.
        """
        return value.strip()

    def transform_location(self, value: str) -> str:
        """Transform a raw location.

        Args:
            value (str): The raw location string provided by the source

        Returns: A string object ready for consolidation.
        """
        return value.strip()

    def transform_date(self, value: str) -> typing.Optional[str]:
        """Transform a raw date string into a date object.

        Args:
            value (str): The raw date string provided by the source

        Returns: A date object ready for consolidation. Or, if the date string is invalid, a None.
        """
        # Clean up the string
        value = value.strip()

        # If there's nothing to convert, return None
        if not value:
            return None

        # The result, whene we find it
        dt: typing.Any = None

        # If there's only one date_format, try that
        if isinstance(self.date_format, str):
            try:
                dt = datetime.strptime(value, self.date_format)
            except ValueError:
                logger.debug(
                    f"{self.postal_code} - Could not parse '{value}'. Looking up correction"
                )
                dt = self.date_corrections[value]

        # If it's a list, try them one by one
        elif isinstance(self.date_format, (list, tuple)):
            for f in self.date_format:
                try:
                    dt = datetime.strptime(value, f)
                except ValueError:
                    continue
            # If there's nothing at the end of the loop, try the correction
            if not dt:
                logger.debug(
                    f"{self.postal_code} - Could not parse '{value}'. Looking up correction"
                )
                dt = self.date_corrections[value]

        # If the date parses as None, return that
        if dt is None:
            return None

        # Make sure we've got a date at this point
        assert dt is not None and isinstance(dt, datetime)

        # If the date is more than 365 days in future, fix it
        today = datetime.today()
        if dt > today + timedelta(days=self.max_future_days):
            logger.debug(
                f"{self.postal_code} - Date '{dt}' is more than {self.max_future_days} days in the future. Looking up correction"
            )
            dt = self.date_corrections[value]

        # If the date is below the minimum year, fix it
        if dt.year < self.minimum_year:
            logger.debug(
                f"{self.postal_code} - Year {dt.year} below minimum of {self.minimum_year}. Looking up correction"
            )
            dt = self.date_corrections[value]

        # If the date parses as None, return that
        if dt is None:
            return None

        # Make sure we've got a date at this point
        assert dt is not None and isinstance(dt, datetime)

        # If we have a datetime, return the result as a string
        return str(dt.date())

    def transform_jobs(self, value: str) -> typing.Optional[int]:
        """Transform a raw jobs number into an integer.

        Args:
            value (str): A raw jobs number provided by the source

        Returns: An integer number ready for consolidation. Or, if the value is invalid, a None.
        """
        # If there's nothing there, return None
        if not value:
            return None

        # Cut whitespace
        value = value.strip()

        # If there's nothing there, return None
        if not value:
            return None

        # Cut any commas
        value = value.replace(",", "")
        try:
            # Convert to integer
            clean_value = int(float(value))
        except ValueError:
            # If it won't convert, look for a manual correction
            logger.debug(
                f"{self.postal_code} - Could not parse '{value}'. Looking up correction"
            )
            clean_value = self.jobs_corrections[value]

        # If it's None, return it now
        if not clean_value:
            return clean_value

        # Now validate it
        if clean_value < 0:
            logger.debug(
                "{self.postal_code} - Jobs must be greater than 0. Looking up correction"
            )
            clean_value = self.jobs_corrections[clean_value]
        if clean_value > self.maximum_jobs:
            logger.debug(
                f"{self.postal_code} - Jobs greater than {self.maximum_jobs} are probably wrong. Looking up correction"
            )
            clean_value = self.jobs_corrections[clean_value]

        # Pass it out
        return clean_value

    def check_if_temporary(self, row: typing.Dict) -> typing.Optional[bool]:
        """Determine whether a row is a temporary or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean or null
        """
        return None

    def check_if_closure(self, row: typing.Dict) -> typing.Optional[bool]:
        """Determine whether a row is a closure or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean or null
        """
        return None

    def check_if_amendment(self, row: typing.Dict) -> bool:
        """Determine whether a row is an amendment or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean
        """
        return False

    def handle_amendments(
        self, row_list: typing.List[typing.Dict]
    ) -> typing.List[typing.Dict]:
        """Remove amended filings from the provided list of records.

        Args:
            row_list (list): A list of clean rows of data.

        Returns: A list of cleaned data, minus amended records.
        """
        amendments_count = len([r for r in row_list if r["is_amendment"] is True])
        if amendments_count == 0:
            logger.debug(f"No amendments in {self.postal_code}")
            return row_list
        raise NotImplementedError
