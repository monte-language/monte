"""
Tests for the E/Python bridge.
"""
import ctypes
from twisted.trial import unittest
from monte import api

class EvalTest(unittest.TestCase):
    """
    Tests for evaluation of code.
    """
    def test_simpleInteractiveEval(self):
        """
        C{interactiveEval} evaluates expressions, extending the list of bound
        names as appropriate.
        """
        stackp = ctypes.POINTER(api.Stackframe)()
        res = api.interactiveEval("1+1", api.e_safeScope, [], stackp)
        self.assertEqual(res.strip(), "2")
