import csv
import json
import logging
import typing
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
    init_current_data: bool = False,
) -> Path:
    """Integrate new consolidated data with the current database.

    Args:
        new_path (Path): The path to the latest consolidated file on the local file system
        init_current_data (bool): Set to True when you want to create a new integrated dataset from scratch. Default False.

    Returns a Path to the newly integrated file.
    """
    # Get the most recently published integrated dataset
    current_data_list = get_current_data(init_current_data)

    # Read in new consolidated.csv file
    with open(new_path) as fh:
        new_data_reader = csv.DictReader(fh)
        new_data_list = list(new_data_reader)
    logger.debug(f"{len(new_data_list)} records in new file at {new_path}")

    # Regroup each list by state
    current_data_by_source = regroup_by_source(current_data_list)
    new_data_by_source = regroup_by_source(new_data_list)

    # Winnow down the new data to records that have changed
    changed_data_by_source = get_changed_data(
        new_data_by_source, current_data_by_source
    )

    # Loop through the changed data to determine which are new and which are amendements
    amend_by_source = {}
    insert_by_source = {}
    for postal_code, change_list in changed_data_by_source.items():
        logger.debug(
            f"Inspecting {len(change_list)} changed records from {postal_code}"
        )
        current_row_list = current_data_by_source[postal_code]
        amend_list = []
        insert_list = []
        for new_row in change_list:
            # See if we can find a likely parent that was amended
            likely_ancestor = get_likely_ancestor(new_row, current_row_list)
            # If there is one, we assume this is an amendment
            if likely_ancestor:
                amend_list.append({"new": new_row, "current": likely_ancestor})
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
    full_amend_list = flatten_grouped_data(amend_by_source)
    full_insert_list = flatten_grouped_data(insert_by_source)
    logger.debug(f"{len(full_insert_list)} total new records")
    logger.debug(f"{len(full_amend_list)} total amended records")

    # Write out both lists
    insert_path = utils.WARN_TRANSFORMER_OUTPUT_DIR / "processed" / "additions.csv"
    with open(insert_path, "w") as fh:
        if full_insert_list:
            logger.debug(f"Writing {len(full_insert_list)} records to {insert_path}")
            writer = csv.DictWriter(fh, full_insert_list[0].keys())
            writer.writeheader()
            writer.writerows(full_insert_list)

    amend_path = utils.WARN_TRANSFORMER_OUTPUT_DIR / "processed" / "amendments.csv"
    with open(amend_path, "w") as fh:
        if full_amend_list:
            logger.debug(f"Writing {len(full_amend_list)} records to {amend_path}")
            writer = csv.DictWriter(fh, full_amend_list[0].keys())
            writer.writeheader()
            writer.writerows(full_amend_list)

    # Create a new list to store everything
    integrated_list: typing.List[typing.Dict[str, typing.Any]] = []

    # Create a lookup of the current amended records that links them their likely replacements
    amend_lookup = {d["current"]["hash_id"]: d["new"] for d in full_amend_list}

    # Get the current timestamp to mark the updates we make in this run
    now = datetime.now(timezone.utc)

    # Loop through everything in the current database
    for current_row in current_data_list:
        # If this is an amended row ...
        if current_row["hash_id"] in amend_lookup:
            # Pull out the new record from the our lookup
            amended_row = amend_lookup[current_row["hash_id"]]

            # Link it to its likely ancestor
            amended_row["is_amendment"] = True
            amended_row["is_superseded"] = False
            amended_row["likely_ancestor"] = current_row["hash_id"]

            # Update is metadata
            amended_row["first_inserted_date"] = current_row["first_inserted_date"]
            amended_row["last_updated_date"] = now
            amended_row["estimated_amendments"] = (
                current_row["estimated_amendments"] + 1
            )

            # Add it to the new integrated database
            integrated_list.append(amended_row)

            # Mark the current record as superseded
            # This allows it to be excluded circumstances where we only want unique records
            # But without deleting it entirely
            current_row["is_superseded"] = True

            # Add it to the integrated database
            integrated_list.append(current_row)

        # If the current row is not amended ...
        else:
            # If these field haven't already been filled in, nope 'em
            if "is_superseded" not in current_row.keys():
                current_row["is_superseded"] = False
            if "is_amendment" not in current_row.keys():
                current_row["is_amendment"] = False
            # Then we just keep what we got
            integrated_list.append(current_row)

    # Now insert the new records with today's timestamp
    for new_row in full_insert_list:
        new_row["first_inserted_date"] = now
        new_row["last_updated_date"] = now
        new_row["estimated_amendments"] = 0
        new_row["is_superseded"] = False
        new_row["is_amendment"] = False
        integrated_list.append(new_row)

    # And sort everything in reverse chronological order
    sorted_list = sorted(
        integrated_list,
        key=itemgetter("last_updated_date", "first_inserted_date", "notice_date"),
        reverse=True,
    )

    # Finally, write out what we got
    integrated_path = utils.WARN_TRANSFORMER_OUTPUT_DIR / "processed" / "integrated.csv"
    logger.debug(f"Writing {len(integrated_list)} records to {integrated_path}")
    with open(integrated_path, "w") as fh:
        fieldnames = [
            "hash_id",
            "first_inserted_date",
            "notice_date",
            "effective_date",
            "postal_code",
            "company",
            "location",
            "jobs",
            "is_closure",
            "is_temporary",
            "is_superseded",
            "is_amendment",
            "likely_ancestor",
            "estimated_amendments",
            "last_updated_date",
        ]
        writer = csv.DictWriter(fh, fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(sorted_list)

    # And return the path
    return integrated_path


def is_similar_string(s1, s2):
    """Evaluate whether we consider the two strings close enough to be likely variations.

    Args:
        s1 (str): The first string.
        s2 (str): The second string.

    Returns True or False.
    """
    return jellyfish.jaro_winkler_similarity(s1, s2) > 0.95


def is_similar_date(d1, d2):
    """Evaluate whether we consider the two date strings close enough to be likely variations.

    Args:
        d1 (str): The first string.
        d2 (str): The second string.

    Returns True or False.
    """
    return jellyfish.levenshtein_distance(d1, d2) <= 3


def get_likely_ancestor(
    new_row: typing.Dict[str, typing.Any], current_data: typing.List
) -> typing.Optional[typing.Dict[str, typing.Any]]:
    """Determine if the provided new row has a likely parent in the current dataset.

    Args:
        new_row (dict): A record from the new dataset believed to contain a change to the current dataset.
        current_data (list): All of the records in the current dataset for comparison

    Returns:
        The record in the current data judged most likely to be the ancestor of the new record.
        Returns None if the record is estimated to be new.
    """
    # Check our key fields against everything in the dataset
    likely_match_list = []
    for current_row in current_data:
        # Check the company names
        if not is_similar_string(new_row["company"], current_row["company"]):
            continue

        # Check the notice date
        if not is_similar_date(new_row["notice_date"], current_row["notice_date"]):
            continue

        # Check the effective date, if it exists
        if new_row["effective_date"] and current_row["effective_date"]:
            if not is_similar_date(
                new_row["effective_date"], current_row["effective_date"]
            ):
                continue

        # Check the location, if it exists
        if new_row["location"] and current_row["location"]:
            if not is_similar_string(new_row["location"], current_row["location"]):
                continue

        # Whatever is left we keep
        likely_match_list.append(current_row)

    # If there's nothing, return None
    if not likely_match_list:
        return None

    # If there is more than one likely match, we are going to log out
    if len(likely_match_list) > 1:
        # Log here. Might do more later.
        logger.debug("New row has more than one likely match")
        logger.debug(f"New row: {json.dumps(new_row, indent=2, default=str)}")
        logger.debug(
            f"Likely matches: {json.dumps(likely_match_list, indent=2, default=str)}"
        )

    # For now we just return the first one
    return likely_match_list[0]


def get_current_data(init: bool = False) -> typing.List[typing.Dict[str, typing.Any]]:
    """Fetch the most recent published version of our integrated dataset.

    Args:
        init (bool): Set to True when you want to create a new integrated dataset from scratch. Default False.

    Returns a list of dictionaries ready for comparison against the new consolidated data file.
    """
    # Set which file to pull
    base_url = "https://raw.githubusercontent.com/biglocalnews/warn-github-flow/transformer/data/warn-transformer/processed/"
    if init:
        current_url = f"{base_url}consolidated.csv"
        logger.debug(f"Initializing new current file from {current_url}")
    else:
        current_url = f"{base_url}integrated.csv"
        logger.debug(f"Downloading most recent current file from {current_url}")

    # Download the current database
    current_r = requests.get(current_url)
    current_data_str = current_r.content.decode("utf-8")

    # Read in the current database
    current_data_reader = csv.DictReader(current_data_str.splitlines(), delimiter=",")
    current_data_list: typing.List[typing.Dict[str, typing.Any]] = list(
        current_data_reader
    )

    # Get the current timestamp to mark the updates we make in this run
    now = datetime.now(timezone.utc)

    # If we're initializing a new dataset, we'll need to fill in the extra
    # fields custom to the integrated set.
    if init:
        for row in current_data_list:
            row["first_inserted_date"] = now
            row["last_updated_date"] = now
            row["estimated_amendments"] = 0
    else:
        for row in current_data_list:
            # Otherwise we'll want to parse a few data types for later use
            row["last_updated_date"] = datetime.fromisoformat(row["last_updated_date"])
            row["first_inserted_date"] = datetime.fromisoformat(
                row["first_inserted_date"]
            )
            row["estimated_amendments"] = int(row["estimated_amendments"])

    # Return the list
    logger.debug(f"{len(current_data_list)} records downloaded from current database")
    return current_data_list


def get_changed_data(
    new_data: typing.DefaultDict[str, typing.List],
    current_data: typing.DefaultDict[str, typing.List],
) -> typing.DefaultDict[str, typing.List]:
    """Determine which rows in a new data file are different from the current dataset.

    Args:
        new_data (dict): A dictionary keyed by postal code. Each value is a list of all records from that source.
        current_data (dict): A dictionary keyed by postal code. Each value is a list of all records from that source.

    Returns a dictionary keyed by postal code. Each value is a list of all records with that value deemed to have changed.
    """
    changed_dict = defaultdict(list)
    for postal_code, new_row_list in new_data.items():
        logger.debug(f"Inspecting {len(new_row_list)} new records from {postal_code}")

        # Pull the current rows from the source
        current_row_list = current_data[postal_code]
        logger.debug(
            f"Comparing against {len(current_row_list)} records from the current database"
        )

        # Loop through the rows in this source
        for new_row in new_row_list:
            # Identify new rows that are identical to a record in the current database
            if not any(
                r for r in current_row_list if r["hash_id"] == new_row["hash_id"]
            ):
                # If not, it's either a new record or an amendment.
                # So it goes in our change list
                changed_dict[postal_code].append(new_row)

        # Log where we stand
        change_list = changed_dict[postal_code]
        logger.debug(
            f"{len(change_list)} changed rows ({round((len(change_list)/len(new_row_list))*100, 2)}%)"
        )

    # Pass it out
    return changed_dict


def regroup_by_source(data_list: typing.List) -> typing.DefaultDict[str, typing.List]:
    """Regroup the provided list by its source field.

    Args:
        data_list: A list of dictionaries presumed to have a "postal_code" field.

    Returns: A dictionary keyed by postal code. Each value is a list of all records with that value.
    """
    regrouped_dict = defaultdict(list)
    for row in data_list:
        regrouped_dict[row["postal_code"]].append(row)
    return regrouped_dict


def flatten_grouped_data(grouped_data: typing.Dict[str, typing.List]):
    """Flatten a dictionary of data grouped by source down to a single list.

    Args:
        grouped_data (dict): The grouped data

    Returns a list of the data for all sources
    """
    return list(chain(*grouped_data.values()))


if __name__ == "__main__":
    run()
