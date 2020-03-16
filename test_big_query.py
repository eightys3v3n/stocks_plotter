from big_query import *
import datetime
import unittest


class TestFirstCalgary(unittest.TestCase):
    def test_parse_csv_row(self):
        row = parse_csv_row(0, ["2014-09-17", "22"])
        self.assertEqual(len(row), 2)
        self.assertEqual(row[0], datetime.date(2014, 9, 17))
        self.assertEqual(row[1], 22)
