from textwrap import dedent
from monte.test import unittest

from monte.runtime import eval as monte_eval

class EvalTest(unittest.TestCase):

    def test_base(self):
        self.assertEqual(monte_eval("3 + 4"), 7)

    def test_string(self):
        self.assertEqual(monte_eval('"foo"'), u'foo')

    def test_object(self):
        self.assertEqual(monte_eval(dedent(
            """
            def foo():
                return 3
            def baz():
                return 4
            foo() + baz()
            """)),
            7)

    def test_scope(self):
        self.assertEqual(monte_eval("if (true) {1} else {2}"), 1)
