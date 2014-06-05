from monte.runtime.guards.base import deepFrozenFunc

@deepFrozenFunc
def trace(x):
    print x,

@deepFrozenFunc
def traceln(x):
    print x
