import unittest
import datetime


class Transaction:
    def __init__(self, act=None, date=None, desc=None, amt=None, bal_af=None):
        if act is not None and not isinstance(act, str):
            raise ValueError("act must be a str object or None, not {}".format(type(act)))
        if date is not None and not isinstance(date, datetime.date):
            raise ValueError("date must be a datetime.date object or None, not {}".format(type(date)))
        if desc is not None and not isinstance(desc, str):
            raise ValueError("desc must be a str object or None, not {}".format(type(desc)))
        if amt is not None and not isinstance(amt, (float, int)):
            raise ValueError("amt must be a float/int object or None, not {}".format(type(amt)))
        if bal_af is not None and not isinstance(bal_af, (float, int)):
            raise ValueError("bal_af must be a float/int or None, not {}".format(type(bal_af)))

        self.act = act
        self.date = date
        self.desc = desc
        self.amt = amt
        self.bal_af = bal_af
        self.bal_be = None

        if self.bal_af and self.amt:
            self.bal_be = self.bal_af + -self.amt


    def __repr__(self):
        return {'act' : self.act,
                'date': self.date, 
                'desc': self.desc,
                'amt' : self.amt,
                'bal_af': self.bal_af,
                'bal_be': self.bal_be,
                }.__str__()

    def __str__(self):
        return "{{act: '{}',\n date: {},\n desc: '{}',\n amt: {},\n bal_af: {},\n bal_be: {}}}".format(
                self.act, self.date.__str__().replace('datetime.date(', '('),
                self.desc, self.amt, self.bal_af, self.bal_be)

    def __hash__(self):
        return hash("{}:{}:{}:{}:{}".format(self.act, self.date, self.desc, self.amt, self.bal_af))

    def __eq__(self, o):
        if self.__hash__() == o.__hash__(): return True
        return False


