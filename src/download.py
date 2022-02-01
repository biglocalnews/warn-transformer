import os

from bln.client import Client

from . import utils

BLN_API_KEY = os.getenv("BLN_API_KEY")
BLN_PROJECT_ID = os.getenv("BLN_PROJECT_ID")


def main():
    """Download all the CSVs in the WARN Notice project on biglocalnews.org."""
    c = Client(BLN_API_KEY)
    if not utils.OUTPUT_DIR.exists():
        utils.OUTPUT_DIR.mkdir(parents=True)
    c.download_file(BLN_PROJECT_ID, 'ia.csv', output_dir=utils.OUTPUT_DIR)


if __name__ == "__main__":
    main()