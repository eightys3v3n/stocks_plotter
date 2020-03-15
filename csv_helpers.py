import csv
import datetime
from path import Path
    

def read_csv(path, parser=None):
    """Read and parse all rows in a given file path."""
    reader = csv.reader(open(path, 'r'))
    data = []
    for i, row in enumerate(reader):
        if parser is not None:
            row = parser(i, row)
        data.append(row)
    return data
