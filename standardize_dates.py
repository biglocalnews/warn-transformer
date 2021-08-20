# input: standardized_field_names.csv
# output: standardized_dates.csv
# datasets from some states contain different date formats within themselves (eg: MO, DC) and possibly different conventions for documenting updates.
# A thorough date format standardization can be done to all of the states at some point.

# examples of cases we've seen:
# September 15, 2020 and March 18, 2020
# 12/1/20 (MM/D/YY)
# 10/24/2016 (MM/DD/YYY)
# December 25, and Feb - Jun 2021

import csv
import os

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

# date_received_raw, date_effective_raw from standardize_field_names.csv
DATE_COLS = [3, 4]

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
    rows[0].append("date_effective_cleaned")
    output_rows = []
    for row_idx, row in enumerate(rows):
        if row_idx == 0:
            continue
        for col_idx, col in enumerate(row):
            # standardize any date input
            if col_idx in DATE_COLS:
                # note: these fields are expected to add in order of the column headers we added
                row.append(standardize_date(col))
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

# take a date field and standardize the formatting
def standardize_date(date):
    # TODO: what if date field is actually a list of dates, such as "12-21-17 - 1-01-18"?
    # date_list = split_date(date_numbers)
    # if(len(date_list) > 2):
    #     print(f"error: more dates than expected: {date_list}")
    #     raise Exception

    # use pendulum library to parse date
    dt = pendulum.parse(date)
    # pendulum has a nice print feature
    standardized_date = dt.to_date_string()

    return standardized_date


def split_date(date):
    dates = date.split("-")
    return [date in dates]


if __name__ == '__main__':
    main()
