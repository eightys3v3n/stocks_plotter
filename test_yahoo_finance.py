from xrp_usd import *
import datetime
import unittest


class TestFirstCalgary(unittest.TestCase):
    def test_parse_csv_row(self):
        row = parse_csv_row(0, ["2014-09-17", "0.005123", "0.005803", "0.005123", "0.005399", "0.005399", "1281960"])
        self.assertEqual(len(row), 7)
        self.assertEqual(row[0], datetime.date(2014, 9, 17))
        self.assertEqual(row[1], 0.005123)
        self.assertEqual(row[2], 0.005803)
        self.assertEqual(row[3], 0.005123)
        self.assertEqual(row[4], 0.005399)
        self.assertEqual(row[5], 0.005399)
        self.assertEqual(row[6], 1281960)
