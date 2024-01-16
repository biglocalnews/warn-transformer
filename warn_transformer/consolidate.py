import csv
import logging
import typing
from importlib import import_module
from pathlib import Path

from . import utils

logger = logging.getLogger(__name__)


def run(
    input_dir: Path = utils.WARN_TRANSFORMER_OUTPUT_DIR / "raw",
    source: typing.Optional[str] = None,
) -> Path:
    """Consolidate raw data using a common data schema.

    Args:
        input_dir (Path): The directory where our raw data files are stored.
        source (string): The slug of a source you'd like to transform as a one-off (optional)

    Returns: The path to our consolidated comma-delimited file.
    """
    logging.basicConfig(level="DEBUG", format="%(asctime)s - %(name)s - %(message)s")

    # Get all of the transformers
    transformer_list = utils.get_all_transformers()
    logger.info(f"Consolidating {len(transformer_list)} sources")

    # If a source is provided, limit the list
    if source:
        transformer_list = [t for t in transformer_list if source.lower() in t.lower()]

    # Loop through them
    obj_list = []
    for t in transformer_list:
        # Get the module
        module = import_module(f"warn_transformer.transformers.{t}")

        # Transform the data
        source_list = module.Transformer(input_dir).transform()
        if len(source_list) <= 3:
            logger.warning(
                f"{t.upper()} data quality problem: {len(source_list):,} items found."
            )
        else:
            logger.debug(f"{t.upper()} data {len(source_list):,} items found.")

        # Add it to the master list
        obj_list += source_list

    # Drop duplicates by using the hash as a unique identifer
    unique_list = list({d["hash_id"]: d for d in obj_list}.values())
    logger.debug(f"Dropped {len(obj_list) - len(unique_list)} duplicates")

    # Get the output directory
    processed_dir = utils.WARN_TRANSFORMER_OUTPUT_DIR / "processed"
    if not processed_dir.exists():
        processed_dir.mkdir(parents=True)

    # Output a consolidated CSV
    consolidated_path = processed_dir / "consolidated.csv"
    logger.debug(f"Writing {len(unique_list)} records to {consolidated_path}")
    with open(consolidated_path, "w") as fh:
        writer = csv.DictWriter(fh, unique_list[0].keys())
        writer.writeheader()
        writer.writerows(unique_list)

    # Return the path
    return consolidated_path


if __name__ == "__main__":
    run()
