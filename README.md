# warn-analysis
Analysis and data quality checks related to WARN data

### `standardize_field_names.py`
This file is the first in the data cleaning process for WARN exports. It takes as input each state's WARN data `.csv` files from the `.warnscraper\exports\` directory and outputs a single field-standardized `.csv` file in the `.warnscraper\` directory, `standardize_field_names.csv`. This effectively merges all the state data into one nation-wide WARN database. 

### `standardize_dates.py`
This file continues the data cleaning process, taking in the output from the previous file, `standardize_field_names.csv`, abd outputting a version with a standardized date formatting.

**TODO**: determine a consistent date standard (how about DD/MM/YYYY?)
