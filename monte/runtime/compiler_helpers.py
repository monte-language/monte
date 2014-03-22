"""
Functions called by the Python code generated by monte.compiler.
"""
from monte.runtime.base import _MatchFailure
from monte.runtime.data import Character, String, Bool, Integer, Float
from monte.runtime.guards.base import anyGuard
from monte.runtime.tables import ConstList

makeCharacter = Character

def matcherFail(v):
    raise _MatchFailure(v)


def getObjectGuard(o):
    """
    Returns the guard for an object.
    """

    # XXX haha what
    return anyGuard


def getGuard(o, name):
    """
    Returns the guard object for a name in a Monte object's frame.
    """
    b = o.__class__.__dict__.get(name)
    if b is not None:
        return b.getGuard(o)
    return anyGuard


def wrap(pyobj):
    if isinstance(pyobj, str):
        return Bytes(pyobj)
    if isinstance(pyobj, unicode):
        return String(pyobj)
    # Perform bool check before int because bool subclasses int.
    if isinstance(pyobj, bool):
        return Bool(pyobj)
    if isinstance(pyobj, int):
        return Integer(pyobj)
    if isinstance(pyobj, float):
        return Float(pyobj)
    if isinstance(pyobj, list):
        return FlexList(pyobj)
    if isinstance(pyobj, tuple):
        return ConstList(pyobj)
    if isinstance(pyobj, dict):
        return FlexMap(pyobj)
    if isinstance(pyobj, set):
        return FlexSet(pyobj)
    if isinstance(pyobj, frozenset):
        return Set(pyobj)
