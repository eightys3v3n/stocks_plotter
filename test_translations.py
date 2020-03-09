import unittest
import datetime
from transaction import Transaction
from translations import *


class TestTranslations(unittest.TestCase):
    def test_act_wise(self):
        trans = [Transaction(act="1", amt=1),
                 Transaction(act="1", amt=2),
                 Transaction(act="2", amt=3),
                 Transaction(act="3", amt=4)]
        act_trans = act_wise(trans)
        self.assertEqual(act_trans, {
            "1": [Transaction(act="1", amt=1),
                  Transaction(act="1", amt=2)],
            "2": [Transaction(act="2", amt=3),],
            "3": [Transaction(act="3", amt=4),]})
        

    def test_date_wise(self):
        act_trans = {
            "1": [Transaction(act="1", amt=1, date=datetime.date(2020, 1, 1)),
                  Transaction(act="1", amt=2, date=datetime.date(2020, 1, 1))],
            "2": [Transaction(act="2", amt=3, date=datetime.date(2020, 1, 1)),
                  Transaction(act="2", amt=4, date=datetime.date(2020, 1, 2))]}
        date_trans = date_wise(act_trans)
        self.assertEqual(date_trans, {
            "1": {
                datetime.date(2020, 1, 1): [Transaction(act="1", amt=1, date=datetime.date(2020, 1, 1)),
                                            Transaction(act="1", amt=2, date=datetime.date(2020, 1, 1))]},
            "2": {
                datetime.date(2020, 1, 1): [Transaction(act="2", amt=3, date=datetime.date(2020, 1, 1))],
                datetime.date(2020, 1, 2): [Transaction(act="2", amt=4, date=datetime.date(2020, 1, 2))]}
        })
