from pathlib import Path

import click

from . import consolidate as consolidate_runner
from . import download as download_runner
from . import utils


@click.group()
def cli():
    """Consolidate, enrich and republish the data gathered by warn-scraper."""
    pass


@cli.command()
@click.option(
    "--download-dir",
    default=utils.WARN_TRANSFORMER_OUTPUT_DIR / "raw",
    type=click.Path(),
    help="The Path were the results will be downloaded",
)
def download(download_dir: Path):
    """Download all the CSVs in the WARN Notice project on biglocalnews.org."""
    download_runner.run(download_dir)


@cli.command()
@click.option(
    "--input-dir",
    default=utils.WARN_TRANSFORMER_OUTPUT_DIR / "raw",
    type=click.Path(),
    help="The Path were the raw files results are located",
)
def consolidate(input_dir: Path):
    """Consolidate raw data using a common data schema."""
    consolidate_runner.run(input_dir)


if __name__ == "__main__":
    cli()
