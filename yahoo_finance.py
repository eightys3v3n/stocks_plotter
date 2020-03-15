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
        if c == "null": c = None
        n_row.append(c)

    try:
        n_row[0] = datetime.datetime.strptime(n_row[0], "%Y-%m-%d").date()
    except ValueError as e:
        print("Invalid date in row: '{}'".format(n_row[0]))
        return ()

    if n_row[1]:
        n_row[1] = float(n_row[1])
    if n_row[2]:
        n_row[2] = float(n_row[2])
    if n_row[3]:
        n_row[3] = float(n_row[3])
    if n_row[4]:
        n_row[4] = float(n_row[4])
    if n_row[5]:
        n_row[5] = float(n_row[5])
    if n_row[6]:
        n_row[6] = float(n_row[6])
    
    return tuple(n_row)


def read_csv(path):
    """Read a given CSV file into a list of Transaction objects."""
    csv = csv_helpers.read_csv(path, parser=parse_csv_row)
    prices = []
    for row in csv:
        if len(row) > 0:
            prices.append(row)
    return prices


def adjust_scale(prices, scale):
    n_prices = []
    for price in prices:
        if all(p is not None for p in price):
            n_price = (price[0], *(p * scale for p in price[1:-1]), price[-1])
            n_prices.append(n_price)
    return n_prices


def power_prices(prices, power):
    n_prices = []
    for price in prices:
        if all(p is not None for p in price):
            n_price = (price[0], *(p**power for p in price[1:-1]), price[-1])
            n_prices.append(n_prices)
    return n_prices


def load(path, name, *, scale=None, power=False):
    prices = read_csv(Path(path))
    # [(date, open, high, low, close, adj_close, volume)]

    if scale is not None:
        prices = adjust_scale(prices, scale)
    if power:
        prices = power_prices(prices, power)

    bals = {date: close for date, open, high, low, close, adj_close, volume in prices}
    act_bals = {name: bals}
    # {act_name: {date: close_price}}
    
    return act_bals
