import unittest
import datetime
from helpers import *


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


    def test_map_range(self):
        self.assertEqual(map_range((0, 10), (1, 2), 5), 1.5)
        self.assertEqual(map_range((0, 10), (0, 1), 5), 0.5)
        self.assertEqual(map_range((0, 10), (0, 100), 4.9), 49)
        self.assertEqual(map_range((0, 10), (0, 100), 2.2), 22)


    def test_min_max_prices(self):
        inp = [("a random date", 1),
               ("another date ", 2),
               ("third date   ", 3)]
        outp = min_max_prices(inp)
        self.assertEqual(outp, (1, 3))
