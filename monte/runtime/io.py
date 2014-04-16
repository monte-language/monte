import sys

from monte.runtime.base import MonteObject

class MonteStdin(MonteObject):
    """
    Read from stdin.
    """

    def read(self):
        return sys.stdin.read(16)

stdin = MonteStdin()
