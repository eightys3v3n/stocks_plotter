import datetime
from copy import copy
from queue import Queue


def list_files(root, recursive=True):
    files = []
    to_search = Queue()
    to_search.put(root)

    while not to_search.empty():
        path = to_search.get()
        for p in path.iterdir():
            if p.is_file() and not p.is_symlink():
                files.append(p)
            elif recursive and p.is_dir():
                to_search.put(p)
    return files


def get_date_range(accounts):
    """Returns a min and max date for the {act: {date: [Transaction]}} array given"""
    min_date = None
    max_date = None
    
    for act, date_trans in accounts.items():
        for date, trans in date_trans.items():
            if min_date is None:
                min_date = date
            elif min_date > date:
                min_date = date

            if max_date is None:
                max_date = date
            elif max_date < date:
                max_date = date
    return min_date, max_date


def day_range(start, end):
    """Returns a list of date objects containing every day between the start and end dates (inclusive)"""
    if end < start: return None

    diff = end - start
    dates = []

    for d in range(diff.days+1):
        dates.append(start + datetime.timedelta(days=d))

    return dates


def create_total(act_bals):
    """Creates a new account, "total", that is the sum of all other accounts."""
    totals = {}
    for act, dates in act_bals.items():
        for date, bal in dates.items():
            if date in totals:
                totals[date] += bal
            else:
                totals[date] = bal
    act_bals["total"] = totals
