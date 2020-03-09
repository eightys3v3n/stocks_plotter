import unittest
import datetime
from main import *
from transaction import Transaction


class TestHelpers(unittest.TestCase):
    def test_date_range(self):
        acts = {"1": {datetime.date(2019, 1, 1): []},
                "2": {datetime.date(2020, 10, 10): []},
                "3": {datetime.date(2018, 1, 1): []}
        }
        min_date, max_date = date_range(acts)
        self.assertEqual(min_date, datetime.date(2018, 1, 1))
        self.assertEqual(max_date, datetime.date(2020, 10, 10))


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


    def test_date_wise(self):
        trans = {"1": [Transaction(act="1", amt=10, date=datetime.date(2020, 1, 1)),
                       Transaction(act="1", amt=20, date=datetime.date(2020, 1, 2)),
                       Transaction(act="1", amt=30, date=datetime.date(2020, 1, 3)),
                       Transaction(act="1", amt=40, date=datetime.date(2020, 1, 2)),
                       Transaction(act="1", amt=50, date=datetime.date(2020, 1, 3)),                 
        ]}
        new = date_wise(trans)
        self.assertEqual(new, {"1": {
            datetime.date(2020, 1, 1): [trans["1"][0]],
            datetime.date(2020, 1, 2): [trans["1"][1], trans["1"][3]],
            datetime.date(2020, 1, 3): [trans["1"][2], trans["1"][4]]
        }})


    def test_most_recent_bal_before(self):
        date_trans = {datetime.date(2020, 1, 1): [Transaction(bal_af=10),
                                                  Transaction(bal_af=20)],
                      datetime.date(2020, 1, 2): [Transaction(bal_af=30),
                                                  Transaction(bal_af=40)],
                      datetime.date(2020, 1, 3): [Transaction(bal_af=50),
                                                  Transaction(bal_af=60)],
        }
        most_recent = most_recent_bal_before(datetime.date(2020, 1, 2), date_trans)
        self.assertNotEqual(most_recent, None)
        self.assertEqual(most_recent, 20)


    def test_seperate_acts(self):
        
        
