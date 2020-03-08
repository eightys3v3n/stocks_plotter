import unittest
import datetime
from transaction import *


class TestTransaction(unittest.TestCase):
    def test_manual_init(self):
        t = Transaction(act="12",
                        date=datetime.date(year=2019, month=3, day=3),
                        desc="Transfer out of ...",
                        amt=-10.0,
                        bal_af=315.0)
        self.assertEqual(t.act, "12")
        self.assertEqual(t.date, datetime.date(year=2019, month=3, day=3))
        self.assertEqual(t.desc, "Transfer out of ...")
        self.assertEqual(t.amt, -10)
        self.assertEqual(t.bal_af, 315)
        self.assertEqual(t.bal_be, 315+10)


    def test_str(self):
        t = Transaction(act="12",
                        date=datetime.date(year=2019, month=3, day=3),
                        desc="Transfer out of ...",
                        amt=-10.0,
                        bal_af=315.0)
        self.assertEqual(t.__repr__(), "{'act': '12', 'date': datetime.date(2019, 3, 3), 'desc': 'Transfer out of ...', 'amt': -10.0, 'bal_af': 315.0, 'bal_be': 325.0}")

        self.assertEqual(t.__str__(), "{act: '12',\n date: 2019-03-03,\n desc: 'Transfer out of ...',\n amt: -10.0,\n bal_af: 315.0,\n bal_be: 325.0}")

