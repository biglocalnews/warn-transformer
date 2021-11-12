# input: standardized_field_names.csv
# reads 3 'raw' date columns:
# (1) date_received_raw
# (2) date_layoff_raw
# (3) date_closure_raw

# output: standardized_dates.csv
# appends 5 'cleaned' columns:
# (1) date_received_cleaned
# (2) date_received_year
# (3) date_received_month
# (4) date_layoff_cleaned
# (5) date_closing_cleaned

#-----METHODS-----
# (1) dateutil.parser.parse() is best at making sense out of messy strings
# (2) pendulum.parse() is a last-ditch effort
# (3) datetime.strptime() with hard-coded regex checks for specific tricky dates(?):
#   d = datetime.datetime.strptime('Mon Feb 15 2020', '%a %b %d %Y').strftime('%d/%m/%Y')

import csv
import datetime
import re
import os

from dateutil.parser import parse
from pathlib import Path
import pendulum

from utils import write_rows_to_csv

USER_HOME = os.path.expanduser('~')
DEFAULT_HOME = str(Path(USER_HOME, '.warn-scraper'))
ETL_DIR = os.environ.get('WARN_ETL_DIR', DEFAULT_HOME)
WARN_DATA_PATH = str(Path(ETL_DIR, 'exports'))
WARN_ANALYSIS_PATH = str(Path(ETL_DIR, 'analysis'))
INPUT_DIR = WARN_ANALYSIS_PATH
OUTPUT_DIR = WARN_ANALYSIS_PATH

# date_received_raw, date_layoff_raw, date_closure_raw from standardize_field_names.csv
INPUT_COLS = [3, 4, 5]


def main():
    Path(WARN_ANALYSIS_PATH).mkdir(parents=True, exist_ok=True)
    input_csv = '{}/standardize_field_names.csv'.format(INPUT_DIR)
    output_csv = '{}/standardize_dates.csv'.format(OUTPUT_DIR)
    source_file = str(Path(INPUT_DIR).joinpath(input_csv))
    print(f'Processing {input_csv}...')

    # convert file into list of rows
    try:
        rows = open_file(source_file, input_csv)
    except UnicodeDecodeError:
        rows = open_file(source_file, input_csv, encoding="utf-8")
    # add new column headers
    rows[0].append("date_received_cleaned")
    rows[0].append("date_received_year")
    rows[0].append("date_received_month")
    rows[0].append("date_layoff_cleaned")
    rows[0].append("date_closure_cleaned")
    output_rows = []

    # go through rows of input csv
    for row_idx, row in enumerate(rows):
        # skip date extraction for header row
        if row_idx == 0:
            output_rows.append(row)
            continue
        for col_idx, col in enumerate(row):
            # if the column is the date_received column, clean & extract it
            if col_idx == INPUT_COLS[0]:
                date = col
                date = clean_date(date)
                date_str, year_str, month_str = standardize_date(date)
                # add cleaned date data to our output data
                row.append(date_str)
                row.append(year_str)
                row.append(month_str)
            # for all other input columns, just clean it and append
            elif col_idx in INPUT_COLS:
                date = col
                date = clean_date(date)
                date_str, year_str, month_str = standardize_date(date)
                # add cleaned date data to our output data
                row.append(date_str)
        output_rows.append(row)

    write_rows_to_csv(output_rows, output_csv)


def open_file(source_file, filename, encoding=''):
    kwargs = {"newline": "", }
    # work-around for encoding differences between states
    if encoding:
        kwargs["encoding"] = encoding
    output_rows = []
    with open(source_file, **kwargs) as f:
        file = csv.reader(f)
        for row in file:
            output_rows.append(row)
    return output_rows

# input: unstandardized date
# output: standardized date, year substring
def standardize_date(date):
    standardized_date = ""
    date_str = ""
    year_str = ""
    month_str = ""
    try:
        # using dateutil's parse() function
        standardized_date = parse(date)
        date_str = standardized_date.strftime('%m/%d/%Y')
        year_str = standardized_date.strftime('%Y')
        month_str = standardized_date.strftime('%m')
        # TODO if year before 1989, raise Warning
    except (Exception) as e:
        pass
        # print(f"Dateutil: An exception of type {type(e)} occurred. Arguments:\n{e.args}")

        # try:
        #     # use pendulum library to parse date
        #     dt = pendulum.parse(date, strict=False)
        #     # pendulum has a nice print feature
        #     standardized_date = dt.to_date_string()

        # except (Exception) as e:
        #     pass
        # print(f"Pendulum: An exception of type {type(e)} occurred. Arguments:\n{e.args}")

    # print(standardized_date)

    return date_str, year_str, month_str

# get a single date from a range of dates
# because we preserve original date in data,
# we are allowed to edit destructively.
def clean_date(date):
    # pick the first date if date is a range
    delimiter_tokens = ['-', ' to ', ' ', ',']
    for t in delimiter_tokens:
        # if the token bisects the string, split it
        if(len(date.split(t)) == 2):
            date = date.split(t)[0]
    # remove &, remove ',', remove '*'
    remove_tokens = ['*', '&']
    for t in remove_tokens:
        date = date.replace(t, "")

    # # convert all lettered months to numbers
    # date.replace("Jan", "1")
    # date.replace("Feb", "2")
    # date.replace("Mar", "3")
    # date.replace("Apr", "4")
    # date.replace("May", "5")
    # date.replace("Jun", "6")
    # date.replace("Jul", "7")
    # date.replace("Aug", "8")
    # date.replace("Sep", "9")
    # date.replace("Oct", "10")
    # date.replace("Nov", "11")
    # date.replace("Dec", "12")
    # # eliminate all letters
    # for char in date:
    #     if char.isalpha():
    #         date += char
    return date


if __name__ == '__main__':
    main()
