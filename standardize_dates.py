# datasets from some states contain different date formats within themselves (eg: MO, DC) and possibly different conventions for documenting updates.
# A thorough date format standardization can be done to all of the states at some point.


import calendar
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

DATE_COLS = [3, 4]  # these are the columns of standardized_field_names.csv where we will read dates

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
    # remove text,letters, and unwanted characters
    date_numbers = numeric_date(date)
    # split field into a list of 1 or 2 dates
    # NOTE on strategy: should we keep both dates or just stick to processing the first?
    date_list = split_date(date_numbers)
    if(len(date_list) > 2):
        print(f"error: more dates than expected: {date_list}")
        raise Exception
    # extract month, day, year
    date_list = extract_date(date_list)
    # separate two dates with a dash
    standardized_date = (" - ").join(date_list)
    return standardized_date

# input: dates that may have informative text like "January" or " from x to y"
# return: only numbers, slashes, dashes
# slashes should separate D/M/Y while dashes should separate different dates
def numeric_date(date):
    # let's preserve important information that is currently in text form
    date.replace("to", "-")
    # convert any months into numbers
    date = months_to_numbers(date)

    # then, convert dashes between D/M/Y into slashes
    # content_between_dashes = date.split("-")
    # if the dashes are separating D/M/Y, then convert them to slashes

    # now that we've preserved all important text, let's leave only preferred chars
    newstring = ''
    for char in date:
        # we want only date numbers and formatting characters
        if char.isnumeric() or char == '/' or char == '-':
            newstring += char
    return newstring.replace(" ", "")


# convert months to numbers (eg 'February' -> 2, 'Jun' -> 6)
def months_to_numbers(date):
    # strategy for full months
    pass
    # strategy for abbreviated months
    pass
    # {month: index for index, month in enumerate(calendar.month_abbr) if month}
    return date

def split_date(date):
    dates = date.split("-")
    return [date1, date2]

# input list of dates with questionable D/M/Y ordering
# output list of dates with ordering standardized to DD/MM/YYYY
def extract_date(date_list):
    # dicts to keep track of the dates we've extracted
    date1 = {'DD': '', 'MM': '', 'YYYY': ''}
    date2 = {'DD': '', 'MM': '', 'YYYY': ''}
    for date in date_list:
        # use context clues
        # eg if date 1 has a year and date 2 doesn't, use the year from date 1


if __name__ == '__main__':
    main()
