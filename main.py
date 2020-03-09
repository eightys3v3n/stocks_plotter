from collections import defaultdict
from pathlib import Path
from statements import get_statements
from translations import *
from plot import plot
import datetime


def date_range(accounts):
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
    if end <= start: return 0

    diff = end - start
    dates = []

    for d in range(diff.days+1):
        dates.append(start + datetime.timedelta(days=d))

    return dates


def most_recent_bal_before(date, date_trans):
    """
    Returns the most recent balance <= the given date or None.
    That means, the first date before the given date, and the last transaction in that list.

    date_trans: {datetime.date: [Transaction]}
    """
    dates_before = []
    for d, trans in date_trans.items():
        if d < date:
            dates_before.append((d, trans))
    dates_before.sort()
    
    bal_af = None
    while len(dates_before) > 0:
        trans_before = dates_before.pop()[1]
        
        while bal_af is None:
            bal_af = trans_before.pop().bal_af
        
    return bal_af


def deduce_date(date, date_trans):
    pass


def daily_balances(act_dates):
    """Returns the balance at a daily interval."""
    dates = day_range(*date_range(act_dates))
    daily = {}
    
    for act, date_trans in act_dates.items():
        daily[act] = {}
        for date in dates:
            if date in date_trans:
                daily[act][date] = deduce_balance(date, date_trans)
            else:
                daily[act][date] = date_trans[date][-1]
    return daily


def main():
    transactions = get_statements(Path("statements"))
    # [Transaction, ...]

    dates = daily_date_list(*date_range(transactions))

    accounts = act_wise(transactions)
    # {act: [Transaction, ...]}

    act_date = date_wise(accounts)
    # {act: {date: [Transaction, ...]}}

    act_date = fill_balances(act_dates)

    plot(act_date)


if __name__ == '__main__':
    main()


"""
        def test_seperate_acts(self):
        trans = [Transaction("1"), Transaction("2"), Transaction("2")]
        acts = seperate_acts(trans)
        self.assertEqual(list(acts.keys()), ["1", "2"])
        self.assertEqual(len(acts["1"]), 1)
        self.assertEqual(len(acts["2"]), 2)
        """
