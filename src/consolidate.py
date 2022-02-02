import csv
from importlib import import_module
import logging

from . import utils
from .transformers.ia import Transformer

logger = logging.getLogger(__name__)


def main():
    """Consolidate raw data using a common data schema."""
    logging.basicConfig(level="DEBUG", format="%(asctime)s - %(name)s - %(message)s")

    # Get all of the transformers
    transformer_list = utils.get_all_transformers()
    logger.info(f"Consolidating {len(transformer_list)} sources")

    # Loop through them
    for t in transformer_list:
        # Get the module
        module = import_module(f"src.transformers.{t}")

        # Transform the data
        obj_list = module.Transformer().transform()

    # Get the output directory
    processed_dir = utils.WARN_ANALYSIS_OUTPUT_DIR / "processed"
    if not processed_dir.exists():
        processed_dir.mkdir(parents=True)

    # Output a consolidated CSV
    consolidated_path = processed_dir / "consolidated.csv"
    logger.debug(f"Writing to {consolidated_path}")
    with open(consolidated_path, "w") as fh:
        writer = csv.DictWriter(fh, obj_list[0].keys())
        writer.writeheader()
        writer.writerows(obj_list)


if __name__ == "__main__":
    main()
