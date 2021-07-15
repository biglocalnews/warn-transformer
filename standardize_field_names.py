# Input: files in exports/ directory
# Output: a single CSV that merges all states

# For each state, it should map a subset of fields to some minimal set of standardized fields
# (e.g. Company Name -> employer, Number of Employees Affected -> number_affected, etc.).
# Something to consider: we may want to model a wider range of standardized field names on the approach used by https://layoffdata.com/data/
# to consider: Union (yes, no), Temporary/permanent, Layoff_type (closure, layoff), region, county
import csv
import logging
import os

from pathlib import Path

from warn.utils import write_dict_rows_to_csv

logger = logging.getLogger(__name__)

USER_HOME = os.path.expanduser('~')
DEFAULT_HOME = str(Path(USER_HOME, '.warn-scraper'))
ETL_DIR = os.environ.get('WARN_ETL_DIR', DEFAULT_HOME)
WARN_DATA_PATH = str(Path(ETL_DIR, 'exports'))
OUTPUT_DIR = DEFAULT_HOME

FIELD_NAMES = ['state', 'employer', 'number_affected', 'date_received']  # 'city', 'date_effective', 'industry'
# Replace these field names
EMPLOYER_FIELDS = ['company name', 'company']
NUMBER_AFFECTED_FIELDS = ['employees affected', 'affected empoyees', 'employees']
DATE_RECEIVED_FIELDS = ['initial report date', 'notice date', 'state notification date']
AMBIGUOUS_FIELDS = ['date']  # requires state-by-state approach
def standardize():
    output_csv = '{}/all_states_standardized.csv'.format(OUTPUT_DIR)
    # open each state's output file from exports/ directory.
    for filename in os.listdir(WARN_DATA_PATH):
        with open(f"{WARN_DATA_PATH}\\{filename}") as f:
            state_csv = csv.reader(f)
            state_header_row = state_csv[0]
            state_postal = filename.split(".")[0].upper()

            # store state's rows
            state_rows = []
            for row in state_csv:
                row.append(state_postal)  # store which state the row belongs to
                state_rows.append(row)
            # standardize fields in the header
            state_header_row = standardize_header(state_header_row, FIELD_NAMES, state_postal)
            state_rows[0] = state_header_row

    # Convert rows to dicts
    rows_as_dicts = [dict(zip(FIELD_NAMES, row)) for row in state_rows]
    # once output_rows is full of all states, generate the final csv
    write_dict_rows_to_csv(output_csv, FIELD_NAMES, rows_as_dicts)


# replace field names in-place with standardized versions
def standardize_header(header_row, FIELD_NAMES, state):
    header_row.append(FIELD_NAMES[0])  # add 'state' field
    for field_idx, field_name in enumerate(header_row):
        field_name = field_name.lower().strip()  # standardize string formatting
        if field_name in EMPLOYER_FIELDS:
            field_name = FIELD_NAMES[1]
        elif field_name in NUMBER_AFFECTED_FIELDS:
            field_name = FIELD_NAMES[2]
        elif field_name in DATE_RECEIVED_FIELDS:
            field_name = FIELD_NAMES[3]
        elif field_name in AMBIGUOUS_FIELDS:  # determine per-state
            if state == "sd":
                if field_name == "date":
                    # TODO check and report on SD date field
                    # field_name = FIELD_NAMES[3]
                    pass
        else:
            logger.debug(f"Unmodified field {field_name} in {state}.csv")
        header_row[field_idx] = field_name
    return header_row
