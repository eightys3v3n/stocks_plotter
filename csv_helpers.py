import csv
import datetime
from path import Path
    

def read_csv(path, parser=None):
    """Read and parse all rows in a given file path."""
    reader = csv.reader(open(path, 'r'))
    data = []
    for row in reader:
        if parser is not None:
            row = parser(row)
        data.append(row)
    return data
