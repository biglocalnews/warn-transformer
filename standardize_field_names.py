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
INPUT_DIR = WARN_DATA_PATH
WARN_ANALYSIS_PATH = str(Path(ETL_DIR, 'analysis'))
OUTPUT_DIR = WARN_ANALYSIS_PATH

# standardize formatting of our field map lists so we can write pretty
# remove spaces, normalize case, remove underscores
def format_str(str):
    return str.lower().replace(" ", "").replace("_", "")


def format_list(list):
    return [format_str(x) for x in list]


# Let's make a list of the fields we want each state to map onto:
# note that the order of this list is sensitive to standardize_header() func
STANDARDIZED_FIELD_NAMES = ['state', 'employer', 'number_affected', 'date_received', 'date_effective', 'location', 'industry', 'notes', 'layoff_type']
# Replace these field names with standardize field names
EMPLOYER_MAP = format_list(['company name', 'company', 'Organization Name', 'employer'])
NUMBER_AFFECTED_MAP = format_list(['employees affected', 'affected empoyees', 'employees', 'workforce affected', 'planned#affectedemployees', 'Number toEmployees Affected', '# of workers', 'AffectedWorkers', '# Affected', 'number_of_employees_affected'])
DATE_RECEIVED_MAP = format_list(['initial report date', 'notice_date', 'notice date', 'state notification date', 'warn date', 'date received'])
DATE_EFFECTIVE_MAP = format_list(['layoff date', 'LayoffBeginDate', 'layoff start date', 'effective date', 'planned starting date', 'effective layoff date', 'LO/CL date', 'impact date'])
INDUSTRY_MAP = format_list(['industry', 'description of work', 'NAICSDescription'])
LOCATION_MAP = format_list(['city', 'address', 'location', 'company address', 'company address - 2', 'city/town', 'zip', 'location city', 'region', 'county', 'lwib_area'])  # TODO make sure that multiple maps results in appending
NOTES_MAP = format_list(['notes', 'misc'])
LAYOFF_TYPE_MAP = format_list(['Type', 'Notice Type', 'Code Type', 'Closure Layoff'])
AMBIGUOUS_MAP = format_list(['date'])  # require state-by-state approach

def main():
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    output_csv = '{}/standardize_field_names.csv'.format(OUTPUT_DIR)
    # we will put our dict rows here
    output_rows = []
    # open each state's output file from exports/ directory.
    for filename in os.listdir(INPUT_DIR):
        print(f'Processing state {filename}...')
        source_file = str(Path(INPUT_DIR).joinpath(filename))
        with open(source_file, newline='') as f:  # , encoding='utf-8'
            state_rows = []
            state_csv = csv.reader(f)
            state_postal = filename.split(".")[0].upper()
            # store state's rows
            for row_idx, row in enumerate(state_csv):
                # ignore blank rows
                if row:
                    if row_idx == 0:
                        # standardize fields in the header!
                        row = standardize_header(row, STANDARDIZED_FIELD_NAMES, state_postal)
                    else:
                        row.append(state_postal)  # store 'state' field in body
                    state_rows.append(row)

        # run state-specific standardizations like column-merging
        state_rows = standardize_state(state_rows, state_postal)
        ''' 
        transfer the current state's data to standardized dict list state_rows_as_dicts
        eg. state_rows_as_dicts = [
            { "company": "ABC Wood Systems", "WARN date": 12/01/1999, "Employees Affected": 56, },
            { "company": "Wood Emporium", "WARN date": 12/02/1999, "Employees Affected": 7 },
             ...
            ]
        '''
        state_rows_header = state_rows[0]
        state_rows_body = state_rows[1:]
        state_rows_as_dicts = [dict(zip(state_rows_header, row)) for row in state_rows_body]
        output_rows.extend(state_rows_as_dicts)
    # once output_rows is full of all states, generate the final csv
    write_dict_rows_to_csv(output_csv, STANDARDIZED_FIELD_NAMES, output_rows)
    print(f"standardized_field_names.csv generated successfully.")


# replace field names in-place with standardized versions
def standardize_header(header_row, FIELD, state):
    # add 'state' field to header
    header_row.append(FIELD[0])
    for field_idx, field_name in enumerate(header_row):
        field_name = format_str(field_name)  # standardize strings to lowercase and no whitespace
        if field_name in EMPLOYER_MAP:
            field_name = FIELD[1]
        elif field_name in NUMBER_AFFECTED_MAP:
            field_name = FIELD[2]
        elif field_name in DATE_RECEIVED_MAP:
            field_name = FIELD[3]
        elif field_name in DATE_EFFECTIVE_MAP:
            field_name = FIELD[4]
        elif field_name in LOCATION_MAP:
            field_name = FIELD[5]
        elif field_name in INDUSTRY_MAP:
            field_name = FIELD[6]
        elif field_name in NOTES_MAP:
            field_name = FIELD[7]
        elif field_name in LAYOFF_TYPE_MAP:
            field_name = FIELD[8]
        elif field_name in AMBIGUOUS_MAP:  # determine per-state
            if state == "sd":
                if field_name == "date":
                    # TODO check and report on SD date field
                    # field_name = FIELD[3]
                    pass
        elif field_name == 'state':
            # we created this field, no standardization necessary
            pass
        else:
            # make no changes to undesired field
            print(f"Unhandled field {field_name} in {state}.csv")
        header_row[field_idx] = field_name
    return header_row

# input/output: a list of state rows (including header)
def standardize_state(state_rows, state):
    # TODO re-implement, maybe import from separate file
    # if state == 'VA':
    #     return standardize_VA(state_rows)
    # else:
        # some states don't need any standardization
    return state_rows


# additively merge "closure" and "Layoff" columns into "layoff type" column:
#   "closure: Yes", "Layoff: No" => "Layoff Type: Closure"
# input/output: list of state's rows including header
def standardize_VA(state_rows, state="VA"):
    # add field
    state_rows[0].append("Layoff Type")
    for row_idx, row in enumerate(state_rows):
        if not row_idx == 0:
            # extract data
            closure = format_str(row[14]) == 'yes'
            layoff = format_str(row[15]) == 'yes'
            layoff_type = ''
            if not closure and not layoff:
                layoff_type = 'None'
            elif not closure and layoff:
                layoff_type = 'Layoff'
            elif closure and not layoff:
                layoff_type = 'Closure'
            else:
                layoff_type = 'Both'
            row.append(layoff_type)
    return state_rows


if __name__ == '__main__':
    main()
