from collections import defaultdict
from pathlib import Path
from statements import get_statements
from plot import plot


def date_range(transactions):
    """Returns a min and max date for the transactions given"""
    min_date = None
    max_date = None
    for t in transactions:
        if min_date is None:
            min_date = t.date
        elif min_date > t.date:
            min_date = t.date

        if max_date is None:
            max_date = t.date
        elif max_date < t.date:
            max_date = t.date
    return min_date, max_date


def day_date_list(start, end):
    """Returns a list of date objects containing every day between the start and end (inclusive)"""
    if end <= start: return 0

    diff = end - start
    dates = []

    for d in range(diff.days):
        dates.append(start + timedelta(days=d))

    return dates


def date_wise(accounts):
    """Translates [Transaction, ...] to {date:Transaction, ...}"""
    accounts_date = {}
    for act, trans in accounts.items():
        dates_trans = defaultdict(lambda:[])
        for t in trans:
            dates_trans[t.date].append(t)
        accounts_date[act] = dates_trans
    return accounts_date


def most_recent_before(date, date_trans):
    """Returns the most recent balance <= the given date."""


def fill_balances(dates, date_trans):
    """Discover the balance for every given date."""
    pass


def fill_balances(plot_data):
    # [ [act, [dates], [bals]] ]
    dates = set()
    for act, dates, bals in plot_data:
        for d in dates:
            dates.add(d)


def seperate_acts(trans):
    """Takes in [Transaction, ...] and returns {act: [Transaction, ...]}."""
    acts = {}
    for t in trans:
        if t.act in acts:
            acts[t.act].append(t)
        else:
            acts[t.act] = [t,]
    return acts


def main():
    transactions = get_statements(Path("statements"))
    # [Transaction, ...]

    accounts = seperate_acts(transactions)
    # {act: [Transaction, ...]}

    act_date = date_wise(accounts)
    # {act: {date: [Transaction, ...]}}

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
