# Input: files in exports/ directory
# Output: a single CSV that merges all states

# For each state, it should map a subset of fields to some minimal set of standardized fields
# (e.g. Company Name -> employer, Number of Employees Affected -> number_affected, etc.).
# Something to consider: we may want to model a wider range of standardized field names on the approach used by https://layoffdata.com/data/
# to consider: Union (yes, no), Temporary/permanent, Layoff_type (closure, layoff), region, county
import csv
import os

from pathlib import Path

from utils import write_dict_rows_to_csv

USER_HOME = os.path.expanduser('~')
DEFAULT_HOME = str(Path(USER_HOME, '.warn-scraper'))
ETL_DIR = os.environ.get('WARN_ETL_DIR', DEFAULT_HOME)
WARN_DATA_PATH = str(Path(ETL_DIR, 'exports'))
WARN_ANALYSIS_PATH = str(Path(ETL_DIR, 'analysis'))
OUTPUT_DIR = WARN_ANALYSIS_PATH

# standardize formatting of our field name lists so we can write pretty
# normalize case, remove underscores, strip spaces
def format_list(list):
    return [x.lower().replace(" ", "").replace("_", "") for x in list]


# standardize_header() is coded based on the order of this list
STANDARDIZED_FIELD_NAMES = ['state', 'employer', 'number_affected', 'date_received', 'date_effective', 'location', 'industry', 'notes']
# Replace these field names
EMPLOYER_FIELDS = format_list(['company name', 'company', 'Organization Name'])
NUMBER_AFFECTED_FIELDS = format_list(['employees affected', 'affected empoyees', 'employees', 'workforce affected', 'planned#affectedemployees', 'Number toEmployees Affected', '# of workers', 'AffectedWorkers'])
DATE_RECEIVED_FIELDS = format_list(['initial report date', 'notice date', 'state notification date', 'warn date'])
DATE_EFFECTIVE_FIELDS = format_list(['layoff date', 'LayoffBeginDate', 'layoff start date', 'effective date', 'planned starting date','effective layoff date','LO/CL date', 'impact date'])
INDUSTRY_FIELDS = format_list(['industry','description of work','NAICSDescription','NAICS'])
LOCATION_FIELDS = format_list(['city', 'address', 'location', 'company address', 'company address - 2','city/town', 'zip', 'location city', 'region', 'county'])  # TODO what do we want our city/address approach to look like?
NOTES_FIELDS = format_list(['notes', 'misc'])
# CLOSING_OR_LAYOFF_FIELDS = format_list(['Notice Type', 'Code Type', 'Closure Layoff'])
AMBIGUOUS_FIELDS = format_list(['date'])  # require state-by-state approach

def main():
    output_csv = '{}/standardize_field_names.csv'.format(OUTPUT_DIR)
    # we will put our dict rows here
    output_rows = []
    # open each state's output file from exports/ directory.
    for filename in os.listdir(WARN_DATA_PATH):
        print(f'Processing state {filename}...')
        with open(f"{WARN_DATA_PATH}\\{filename}", newline='') as f:
            state_rows = []
            state_csv = csv.reader(f)
            state_postal = filename.split(".")[0].upper()
            # store state's rows
            for row_idx, row in enumerate(state_csv):
                if row_idx == 0:
                    # standardize fields in the header!
                    row = standardize_header(row, STANDARDIZED_FIELD_NAMES, state_postal)
                else:
                    row.append(state_postal)  # store 'state' field in body
                state_rows.append(row)

        state_fields = state_rows[0]
        state_rows = state_rows[1:]
        # transfer individual state data to standardized dict list
        state_rows_as_dicts = [dict(zip(state_fields, row)) for row in state_rows]
        output_rows.extend(state_rows_as_dicts)
    # once output_rows is full of all states, generate the final csv
    write_dict_rows_to_csv(output_csv, STANDARDIZED_FIELD_NAMES, output_rows)
    print(f"standardized_field_names.csv generated successfully.")


# replace field names in-place with standardized versions
def standardize_header(header_row, FIELD, state):
    # add 'state' field to header
    header_row.append(FIELD[0])
    for field_idx, field_name in enumerate(header_row):
        field_name = field_name.lower().replace(" ", "")  # standardize strings to lowercase and no whitespace
        if field_name in EMPLOYER_FIELDS:
            field_name = FIELD[1]
        elif field_name in NUMBER_AFFECTED_FIELDS:
            field_name = FIELD[2]
        elif field_name in DATE_RECEIVED_FIELDS:
            field_name = FIELD[3]
        elif field_name in DATE_EFFECTIVE_FIELDS:
            field_name = FIELD[4]
        elif field_name in LOCATION_FIELDS:
            field_name = FIELD[5]
        elif field_name in INDUSTRY_FIELDS:
            field_name = FIELD[6]
        elif field_name in NOTES_FIELDS:
            field_name = FIELD[7]
        elif field_name in AMBIGUOUS_FIELDS:  # determine per-state
            if state == "sd":
                if field_name == "date":
                    # TODO check and report on SD date field
                    # field_name = FIELD[3]
                    pass
        elif field_name == 'state':
            # we created this field, no standardization necessary
            pass
        else:
            print(f"Unhandled field {field_name} in {state}.csv")
        header_row[field_idx] = field_name
    return header_row


if __name__ == '__main__':
    main()
