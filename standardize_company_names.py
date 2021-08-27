# TODO use opencorporates API to standardize company names
import csv
import json
import requests
import os

from pathlib import Path

from cache import Cache
from utils import download_file
from utils import write_dict_rows_to_csv
from utils import write_rows_to_csv

USER_HOME = os.path.expanduser('~')
DEFAULT_HOME = str(Path(USER_HOME, '.warn-scraper'))
ETL_DIR = os.environ.get('WARN_ETL_DIR', DEFAULT_HOME)
WARN_ANALYSIS_PATH = str(Path(ETL_DIR, 'analysis'))
# TODO: do we want the user to input their own cache path?
WARN_CACHE_PATH = str(Path(ETL_DIR, 'cache'))
INPUT_DIR = WARN_ANALYSIS_PATH
OUTPUT_DIR = WARN_ANALYSIS_PATH


# company_name column from standardize_field_names.csv
COMPANY_COL = 1


def main():
    # create cache dir if doesnt exist
    cache_dir = Path(WARN_CACHE_PATH, 'opencorporates')
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache = Cache(cache_dir)
    Path(WARN_ANALYSIS_PATH).mkdir(parents=True, exist_ok=True)
    input_csv = '{}/standardize_field_names.csv'.format(INPUT_DIR)
    output_csv = '{}/standardize_company_names.csv'.format(OUTPUT_DIR)
    source_file = str(Path(INPUT_DIR).joinpath(input_csv))
    print(f'Processing {input_csv}...')
    # convert file into list of rows
    try:
        rows = open_file(source_file, input_csv)
    except UnicodeDecodeError:
        rows = open_file(source_file, input_csv, encoding="utf-8")
    # add header
    rows[0].append("company_name_canonical")
    output_rows = []

    company = 'Chevron'
    company_to_standardize = preprocess(company)
    standardize_company(company, cache_dir)

    for row_idx, row in enumerate(rows):
        if row_idx == 0:
            continue
        for col_idx, company_str in enumerate(row):
            # standardize company
            if col_idx == COMPANY_COL:
                company_str = preprocess(company_str)
                # TODO actually implement OpenCorporates.
                # for now, we just want to test it out.
                # company_str = standardize_company(company_str, cache_dir)
                row.append(company_str)
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

def preprocess(str_to_process):
    str_to_process.replace('*', '').replace('_', '')
    # drop various formats of revision text
    str_to_process = str_to_process.split(" - Revision")[0]
    str_to_process = str_to_process.split("(Revised")[0]
    str_to_process = str_to_process.split("(Updated Notice")[0]


# TODO implement cacheing
def standardize_company(company_name, cache_dir):
    url = f'https://api.opencorporates.com/v0.4/companies/search?q={company_name}'
    cache_key = company_name
    downloaded_dir = f'{cache_dir}/{cache_key}.json'
    api_json = ""
    try:
        print(f'trying to read company {company_name} from cache...')
        # read from cache
        try:
            api_json = open_json(downloaded_dir)
        except UnicodeDecodeError:
            api_json = open_json(downloaded_dir, encoding="utf-8")

    except (FileNotFoundError, SyntaxError):
        print(f'failed to read from cache. Downloading API data for company {company_name}...')
        # cody's api key
        auth = requests.auth.HTTPBasicAuth('apikey', 'vLHe38cEAyunPAOORaxV')
        # api_response = requests.get(url, auth=auth)
        # print(f'Response Code: {api_response.status_code}')
        # api_response.raise_for_status()
        file_path = download_file(url, auth=auth, local_path=downloaded_dir)
        try:
            api_json = open_json(file_path)
        except UnicodeDecodeError:
            api_json = open_json(file_path, encoding="utf-8")
        # print(f'API text: {api_text}')
        # cache.write(cache_key, api_text)
        # api_json = eval(api_text)
    print(f'JSON: \n {api_json}')
    standardized_company_name = find_canonical(api_json)
    return standardized_company_name


def open_json(source_file, encoding=''):
    kwargs = {"newline": "", }
    # work-around for encoding differences between states
    if encoding:
        kwargs["encoding"] = encoding
    output_rows = []
    with open(source_file, **kwargs) as f:
        json_file = json.load(f)
    return json_file


def find_canonical(json):
    json = json['results']
    if json['companies']:
        for company in json['companies']:
            return evaluate_match(company)
    elif json['company']:
        return evaluate_match(company)
    else:
        print('No matching companies found.')
    return None


# run a series of filters to determine whether this entry is the canonical company
def evaluate_match(company):
    # TODO: filter to match address
    print(company)
    print(company['name'])


if __name__ == '__main__':
    main()
