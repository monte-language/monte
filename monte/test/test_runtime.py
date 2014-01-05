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

    def test_list(self):
        self.assertEqual(monte_eval("[0, 1]"), (0, 1))

    def test_def(self):
        self.assertEqual(monte_eval("def x := 1; x"), 1)

    def test_var(self):
        self.assertEqual(monte_eval("var x := 1; x := 2; x"), 2)

    def test_for(self):
        self.assertEqual(monte_eval("var x := 0; for y in [1, 2] { x := y }; x"), 2)
        self.assertEqual(monte_eval("var x := 0; for y in [1, 2] { x := y; break}; x"), 1)
        self.assertEqual(monte_eval("for y in [1, 2] { break(3)}"), 3)

    def test_listcomp(self):
        self.assertEqual(monte_eval("[x + 1 for x in [0, 1]]"), (1, 2))
