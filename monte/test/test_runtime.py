from textwrap import dedent
from monte.test import unittest

from monte.runtime import eval as monte_eval
from twisted.trial.unittest import SkipTest


class NullPropertiesTest(unittest.TestCase):

    def test_equal(self):
        self.assertTrue(monte_eval("null == null"))

    def test_inequal(self):
        # XXX Should pass after fixing up bool objects
        raise SkipTest
        self.assertFalse(monte_eval("null != null"))


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

    def test_comparer(self):
        self.assertEqual(monte_eval("1 < 2"), True)
        self.assertEqual(monte_eval("1 > 2"), False)
        self.assertEqual(monte_eval("3 >= 3"), True)
        self.assertEqual(monte_eval("3 <= 3"), True)
        self.assertEqual(monte_eval("3 <=> 4"), False)

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
        self.assertEqual(monte_eval("[k + v for k => v in [3, 4, 7]]"), (3, 5, 9))

    def test_map(self):
        self.assertEqual(monte_eval('["a" => 3, "b" => 4]["a"]'), 3)

    def test_mapcomp(self):
        self.assertEqual(monte_eval('[x => x + 1 for x in [1, 2]][2]'), 3)

    def test_while(self):
        self.assertEqual(monte_eval('var x := 0; while (x <= 3) { x += 1}; x'), 4)

    def test_tryDoesntCatchEjections(self):
        self.assertEqual(
            monte_eval(
                'var x := 0; escape e { try { e(1) } catch p { x := p } }; x'),
            0)

    def test_scopesDontOverlap(self):
        self.assertEqual(
            monte_eval(
                'def x := 1; if (true) { def x := 2}; x'),
            1)

    def test_verbFacet(self):
        self.assertEqual(monte_eval("def foo() { return 1 }; def x := foo.run; x()"), 1)

    def test_matchsame(self):
        self.assertEqual(monte_eval("def ==1 := 1"), 1)
        self.assertRaises(RuntimeError, monte_eval, "def ==1 := 2")

    def test_bind(self):
        raise SkipTest
        self.assertEqual(monte_eval("def x; bind x := 1; x"), 1)

    def test_map_patt(self):
        self.assertEqual(monte_eval('def ["a" => a, "b" => c] := ["a" => 1, "b" => 3]; c - a'), 2)
#        self.assertEqual(monte_eval('def ["a" => a, "b" => c, "e" => e default {9}] := ["a" => 1, "b" => 3]; e'), 9)
        self.assertRaises(RuntimeError, monte_eval,
                          'def ["a" => a, "b" => c] := ["a" => 1, "b" => 3, "e" => 4]')

        self.assertEqual(monte_eval(
            'def ["a" => a, "b" => c] | d := ["a" => 1, "b" => 3, "e" => 4]; d'),
            {'e': 4})

    def test_list_patt(self):
        self.assertEqual(monte_eval('def [a, b, c] := [2, 3, 4]; c - a'), 2)
        self.assertEqual(monte_eval('def [a, b, c] + d := [2, 3, 4, 7, 6]; d'), (7, 6))

    def test_suchthat(self):
        self.assertEqual(monte_eval('def a ? (a > 0) := 1; a'), 1)
        self.assertRaises(RuntimeError, monte_eval, 'def a ? (a > 10) := 1')

    def test_switch(self):
        self.assertEqual(monte_eval('switch (1) { match ==0 { 1} match ==1 { 2}}'), 2)
        self.assertRaises(RuntimeError, monte_eval, 'switch (2) { match ==0 { 1} match ==1 { 2}}')

    def test_coerce(self):
        self.assertEqual(monte_eval('true :boolean'), True)

    def test_simple_quasiParser_value(self):
        self.assertEqual(monte_eval('def x := 1; def y := [2, 3]; `one $x and $y and two`'),
                         "one 1 and [2, 3] and two")

    def test_simple_quasiParser_pattern(self):
        self.assertEqual(
            monte_eval('def `one @x and @y and two` := "one foo and bar and two"; [x, y]'),
            ("foo", "bar"))
        self.assertEqual(
            monte_eval('def `foo @x@y` := "foo baz"; [x, y]'),
            ("", "baz"))
        self.assertEqual(
            monte_eval('def a := "baz"; def `foo @x$a` := "foo baz"; x'),
            "")

    def test_and(self):
        self.assertEqual(monte_eval("true and false"), False)
        self.assertEqual(monte_eval("[(def x := true) and true, x]"), (True, True))

    def test_or(self):
        self.assertEqual(monte_eval("true or false"), True)
        self.assertEqual(monte_eval("[(def x := true) or true, x]"), (True, True))
