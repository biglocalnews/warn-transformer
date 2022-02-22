import typing
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
@click.option(
    "--source",
    default=None,
    help="The source to download. Default is all sources.",
)
def download(download_dir: Path, source: typing.Optional[str] = None):
    """Download all the CSVs in the WARN Notice project on biglocalnews.org."""
    download_runner.run(download_dir, source)


@cli.command()
@click.option(
    "--input-dir",
    default=utils.WARN_TRANSFORMER_OUTPUT_DIR / "raw",
    type=click.Path(),
    help="The Path were the raw files results are located",
)
@click.option(
    "--source",
    default=None,
    help="The source to download. Default is all sources.",
)
def consolidate(input_dir: Path, source: typing.Optional[str] = None):
    """Consolidate raw data using a common data schema."""
    consolidate_runner.run(input_dir, source)


if __name__ == "__main__":
    cli()
