
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
import numpy as np
from random import random


class EmptyDataSet(object):
    min = None
    max = None
    def __init__(self):
        pass
    def count(self):
        return 0
    def min(self):
        return self.min
    def max(self):
        return self.max
    def random(self):
        pass
    def __repr__(self):
        return '<EmptyDataSet>'

class IntDataSet(EmptyDataSet):
    def __init__(self, data):
        data = list(data)
        items = sorted(Counter(data).items())
        self.cnt = len(data)
        self.keys = [k for k, _ in items]
        self.vals = [v for _, v in items]
        self.total = sum(self.vals)
        self.p = [float(v) / self.total for v in self.vals]
        self.min = min(self.keys)
        self.max = max(self.keys)
    def random(self):
        return int(np.random.choice(self.keys, 1, p=self.p)[0])
    def __repr__(self):
        return '<IntDataSet count=%s min=%s max=%s>' % (
            self.cnt, self.min, self.max)

class DateDataSet(EmptyDataSet):
    def __init__(self, data):
        data = list(data)
        self._check(data)
        self.cnt = len(data)
        self.min = min(data)
        self.max = max(data)
        self.years = IntDataSet(d.year for d in data)
        self.months = IntDataSet(d.month for d in data)
        self.days = IntDataSet(d.day for d in data)
    def _check(self, data):
        if not all(isinstance(d, date) for d in data):
            errmsg = 'not a date: %s' % (
                [d for d in data if not isinstance(d, date)][0])
            raise TypeError(errmsg)
    def random(self):
        y = self.years.random()
        m = self.months.random()
        d = self.days.random()
        return date(y, m, d)
    def __repr__(self):
        return '<DateDataSet count=%s min=%s max=%s>' % (self.cnt, self.min, self.max)

class DatetimeDataSet(EmptyDataSet):
    def __init__(self, data):
        data = list(data)
        self._check(data)
        self.cnt = len(data)
        self.min = min(data)
        self.max = max(data)
        self.years = IntDataSet(d.year for d in data)
        self.months = IntDataSet(d.month for d in data)
        self.days = IntDataSet(d.day for d in data)
        self.hours = IntDataSet(d.hour for d in data)
        self.mins = IntDataSet(d.minute for d in data)
        self.secs = IntDataSet(d.second for d in data)
        self.usecs = IntDataSet(d.microsecond for d in data)
    def _check(self, data):
        if not all(isinstance(d, datetime) for d in data):
            errmsg = 'not a datetime: %s' % (
                [d for d in data if not isinstance(d, date)][0])
            raise TypeError(errmsg)
    def random(self):
        y = self.years.random()
        m = self.months.random()
        d = self.days.random()
        h = self.hours.random()
        i = self.mins.random()
        s = self.secs.random()
        u = self.usecs.random()
        return datetime(y, m, d, h, i, s, u)
    def __repr__(self):
        return '<DatetimeDataSet count=%s min=%s max=%s>' % (self.cnt, self.min, self.max)

class TimedeltaDataSet(EmptyDataSet):
    def __init__(self, data):
        data = list(data)
        self._check(data)
        self.cnt = len(data)
        self.min = min(data)
        self.max = max(data)
        self.days = IntDataSet(d.days for d in data)
        self.secs = IntDataSet(d.seconds for d in data)
        self.usecs = IntDataSet(d.microseconds for d in data)
    def _check(self, data):
        if not all(isinstance(d, timedelta) for d in data):
            errmsg = 'not a timedelta: %s' % (
                [d for d in data if not isinstance(d, timedelta)][0])
            raise TypeError(errmsg)
    def random(self):
        d = self.days.random()
        s = self.secs.random()
        u = self.usecs.random()
        return timedelta(d, s, u)
    def __repr__(self):
        return '<TimedeltaDataSet count=%s min=%s max=%s>' % (self.cnt, self.min, self.max)

class DatetimeRangeDataSet(EmptyDataSet):
    def __init__(self, data):
        self._check(data)
        self.cnt = len(data)
        self.min = min(data)
        self.max = max(data)
        self.dates = DatetimeDataSet(x for x, _ in data)
        self.deltas = TimedeltaDataSet(y - x for x, y in data)
    def _check(self, data):
        if not all(isinstance(x, datetime) and isinstance(y, datetime) for x, y in data):
            errmsg = 'not a datetime: %s' % (
                [d for d in data if not isinstance(d, timedelta)][0])
            raise TypeError(errmsg)
    def random(self):
        d = self.dates.random()
        i = self.deltas.random()
        return (d, d + i)
    def __repr__(self):
        return '<DatetimeRangeDataSet count=%s min=%s max=%s>' % (self.cnt, self.min, self.max)

class StringDataSet(EmptyDataSet):
    def __init__(self, data):
        self.cnt = len(data)
        self.min = min(data)
        self.max = max(data)
        self.lens = IntDataSet(len(d) for d in data)
        self.markov = StringDataSet.calc_markov(data)
        print(self.markov)
    def random(self):
        s = ''
        c = ''
        while True:
            c2 = self.next(c)
            if not c2:
                break
            s += c2
            c = c2
        return s
    def __repr__(self):
        return '<StringDataSet count=%s min=%s max=%s>' % (self.cnt, repr(self.min), repr(self.max))
    def next(self, c):
        kv = self.markov[c]
        k = [k for k, _ in kv]
        v = [v for _, v in kv]
        x = np.random.choice(k, 1, p=v)[0]
        #print('next(%s) = %s' % (repr(c), repr(x)))
        return x
    @staticmethod
    def calc_markov(data):
        nextchar = defaultdict(dict)
        for d in data:
            if not d:
                nextchar[''][''] = nextchar[''].get('', 0) + 1
            else:
                chars = list(d)
                chars.insert(0, '')
                chars.append('')
                #print(chars)
                for x, y in zip(chars, chars[1:]):
                    nextchar[x][y] = nextchar[x].get(y, 0) + 1
        countnext = sum(max(0, len(d)) for d in data)
        totals = {k: sum(v.values()) for k, v in nextchar.items()}
        return {x: [(y, float(cnt) / totals[x]) for y, cnt in d.items()]
                    for x, d in nextchar.items()}

class NullableDataSet(EmptyDataSet):
    def __init__(self, cls, data):
        self.cnt = len(data)
        nonecnt = data.count(None)
        self.cls = cls
        self.p = float(nonecnt) / self.cnt
        minusnone = [d for d in data if d is not None]
        if minusnone:
            self.s = cls(minusnone)
    def random(self):
        if random() < self.p:
            return None
        return self.s.random()
    def __repr__(self):
        return '<NullableDataSet cls=%s count=%s min=%s max=%s>' % (
            self.cls, self.cnt, None, self.s.max)

class DataSet(EmptyDataSet):

    def __new__(cls, data):
        data = list(data)
        if not data:
            return EmptyDataSet()
        t = set(DataSet.get_type(d) for d in data)
        cls = None
        is_nullable = type(None) in t
        if is_nullable:
            t -= set([type(None)])
        if not t:
            cls = EmptyDataSet
        if t == {int}:
            cls = IntDataSet
        elif t == {str}:
            cls = StringDataSet
        elif t == {date}:
            cls = DateDataSet
        elif t == {datetime}:
            cls = DatetimeDataSet
        elif t == {timedelta}:
            cls = TimedeltaDataSet
        elif t == {(datetime, datetime)}:
            cls = DatetimeRangeDataSet
        if cls:
            if is_nullable:
                return NullableDataSet(cls, data)
            else:
                return cls(data)
        raise NotImplementedError(str(t))

    @staticmethod
    def get_type(x):
        if isinstance(x, list):
            return [type(y) for y in x]
        elif isinstance(x, tuple):
            return tuple(type(y) for y in x)
        return type(x)

