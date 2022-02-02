import logging
import os

from bln.client import Client

from . import utils

BLN_API_KEY = os.getenv("BLN_API_KEY")
BLN_PROJECT_ID = os.getenv("BLN_PROJECT_ID")

logger = logging.getLogger(__name__)


def main():
    """Download all the CSVs in the WARN Notice project on biglocalnews.org."""
    logging.basicConfig(level="DEBUG", format="%(asctime)s - %(name)s - %(message)s")

    # Login to BLN.
    c = Client(BLN_API_KEY)

    # Get the Warn Act Notices project.
    p = c.get_project_by_name("WARN Act Notices")

    # Get all the files in the project.
    file_list = [f["name"] for f in p["files"]]

    # Make the download directory, if it doesn't already exist.
    download_dir = utils.WARN_ANALYSIS_OUTPUT_DIR / "raw"
    if not download_dir.exists():
        download_dir.mkdir(parents=True)

    # Download all the files.
    for f in file_list:
        logger.debug(f"Download {f} to {download_dir}")
        c.download_file(BLN_PROJECT_ID, f, output_dir=download_dir)


if __name__ == "__main__":
    main()
