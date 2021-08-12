# Input: state .csv files in .warn-scraper/exports/ directory
# Output: a single CSV in .warn-scraper/analysis/ directory that merges all states

# For each state, it should map a subset of fields to some minimal set of standardized fields
# (e.g. Company Name -> employer, Number of Employees Affected -> number_affected, etc.).
import csv
import re
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


# remove spaces, normalize to lowercase, remove underscores
def format_str(str):
    return str.lower().replace(" ", "").replace("_", "")


# standardize formatting of our field map lists so we can write pretty
def format_list(list):
    return [format_str(x) for x in list]


# Let's make a list of the fields we want each state to map onto (case-, whitespace-, underscore-insensitive):
# NOTE: any alteration to the length/ order of this list should also check every instance of STANDARDIZED_FIELD_NAMES
STANDARDIZED_FIELD_NAMES = ['state', 'employer', 'number_affected', 'date_received_raw', 'date_layoff_raw', 'date_closure_raw', 'location', 'parent_location', 'industry', 'notes', 'layoff_type']
# Replace these field names with standardized field names
EMPLOYER_MAP = format_list(['employer', 'company name', 'company', 'Organization Name', 'affected company', 'name of company'])
NUMBER_AFFECTED_MAP = format_list(['number affected', 'employees affected', 'affected empoyees', 'employees', 'workforce affected', 'planned#affectedemployees', 'Number toEmployees Affected', '# of workers', 'AffectedWorkers', '# Affected', 'number_of_employees_affected', 'jobs affected', 'total employees', 'number workers'])
DATE_RECEIVED_MAP = format_list(['NoticeRcvd', 'date received', 'initial report date', 'date of notice', 'notice date', 'state notification date', 'warn date', 'noticercvd', 'received date'])
DATE_LAYOFF_MAP = format_list(['layoff date', 'layoff start date'])
DATE_CLOSURE_MAP = format_list(['closing date'])
INDUSTRY_MAP = format_list(['industry', 'description of work', 'NAICSDescription'])
LOCATION_MAP = format_list(['location', 'location city', 'region', 'county', 'city', 'address', 'zip', 'zipcode', 'lwib_area', 'location of layoffs', 'layoff location'])
PARENT_LOCATION_MAP = format_list(['company address', 'company address - 2', 'city/town'])
NOTES_MAP = format_list(['notes', 'misc'])
LAYOFF_TYPE_MAP = format_list(['layoff type', 'Type', 'Notice Type', 'Code Type', 'Closure Layoff', 'type code', 'warn type', 'typeoflayoff', 'Closing or Layoff', 'cl/lo', 'lo/cl', 'closing yes/no'])  # refers to closing vs layoff (CL/LO)
AMBIGUOUS_MAP = format_list(['date', 'date effective', 'LayoffBeginDate', 'effective date', 'LO/CL date', 'impact date', 'date of impact', 'planned starting date', 'state', 'effective layoff date'])  # require state-by-state approach

def main():
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    output_csv = '{}/standardize_field_names.csv'.format(OUTPUT_DIR)
    # we will put our dict rows here
    output_rows = []
    # extract each state's .csv from exports/ directory.
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

        # this function will smooth out lengths of rows and columns to prevent data errors
        state_rows = fill_rows_columns(state_rows)
        # run state-specific standardizations such as data cleaning, restructuring
        state_rows = standardize_state(state_rows, state_postal)
        state_rows = fill_rows_columns(state_rows)
        # add state field
        state_rows = add_state_field(state_rows, STANDARDIZED_FIELD_NAMES, state_postal)
        state_rows = fill_rows_columns(state_rows)
        # convert data to a list of dicts, and merge redundant columns non-destructively
        # for example, two fields that map to 'location' with be combined into one field,
        # separated by newlines
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
            if row and row.count('') != len(row):
                if row_idx == 0:
                    # standardize fields in the header!
                    row = standardize_header(row, STANDARDIZED_FIELD_NAMES, state_postal)
                # add row to the list
                state_rows.append(row)
    return state_rows

# replace field names that match our map
# also make state-by-state header changes using standardize_header_For_state()
def standardize_header(header_row, STANDARDIZED_FIELD_NAMES, state):
    for field_idx, field_name in enumerate(header_row):
        field_name = format_str(field_name)  # standardize strings to lowercase, no space, and no whitespace
        if field_name in EMPLOYER_MAP:
            field_name = STANDARDIZED_FIELD_NAMES[1]
        elif field_name in NUMBER_AFFECTED_MAP:
            field_name = STANDARDIZED_FIELD_NAMES[2]
        elif field_name in DATE_RECEIVED_MAP:
            field_name = STANDARDIZED_FIELD_NAMES[3]
        elif field_name in DATE_LAYOFF_MAP:
            field_name = STANDARDIZED_FIELD_NAMES[4]
        elif field_name in DATE_CLOSURE_MAP:
            field_name = STANDARDIZED_FIELD_NAMES[5]
        elif field_name in LOCATION_MAP:
            field_name = STANDARDIZED_FIELD_NAMES[6]
        elif field_name in PARENT_LOCATION_MAP:
            field_name = STANDARDIZED_FIELD_NAMES[7]
        elif field_name in INDUSTRY_MAP:
            field_name = STANDARDIZED_FIELD_NAMES[8]
        elif field_name in NOTES_MAP:
            field_name = STANDARDIZED_FIELD_NAMES[9]
        elif field_name in LAYOFF_TYPE_MAP:
            field_name = STANDARDIZED_FIELD_NAMES[10]
        elif field_name in AMBIGUOUS_MAP:
            # here we use a precise touch to replace header names per-state when we know what they *should* be
            field_name = standardize_header_for_state(field_name, STANDARDIZED_FIELD_NAMES, state)
        else:
            # make no changes to other fields
            print(f"Info: Unhandled field {field_name} in {state}.csv")
        # replace the field
        header_row[field_idx] = field_name
    return header_row

# called by standardize_header() to make state-specific header mappings for ambiguous fields
# for example, the field 'date' could mean different things in different states. for SD, it means WARN date.
def standardize_header_for_state(field_name, STANDARDIZED_FIELD_NAMES, state):
    if state == "SD":
        if field_name == format_str("date"):
            # map date field to WARN notice received date
            field_name = STANDARDIZED_FIELD_NAMES[3]
    elif state == 'VA':
        if field_name == format_str('impact date'):
            # since each row varies between closing and layoff for the same date column,
            # we will sort into 'closing' and 'layoff' field-by-field in standardize_AL()
            pass
        if field_name == format_str('state'):
            # map parent company state to 'parent_location' field
            field_name = STANDARDIZED_FIELD_NAMES[7]
    elif state == 'AL':
        if field_name == format_str('planned starting date'):
            # since each row varies between closing and layoff for the same date column,
            # we will sort into 'closing' and 'layoff' field-by-field in standardize_AL()
            pass
    elif state == 'DC':
        if field_name == format_str('effective layoff date'):
            # since each row varies between closing and layoff for the same date column,
            # we will sort into 'closing' and 'layoff' field-by-field in standardize_DC()
            pass
    elif state == 'MD':
        if field_name == format_str('effective layoff date'):
            # since each row varies between closing and layoff for the same date column,
            # we will sort into 'closing' and 'layoff' field-by-field in standardize_MD()
            pass
    elif state == 'RI':
        if field_name == format_str('effective date'):
            # since each row varies between closing and layoff for the same date column,
            # we will sort into 'closing' and 'layoff' field-by-field in standardize_RI()
            pass
    elif state == 'MO':
        if field_name == format_str('LAYOFF DATE'):
            # since each row varies between closing and layoff for the same date column,
            # we will sort into 'closing' and 'layoff' field-by-field in standardize_MO()
            pass
    elif state == 'WI':
        if field_name == format_str('LayoffBeginDate'):
            # since each row varies between closing and layoff for the same date column,
            # we will sort into 'closing' and 'layoff' field-by-field in standardize_WI()
            pass
    elif state == 'WA':
        if field_name == format_str('Layoff Start Date'):
            # since each row varies between closing and layoff for the same date column,
            # we will sort into 'closing' and 'layoff' field-by-field in standardize_WA()
            pass
    elif state == 'NE':
        if field_name == format_str('date'):
            # this field represents the date of WARN notice being received
            # effective date is missing from the data and would need to be scraped from WARN notice pdfs themsevles
            field_name = STANDARDIZED_FIELD_NAMES[3]
            pass
    elif state == 'NJ':
        if field_name == format_str('effective date'):
            # no 'closing' vs 'layoff' distinction => just put all the dates into date_layoff_raw
            field_name = STANDARDIZED_FIELD_NAMES[4]
            pass
    elif state == 'MT':
        if field_name == format_str('date of impact'):
            # no 'closing' vs 'layoff' distinction => just put all the dates into date_layoff_raw
            field_name = STANDARDIZED_FIELD_NAMES[4]
    else:
        print(f"Info: Unhandled header field standardization {field_name} for {state}.csv")
    return field_name

# pad rows and columns with empty values to match row length with header length
# input: list of state rows
# output: same, but with headers and fields added to even out data symmetry
def fill_rows_columns(state_rows):
    state_rows_header = state_rows[0]
    state_rows_body = state_rows[1:]
    # make sure all columns with data have a column header
    for row_idx, row in enumerate(state_rows_body):
        if row == [] or not row:
            state_rows_body.pop(row_idx)
        elif len(state_rows_header) < len(row):
            # print(f"Info: Found more values than headers in {state}.csv, line {row_idx}. Adding header for unknown field...")
            while len(state_rows_header) < len(row):
                field_identifier = len(state_rows_body[0]) - len(state_rows_header)
                # adds column header so the state can be processed w/o error
                state_rows_header.append(f"UnknownField{field_identifier}")
    # make sure all fields with a column header have enough fields of data
    for row_idx, row in enumerate(state_rows_body):
        if len(row) < len(state_rows_header):
            # print(f"Info: Found more headers than fields in {state}.csv, line {row_idx}. Adding blank string to field...")
            while len(row) < len(state_rows_header):
                row.append('')
    return state_rows

# this step is the counterpart of the step above;
# input/output: state rows list
def add_state_field(state_rows, STANDARDIZED_FIELD_NAMES, state):
    # add 'state' field to header
    state_rows[0].append(STANDARDIZED_FIELD_NAMES[0])
    for row in state_rows:
        row.append(state)  # store 'state' field in body
    return state_rows

# run state-specific processing
# input/output: a list of state rows (including header)
def standardize_state(state_rows, state):
    if state == 'AL':
        return standardize_AL(state_rows, state)
    elif state == 'DC':
        return standardize_DC(state_rows, state)
    elif state == 'MD':
        return standardize_MD(state_rows, state)
    elif state == 'IN':
        return standardize_IN(state_rows, state)
    elif state == 'RI':
        return standardize_RI(state_rows, state)
    elif state == 'VA':
        return standardize_VA(state_rows, state)
    elif state == 'WI':
        return standardize_WI(state_rows, state)
    elif state == 'WA':
        return standardize_WA(state_rows, state)
    elif state == 'MO':
        return standardize_MO(state_rows, state)
    elif state == 'CT':
        return standardize_CT(state_rows, state)
        # TODO: im going to put some comments here about a state we might eventually want to alter our strategy for
        # for CT, the mapping merges columns "closing date" and "layoff date" into the "date effective column".
        # CT has a pretty weird system where the dates are the same for the most part but sometimes they're not;
        # in those cases, you'll have two dates listed under date_effective and there's no explanation in the data.
        # we might want to create a new column for data to map to, in case this data is considered substatial or worthwhile.
        # would require some looking into, maybe speaking with CT about it.
        pass
    else:
        pass
    return state_rows

# the goal of this function is to convert to dict
# also implements non-destructive merging as a last defense when multiple columns map to one
# (e.g, if two source columns map to our 'location' col and we haven't handled it in a prior step, let's combine them)
# input: a list of rows
# output: a list of dicts
def merge_to_dict(state_rows):
    '''
    transfer the current state's data to dict list & merge redundant columns.
    at this point: any fields we've mapped will be merged into column names listed in STANDARDIZED_FIELD_NAMES
    merging strategy: separate by newlines
    and fields left unmapped are still in the data to be removed later
    eg. state_rows_as_dicts = [
        { "company": "ABC Wood Systems", "some_unwanted_field" : "(123) 456-7890", "merged_field": "1234 Avenue \n 90210", ...},
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
def standardize_AL(state_rows, state):
    # use a layoff type column to sort date into date_layoff_raw vs date_closing_raw
    lo_cl_col = 0  # extract "Closing or layoff" col
    date_col = 2  # extract 'Planned Starting Date' col
    closing_str = 'cl'  # if the value in lo_cl_col contains closing_str, the row is a closing
    for row_idx, row in enumerate(state_rows):
        if row_idx == 0:
            # create new columns in header and get their indices
            state_rows, layoff_index, closure_index = create_layoff_closure_date_fields(state_rows)
        else:
            row = sort_lo_cl_date(row, layoff_index, closure_index, lo_cl_col, date_col, closing_str)
    return state_rows

# input/output: list of state's rows including header
def standardize_DC(state_rows, state):
    # use a layoff type column to sort date into date_layoff_raw vs date_closing_raw
    # Code Type: 1=Layoff, 2=Permanent Closures
    lo_cl_col = 4  # extract "code type" col
    date_col = 3  # extract 'effective layoff date' col
    closing_str = '2'  # if the value in lo_cl_col contains closing_str, the row is a closing
    for row_idx, row in enumerate(state_rows):
        if row_idx == 0:
            # create new columns in header and get their indices
            state_rows, layoff_index, closure_index = create_layoff_closure_date_fields(state_rows)
        else:
            row = sort_lo_cl_date(row, layoff_index, closure_index, lo_cl_col, date_col, closing_str)
    return state_rows

# input/output: list of state's rows including header
def standardize_IN(state_rows, state):
    # use a layoff type column to sort date into date_layoff_raw vs date_closing_raw
    # Code Type: LO=Layoff, CL=Closure
    lo_cl_col = 7  # extract "notice type" col
    date_col = 4  # extract 'LO/CL date' col
    closing_str = 'cl'  # if the value in lo_cl_col contains closing_str, the row is a closing
    for row_idx, row in enumerate(state_rows):
        if row_idx == 0:
            # create new columns in header and get their indices
            state_rows, layoff_index, closure_index = create_layoff_closure_date_fields(state_rows)
        else:
            row = sort_lo_cl_date(row, layoff_index, closure_index, lo_cl_col, date_col, closing_str)
    return state_rows
# input/output: list of state's rows including header
def standardize_MD(state_rows, state):
    # use a layoff type column to sort date into date_layoff_raw vs date_closing_raw
    # Code Type: 1=closure, 2=layoff (this is different from most states)
    lo_cl_col = 7  # extract "type code" col
    date_col = 6  # extract 'effective date' col
    closing_str = '1'  # if the value in lo_cl_col contains closing_str, the row is a closing
    for row_idx, row in enumerate(state_rows):
        if row_idx == 0:
            # create new columns in header and get their indices
            state_rows, layoff_index, closure_index = create_layoff_closure_date_fields(state_rows)
        else:
            row = sort_lo_cl_date(row, layoff_index, closure_index, lo_cl_col, date_col, closing_str)
    return state_rows


# input/output: list of state's rows including header
def standardize_RI(state_rows, state):
    # use a layoff type column to sort date into date_layoff_raw vs date_closing_raw
    lo_cl_col = 6  # extract "closing yes/no" col
    date_col = 5  # extract 'effective date' col
    closing_str = 'yes'  # if the value in lo_cl_col contains closing_str, the row is a closing
    for row_idx, row in enumerate(state_rows):
        if row_idx == 0:
            # create new columns in header and get their indices
            state_rows, layoff_index, closure_index = create_layoff_closure_date_fields(state_rows)
        else:
            row = sort_lo_cl_date(row, layoff_index, closure_index, lo_cl_col, date_col, closing_str)
    return state_rows

# input/output: list of state's rows including header
def standardize_VA(state_rows, state):
    # use a layoff type column to sort date into date_layoff_raw vs date_closing_raw
    lo_cl_col = 15  # "Closure" col
    date_col = 12  # "Impact Date" col
    closing_str = 'cl'  # if the value in lo_cl_col contains closing_str, the row is a closingfor row_idx, row in enumerate(state_rows):
    for row_idx, row in enumerate(state_rows):
        if row_idx == 0:
            # create new columns in header and get their indices
            state_rows, layoff_index, closure_index = create_layoff_closure_date_fields(state_rows)
        else:
            row = sort_lo_cl_date(row, layoff_index, closure_index, lo_cl_col, date_col, closing_str)
    return state_rows


# input/output: list of state's rows including header
def standardize_WI(state_rows, state):
    # drop revision text
    indexes_to_pop = []
    for row_idx, row in enumerate(state_rows):
        if not row_idx == 0:
            current_company_field = row[0]
            if 'Revision' in current_company_field:
                # if the current row is a revision, drop the previous row
                indexes_to_pop.append(row_idx - 1)
                # and remove the revision text from company name
                current_company_field = current_company_field.split(" - Revision")[0]
            row[0] = current_company_field
    popped = 0
    # remove rows after looping to prevent looping bugs
    for i in indexes_to_pop:
        state_rows.pop(i - popped)
        popped += 1
    # use a layoff type column to sort date into date_layoff_raw vs date_closing_raw
    closing_str = 'cl'  # if the value in lo_cl_col contains closing_str, the row is a closing
    lo_cl_col = 4  # "NoticeType" col
    date_col = 5  # "LayoffBegins" col
    for row_idx, row in enumerate(state_rows):
        if row_idx == 0:
            # create new columns in header and get their indices
            state_rows, layoff_index, closure_index = create_layoff_closure_date_fields(state_rows)
        else:
            row = sort_lo_cl_date(row, layoff_index, closure_index, lo_cl_col, date_col, closing_str)
    return state_rows

# input/output: list of state's rows including header
# def standardize_CT(state_rows, state):
#     closing_str = 'yes'  # if the value in lo_cl_col contains closing_str, the row is a closing
#     lo_cl_col = 6  # "type" col
#     date_col = 7  # "layoff date" col
#     state_rows = standardize_closing_layoff(state_rows, closing_str, lo_cl_col, date_col)
#     return state_rows


# input/output: list of state's rows including header
def standardize_MO(state_rows, state):
    closing_str = 'cl'  # if the value in lo_cl_col contains closing_str, the row is a closing
    lo_cl_col = 6  # "type" col
    date_col = 7  # "layoff date" col
    state_rows = standardize_closing_layoff(state_rows, closing_str, lo_cl_col, date_col)
    return state_rows


# input/output: list of state's rows including header
def standardize_WA(state_rows, state):
    closing_str = 'cl'  # if the value in lo_cl_col contains closing_str, the row is a closing
    lo_cl_col = 4  # "closure layoff" col
    date_col = 2  # "received date" col
    state_rows = standardize_closing_layoff(state_rows, closing_str, lo_cl_col, date_col)
    return state_rows

# use a layoff type column to sort date into date_layoff_raw vs date_closing_raw
def standardize_closing_layoff(state_rows, closing_str, lo_cl_col, date_col):
    for row_idx, row in enumerate(state_rows):
        if row_idx == 0:
            # create new columns in header and get their indices
            state_rows, layoff_index, closure_index = create_layoff_closure_date_fields(state_rows)
        else:
            row = sort_lo_cl_date(row, layoff_index, closure_index, lo_cl_col, date_col, closing_str)
    return state_rows

# sort ambiguous date columns like "effective date" into "layoff date" and "closing date" columns
def sort_lo_cl_date(row, layoff_index, closure_index, lo_cl_col, date_col, closing_str):
    # extract boolean for whether or not plant is closing
    closure_layoff_str = str(row[lo_cl_col])
    is_closing = is_closing_str(closure_layoff_str, closing_str)
    # add date into correct col depending on whether is_closing is true
    date_to_add = str(row[date_col])
    row = add_lo_cl_date_for_row(row, date_to_add, is_closing, layoff_index, closure_index)
    return row

# create date_layoff_raw and date_closure_raw fields
# and return the new data + the corresponding index of each of those fields
def create_layoff_closure_date_fields(state_rows):
    # add fields to header
    if "date_layoff_raw" not in state_rows[0]:
        state_rows[0].append("date_layoff_raw")
    if "date_closure_raw" not in state_rows[0]:
        state_rows[0].append("date_closure_raw")
    # get indices
    layoff_index = state_rows[0].index("date_layoff_raw")
    closure_index = state_rows[0].index("date_closure_raw")
    # add fields to rest of code
    state_rows = fill_rows_columns(state_rows)
    return state_rows, layoff_index, closure_index


# returns boolean of whether or not a given string indicates a closing
# any string containing the text in "key" will be considered to denote a closing
# without additional args, defaults to checking whether the string contains "cl"
def is_closing_str(string_to_check, key='cl'):
    string_to_check = ''.join(char for char in string_to_check if char.isalnum())  # remove non-alphanumeric chars
    is_closing = key in format_str(string_to_check)
    return is_closing


def add_lo_cl_date_for_row(row, date, is_closing, layoff_index, closure_index):
    if is_closing:
        row[closure_index] = date  # add to date_closure col
    else:
        row[layoff_index] = date  # add to date_closure col
    return row


if __name__ == '__main__':
    main()
