from textwrap import dedent
from monte.test import unittest
from monte.runtime.base import toQuote
from monte.runtime.data import false, true, Integer, String
from monte.runtime.load import eval as monte_eval
from monte.runtime.tables import ConstList, ConstMap
from twisted.trial.unittest import SkipTest


class NullPropertiesTest(unittest.TestCase):

    def test_equal(self):
        self.assertEqual(monte_eval("null == null"), true)

    def test_inequal(self):
        self.assertEqual(monte_eval("null != null"), false)


class EvalTest(unittest.TestCase):

    def test_base(self):
        self.assertEqual(monte_eval("3 + 4"), Integer(7))

    def test_string(self):
        self.assertEqual(monte_eval('"foo"'), String(u'foo'))

    def test_object(self):
        self.assertEqual(monte_eval(dedent(
            """
            def foo():
                return 3
            def baz():
                return 4
            foo() + baz()
            """)),
            Integer(7))

    def test_scope(self):
        self.assertEqual(monte_eval("if (true) {1} else {2}"), Integer(1))

    def test_comparer(self):
        self.assertEqual(monte_eval("1 < 2"), true)
        self.assertEqual(monte_eval("1 > 2"), false)
        self.assertEqual(monte_eval("3 >= 3"), true)
        self.assertEqual(monte_eval("3 <= 3"), true)
        self.assertEqual(monte_eval("3 <=> 4"), false)

    def test_list(self):
        self.assertEqual(monte_eval("[0, 1]"), ConstList((Integer(0), Integer(1))))

    def test_def(self):
        self.assertEqual(monte_eval("def x := 1; x"), Integer(1))

    def test_var(self):
        self.assertEqual(monte_eval("var x := 1; x := 2; x"), Integer(2))

    def test_for(self):
        self.assertEqual(monte_eval("var x := 0; for y in [1, 2] { x := y }; x"), Integer(2))
        self.assertEqual(monte_eval("var x := 0; for y in [1, 2] { x := y; break}; x"), Integer(1))
        self.assertEqual(monte_eval("for y in [1, 2] { break(3)}"), Integer(3))

    def test_listcomp(self):
        self.assertEqual(monte_eval("[x + 1 for x in [0, 1]]"), ConstList((Integer(1), Integer(2))))
        self.assertEqual(monte_eval("[k + v for k => v in [3, 4, 7]]"), ConstList((Integer(3), Integer(5), Integer(9))))

    def test_map(self):
        self.assertEqual(monte_eval('["a" => 3, "b" => 4]["a"]'), Integer(3))

    def test_mapcomp(self):
        self.assertEqual(monte_eval('[x => x + 1 for x in [1, 2]][2]'), Integer(3))

    def test_while(self):
        self.assertEqual(monte_eval('var x := 0; while (x <= 3) { x += 1}; x'), Integer(4))

    def test_tryDoesntCatchEjections(self):
        self.assertEqual(
            monte_eval(
                'var x := 0; escape e { try { e(1) } catch p { x := p } }; x'),
            Integer(0))

    def test_scopesDontOverlap(self):
        self.assertEqual(
            monte_eval(
                'def x := 1; if (true) { def x := 2}; x'),
            Integer(1))

    def test_verbFacet(self):
        self.assertEqual(monte_eval("def foo() { return 1 }; def x := foo.run; x()"), Integer(1))

    def test_matchsame(self):
        self.assertEqual(monte_eval("def ==1 := 1"), Integer(1))
        self.assertRaises(RuntimeError, monte_eval, "def ==1 := 2")

    def test_bind(self):
        raise SkipTest
        self.assertEqual(monte_eval("def x; bind x := 1; x"), Integer(1))

    def test_map_patt(self):
        self.assertEqual(monte_eval('def ["a" => a, "b" => c] := ["a" => 1, "b" => 3]; c - a'), Integer(2))
#        self.assertEqual(monte_eval('def ["a" => a, "b" => c, "e" => e default {9}] := ["a" => 1, "b" => 3]; e'), Integer(9))
        self.assertRaises(RuntimeError, monte_eval,
                          'def ["a" => a, "b" => c] := ["a" => 1, "b" => 3, "e" => 4]')

        self.assertEqual(monte_eval(
            'def ["a" => a, "b" => c] | d := ["a" => 1, "b" => 3, "e" => 4]; d'),
                         ConstMap({String(u'e'): Integer(4)}))

    def test_list_patt(self):
        self.assertEqual(monte_eval('def [a, b, c] := [2, 3, 4]; c - a'), Integer(2))
        self.assertEqual(monte_eval('def [a, b, c] + d := [2, 3, 4, 7, 6]; d'), ConstList((Integer(7), Integer(6))))

    def test_suchthat(self):
        self.assertEqual(monte_eval('def a ? (a > 0) := 1; a'), Integer(1))
        self.assertRaises(RuntimeError, monte_eval, 'def a ? (a > 10) := 1')

    def test_switch(self):
        self.assertEqual(monte_eval('switch (1) { match ==0 { 1} match ==1 { 2}}'), Integer(2))
        self.assertRaises(RuntimeError, monte_eval, 'switch (2) { match ==0 { 1} match ==1 { 2}}')

    def test_coerce(self):
        self.assertEqual(monte_eval('true :boolean'), true)

    def test_simple_quasiParser_value(self):
        self.assertEqual(monte_eval('def x := 42; `($x)`'), String(u"(42)"))
        self.assertEqual(monte_eval('def x := 1; def y := [2, 3]; `one $x and $y and two`'),
                         String(u"one 1 and [2, 3] and two"))

    def test_simple_quasiParser_pattern(self):
        self.assertEqual(
            monte_eval('def `one @x and @y and two` := "one foo and bar and two"; [x, y]'),
            ConstList((String(u"foo"), String(u"bar"))))
        self.assertEqual(
            monte_eval('def `foo @x@y` := "foo baz"; [x, y]'),
            ConstList((String(u""), String(u"baz"))))
        self.assertEqual(
            monte_eval('def a := "baz"; def `foo @x$a` := "foo baz"; x'),
            String(u""))

        self.assertEqual(monte_eval("true and false"), false)
        self.assertEqual(monte_eval("[(def x := true) and true, x]"), ConstList((true, true)))

    def test_or(self):
        self.assertEqual(monte_eval("true or false"), true)
        self.assertEqual(monte_eval("[(def x := true) or true, x]"), ConstList((true, true)))


class EqualizerTest(unittest.TestCase):
    def test_prims(self):
        self.assertEqual(monte_eval("1 == 1"), true)
        self.assertEqual(monte_eval("1 == 2"), false)
        self.assertEqual(monte_eval("1 == 1.0"), false)
        self.assertEqual(monte_eval("'a' == 'a'"), true)
        self.assertEqual(monte_eval("'a' == 'b'"), false)
        self.assertEqual(monte_eval("'a' == 1"), false)
        self.assertEqual(monte_eval("3.14 == 3.14"), true)
        self.assertEqual(monte_eval("3.14 == 3.15"), false)
        self.assertEqual(monte_eval('"fred" == "fred"'), true)
        self.assertEqual(monte_eval('"fred" == "barney"'), false)
        self.assertEqual(monte_eval('true == false'), false)
        self.assertEqual(monte_eval('false == false'), true)

    def test_list(self):
        self.assertEqual(monte_eval("[] == []"), true)
        self.assertEqual(monte_eval("[1] == [1]"), true)
        self.assertEqual(monte_eval("[1] == []"), false)
        self.assertEqual(monte_eval("[1, 2] == [3, 4]"), false)
        self.assertEqual(monte_eval("[5, [6, 7]] == [5, [6, 7]]"), true)
        self.assertEqual(monte_eval("[5, [6, 7]] == [5, [8, 7]]"), false)

    def test_opaque(self):
        self.assertEqual(monte_eval("object x {}; x == x"), true)

    def test_map(self):
        self.assertEqual(monte_eval("[1 => 2, 3 => 4] == [1 => 2, 3 => 4]"), true)
        self.assertEqual(monte_eval("[1 => 2, 3 => 4] == [3 => 4, 1 => 2]"), false)
        self.assertEqual(monte_eval("[].asMap() == [].asMap()"), true)

    def test_cycle(self):
        self.assertEqual(monte_eval("def x := [1, x]; x == x[1]"), true)

class PrinterTest(unittest.TestCase):

    def pr(self, s):
        return toQuote(monte_eval(s))

    def test_prims(self):
        self.assertEqual(self.pr("1"), "1")
        self.assertEqual(self.pr("1.5"), "1.5")
        self.assertEqual(self.pr("'a'"), "'a'")
        self.assertEqual(self.pr('"foo baz \\u03b5"'), '"foo baz \\u03b5"')
        self.assertEqual(self.pr('"foo baz \\u03b5"[8]'), "'\\u03b5'")

    def test_list(self):
        self.assertEqual(self.pr("[1, 2]"), "[1, 2]")
        self.assertEqual(self.pr("[1, [2, 3, []]]"), "[1, [2, 3, []]]")
        self.assertEqual(self.pr("def x := [1, x]"), "[1, <**CYCLE**>]")

    def test_map(self):
        self.assertEqual(self.pr("[].asMap()"), "[].asMap()")
        self.assertEqual(self.pr("[1 => 2]"), "[1 => 2]")
        self.assertEqual(self.pr("[1 => 2, 3 => 4]"), "[1 => 2, 3 => 4]")
        self.assertEqual(self.pr("def x := [1 => 2, 3 => x]"), "[1 => 2, 3 => <**CYCLE**>]")

