# A plotting program

This program is intended to be used as a framework for comparing plots from various data sets against
currencies/stocks to identify predicting data sets. There are modules that have a load() function.
This load function takes the file path to load, and possibly some other arguments. Much of this source
code was borrowed from my word_processing program.

## Getting started
Install plotly, run main.py.
To update the information, replace the CSV files in csv_files/ with their corresponding files.

## Modules
### Yahoo Finance
This module will import data downloaded from Yahoo Finance. The load function takes a min and max
value that are the estimated min and max of the data. This allows for the data to be scaled to a
common range for easier comparison.

### Big Query
This module imports CSV data in the form of `YYYY-mm-dd,price`. It was used to get the activity on
the /r/xrp subreddit. The query and url used are in the header of the file.

