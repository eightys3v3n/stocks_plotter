import datetime, csv_helpers
from collections import defaultdict
from helpers import *
from pathlib import Path


"""Export from Yahoo Finance"""


def parse_csv_row(i, row):
    """Turn a CSV row from an XRP/USD CSV into Python objects."""
    n_row = []
    for c in row:
        c = c.strip()
        if c == "": c = None
        n_row.append(c)

    try:
        n_row[0] = datetime.datetime.strptime(n_row[0], "%Y-%m-%d").date()
    except ValueError as e:
        print("Invalid date in row: '{}'".format(n_row[0]))
        return ()

    if n_row[1]:
        n_row[1] = float(n_row[1])
    
    return tuple(n_row)


def read_csv(path):
    """Read a given CSV file into a list of Transaction objects."""
    csv = csv_helpers.read_csv(path, parser=parse_csv_row)
    prices = []
    for row in csv:
        if len(row) > 0:
            prices.append(row)
    return prices


def map_price_range(prices, min, max):
    """prices: [(date, price)]"""
    min_p, max_p = min_max_prices(prices)
    n_prices = map(
        lambda row:
            (row[0], map_range((min, max), (0, 100), row[1])),
        prices)
    return n_prices


def load(path, name, min=0, max=100):
    prices = read_csv(Path(path))
    # [(date, num_comments+num_posts)]

    prices = map_price_range(prices, min, max)

    bals = {date: activity for date, activity in prices}
    act_bals = {name: bals}
    # {act_name: {date: close_price}}
    
    return act_bals
