from monte.runtime.data import Integer
from monte.runtime.flow import MonteIterator

class ConstList(tuple):
    def __repr__(self):
        orig = tuple.__repr__(self)
        return '[' + orig[1:-1] + ']'

    def __str__(self):
        return self.__repr__()

    def _makeIterator(self):
        return MonteIterator((Integer(i), o) for (i, o) in zip(range(len(self)), self))

    size = tuple.__len__
    #XXX Is this a good name/API? no idea.
    def contains(self, item):
        return item in self

def makeMonteList(*items):
    return ConstList(items)

class Map(dict):
    _m_fqn = "Dict"
    __setitem__ = None
    get = dict.__getitem__


class mapMaker(object):
    _m_fqn = "__makeMap"
    @staticmethod
    def fromPairs(pairs):
        return Map(pairs)
