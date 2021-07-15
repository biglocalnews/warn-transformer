# datasets from some states contain different date formats within themselves (eg: MO, DC) and possibly different conventions for documenting updates.
# A thorough date format standardization can be done to all of the states at some point.


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

DATE_COLS = [3, 4]  # the columns of standardize_field_names.py that store dates

def main():
    output_csv = '{}/standardize_field_names.csv'.format(OUTPUT_DIR)
    output_rows = []
    # open each state's output file from exports/ directory.
    for filename in os.listdir(OUTPUT_DIR):
        print(f'Processing {filename}...')
        with open(f"{OUTPUT_DIR}\\{filename}", newline='') as f:
            file = csv.reader(f)
            for row in file:
                for col_idx, col in enumerate(row):
                    # if the data is a date, standardize its format!
                    if col_idx in DATE_ROWS:
                        row[col_idx] = standardize_date(col)
                    row.append(col)
                output_rows.append(row)
    write_rows_to_csv(output_rows, output_csv)


# takes a date field and standardizes it
def standardize_date(date):
    pass
    return date.replace(" ", "")


if __name__ == '__main__':
    main()
