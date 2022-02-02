import csv

from . import utils
from .transformers.ia import Transformer


def main():
    """Consolidate raw data using a common data schema."""
    # Transform the data
    obj_list = Transformer().transform()

    # Output what we got
    processed_dir = utils.OUTPUT_DIR / "processed"
    if not processed_dir.exists():
        processed_dir.mkdir(parents=True)

    consolidated_path = processed_dir / "consolidated.csv"
    with open(consolidated_path, "w") as fh:
        writer = csv.DictWriter(fh, obj_list[0].keys())
        writer.writeheader()
        writer.writerows(obj_list)


if __name__ == "__main__":
    main()
