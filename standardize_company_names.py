# TODO use opencorporates API to standardize company names
import csv
import requests

from pathlib import Path

from utils import write_dict_rows_to_csv
from utils import write_rows_to_csv

USER_HOME = os.path.expanduser('~')
DEFAULT_HOME = str(Path(USER_HOME, '.warn-scraper'))
ETL_DIR = os.environ.get('WARN_ETL_DIR', DEFAULT_HOME)
WARN_DATA_PATH = str(Path(ETL_DIR, 'exports'))
INPUT_DIR = WARN_DATA_PATH
WARN_ANALYSIS_PATH = str(Path(ETL_DIR, 'analysis'))
OUTPUT_DIR = WARN_ANALYSIS_PATH


# company_name column from standardize_field_names.csv
COMPANY_COL = 1


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
    rows[0].append("company_name_canonical")
    output_rows = []
    for row_idx, row in enumerate(rows):
        if row_idx == 0:
            continue
        for col_idx, col in enumerate(row):
            # standardize company
            if col_idx == COMPANY_COL:
                row.append(standardize_company(col))
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


def standardize_company():
    return "this company is, like, so standardized. TODO standardize."


if __name__ == '__main__':
    main()
