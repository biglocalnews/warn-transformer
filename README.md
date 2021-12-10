# warn-analysis
Analysis and data quality checks related to WARN data

As of 12/2021, this is the order that files should be run in for analysis: standardize_field_names.py => standardize_dates.py

Then run merge_warn_ppp.ipny if you would like WARN x PPP analysis.

### `standardize_field_names.py`
Input: each state's WARN data `.csv` files from the `.warnscraper\exports\` directory
Output: `standardize_field_names.csv`, a single standardized & merged `.csv` file of all scraped states

### `standardize_dates.py`
Input: `standardize_field_names.csv`
Output: `standardize_dates.csv`
This program adds 5 additional columns to the data: 
+ (1) date_received_cleaned
+ (2) date_received_year
+ (3) date_received_month
+ (4) date_layoff_cleaned
+ (5) date_closing_cleaned

### `merge_warn_ppp.ipny`
Input: `standardize_dates.csv`
Output: `merge_warn_ppp.csv`, an inner merge of WARN & PPP datasets

