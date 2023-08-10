import logging
import os
import typing
from pathlib import Path

from bln.client import Client

from . import utils

BLN_API_KEY = os.getenv("BLN_API_TOKEN")
BLN_PROJECT_ID = "UHJvamVjdDpiZGM5NmU1MS1kMzBhLTRlYTctODY4Yi04ZGI4N2RjMzQ1ODI="

logger = logging.getLogger(__name__)


def run(
    download_dir: Path = utils.WARN_TRANSFORMER_OUTPUT_DIR / "raw",
    source: typing.Optional[str] = None,
):
    """Download all the CSVs in the WARN Notice project on biglocalnews.org.

    Args:
        download_dir (Path): The directory where files will be downloaded.
        source (str): The postal code of the source to download. Default is all sources.
    """
    logging.basicConfig(level="DEBUG", format="%(asctime)s - %(name)s - %(message)s")

    # Login to BLN.
    c = Client(BLN_API_KEY)

    # Get the Warn Act Notices project.
    p = c.get_project_by_name("WARN Act Notices")

    # Get all the files in the project.
    file_list = [f["name"] for f in p["files"]]

    # If a source is provided, limit the list
    if source:
        file_list = [f for f in file_list if source.lower() in f.lower()]
        if len(file_list) == 0:
            logger.debug(f"No source '{source}' found")

    # Make the download directory, if it doesn't already exist.
    if not download_dir.exists():
        download_dir.mkdir(parents=True)

    # Download all the files.
    for i, f in enumerate(sorted(file_list)):
        logger.debug(
            f"Download {f} to {download_dir} as file {i+1:02d} of {len(file_list):02d}"
        )
        c.download_file(BLN_PROJECT_ID, f, output_dir=download_dir)


if __name__ == "__main__":
    run()
