# TODO CT missing employers/employees

# Input: state .csv files in .warn-scraper/exports/ directory
# Output: a single CSV in .warn-scraper/analysis/ directory that merges all states

# For each state, it should map a subset of fields to some minimal set of standardized fields
# (e.g. Company Name -> employer, Number of Employees Affected -> number_affected, etc.).
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


# remove spaces, normalize case, remove underscores
def format_str(str):
    return str.lower().replace(" ", "").replace("_", "")


# standardize formatting of our field map lists so we can write pretty
def format_list(list):
    return [format_str(x) for x in list]


# Let's make a list of the fields we want each state to map onto:
# note that the order of this list is sensitive to standardize_header() func
STANDARDIZED_FIELD_NAMES = ['state', 'employer', 'number_affected', 'date_received_raw', 'date_effective_raw', 'location', 'industry', 'notes', 'layoff_type']
# Replace these field names with standardize field names
EMPLOYER_MAP = format_list(['employer', 'company name', 'company', 'Organization Name', 'affected company'])
NUMBER_AFFECTED_MAP = format_list(['number affected', 'employees affected', 'affected empoyees', 'employees', 'workforce affected', 'planned#affectedemployees', 'Number toEmployees Affected', '# of workers', 'AffectedWorkers', '# Affected', 'number_of_employees_affected', 'jobs affected', 'total employees', 'number workers'])
DATE_RECEIVED_MAP = format_list(['date received', 'initial report date', 'date of notice', 'notice date', 'state notification date', 'warn date', 'noticercvd', 'received date'])
DATE_EFFECTIVE_MAP = format_list(['date effective', 'layoff date', 'closing date', 'LayoffBeginDate', 'layoff start date', 'effective date', 'planned starting date', 'effective layoff date', 'LO/CL date', 'impact date', 'typeoflayoff'])
INDUSTRY_MAP = format_list(['industry', 'description of work', 'NAICSDescription'])
# TODO make sure that having multiple columns that map to the same column results in appending not replacing
LOCATION_MAP = format_list(['location', 'city', 'address', 'zip', 'location city', 'region', 'county', 'lwib_area', 'location of layoffs', 'layoff location'])  # removed from VA: , 'company address', 'company address - 2', 'city/town',
NOTES_MAP = format_list(['notes', 'misc'])
LAYOFF_TYPE_MAP = format_list(['layoff type', 'Type', 'Notice Type', 'Code Type', 'Closure Layoff', 'type code', 'warn type'])
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
        state_postal = filename.split(".")[0].upper()
        # process_file converts csv to list-of-rows, while also
        # replacing idiosyncratic headers w standardized counterparts!
        try:
            state_rows = process_file(source_file, filename, state_postal)
        except UnicodeDecodeError:
            state_rows = process_file(source_file, filename, state_postal, encoding="utf-8")

        # smooth out lengths of rows and columns to prevent data errors
        state_rows = standardize_rows_columns(state_rows, state_postal)
        state_rows = add_state_field(state_rows, STANDARDIZED_FIELD_NAMES, state_postal)
        # run state-specific standardizations such as data cleaning, restructuring
        state_rows = standardize_state(state_rows, state_postal)
        # convert data to a list of dicts, and merge redundant columns non-destructively
        state_rows_as_dicts = merge_to_dict(state_rows)
        output_rows.extend(state_rows_as_dicts)
    # once output_rows full of all states' rows of dicts, generate the final csv
    # extrasaction='ignore' flag keeps only fields mapped to STANDARDIZED_FIELD_NAMES
    write_dict_rows_to_csv(output_csv, STANDARDIZED_FIELD_NAMES, output_rows, extrasaction='ignore')
    print(f"standardized_field_names.csv generated successfully.")


# return state_rows list of lists
def process_file(source_file, filename, state_postal, encoding=""):
    kwargs = {"newline": "", }
    # work-around for encoding differences between states
    if encoding:
        kwargs["encoding"] = encoding
    with open(source_file, **kwargs) as f:
        state_rows = []
        state_csv = csv.reader(f)
        # store state's rows
        for row_idx, row in enumerate(state_csv):
            # ignore blank rows
            if row:
                if row_idx == 0:
                    # standardize fields in the header!
                    row = standardize_header(row, STANDARDIZED_FIELD_NAMES, state_postal)
                # add row to the list
                state_rows.append(row)
    return state_rows

# replace field names in-place with standardized versions
def standardize_header(header_row, FIELD, state):
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
        else:
            # make no changes to other fields
            print(f"Info: Unhandled field {field_name} in {state}.csv")
        # replace the field
        header_row[field_idx] = field_name
    return header_row


# match row length with header length
# input: list of state rows
# output: same, but with headers and fields added to even out data symmetry
def standardize_rows_columns(state_rows, state):
    state_rows_header = state_rows[0]
    state_rows_body = state_rows[1:]
    # make sure all columns with data have a column header
    for row_idx, row in enumerate(state_rows_body):
        while len(state_rows_header) < len(row):
            print(f"Info: Found more values than headers in {state}.csv, line {row_idx}. Adding header for unknown field...")
            field_identifier = len(state_rows_body[0]) - len(state_rows_header)
            # adds column header so the state can be processed w/o error
            state_rows_header.append(f"UnknownField{field_identifier}")
    # make sure all fields with a column header have enough fields of data
    for row_idx, row in enumerate(state_rows_body):
        while len(row) < len(state_rows_header):
            print(f"Info: Found more headers than fields in {state}.csv, line {row_idx}. Adding blank string to field...")
            row.append('')
    return state_rows

# this step is the counterpart of the step above;
#
# input/output: state rows list
def add_state_field(state_rows, FIELD, state):
    # add 'state' field to header
    state_rows[0].append(FIELD[0])
    for row in state_rows:
        row.append(state)  # store 'state' field in body
    return state_rows

# run state-specific processing
# input/output: a list of state rows (including header)
def standardize_state(state_rows, state):
    if state == 'VA':
        return standardize_VA(state_rows)
    elif state == 'CT':
        # im going to put some comments here about a state we might eventually want to alter our strategy for
        # for CT, the mapping merges columns "closing date" and "layoff date" into the "date effective column".
        # CT has a pretty weird system where the dates are the same for the most part but sometimes they're not;
        # in those cases, you'll have two dates listed under date_effective and there's no explanation in the data.
        # we might want to create a new column for data to map to, in case this data is considered substatial or worthwhile.
        # would require some looking into, maybe speaking with CT about it.
        pass
    else:
        pass
    return state_rows


# the goal of this function is to merge columns non-destructively while converting to dict
# (e.g, if two source columns map to 'location', let's combine them for maximum fidelity)
# input: a list of rows
# output: a list of dicts
def merge_to_dict(state_rows):
    '''
    transfer the current state's data to dict list, preserving unwanted fields
    eg. state_rows_as_dicts = [
        { "company": "ABC Wood Systems", "SomeUnwantedField" : "(123) 456-7890", "OtherUnwantedField": "...", ...},
         ...
        ]
    '''
    state_rows_header = state_rows[0]
    state_rows_body = state_rows[1:]
    # tuples: {('employer', {'ABC business', 'GFE corp', ...}), ('location', {'XYZ town', 'YHG city'}), ... }
    state_rows_as_tuples = [list(zip(state_rows_header, row)) for row in state_rows_body]
    # build a list of dicts with non-destructive column merging
    state_rows_as_dicts = []
    for row in state_rows_as_tuples:
        newdict = dict()
        for col in row:
            key = col[0]
            val = col[1]
            if newdict.get(key):
                # merge repeating columns
                # strategy: combine into one column, insert newline between
                if val is "":
                    val = f"{newdict.get(key)}"  # prettier formatting
                else:
                    val += f"{os.linesep}{newdict.get(key)}"
            newdict.update({key: val})
        state_rows_as_dicts.append(newdict)
    return state_rows_as_dicts


# input/output: list of state's rows including header
def standardize_VA(state_rows, state="VA"):
    # additively merge "closure" and "Layoff" columns into "layoff type" column:
    #   "closure: Yes", "Layoff: No" => "Layoff Type: Closure"
    state_rows[0].append("Layoff Type")  # add field
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
            # add value for Layoff Type field
            row.append(layoff_type)
    return state_rows


if __name__ == '__main__':
    main()
