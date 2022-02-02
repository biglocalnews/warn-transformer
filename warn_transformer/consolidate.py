import csv
from importlib import import_module
import logging
from pathlib import Path

from . import utils

logger = logging.getLogger(__name__)


def run(input_dir: Path = utils.WARN_ANALYSIS_OUTPUT_DIR / "raw") -> Path:
    """Consolidate raw data using a common data schema.

    Args:
        input_dir (Path): The directory where our raw data files are stored.

    Returns: The path to our consolidated comma-delimited file.
    """
    logging.basicConfig(level="DEBUG", format="%(asctime)s - %(name)s - %(message)s")

    # Get all of the transformers
    transformer_list = utils.get_all_transformers()
    logger.info(f"Consolidating {len(transformer_list)} sources")

    # Loop through them
    obj_list = []
    for t in transformer_list:
        # Get the module
        module = import_module(f"warn_transformer.transformers.{t}")

        # Transform the data
        source_list = module.Transformer(input_dir).transform()

        # Add it to the master list
        obj_list += source_list

    # Get the output directory
    processed_dir = utils.WARN_ANALYSIS_OUTPUT_DIR / "processed"
    if not processed_dir.exists():
        processed_dir.mkdir(parents=True)

    # Output a consolidated CSV
    consolidated_path = processed_dir / "consolidated.csv"
    logger.debug(f"Writing {len(obj_list)} records to {consolidated_path}")
    with open(consolidated_path, "w") as fh:
        writer = csv.DictWriter(fh, obj_list[0].keys())
        writer.writeheader()
        writer.writerows(obj_list)

    # Return the path
    return consolidated_path


if __name__ == "__main__":
    run()
