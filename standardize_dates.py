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

DATE_COLS = [3, 4]  # columns of standardize_field_names.csv from which we will read dates

def main():
    Path(WARN_ANALYSIS_PATH).mkdir(parents=True, exist_ok=True)
    input_csv = '{}/standardize_field_names.csv'.format(INPUT_DIR)
    output_csv = '{}/standardize_dates.csv'.format(OUTPUT_DIR)
    output_rows = []
    print(f'Processing {input_csv}...')
    source_file = str(Path(INPUT_DIR).joinpath(input_csv))
    with open(source_file, newline='', encoding='utf-8') as f:
        file = csv.reader(f)
        for row_idx, row in enumerate(file):
            if row_idx == 1:
                # add new column headers
                row.append("date_received_cleaned")
                row.append("date_effective_cleaned")
            for col_idx, col in enumerate(row):
                # standardize any date input
                if col_idx in DATE_COLS:
                    row.append(standardize_date(col))
            output_rows.append(row)
    write_rows_to_csv(output_rows, output_csv)


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
