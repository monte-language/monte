import sys

from monte.runtime.base import MonteObject

class MonteStdin(MonteObject):
    """
    Read from stdin.
    """

    def read(self):
        from monte.runtime.compiler_helpers import wrap
        return wrap(sys.stdin.read(16))

class MonteStdout(MonteObject):
    """
    Write to stdout.
    """

    def write(self, data):
        from monte.runtime.data import String
        if not isinstance(data, String):
            raise RuntimeError("%r is not a string" % (data,))
        return sys.stdout.write(data.s)

stdin = MonteStdin()
stdout = MonteStdout()
