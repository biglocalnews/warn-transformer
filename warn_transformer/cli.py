import logging
import typing
from pathlib import Path

import click

from . import consolidate as consolidate_runner
from . import download as download_runner
from . import integrate as integrate_runner
from . import utils
from . import validate as validate_runner


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
@click.option(
    "--log-level",
    "-l",
    default="INFO",
    type=click.Choice(
        ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"), case_sensitive=False
    ),
    help="Set the logging level",
)
def download(
    download_dir: Path, source: typing.Optional[str] = None, log_level: str = "INFO"
):
    """Download all the CSVs in the WARN Notice project on biglocalnews.org."""
    logging.getLogger("urllib3").setLevel(logging.ERROR)
    logging.basicConfig(level=log_level, format="%(asctime)s - %(name)s - %(message)s")
    logger = logging.getLogger(__name__)
    logger.debug("Running download command")
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
@click.option(
    "--log-level",
    "-l",
    default="INFO",
    type=click.Choice(
        ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"), case_sensitive=False
    ),
    help="Set the logging level",
)
def consolidate(
    input_dir: Path, source: typing.Optional[str] = None, log_level: str = "INFO"
):
    """Consolidate raw data using a common data schema."""
    logging.basicConfig(level=log_level, format="%(asctime)s - %(name)s - %(message)s")
    logger = logging.getLogger(__name__)
    logger.debug("Running consolidate command")
    consolidate_runner.run(input_dir, source)


@cli.command()
@click.option(
    "--input-dir",
    default=utils.WARN_TRANSFORMER_OUTPUT_DIR / "processed" / "consolidated.csv",
    type=click.Path(),
    help="The Path were the new results are located",
)
@click.option(
    "--init",
    default=False,
    is_flag=True,
)
@click.option(
    "--log-level",
    "-l",
    default="INFO",
    type=click.Choice(
        ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"), case_sensitive=False
    ),
    help="Set the logging level",
)
def integrate(input_dir: Path, init: bool = False, log_level: str = "INFO"):
    """Integrate the latest consolidated data with the current database."""
    logging.getLogger("urllib3").setLevel(logging.ERROR)
    logging.basicConfig(level=log_level, format="%(asctime)s - %(name)s - %(message)s")
    logger = logging.getLogger(__name__)
    logger.debug("Running integrate command")
    integrate_runner.run(input_dir, init_current_data=init)


@cli.command()
@click.option(
    "--input-dir",
    default=utils.WARN_TRANSFORMER_OUTPUT_DIR / "raw",
    type=click.Path(),
    help="The Path where data to validate is located",
)
@click.option(
    "--stage",
    default="raw",
    type=click.Choice(("raw",)),
    help="The stage of the data to validate.",
)
@click.option(
    "--log-level",
    "-l",
    default="INFO",
    type=click.Choice(
        ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"), case_sensitive=False
    ),
    help="Set the logging level",
)
def validate(input_dir: Path, stage: str = "raw", log_level: str = "INFO"):
    """Validate the specified data."""
    logging.getLogger("urllib3").setLevel(logging.ERROR)
    logging.basicConfig(level=log_level, format="%(asctime)s - %(name)s - %(message)s")
    logger = logging.getLogger(__name__)
    logger.debug("Running validate command")
    validate_runner.run(input_dir, stage)


if __name__ == "__main__":
    cli()
