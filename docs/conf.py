import os
import sys
from datetime import datetime

# Insert the parent directory into the path
sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath("./"))

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinxcontrib.napoleon",
    "sphinx_click",
]
templates_path = ["_templates"]
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
master_doc = "index"

project = "warn-transformer"
year = datetime.now().year
copyright = f"{year} Big Local News"

exclude_patterns = ["_build"]

pygments_style = "sphinx"
