from first_calgary import *
import datetime
import unittest


class TestStatements(unittest.TestCase):
    def test_parse_csv_row(self):
        row = parse_csv_row(["Account Number      ", "28-Feb-2020", "Transfer out to ...      ", "", "85.00", "", "390.47"])
        self.assertEqual(len(row), 7)
        self.assertEqual(row[0], "Account Number")
        self.assertEqual(row[1], datetime.date(2020, 2, 28))
        self.assertEqual(row[2], "Transfer out to ...")
        self.assertEqual(row[3], None)
        self.assertEqual(row[4], 85.0)
        self.assertEqual(row[5], None)
        self.assertEqual(row[6], 390.47)


    def test_parse_trans_withdrawal(self):
        t = parse_trans(["12", datetime.date(2020, 2, 28), "Transfer out to ...", None, 85, None, 390.47])
        self.assertEqual(t.act, "12")
        self.assertEqual(t.date, datetime.date(2020, 2, 28))
        self.assertEqual(t.desc, "Transfer out to ...")
        self.assertEqual(t.amt, -85)
        self.assertEqual(t.bal_af, 390.47)
        self.assertEqual(t.bal_be, 390.47+85)


    def test_parse_trans_deposit(self):
        t = parse_trans(["12", datetime.date(2020, 2, 28), "Transfer out to ...", None, None, 85, 390.47])
        self.assertEqual(t.act, "12")
        self.assertEqual(t.date, datetime.date(2020, 2, 28))
        self.assertEqual(t.desc, "Transfer out to ...")
        self.assertEqual(t.amt, 85)
        self.assertEqual(t.bal_af, 390.47)
        self.assertEqual(t.bal_be, 390.47-85)
