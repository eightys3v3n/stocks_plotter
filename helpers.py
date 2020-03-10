import datetime
from copy import copy
from translations import *
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


def most_recent_bal_before(date, date_trans):
    """
    Returns the most recent balance < the given date or None.
    That means, the first date before the given date, and the last transaction in that list.

    date_trans: {datetime.date: [Transaction]}
    """
    dates_before = []
    for d, trans in date_trans.items():
        if d < date:
            dates_before.append((d, copy(trans)))
    dates_before.sort()
    
    bal_af = None
    while bal_af is None and len(dates_before) > 0:
        trans_before = dates_before.pop()[1]
        
        while bal_af is None and len(trans_before) > 0:
            bal_af = trans_before.pop().bal_af
            
    return bal_af


def deduce_balance(date, date_trans):
    """
    Given a date and a bunch of transactions, this will return the last balance before the given date.

    input(date_trans): {date: [Transaction]}
    output: balance on that date
    """
    
    recent_bal = most_recent_bal_before(date, date_trans)
    
    if recent_bal is not None: # there was a previous balance, so it carries to this day.
        return recent_bal

    # there are no transactions before the given date.
    return 0


def daily_balances(act_dates):
    """Returns the balance at a daily interval."""
    dates = day_range(*get_date_range(act_dates))
    daily = {}

    for act, date_trans in act_dates.items():
        daily[act] = {}
        for date in dates:
            if date in date_trans:
                daily[act][date] = date_trans[date][-1].bal_af
            else:
                daily[act][date] = deduce_balance(date, date_trans)
    return daily


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


def apply_aliases(act_bals, aliases):
    """Renames accounts present in act_bals and aliases according to the aliases dictionary."""
    new_act_bals = {}
    for act, date_bals in act_bals.items():
        if act in aliases:
            act = aliases[act]
        new_act_bals[act] = date_bals
    return new_act_bals
