import csv
import logging
from collections import defaultdict
from datetime import datetime, timezone
from itertools import chain
from operator import itemgetter
from pathlib import Path

import jellyfish
import requests

from . import utils

logger = logging.getLogger(__name__)


def run(
    new_path: Path = utils.WARN_TRANSFORMER_OUTPUT_DIR
    / "processed"
    / "consolidated.csv",
) -> Path:
    """Integrate the latest consolidated data with the current database.

    Args:
        new_path (Path): The path to the latest consolidated file on the local file system

    Returns a Path to the newly integrated file.
    """
    # Download the current database
    current_url = "https://raw.githubusercontent.com/biglocalnews/warn-github-flow/transformer/data/warn-transformer/processed/integrated.csv"
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
    amend_by_source = {}
    insert_by_source = {}
    for postal_code, new_row_list in new_data_by_source.items():
        logger.debug(f"Inspecting {len(new_row_list)} new records from {postal_code}")

        # Pull the current rows from the source
        current_row_list = current_data_by_source[postal_code]
        logger.debug(
            f"Comparing against {len(current_row_list)} records from the current database"
        )

        # Loop through the rows in this source
        unchanged_list = []
        change_list = []
        for new_row in new_row_list:
            # Identify new rows that are identical to a record in the current database
            new_hash = new_row["hash_id"]
            if any(r for r in current_row_list if r["hash_id"] == new_hash):
                unchanged_list.append(new_row)
            else:
                change_list.append(new_row)

        # Log where we stand
        logger.debug(
            f"{len(unchanged_list)} unchanged rows ({round((len(unchanged_list)/len(new_row_list))*100, 2)}%)"
        )
        logger.debug(
            f"{len(change_list)} changed rows ({round((len(change_list)/len(new_row_list))*100, 2)}%)"
        )

        # Loop through the change list
        insert_list = []
        amend_list = []
        for new_row in change_list:
            # Check our key fields against everything in the dataset
            likely_match_list = []
            for current_row in current_row_list:
                likely_matches = 0
                # Check the company names
                if (
                    jellyfish.jaro_winkler_similarity(
                        new_row["company"], current_row["company"]
                    )
                    > 0.95
                ):
                    likely_matches += 1

                # Check the notice date
                if (
                    jellyfish.levenshtein_distance(
                        new_row["notice_date"], current_row["notice_date"]
                    )
                    < 4
                ):
                    likely_matches += 1

                # If both match, we call it a likely match
                if likely_matches == 2:
                    likely_match_list.append(current_row)

            # If there is more than one likely match, we should compare some extra fields
            likely_match = None
            if len(likely_match_list) > 1:
                # Score all the location similarities
                location_similarity_list = []
                for current_row in likely_match_list:
                    score = jellyfish.jaro_winkler_similarity(
                        current_row["location"], new_row["location"]
                    )
                    location_similarity_list.append((current_row, score))
                # Take the one that's most similar, if it's over a certain score
                location_similarity_list.sort(key=itemgetter(1), reverse=True)
                if location_similarity_list[0][1] > 0.95:
                    likely_match = likely_match_list[0]
            elif len(likely_match_list) == 1:
                likely_match = likely_match_list[0]

            # If there is one, we assume this is an amendment
            if likely_match:
                amend_list.append({"new": new_row, "current": likely_match})
            # Otherwise we estimate it's a new record
            else:
                insert_list.append(new_row)

        # Log the result
        logger.debug(f"{len(insert_list)} new records")
        logger.debug(f"{len(amend_list)} amended records")

        # Add to master list for integration
        insert_by_source[postal_code] = insert_list
        amend_by_source[postal_code] = amend_list

    # Final report on what we'll do
    full_amend_list = list(chain(*amend_by_source.values()))
    full_insert_list = list(chain(*insert_by_source.values()))
    logger.debug(f"{len(full_insert_list)} total new records")
    logger.debug(f"{len(full_amend_list)} total amended records")

    # Overwrite the amendments, storing the old versions somewhere ...
    now = datetime.now(timezone.utc)
    amend_lookup = {d["current"]["hash_id"]: d["new"] for d in full_amend_list}
    integrated_list = []
    for current_row in current_data_list:
        # If this is an amended row, change it
        if current_row["hash_id"] in amend_lookup:
            amend_dict = amend_lookup[current_row["hash_id"]]
            amend_dict["last_updated_date"] = str(now)
            amend_dict["estimated_amendments"] = str(
                int(current_row["estimated_amendments"]) + 1
            )
            integrated_list.append(amend_dict)
        # If it's not, pass it along
        else:
            # Otherwise keep what we got
            integrated_list.append(current_row)

    # Insert the new records with today's timestamp
    for row in full_insert_list:
        row["first_inserted_date"] = str(now)
        row["last_updated_date"] = str(now)
        row["estimated_amendments"] = "0"
        integrated_list.append(row)

    # Write out what we got
    processed_dir = utils.WARN_TRANSFORMER_OUTPUT_DIR / "processed"
    integrated_path = processed_dir / "integrated.csv"
    logger.debug(f"Writing {len(integrated_list)} records to {integrated_path}")
    with open(integrated_path, "w") as fh:
        writer = csv.DictWriter(fh, integrated_list[0].keys())
        writer.writeheader()
        writer.writerows(integrated_list)

    # Return it
    return integrated_path


if __name__ == "__main__":
    run()
