import datetime, csv_helpers
from collections import defaultdict
from transaction import Transaction
from helpers import *
from pathlib import Path


def parse_csv_row(row):
    """Turn a CSV row from a First Calgary statement into Python objects"""
    n_row = []
    for c in row:
        c = c.strip()
        if c == "": c = None

        n_row.append(c)

    try:
        n_row[1] = datetime.datetime.strptime(n_row[1], "%d-%b-%Y").date()
    except ValueError as e:
        print("Invalid date in row: '{}'".format(n_row[1]))
        return ()

    if n_row[4]:
        n_row[4] = float(n_row[4])
    elif n_row[5]:
        n_row[5] = float(n_row[5])
    
    if n_row[6]:
        n_row[6] = float(n_row[6])

    return tuple(n_row)


def parse_trans(row):
    """Turn a CSV row from a First Calgary statement into a Transaction object."""
    if row[4]:
        amt = -row[4]
    elif row[5]:
        amt = row[5]
    else:
        amt = None

    return Transaction(act=row[0],
                       date=row[1],
                       desc=row[2],
                       amt=amt,
                       bal_af=row[6])


def read_trans(path):
    """Read a given CSV file into a list of Transaction objects."""
    csv = csv_helpers.read_csv(path, parser=parse_csv_row)
    trans = []
    for row in csv:
        trans.append(parse_trans(row))
    return trans


def read_statements(path):
    """Read all CSV files in given path into a single list of Transaction objects."""
    files = list_files(path)
    trans = []

    for f in files:
        trans.extend(read_trans(f))

    return trans


def unique_trans(trans):
    trans = list(set(trans))
    return trans


def get_statements(path):
    """Given a path, read all the CSV files within and return {act: [Transaction, ...]} containing all the unique transactions."""
    trans = read_statements(path)
    trans = unique_trans(trans)
    return trans


def load():
    transactions = get_statements(Path("statements/first_calgary"))
    # [Transaction]

    accounts = act_wise(transactions)
    # {act: [Transaction]}

    act_date = date_wise(accounts)
    # {act: {date: [Transaction]}}

    act_bals = daily_balances(act_date)
    # {act: {date: balance}}
    
    return act_bals
