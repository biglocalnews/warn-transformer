import csv

from . import utils
from .schema import WarnNoticeSchema
from .transformers.ak import Transformer


def main():
    """Consolidate raw data using a common data schema."""
    # Get downloaded files
    raw_dir = utils.OUTPUT_DIR / "raw"
    csv_list = list(raw_dir.glob("*.csv"))

    # For now, pluck out Iowa
    ak = next(c for c in csv_list if "ak.csv" in str(c))

    # Open the csv
    with open(ak) as fh:
        reader = csv.DictReader(fh)
        raw_data = Transformer(reader)

    # Transform the data
    transformed_data = raw_data.transform()

    # Load the records into the schema
    obj_list = []
    for row in transformed_data:
        schema = WarnNoticeSchema()
        obj = schema.load(row)
        obj_list.append(obj)

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
