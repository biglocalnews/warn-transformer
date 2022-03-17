import csv
import logging
from collections import defaultdict
from pathlib import Path

import requests

from . import utils

logger = logging.getLogger(__name__)


def run(
    new_path: Path = utils.WARN_TRANSFORMER_OUTPUT_DIR
    / "processed"
    / "consolidated.csv",
):
    # Download the current database
    current_url = "https://raw.githubusercontent.com/biglocalnews/warn-github-flow/transformer/data/warn-transformer/processed/consolidated.csv"
    current_r = requests.get(current_url)
    current_data_str = current_r.content.decode("utf-8")

    # Read in the current database
    current_data_reader = csv.DictReader(current_data_str.splitlines(), delimiter=",")
    current_data_list = list(current_data_reader)
    logger.debug(f"{len(current_data_list)} records downloaded from current database")

    # Read in new consolidated.csv file
    with open(new_path) as fh:
        new_data_reader = csv.DictReader(fh)
        new_data_list = list(new_data_reader)
    logger.debug(f"{len(new_data_list)} records in new file")

    # Regroup each list by state
    current_data_by_source = defaultdict(list)
    for row in current_data_list:
        current_data_by_source[row["postal_code"]].append(row)

    new_data_by_source = defaultdict(list)
    for row in new_data_list:
        new_data_by_source[row["postal_code"]].append(row)

    # Loop through the sources
    for postal_code, new_row_list in new_data_by_source.items():
        logger.debug(f"Inspecting {len(new_row_list)} new records from {postal_code}")

        # Pull the current rows from the source
        current_row_list = current_data_by_source[postal_code]
        logger.debug(
            f"Comparing against {len(current_row_list)} records from the current database"
        )

        # Loop through the rows in this source
        unchanged_list = []
        for new_row in new_row_list:
            # Identify new rows that are identical to a record in the current database
            new_hash = new_row["hash_id"]
            if any(r for r in current_row_list if r["hash_id"] == new_hash):
                unchanged_list.append(new_row)
                print(new_row)

        logger.debug(
            f"{len(unchanged_list)} unchanged rows ({len(unchanged_list)/len(current_row_list)}"
        )

    # Compare the remaining rows against the current
    # database and measure their similarity.

    # If the similarity meets our threshold,
    # mark the record as an amendment

    # If the row in the new file doesn't meet
    # our threshold, mark it as a new record.

    # Overwrite the amendments, storing the old versions somewhere ...

    # Insert the new records with today's timestamp
    pass


if __name__ == "__main__":
    run()
