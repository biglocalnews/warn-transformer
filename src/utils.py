import os
from pathlib import Path


USER_DIR = Path(os.path.expanduser("~"))
DEFAULT_OUTPUT_DIR = USER_DIR / ".warn-analysis"

OUTPUT_DIR = Path(os.environ.get("OUTPUT_DIR", DEFAULT_OUTPUT_DIR))