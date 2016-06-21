
from datetime import date, datetime, timedelta
import unittest

from synthdata import (
    DataSet,
    NullableDataSet,
    IntDataSet,
    DateDataSet,
    DatetimeDataSet,
    TimedeltaDataSet,
    DatetimeDataSet,
    DatetimeRangeDataSet,
    StringDataSet
)


class TestCustomTypes(unittest.TestCase):

    def test_customtype(self):
        class Boom:
            def __init__(self):
                pass
        self.assertRaises(TypeError, DataSet, Boom())

    def test_list(self):
        self.assertRaises(TypeError, DataSet, [[]])

    def test_list_none(self):
        self.assertRaises(TypeError, DataSet, [None, []])


class TestEmpty(unittest.TestCase):

    def test_none(self):
        self.assertRaises(TypeError, DataSet, None)

    def test_empty(self):
        empty = DataSet([])
        empty.count()
        empty.min()
        empty.max()
        print(empty)
        self.assertEquals(None, empty.random())


class TestIntDataSet(unittest.TestCase):

    def test_explicit(self):
        s = IntDataSet([0, 0])
        print(s)
        self.assertEquals(0, s.random())

    def test_implicit(self):
        s = DataSet([0, 0])
        print(s)
        self.assertEquals(0, s.random())

    def test_implicit_nullable(self):
        s = DataSet([None, 0])
        print(s)
        self.assertIn(s.random(), [None, 0])


class TestNullableIntDataSet(unittest.TestCase):

    def test_explicit(self):
        s = IntDataSet([1, 2, 3])
        print(s)
        print([s.random() for _ in range(0, 5)])

    def test_implicit(self):
        s = DataSet([1, 2, 3])
        print(s)
        print([s.random() for _ in range(0, 5)])

    def test_nullable_explicit(self):
        s = NullableDataSet(IntDataSet, [None, 1, 2, 3])
        print(s)
        print([s.random() for _ in range(0, 20)])


class TestDateDataSet(unittest.TestCase):

    def test_explicit(self):
        s = DateDataSet([date(2000, 1, 1), date(2010, 1, 1), date(2015, 6, 20)])
        print(s)
        print([s.random() for _ in range(0, 5)])

    def test_typeerror(self):
        self.assertRaises(TypeError, DateDataSet, ['not a date'])


class TestTimedeltaDataSet(unittest.TestCase):

    def test_explicit(self):
        s = TimedeltaDataSet([timedelta(days=1), timedelta(days=2)])
        print(s)
        print([s.random() for _ in range(0, 5)])

    def test_typeerror(self):
        self.assertRaises(TypeError, TimedeltaDataSet,
                            ['not a timedelta'])


class TestDatetimeDataSet(unittest.TestCase):

    def test_explicit(self):
        s = DatetimeDataSet([datetime(2013, 1, 1),
                             datetime(2014, 2, 2),
                             datetime(2015, 6, 20)])
        print(s)
        print([s.random() for _ in range(0, 3)])


class TestDatetimeRangeDataSet(unittest.TestCase):

    def test_explicit(self):
        s = DatetimeRangeDataSet([
                (datetime(2000, 1, 1), datetime(2001, 1, 1)),
                (datetime(2001, 1, 1), datetime(2001, 3, 1)),
            ])
        print(s)
        print([s.random() for _ in range(0, 3)])

    def test_implicit(self):
        l = [(datetime(2000, 1, 1), datetime(2001, 1, 1))]
        s = DataSet(l)
        print(s)
        s.random()


class TestStringDataSet(unittest.TestCase):

    def test_explicit(self):
        s = StringDataSet([''])
        print(s)
        s.random()

    def test_implicit(self):
        s = DataSet([''])
        print(s)
        s.random()

    def test_hello_world(self):
        s = StringDataSet(['', 'l', 'hello world'])
        print(s)
        print(s.random() for _ in range(0, 20))

