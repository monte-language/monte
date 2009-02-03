from twisted.trial import unittest
from compiler import parse as python_parse
from pymeta.builder import AstBuilder



class AstBuilderTest(unittest.TestCase):
    """
    Tests for creating Python functions and classes.
    """

    def test_method(self):
        """
        C{compileAstMethod} creates a function with a single 'self' arg that
        returns the value of the given expression.
        """
        expr = python_parse("self.data[1] + 3", mode="eval").asList()[0]
        ab = AstBuilder("<test>", None)
        f = ab._compileAstMethod("rule_f", expr)
        class Foo:
            locals = {}
            data = [0, 2]
        self.assertEqual(f(Foo), 5)
