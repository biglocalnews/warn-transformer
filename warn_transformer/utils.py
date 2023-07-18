import os
import typing
from pathlib import Path

USER_DIR = Path(os.path.expanduser("~"))
DEFAULT_WARN_TRANSFORMER_OUTPUT_DIR = USER_DIR / ".warn-transformer"

WARN_TRANSFORMER_OUTPUT_DIR = Path(
    os.environ.get("WARN_TRANSFORMER_OUTPUT_DIR", DEFAULT_WARN_TRANSFORMER_OUTPUT_DIR)
)


def get_all_transformers() -> typing.List[str]:
    """Get all the states and territories that have scrapers.

    Returns: List of lower-case post abbreviations.
    """
    this_dir = Path(__file__).parent
    transformers_dir = this_dir / "transformers"
    return sorted(
        p.stem for p in transformers_dir.glob("*.py") if "__init__.py" not in str(p)
    )
