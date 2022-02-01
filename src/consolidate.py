import csv
from datetime import datetime

from . import utils
from .schema import WarnNoticeSchema


def _parse_dates(value):
    value = value.strip()
    try:
        dt = datetime.strptime(value, "%m/%d/%Y")
    except ValueError:
        return None
    return str(dt.date())


def _parse_jobs(value):
    try:
        return int(value)
    except ValueError:
        return None


def main():
    """Consolidate raw data using a common data schema."""
    # Get downloaded files
    raw_dir = utils.OUTPUT_DIR / "raw"
    csv_list = list(raw_dir.glob("*.csv"))

    # For now, pluck out Iowa
    ia = next(c for c in csv_list if "ia.csv" in str(c))

    # Open the csv
    with open(ia) as fh:
        reader = csv.DictReader(fh)
        row_list = list(reader)

    # Load the records into the schema
    obj_list = []
    for row in row_list:
        # Skip empty rows
        if not row["Company"]:
            continue

        # Load data into schema
        schema = WarnNoticeSchema()
        data = dict(
            state="IA",
            company=row["Company"],
            date=_parse_dates(row["Notice Date"]),
            jobs=_parse_jobs(row["Emp #"]),
        )
        obj = schema.load(data)

        # Add standardized record to list
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
