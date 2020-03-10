import unittest
import datetime
from helpers import *
from transaction import Transaction


class TestHelpers(unittest.TestCase):
    def test_get_date_range(self):
        acts = {"1": {datetime.date(2019, 1, 1): []},
                "2": {datetime.date(2020, 10, 10): []},
                "3": {datetime.date(2018, 1, 1): []}
        }
        min_date, max_date = get_date_range(acts)
        self.assertEqual(min_date, datetime.date(2018, 1, 1))
        self.assertEqual(max_date, datetime.date(2020, 10, 10))


    def test_get_date_range2(self):
        acts = {"1": {datetime.date(2020, 1, 14): [],
                      datetime.date(2020, 1, 31): [],
                      datetime.date(2020, 2, 29): []}}
        min_date, max_date = get_date_range(acts)
        self.assertEqual(min_date, datetime.date(2020, 1, 14))
        self.assertEqual(max_date, datetime.date(2020, 2, 29))
        

    def test_day_range(self):
        min_date = datetime.date(2020, 1, 1)
        max_date = datetime.date(2020, 1, 10)
        days = day_range(min_date, max_date)
        self.assertEqual(days, [
            datetime.date(2020, 1, 1),
            datetime.date(2020, 1, 2),
            datetime.date(2020, 1, 3),
            datetime.date(2020, 1, 4),
            datetime.date(2020, 1, 5),
            datetime.date(2020, 1, 6),
            datetime.date(2020, 1, 7),
            datetime.date(2020, 1, 8),
            datetime.date(2020, 1, 9),
            datetime.date(2020, 1, 10)
        ])


    def test_most_recent_bal_before(self):
        date_trans = {datetime.date(2019, 1, 1): [Transaction(bal_af=10),
                                                  Transaction(bal_af=20)],
                      datetime.date(2020, 1, 2): [Transaction(bal_af=30),
                                                  Transaction(bal_af=40)],
                      datetime.date(2020, 1, 3): [Transaction(bal_af=50),
                                                  Transaction(bal_af=60)],
        }
        most_recent = most_recent_bal_before(datetime.date(2020, 1, 2), date_trans)
        self.assertNotEqual(most_recent, None)
        self.assertEqual(most_recent, 20)


    def test_deduce_balance_before(self):
        date_trans = {
            datetime.date(2020, 1, 1): [
                Transaction(date=datetime.date(2020, 1, 1),
                            bal_af=10),
                Transaction(date=datetime.date(2020, 1, 1),
                            bal_af=20)],
            datetime.date(2020, 1, 3): [
                Transaction(date=datetime.date(2020, 1, 3),
                            bal_af=30)]
        }
        bal = deduce_balance(datetime.date(2020, 1, 2), date_trans)
        self.assertEqual(bal, 20)
        

    def test_deduce_balance_after(self):
        date_trans = {
            datetime.date(2020, 1, 3): [
                Transaction(date=datetime.date(2020, 1, 3),
                            bal_af=10),
                Transaction(date=datetime.date(2020, 1, 3),
                            bal_af=20)],
            datetime.date(2020, 1, 4): [
                Transaction(date=datetime.date(2020, 1, 4),
                            bal_af=30)]
        }
        bal = deduce_balance(datetime.date(2020, 1, 2), date_trans)
        self.assertEqual(bal, 0)
        

    def test_daily_balances_single_normal(self):
        act_dates = {
            "1": {datetime.date(2020, 1, 1): [
                    Transaction(act="1", date=datetime.date(2020, 1, 1), bal_af=10),
                    Transaction(act="1", date=datetime.date(2020, 1, 1), bal_af=20)
                  ],
                  datetime.date(2020, 1, 2): [
                      Transaction(act="1", date=datetime.date(2020, 1, 2), bal_af=30)
                  ]
            },
        }
        bals = daily_balances(act_dates)
        self.assertEqual(bals, {"1": {datetime.date(2020, 1, 1): 20,
                                      datetime.date(2020, 1, 2): 30}})

        
    def test_daily_balances_multi_normal(self):
        act_dates = {
            "1": {datetime.date(2020, 1, 1): [
                    Transaction(act="1", date=datetime.date(2020, 1, 1), bal_af=10),
                    Transaction(act="1", date=datetime.date(2020, 1, 1), bal_af=20)
                  ],
                  datetime.date(2020, 1, 2): [
                      Transaction(act="1", date=datetime.date(2020, 1, 2), bal_af=30)
                  ]
            },
            "2": {datetime.date(2020, 1, 1): [
                    Transaction(act="2", date=datetime.date(2020, 1, 1), bal_af=40),
                    Transaction(act="2", date=datetime.date(2020, 1, 1), bal_af=50)
                  ],
                  datetime.date(2020, 1, 2): [
                      Transaction(act="2", date=datetime.date(2020, 1, 2), bal_af=60)
                  ]
            },
        }
        bals = daily_balances(act_dates)
        self.assertEqual(bals, {"1": {datetime.date(2020, 1, 1): 20,
                                      datetime.date(2020, 1, 2): 30},
                                "2": {datetime.date(2020, 1, 1): 50,
                                      datetime.date(2020, 1, 2): 60}})
        

    def test_daily_balances_missing(self):
        act_dates = {
            "1": {datetime.date(2020, 1, 2): [
                      Transaction(act="1", date=datetime.date(2020, 1, 2), bal_af=10)
                ]},
            "2": {datetime.date(2020, 1, 1): [
                      Transaction(act="2", date=datetime.date(2020, 1, 1), bal_af=20)],
                  datetime.date(2020, 1, 2): [
                      Transaction(act="2", date=datetime.date(2020, 1, 2), bal_af=30)]}
        }
        bals = daily_balances(act_dates)
        self.assertEqual(bals, {"1": {datetime.date(2020, 1, 1): 0,
                                      datetime.date(2020, 1, 2): 10},
                                "2": {datetime.date(2020, 1, 1): 20,
                                      datetime.date(2020, 1, 2): 30}})


    def test_daily_balances_large(self):
        act_dates = {
            "1": {datetime.date(2020, 1, 14): [
                      Transaction(date=datetime.date(2020, 1, 14), bal_af=3779.18),],
                  datetime.date(2020, 1, 20): [
                      Transaction(date=datetime.date(2020, 1, 20), bal_af=3775.74),]}}
        bals = daily_balances(act_dates)
        self.maxDiff = None
        self.assertEqual(bals, {"1": {
            datetime.date(2020, 1, 14): 3779.18,
            datetime.date(2020, 1, 15): 3779.18,
            datetime.date(2020, 1, 16): 3779.18,
            datetime.date(2020, 1, 17): 3779.18,
            datetime.date(2020, 1, 18): 3779.18,
            datetime.date(2020, 1, 19): 3779.18,
            datetime.date(2020, 1, 20): 3775.74,
            
        }})
