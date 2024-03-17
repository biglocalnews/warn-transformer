import logging
import os
from pathlib import Path

import great_expectations as gx
from great_expectations.core.expectation_configuration import ExpectationConfiguration

from . import utils

logger = logging.getLogger(__name__)


def run(
    input_dir: Path = utils.WARN_TRANSFORMER_OUTPUT_DIR / "raw",
    stage: str = "raw",
):
    """Validate data against a suite of validations.

    Args:
        input_dir (Path): The path to the directory containing the data to validate.
        stage (str): The stage of the data. Default is "raw".
    """
    logging.getLogger("great_expectations").setLevel(logging.ERROR)

    os.environ["GE_USAGE_STATS"] = "false"

    # create a Data Context object
    context = gx.get_context()

    expectation_suite_name = f"{stage}_expectation_suite"

    suite = context.add_or_update_expectation_suite(expectation_suite_name)

    source_min_row_count_expectation = ExpectationConfiguration(
        expectation_type="expect_table_row_count_to_be_between",
        kwargs={
            "min_value": 3,
        },
    )

    suite.add_expectation_configurations([source_min_row_count_expectation])

    context.save_expectation_suite(
        expectation_suite=suite, discard_failed_expectations=False
    )

    datasource = context.sources.add_pandas_filesystem(
        name=f"{stage}_data", base_directory=input_dir
    )

    asset = datasource.add_csv_asset(
        name=f"{stage}_data_asset",
        batching_regex=r"(?P<source>[^\.]+)\.csv",
        order_by=["source"],
    )

    batch_request = asset.build_batch_request()

    batch_list = asset.get_batch_list_from_batch_request(batch_request)

    validations = [
        {
            "batch_request": batch.batch_request,
            "expectation_suite_name": expectation_suite_name,
        }
        for batch in batch_list
    ]

    checkpoint = context.add_or_update_checkpoint(
        name=f"{stage}_checkpoint",
        validations=validations,
    )

    checkpoint.run()

    context.build_data_docs()
    context.open_data_docs()


if __name__ == "__main__":
    run()
