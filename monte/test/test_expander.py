# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

from twisted.trial import unittest
from ometa.runtime import ParseError
from monte.eparser import makeParser
from monte.expander import expand
from monte.test.test_eparser import serialize

class ExpanderTest(unittest.TestCase):

    def parse(self, src):
        p = makeParser(src)
        r, e = p.apply('expr')
        return serialize(expand(r))

    def test_anoun(self):
        self.assertEqual(self.parse("x"), ["NounExpr", "x"])

    def test_assign(self):
        self.assertEqual(self.parse("x := y"), ["Assign", ["NounExpr", "x"], ["NounExpr", "y"]])
        self.assertEqual(self.parse("x := y := z"), ["Assign", ["NounExpr", "x"], ["Assign", ["NounExpr", "y"], ["NounExpr", "z"]]])
        self.assertEqual(self.parse("x[i] := y"), ["SeqExpr", [["MethodCallExpr", ["NounExpr", "x"], "put", [["NounExpr", "i"], ["Def", ["FinalPattern", ["NounExpr", "ares__1"], None], None, ["NounExpr", "y"]]]], ["NounExpr", "ares__1"]]])
        self.assertEqual(self.parse("x.get(i) := y"), ["SeqExpr", [["MethodCallExpr", ["NounExpr", "x"], "put", [["NounExpr", "i"], ["Def", ["FinalPattern", ["NounExpr", "ares__1"], None], None, ["NounExpr", "y"]]]], ["NounExpr", "ares__1"]]])
        self.assertEqual(self.parse("x(i) := y"), ["SeqExpr", [["MethodCallExpr", ["NounExpr", "x"], "setRun", [["NounExpr", "i"], ["Def", ["FinalPattern", ["NounExpr", "ares__1"], None], None, ["NounExpr", "y"]]]], ["NounExpr", "ares__1"]]])
        self.assertEqual(self.parse("x.run(i) := y"), ["SeqExpr", [["MethodCallExpr", ["NounExpr", "x"], "setRun", [["NounExpr", "i"], ["Def", ["FinalPattern", ["NounExpr", "ares__1"], None], None, ["NounExpr", "y"]]]], ["NounExpr", "ares__1"]]])

    def test_update(self):
        self.assertEqual(self.parse("x foo= y"), ["Assign", ["NounExpr", "x"], ["MethodCallExpr", ["NounExpr", "x"], "foo", [["NounExpr", "y"]]]])
        self.assertEqual(self.parse("x foo= (y, z)"), ["Assign", ["NounExpr", "x"], ["MethodCallExpr", ["NounExpr", "x"], "foo", [["NounExpr", "y"], ["NounExpr", "z"]]]])
        self.assertEqual(self.parse("x[i] foo= y"), ["SeqExpr", [["Def", ["FinalPattern", ["NounExpr", "recip__1"], None], None, ["NounExpr", "x"]], ["Def", ["FinalPattern", ["NounExpr", "arg__2"], None], None, ["NounExpr", "i"]], ["MethodCallExpr", ["NounExpr", "recip__1"], "put", [["NounExpr", "arg__2"], ["Def", ["FinalPattern", ["NounExpr", "ares__3"], None], None, ["MethodCallExpr", ["MethodCallExpr", ["NounExpr", "recip__1"], "get", [["NounExpr", "arg__2"]]], "foo", [["NounExpr", "y"]]]]]], ["NounExpr", "ares__3"]]])
        self.assertEqual(self.parse("x(a) foo= y"), ["SeqExpr", [["Def", ["FinalPattern", ["NounExpr", "recip__1"], None], None, ["NounExpr", "x"]], ["Def", ["FinalPattern", ["NounExpr", "arg__2"], None], None, ["NounExpr", "a"]], ["MethodCallExpr", ["NounExpr", "recip__1"], "setRun", [["NounExpr", "arg__2"], ["Def", ["FinalPattern", ["NounExpr", "ares__3"], None], None, ["MethodCallExpr", ["MethodCallExpr", ["NounExpr", "recip__1"], "run", [["NounExpr", "arg__2"]]], "foo", [["NounExpr", "y"]]]]]], ["NounExpr", "ares__3"]]])

        self.assertEqual(self.parse("x[i] += y"), ["SeqExpr", [["Def", ["FinalPattern", ["NounExpr", "recip__1"], None], None, ["NounExpr", "x"]], ["Def", ["FinalPattern", ["NounExpr", "arg__2"], None], None, ["NounExpr", "i"]], ["MethodCallExpr", ["NounExpr", "recip__1"], "put", [["NounExpr", "arg__2"], ["Def", ["FinalPattern", ["NounExpr", "ares__3"], None], None, ["MethodCallExpr", ["MethodCallExpr", ["NounExpr", "recip__1"], "get", [["NounExpr", "arg__2"]]], "add", [["NounExpr", "y"]]]]]], ["NounExpr", "ares__3"]]])
        self.assertEqual(self.parse("x(a) += y"), ["SeqExpr", [["Def", ["FinalPattern", ["NounExpr", "recip__1"], None], None, ["NounExpr", "x"]], ["Def", ["FinalPattern", ["NounExpr", "arg__2"], None], None, ["NounExpr", "a"]], ["MethodCallExpr", ["NounExpr", "recip__1"], "setRun", [["NounExpr", "arg__2"], ["Def", ["FinalPattern", ["NounExpr", "ares__3"], None], None, ["MethodCallExpr", ["MethodCallExpr", ["NounExpr", "recip__1"], "run", [["NounExpr", "arg__2"]]], "add", [["NounExpr", "y"]]]]]], ["NounExpr", "ares__3"]]])


        self.assertEqual(self.parse("x += y"), ["Assign", ["NounExpr", "x"], ["MethodCallExpr", ["NounExpr", "x"], "add", [["NounExpr", "y"]]]])
        self.assertEqual(self.parse("x -= y"), ["Assign", ["NounExpr", "x"], ["MethodCallExpr", ["NounExpr", "x"], "subtract", [["NounExpr", "y"]]]])
        self.assertEqual(self.parse("x *= y"), ["Assign", ["NounExpr", "x"], ["MethodCallExpr", ["NounExpr", "x"], "multiply", [["NounExpr", "y"]]]])
        self.assertEqual(self.parse("x /= y"), ["Assign", ["NounExpr", "x"], ["MethodCallExpr", ["NounExpr", "x"], "approxDivide", [["NounExpr", "y"]]]])
        self.assertEqual(self.parse("x //= y"), ["Assign", ["NounExpr", "x"], ["MethodCallExpr", ["NounExpr", "x"], "floorDivide", [["NounExpr", "y"]]]])
        self.assertEqual(self.parse("x %= y"), ["Assign", ["NounExpr", "x"], ["MethodCallExpr", ["NounExpr", "x"], "remainder", [["NounExpr", "y"]]]])
        self.assertEqual(self.parse("x %%= y"), ["Assign", ["NounExpr", "x"], ["MethodCallExpr", ["NounExpr", "x"], "mod", [["NounExpr", "y"]]]])
        self.assertEqual(self.parse("x **= y"), ["Assign", ["NounExpr", "x"], ["MethodCallExpr", ["NounExpr", "x"], "pow", [["NounExpr", "y"]]]])
        self.assertEqual(self.parse("x >>= y"), ["Assign", ["NounExpr", "x"], ["MethodCallExpr", ["NounExpr", "x"], "shiftRight", [["NounExpr", "y"]]]])
        self.assertEqual(self.parse("x <<= y"), ["Assign", ["NounExpr", "x"], ["MethodCallExpr", ["NounExpr", "x"], "shiftLeft", [["NounExpr", "y"]]]])
        self.assertEqual(self.parse("x &= y"), ["Assign", ["NounExpr", "x"], ["MethodCallExpr", ["NounExpr", "x"], "and", [["NounExpr", "y"]]]])
        self.assertEqual(self.parse("x |= y"), ["Assign", ["NounExpr", "x"], ["MethodCallExpr", ["NounExpr", "x"], "or", [["NounExpr", "y"]]]])
        self.assertEqual(self.parse("x ^= y"), ["Assign", ["NounExpr", "x"], ["MethodCallExpr", ["NounExpr", "x"], "xor", [["NounExpr", "y"]]]])

    def test_send(self):
        self.assertEqual(self.parse("foo <- bar(x, y)"), ["MethodCallExpr", ["NounExpr", "E"], "send", [["NounExpr", "foo"], ["LiteralExpr", "bar"], ["MethodCallExpr", ["NounExpr", "__makeList"], "run", [["NounExpr", "x"], ["NounExpr", "y"]]]]])

    def test_binop(self):

        self.assertEqual(self.parse("x + y"),  ["MethodCallExpr", ["NounExpr", "x"], "add", [["NounExpr", "y"]]])
        self.assertEqual(self.parse("x - y"),  ["MethodCallExpr", ["NounExpr", "x"], "subtract", [["NounExpr", "y"]]])
        self.assertEqual(self.parse("x * y"),  ["MethodCallExpr", ["NounExpr", "x"], "multiply", [["NounExpr", "y"]]])
        self.assertEqual(self.parse("x / y"),  ["MethodCallExpr", ["NounExpr", "x"], "approxDivide", [["NounExpr", "y"]]])
        self.assertEqual(self.parse("x // y"), ["MethodCallExpr", ["NounExpr", "x"], "floorDivide", [["NounExpr", "y"]]])
        self.assertEqual(self.parse("x % y"),  ["MethodCallExpr", ["NounExpr", "x"], "remainder", [["NounExpr", "y"]]])
        self.assertEqual(self.parse("x %% y"), ["MethodCallExpr", ["NounExpr", "x"], "mod", [["NounExpr", "y"]]])
        self.assertEqual(self.parse("x ** y"), ["MethodCallExpr", ["NounExpr", "x"], "pow", [["NounExpr", "y"]]])
        self.assertEqual(self.parse("x ** y %% z"), ["MethodCallExpr", ["NounExpr", "x"], "modPow", [["NounExpr", "y"], ["NounExpr", "z"]]])
        self.assertEqual(self.parse("x >> y"), ["MethodCallExpr", ["NounExpr", "x"], "shiftRight", [["NounExpr", "y"]]])
        self.assertEqual(self.parse("x << y"), ["MethodCallExpr", ["NounExpr", "x"], "shiftLeft", [["NounExpr", "y"]]])
        self.assertEqual(self.parse("x & y"),  ["MethodCallExpr", ["NounExpr", "x"], "and", [["NounExpr", "y"]]])
        self.assertEqual(self.parse("x | y"),  ["MethodCallExpr", ["NounExpr", "x"], "or", [["NounExpr", "y"]]])
        self.assertEqual(self.parse("x ^ y"),  ["MethodCallExpr", ["NounExpr", "x"], "xor", [["NounExpr", "y"]]])

    def test_not(self):
        self.assertEqual(self.parse("!x"), ["MethodCallExpr", ["NounExpr", "x"], "not", []])

    def test_def(self):
        self.assertEqual(self.parse("def x := 1"), ["Def", ["FinalPattern", ["NounExpr", "x"], None], None, ["LiteralExpr", 1]])
        self.assertEqual(self.parse("def [x, y] := 1"), ["Def", ["ListPattern", [["FinalPattern", ["NounExpr", "x"], None], ["FinalPattern", ["NounExpr", "y"], None]], None], None, ["LiteralExpr", 1]])
        self.assertEqual(self.parse("def [x, y] := [1, x]"), ["SeqExpr", [["Def", ["ListPattern", [["FinalPattern", ["NounExpr", "x__1"], None], ["FinalPattern", ["NounExpr", "xR__2"], None]], None], None, ["MethodCallExpr", ["NounExpr", "Ref"], "promise", []]], ["Def", ["FinalPattern", ["NounExpr", "value__3"], None], None, ["Def", ["ListPattern", [["FinalPattern", ["NounExpr", "x"], None], ["FinalPattern", ["NounExpr", "y"], None]], None], None, ["MethodCallExpr", ["NounExpr", "__makeList"], "run", [["LiteralExpr", 1], ["NounExpr", "x__1"]]]]], ["MethodCallExpr", ["NounExpr", "xR__2"], "resolve", [["NounExpr", "x"]]], ["NounExpr", "value__3"]]])


    def test_forward(self):
        self.assertEqual(self.parse("def x"), ["SeqExpr", [["Def", ["ListPattern", [["FinalPattern", ["NounExpr", "x"], None], ["FinalPattern", ["NounExpr", "x__Resolver"], None]], None], None, ["MethodCallExpr", ["NounExpr", "Ref"], "promise", []]], ["NounExpr", "x__Resolver"]]])

    def test_noun(self):
        #parens since we're using 'expr' instead of 'start'
        self.assertEqual(self.parse("(x[i] := y; ares__1)"),
                         ["SeqExpr", [["MethodCallExpr", ["NounExpr", "x"], "put", [["NounExpr", "i"], ["Def", ["FinalPattern", ["NounExpr", "ares__2"], None], None, ["NounExpr", "y"]]]], ["NounExpr", "ares__2"], ["NounExpr", "ares__1"]]])
        self.assertEqual(self.parse("x"), ["NounExpr", 'x'])
        self.assertEqual(self.parse("<x>"), ["NounExpr", 'x__uriGetter'])

    def test_coerce(self):
        self.assertEqual(self.parse("x :foo"), ["MethodCallExpr", ["MethodCallExpr", ["NounExpr", "ValueGuard"], "coerce", [["NounExpr", "foo"], ["NounExpr", "throw"]]], "coerce", [["NounExpr", "x"], ["NounExpr", "throw"]]])

    def test_coerce2(self):
        self.assertEqual(self.parse("x :foo[baz]"), ["MethodCallExpr", ["MethodCallExpr", ["NounExpr", "ValueGuard"], "coerce", [['MethodCallExpr', ["NounExpr", "foo"], 'get', [['NounExpr', 'baz']]], ["NounExpr", "throw"]]], "coerce", [["NounExpr", "x"], ["NounExpr", "throw"]]])

    def test_slot(self):
        self.assertEqual(self.parse("&x"), ["MethodCallExpr", ["BindingExpr", ["NounExpr", "x"]], "get", []])

    def test_slotPattern(self):
        def pars(src):
            p = makeParser(src)
            r, e = p.apply('pattern')
            return serialize(expand(r))
        self.assertEqual(pars("&x"), ["ViaPattern", ["NounExpr", "__slotToBinding"], ["BindingPattern", ["NounExpr", "x"]]])
        self.assertEqual(pars("&x :int"), ["ViaPattern", ["MethodCallExpr", ["NounExpr", "__slotToBinding"], "run", [["NounExpr", "int"]]], ["BindingPattern", ["NounExpr", "x"]]])

    def test_ejector(self):
        self.assertEqual(self.parse("return"), ["MethodCallExpr", ["NounExpr", "__return"], "run", []])
        self.assertEqual(self.parse("continue"), ["MethodCallExpr", ["NounExpr", "__continue"], "run", []])
        self.assertEqual(self.parse("break"), ["MethodCallExpr", ["NounExpr", "__break"], "run", []])

        self.assertEqual(self.parse("return 1"), ["MethodCallExpr", ["NounExpr", "__return"], "run", [["LiteralExpr", 1]]])
        self.assertEqual(self.parse("continue 2"), ["MethodCallExpr", ["NounExpr", "__continue"], "run", [["LiteralExpr", 2]]])
        self.assertEqual(self.parse("break 3"), ["MethodCallExpr", ["NounExpr", "__break"], "run", [["LiteralExpr", 3]]])

    def test_and(self):
        #value
        self.assertEqual(self.parse("x && y"),
                         ["SeqExpr",
                          [["Def", ["ListPattern",
                                    [["FinalPattern", ["NounExpr", "ok__1"], None]]],
                            None,
                            ["If", ["NounExpr", "x"],
                             ["If", ["NounExpr", "y"],
                              ["MethodCallExpr", ["NounExpr", "__makeList"], "run",
                               [["NounExpr", "true"]]],
                              ["MethodCallExpr", ["NounExpr", "__booleanFlow"], "failureList",
                               [["LiteralExpr", 0]]]],
                             ["MethodCallExpr", ["NounExpr", "__booleanFlow"], "failureList",
                              [["LiteralExpr", 0]]]]],
                           ["NounExpr", "ok__1"]]])
        #value w/export
        self.assertEqual(
            self.parse("(def x := 1) && (def y := 2)"),
            ["SeqExpr", [["Def", ["ListPattern", [["FinalPattern", ["NounExpr", "ok__1"],
                                                   None],
                                                  ["BindingPattern", ["NounExpr", "y"]],
                                                  ["BindingPattern", ["NounExpr", "x"]]]],
                         None,
                         ["If", ["Def", ["FinalPattern", ["NounExpr", "x"], None],
                                                 None, ["LiteralExpr", 1]],
                          ["If", ["Def", ["FinalPattern", ["NounExpr", "y"], None],
                                      None,
                                      ["LiteralExpr", 2]],
                           ["MethodCallExpr", ["NounExpr", "__makeList"],
                            "run",
                            [["NounExpr", "true"],
                            ["BindingExpr", ["NounExpr", "y"]],
                            ["BindingExpr", ["NounExpr", "x"]]]],
                           ["MethodCallExpr", ["NounExpr", "__booleanFlow"],
                            "failureList",
                            [["LiteralExpr", 2]]]],
                          ["MethodCallExpr", ["NounExpr", "__booleanFlow"],
                           "failureList",
                           [["LiteralExpr", 2]]]]],
           ["NounExpr", "ok__1"]]])

    def test_or(self):
        #value
        self.assertEqual(self.parse("x || y"),
["SeqExpr", [["Def", ["ListPattern", [["FinalPattern", ["NounExpr", "ok__1"], None]]],
                      None,
              ["If", ["NounExpr", "x"],
               ["SeqExpr", [["MethodCallExpr", ["NounExpr", "__makeList"],
                             "run",
                             [["NounExpr", "true"]]]]],
               ["If", ["NounExpr", "y"],
                ["SeqExpr",
                 [["MethodCallExpr", ["NounExpr", "__makeList"],
                   "run",
                   [["NounExpr", "true"]]]]],
                ["MethodCallExpr", ["NounExpr", "__booleanFlow"],
                 "failureList",
                 [["LiteralExpr", 0]]]]]],
             ["NounExpr", "ok__1"]]])
        #value w/ export
        self.assertEqual(
            self.parse("(def x := 1) || (def y := 2)"),
["SeqExpr", [["Def", ["ListPattern", [["FinalPattern", ["NounExpr", "ok__1"], None],
                                        ["BindingPattern", ["NounExpr", "y"]],
                                        ["BindingPattern", ["NounExpr", "x"]]]],
                      None,
              ["If", ["Def", ["FinalPattern", ["NounExpr", "x"], None],
                          None,
                          ["LiteralExpr", 1]],
                          ["SeqExpr", [["Def", ["BindingPattern", ["NounExpr", "y"]],
                                        None,
                                        ["MethodCallExpr", ["NounExpr", "__booleanFlow"],
                                         "broken", []]],
                                       ["MethodCallExpr", ["NounExpr", "__makeList"],
                                        "run",
                                        [["NounExpr", "true"],
                                         ["BindingExpr", ["NounExpr", "y"]],
                                         ["BindingExpr", ["NounExpr", "x"]]]]]],
                           ["If", ["Def", ["FinalPattern", ["NounExpr", "y"], None],
                                       None,
                                       ["LiteralExpr", 2]],
                            ["SeqExpr",
                             [["Def", ["BindingPattern", ["NounExpr", "x"]],
                               None,
                               ["MethodCallExpr", ["NounExpr", "__booleanFlow"],
                                "broken", []]],
                              ["MethodCallExpr", ["NounExpr", "__makeList"],
                               "run",
                               [["NounExpr", "true"],
                                ["BindingExpr", ["NounExpr", "y"]],
                                ["BindingExpr", ["NounExpr", "x"]]]]]],
                            ["MethodCallExpr", ["NounExpr", "__booleanFlow"],
                             "failureList",
                             [["LiteralExpr", 2]]]]]],
             ["NounExpr", "ok__1"]]])

    def test_matchbind(self):
        #value
        self.assertEqual(
            self.parse("x =~ y"),
            ["SeqExpr", [["Def", ["FinalPattern", ["NounExpr", "sp__1"], None],
                          None,
                          ["NounExpr", "x"]],
                         ["Def", ["ListPattern", [["FinalPattern", ["NounExpr", "ok__2"], None],
                                                  ["BindingPattern", ["NounExpr", "y"]]], None],
                          None,
                          ["Escape", ["FinalPattern", ["NounExpr", "fail__3"], None],
                           ["SeqExpr", [["Def", ["FinalPattern", ["NounExpr", "y"], None],
                                         ["NounExpr", "fail__3"],
                                         ["NounExpr", "sp__1"]],
                                        ["MethodCallExpr", ["NounExpr", "__makeList"],
                                         "run",
                                         [["NounExpr", "true"],
                                          ["BindingExpr", ["NounExpr", "y"]]]]]],
                           ["Catch", ["FinalPattern", ["NounExpr", "problem__4"], None],
                            ["SeqExpr", [["Def", ["ViaPattern", ["NounExpr", "__slotToBinding"],
                                                  ["BindingPattern", ["NounExpr", "b__5"]]],
                                          None,
                                          ["MethodCallExpr", ["NounExpr", "Ref"],
                                           "broken",
                                           [["NounExpr", "problem__4"]]]],
                                         ["MethodCallExpr", ["NounExpr", "__makeList"],
                                          "run",
                                          [["NounExpr", "false"],
                                           ["BindingExpr", ["NounExpr", "b__5"]]]]]]]]],
                         ["NounExpr", "ok__2"]]])


    def test_for(self):
        self.assertRaises(ParseError, self.parse, "for via (a) x in [def a := 2, 1] {2}")
        self.assertEqual(self.parse("for x in y { z }"),
                         ["Escape", ["FinalPattern", ["NounExpr", "__break"],
                                     None],
                          ["SeqExpr",
                           [["Def", ["VarPattern",
                                    ["NounExpr", "validFlag__1"],
                                    None],
                            None,
                                   ["NounExpr", "true"]],
                           ["Finally",
                            ["MethodCallExpr", ["NounExpr", "y"], "iterate",
                             [["Object", "For-loop body",
                              ["IgnorePattern", None],
                              ["Script", None, None, [],
                               [["Method", None,
                                 "run",
                                 [["FinalPattern", ["NounExpr", "key__2"],
                                   None],
                                  ["FinalPattern", ["NounExpr", "value__3"],
                                   None]],
                                 None,
                                 ["SeqExpr",
                                  [["MethodCallExpr", ["NounExpr", "__validateFor"],
                                    "run", [["NounExpr", "validFlag__1"]]],
                                   ["Escape", ["FinalPattern",
                                                  ["NounExpr", "__continue"],
                                                  None],
                                    ["SeqExpr",
                                     [["Escape", ["FinalPattern", ["NounExpr", "skip__4"], None],
                                       ["SeqExpr",
                                     [["Def", ["IgnorePattern", None],
                                       ["NounExpr", "skip__4"],
                                       ["NounExpr", "key__2"]],
                                      ['Def',
                                       ['FinalPattern', ['NounExpr', 'x'], None],
                                       ['NounExpr', 'skip__4'],
                                       ['NounExpr', 'value__3']],
                                      ['NounExpr', 'z']]],
                                       None],
                                      ['NounExpr', 'null']]],
                                    None]]]]],
                               []]]]],
                            ['Assign', ['NounExpr', 'validFlag__1'],
                             ['NounExpr', 'false']]],
                            ['NounExpr', 'null']]],
                          None])

    def test_accum(self):
        self.assertEqual(
            self.parse(
                "accum a for x in y { _.foo() }"),
            ['SeqExpr',
             [['Def',
               ['VarPattern', ['NounExpr', 'accum__1'], None],
               None,
               ['NounExpr', 'a']],
              ['Escape',
               ['FinalPattern', ['NounExpr', '__break'], None],
               ['SeqExpr',
                [['Def',
                  ['VarPattern', ['NounExpr', 'validFlag__2'], None],
                  None,
                  ['NounExpr', 'true']],
                 ['Finally',
                  ['MethodCallExpr',
                   ['NounExpr', 'y'],
                   'iterate',
                   [['Object',
                     'For-loop body',
                     ['IgnorePattern', None],
                     ['Script',
                      None,
                      None,
                      [],
                      [['Method',
                        None,
                        'run',
                        [['FinalPattern', ['NounExpr', 'key__3'], None],
                         ['FinalPattern', ['NounExpr', 'value__4'], None]],
                        None,
                        ['SeqExpr',
                         [['MethodCallExpr',
                           ['NounExpr', '__validateFor'],
                           'run',
                           [['NounExpr', 'validFlag__2']]],
                          ['Escape',
                           ['FinalPattern',
                            ['NounExpr', '__continue'],
                            None],
                           ['SeqExpr',
                            [['Escape',
                              ['FinalPattern',
                               ['NounExpr', 'skip__5'],
                               None],
                              ['SeqExpr',
                               [['Def',
                                 ['IgnorePattern', None],
                                 ['NounExpr', 'skip__5'],
                                 ['NounExpr', 'key__3']],
                                ['Def',
                                 ['FinalPattern',
                                  ['NounExpr', 'x'],
                                  None],
                                 ['NounExpr', 'skip__5'],
                                 ['NounExpr', 'value__4']],
                                ['Assign',
                                 ['NounExpr', 'accum__1'],
                                 ['MethodCallExpr',
                                  ['NounExpr', 'accum__1'],
                                  'foo',
                                  []]]]],
                              None],
                             ['NounExpr', 'null']]],
                           None]]]]],
                      []]]]],
                  ['Assign', ['NounExpr', 'validFlag__2'], ['NounExpr', 'false']]],
                 ['NounExpr', 'null']]],
               None],
              ['NounExpr', 'accum__1']]])

        self.assertEqual(self.parse("accum a if (b) { _.foo() }"),
                    ["SeqExpr",
                     [["Def", ["VarPattern", ["NounExpr", "accum__1"], None],
                       None, ["NounExpr", "a"]],
                      ["If",
                       ["NounExpr", "b"],
                       ["Assign", ["NounExpr", "accum__1"],
                        ["MethodCallExpr",
                         ["NounExpr", "accum__1"],
                         "foo", []]],
                       ["NounExpr", "null"]],
                      ["NounExpr", "accum__1"]]])

        self.assertEqual(
            self.parse("accum x while (y) { _.foo() }"),
                    ["SeqExpr",
                     [["Def", ["VarPattern", ["NounExpr", "accum__1"], None],
                       None, ["NounExpr", "x"]],
                      ["Escape",
                       ["FinalPattern", ["NounExpr", "__break"], None],
                       ["MethodCallExpr", ["NounExpr", "__loop"],
                        "run",
                        [["Object", "While loop body",
                          ["IgnorePattern", None],
                          ["Script", None, None, [],
                           [["Method", None, "run", [], ["NounExpr", "boolean"],
                             ["If", ["NounExpr", "y"],
                              ["SeqExpr",
                               [["Escape", ["FinalPattern",
                                            ["NounExpr", "__continue"],
                                            None],
                       ["Assign", ["NounExpr", "accum__1"],
                        ["MethodCallExpr",
                         ["NounExpr", "accum__1"],
                         "foo", []]],
                                 None],
                                ["NounExpr", "true"]]],
                              ["NounExpr", "false"]]]],
                           []]]]], None],
                      ["NounExpr", "accum__1"]]])



    def test_if(self):
        self.assertEqual(
            self.parse("if (x) { y } else { z }"),
                       ["If", ["NounExpr", "x"],
                        ["NounExpr", "y"],
                        ["NounExpr", "z"]])

    def test_while(self):
        self.assertEqual(
            self.parse("while (x) { y }"),
            ["Escape",
             ["FinalPattern", ["NounExpr", "__break"], None],
             ["MethodCallExpr", ["NounExpr", "__loop"],
              "run",
              [["Object", "While loop body",
                ["IgnorePattern", None],
                ["Script", None, None, [],
                 [["Method", None, "run", [], ["NounExpr", "boolean"],
                   ["If", ["NounExpr", "x"],
                    ["SeqExpr",
                     [["Escape", ["FinalPattern",
                                  ["NounExpr", "__continue"],
                                  None],
                       ["NounExpr", "y"],
                       None],
                      ["NounExpr", "true"]]],
                    ["NounExpr", "false"]]]],
                 []]]]], None])

    def test_comparison(self):
        self.assertEqual(
            self.parse("x < y"),
            ["MethodCallExpr", ["NounExpr", "__comparer"],
             "lessThan",
             [["NounExpr", "x"], ["NounExpr", "y"]]])

        self.assertEqual(
            self.parse("x <= y"),
            ["MethodCallExpr", ["NounExpr", "__comparer"],
             "leq",
             [["NounExpr", "x"], ["NounExpr", "y"]]])

        self.assertEqual(
            self.parse("x <=> y"),
            ["MethodCallExpr", ["NounExpr", "__comparer"],
             "asBigAs",
             [["NounExpr", "x"], ["NounExpr", "y"]]])

        self.assertEqual(
            self.parse("x >= y"),
            ["MethodCallExpr", ["NounExpr", "__comparer"],
             "geq",
             [["NounExpr", "x"], ["NounExpr", "y"]]])

        self.assertEqual(
            self.parse("x > y"),
            ["MethodCallExpr", ["NounExpr", "__comparer"],
             "greaterThan",
             [["NounExpr", "x"], ["NounExpr", "y"]]])

    def test_equal(self):
        self.assertEqual(
            self.parse("x == y"),
            ["MethodCallExpr", ["NounExpr", "__equalizer"],
             "sameEver",
             [["NounExpr", "x"], ["NounExpr", "y"]]])

        self.assertEqual(
            self.parse("x != y"),
            ["MethodCallExpr",
             ["MethodCallExpr", ["NounExpr", "__equalizer"],
              "sameEver",
              [["NounExpr", "x"], ["NounExpr", "y"]]],
             "not", []])

    def test_tillthru(self):
        self.assertEqual(
            self.parse("x..y"),
            ["MethodCallExpr",
             ["NounExpr", "__makeOrderedSpace"],
             "op__thru",
             [["NounExpr", "x"], ["NounExpr", "y"]]])
        self.assertEqual(
            self.parse("x..!y"),
            ["MethodCallExpr",
             ["NounExpr", "__makeOrderedSpace"],
             "op__till",
             [["NounExpr", "x"], ["NounExpr", "y"]]])

    def test_mapPattern(self):
        self.assertEqual(
            self.parse('def ["a" => b, "c" => d] := x'),
            ["Def", ["ViaPattern",
                     ["MethodCallExpr", ["NounExpr", "__extract"],
                      "run", [["LiteralExpr", "a"]]],
                     ["ListPattern",
                      [["FinalPattern", ["NounExpr", "b"], None],
                       ["ViaPattern",
                        ["MethodCallExpr", ["NounExpr", "__extract"],
                         "run", [["LiteralExpr", "c"]]],
                        ["ListPattern",
                         [["FinalPattern", ["NounExpr", "d"], None],
                          ["IgnorePattern", ["NounExpr", "__Empty"]]],
                          None]]],
                      None]],
             None,
             ["NounExpr", "x"]])
        self.assertEqual(
            self.parse('def [(a) => b] | c := x'),
            ["Def", ["ViaPattern",
                     ["MethodCallExpr", ["NounExpr", "__extract"],
                      "run", [["NounExpr", "a"]]],
                     ["ListPattern",
                      [["FinalPattern", ["NounExpr", "b"], None],
                       ["FinalPattern", ["NounExpr", "c"], None]],
                      None]],
             None,
             ["NounExpr", "x"]])

        self.assertEqual(
            self.parse('def ["a" => b := 1] := x'),
            ["Def", ["ViaPattern",
                     ["MethodCallExpr", ["NounExpr", "__extract"],
                      "depr", [["LiteralExpr", "a"],
                               ["LiteralExpr", 1]]],
                     ["ListPattern",
                      [["FinalPattern", ["NounExpr", "b"], None],
                       ["IgnorePattern", ["NounExpr", "__Empty"]]],
                      None]],
             None,
             ["NounExpr", "x"]])

        self.assertEqual(
            self.parse('def [=> b] := x'),
            ["Def", ["ViaPattern",
                     ["MethodCallExpr", ["NounExpr", "__extract"],
                      "run", [["LiteralExpr", "b"]]],
                     ["ListPattern",
                      [["FinalPattern", ["NounExpr", "b"], None],
                       ["IgnorePattern", ["NounExpr", "__Empty"]]],
                      None]],
             None,
             ["NounExpr", "x"]])

        self.assertEqual(
            self.parse('def [=> &b] := x'),
            ["Def", ["ViaPattern",
                     ["MethodCallExpr", ["NounExpr", "__extract"],
                      "run", [["LiteralExpr", "&b"]]],
                     ["ListPattern",
                      [["ViaPattern", ["NounExpr", "__slotToBinding"],
                        ["BindingPattern", ["NounExpr", "b"]]],
                       ["IgnorePattern", ["NounExpr", "__Empty"]]],
                      None]],
             None,
             ["NounExpr", "x"]])

    def test_mapExpr(self):
        self.assertEqual(
            self.parse('["a" => b, "c" => d]'),
            ["MethodCallExpr", ["NounExpr", "__makeMap"], "fromPairs",
             [["MethodCallExpr", ["NounExpr", "__makeList"],
               "run",
               [["MethodCallExpr", ["NounExpr", "__makeList"],
                 "run",
                 [["LiteralExpr", "a"], ["NounExpr", "b"]]],
                ["MethodCallExpr", ["NounExpr", "__makeList"],
                 "run",
                 [["LiteralExpr", "c"], ["NounExpr", "d"]]]]]]])
        self.assertEqual(
            self.parse('[=> a, => &b]'),
            ["MethodCallExpr", ["NounExpr", "__makeMap"], "fromPairs",
             [["MethodCallExpr", ["NounExpr", "__makeList"],
               "run",
               [["MethodCallExpr", ["NounExpr", "__makeList"],
                 "run",
                 [["LiteralExpr", "a"], ["NounExpr", "a"]]],
                ["MethodCallExpr", ["NounExpr", "__makeList"],
                 "run",
                 [["LiteralExpr", "&b"], ["SlotExpr", "b"]]]]]]])


    def test_object(self):
        self.assertEqual(self.parse("def foo {}"),
                         ["Object", None,
                          ["FinalPattern", ["NounExpr", "foo"], None],
                          ["Script", None, None, [],
                           [], []]])
        self.assertEqual(self.parse("def foo extends baz {}"),
                         ["Def", ["FinalPattern", ["NounExpr", "foo"], None],
                          None,
                          ["HideExpr",
                           ["SeqExpr",
                            [["Def", ["FinalPattern", ["NounExpr", "super"],
                                      None],
                              None,
                              ["NounExpr", "baz"]],
                             ["Object", None,
                              ["FinalPattern", ["NounExpr", "foo"], None],
                              ["Script", None, None, [],
                               [], 
                               [["Matcher",
                                 ["FinalPattern", ["NounExpr", "pair__1"], None],
                                 ["MethodCallExpr", ["NounExpr", "E"],
                                  "callWithPair",
                                  [["NounExpr", "super"],
                                   ["NounExpr", "pair__1"]]]]]]]]]]])

    def test_to(self):
        self.assertEqual(self.parse("def foo { to baz() { x } }"),
                         ["Object", None,
                          ["FinalPattern", ["NounExpr", "foo"], None],
                          ["Script", None, None, [],
                           [["Method", None, "baz", [], None,
                             ["Escape",
                              ["FinalPattern",
                               ["NounExpr", "__return"],
                               None],
                              ["SeqExpr",
                               [["NounExpr", "x"],
                                ["NounExpr", "null"]]],
                                None]]],
                             []]])

    def test_method(self):
        self.assertEqual(self.parse("def foo { method baz(x) { y } }"),
                         ["Object", None,
                          ["FinalPattern", ["NounExpr", "foo"], None],
                          ["Script", None, None, [],
                           [["Method", None, "baz",
                             [["FinalPattern", ["NounExpr", "x"], None]], None,
                             ["NounExpr", "y"]]],
                             []]])

    def test_matcher(self):
        self.assertEqual(self.parse("def foo { match x { y } }"),
                         ["Object", None,
                          ["FinalPattern", ["NounExpr", "foo"], None],
                          ["Script", None, None, [], [],
                           [["Matcher", ["FinalPattern",
                                         ["NounExpr", "x"], None],
                             ["NounExpr", "y"]]]]])

    def test_function(self):
        self.assertEqual(self.parse("def foo() { y }"),
                         ["Object", None,
                          ["FinalPattern", ["NounExpr", "foo"], None],
                          ["Script", None, None, [],
                           [["Method", None, "run", [], None,
                             ["Escape", ["FinalPattern",
                                           ["NounExpr", "__return"],
                                           None],
                              ["SeqExpr",
                               [["NounExpr", "y"],
                                ["NounExpr", "null"]]],
                                None],
                              ]],
                           []]])

    def test_fn(self):
        self.assertEqual(self.parse("fn x { y }"),
                         ["Object", None,
                          ["IgnorePattern", None],
                          ["Script", None, None, [],
                           [["Method", None, "run",
                             [["FinalPattern", ["NounExpr", "x"], None]], None,
                             ["NounExpr", "y"]]],
                             []]])


    def test_samePattern(self):
        self.assertEqual(self.parse("def ==x := y"),
                         ["Def",
                          ["ViaPattern",
                           ["MethodCallExpr",
                           ["NounExpr", "__matchSame"],
                            "run", [["NounExpr", "x"]]],
                           ["IgnorePattern", None]],
                          None,
                          ["NounExpr", "y"]])

    def test_switch(self):
        self.assertEqual(
            self.parse("switch (x) { match [a, b] { c } match x { y }}"),
            ["HideExpr",
             ["SeqExpr",
              [["Def", ["FinalPattern", ["NounExpr", "specimen__1"], None],
                None, ["NounExpr", "x"]],
                ["Escape", ["FinalPattern", ["NounExpr", "ej__2"], None],
                 ["SeqExpr",
                  [["Def", ["ListPattern",
                            [["FinalPattern", ["NounExpr", "a"], None],
                             ["FinalPattern", ["NounExpr", "b"], None]],
                            None],
                    ["NounExpr", "ej__2"],
                    ["NounExpr", "specimen__1"]],
                    ["NounExpr", "c"]]],
                 ["Catch", ["FinalPattern", ["NounExpr", "failure__3"], None],
                ["Escape", ["FinalPattern", ["NounExpr", "ej__4"], None],
                 ["SeqExpr",
                  [["Def", ["FinalPattern", ["NounExpr", "x"], None],
                    ["NounExpr", "ej__4"],
                    ["NounExpr", "specimen__1"]],
                    ["NounExpr", "y"]]],
                 ["Catch", ["FinalPattern", ["NounExpr", "failure__5"], None],
                  ["MethodCallExpr", ["NounExpr", "__switchFailed"],
                   "run",
                   [["NounExpr", "specimen__1"], ["NounExpr", "failure__3"], ["NounExpr", "failure__5"]]]]]]]]]])

    def test_switch2(self):
        self.assertEqual(
            self.parse("switch (1) {match ==2 {'a'} match ==1 {'c'}}"),
["HideExpr",
             ["SeqExpr",
              [["Def", ["FinalPattern", ["NounExpr", "specimen__1"], None],
                None, ["LiteralExpr", 1]],
                ["Escape", ["FinalPattern", ["NounExpr", "ej__2"], None],
                 ["SeqExpr",
                  [["Def", ["ViaPattern",
                            ["MethodCallExpr", ["NounExpr", "__matchSame"],
                             "run",
                             [["LiteralExpr", 2]]] ,
                            ["IgnorePattern", None]],
                    ["NounExpr", "ej__2"],
                    ["NounExpr", "specimen__1"]],
                    ["LiteralExpr", ["Character", "a"]]]],
                 ["Catch", ["FinalPattern", ["NounExpr", "failure__3"], None],
                ["Escape", ["FinalPattern", ["NounExpr", "ej__4"], None],
                 ["SeqExpr",
                  [["Def", ["ViaPattern",
                            ["MethodCallExpr", ["NounExpr", "__matchSame"],
                             "run",
                             [["LiteralExpr", 1]]],
                            ["IgnorePattern", None]],
                    ["NounExpr", "ej__4"],
                    ["NounExpr", "specimen__1"]],
                    ["LiteralExpr", ["Character", "c"]]]],
                 ["Catch", ["FinalPattern", ["NounExpr", "failure__5"], None],
                  ["MethodCallExpr", ["NounExpr", "__switchFailed"],
                   "run",
                   [["NounExpr", "specimen__1"], ["NounExpr", "failure__3"], ["NounExpr", "failure__5"]]]]]]]]]])


    def test_interface(self):
        self.assertEqual(self.parse("interface foo {}"),
                         ["Def", ["FinalPattern", ["NounExpr", "foo"], None],
                          None,
                          ["HideExpr",
                           ["MethodCallExpr",
                            ["NounExpr", "__makeProtocolDesc"],
                            "run",
                            [None,
                              ["MethodCallExpr",
                               ["MethodCallExpr", ["Meta", "context"],
                                "getFQNPrefix", []],
                               "add",
                               [["LiteralExpr", "foo__T"]]],
                             ["MethodCallExpr", ["NounExpr", "__makeList"],
                              "run", []],
                             ["MethodCallExpr", ["NounExpr", "__makeList"],
                              "run", []],
                             ["MethodCallExpr", ["NounExpr", "__makeList"],
                              "run", []]]]]])
        self.assertEqual(self.parse("/** yay */ interface foo extends x,y  implements a,b { /** blee */ to baz(c :int)\nto boz (d) :float64 }"),
                         ["Def", ["FinalPattern", ["NounExpr", "foo"], None],
                          None,
                          ["HideExpr",
                           ["MethodCallExpr",
                            ["NounExpr", "__makeProtocolDesc"],
                            "run",
                            [["LiteralExpr", "yay"],
                              ["MethodCallExpr",
                               ["MethodCallExpr", ["Meta", "context"],
                                "getFQNPrefix", []],
                               "add",
                               [["LiteralExpr", "foo__T"]]],
                             ["MethodCallExpr", ["NounExpr", "__makeList"],
                              "run",
                              [["NounExpr", "x"],
                               ["NounExpr", "y"]]],
                             ["MethodCallExpr", ["NounExpr", "__makeList"],
                              "run",
                              [["NounExpr", "a"],
                               ["NounExpr", "b"]]],
                             ["MethodCallExpr", ["NounExpr", "__makeList"],
                              "run",
                              [["HideExpr",
                                ["MethodCallExpr",
                                 ["NounExpr", "__makeMessageDesc"],
                                 "run",
                                 [["LiteralExpr", "blee"],
                                  ["LiteralExpr", "baz"],
                                  ["MethodCallExpr", ["NounExpr", "__makeList"],
                                   "run",
                                   [["MethodCallExpr",
                                     ["NounExpr", "__makeParamDesc"],
                                     "run",
                                     [["LiteralExpr", "c"],
                                      ["NounExpr", "int"]]]]],
                                  ["NounExpr", "void"]]]],
                               ["HideExpr",
                                ["MethodCallExpr",
                                 ["NounExpr", "__makeMessageDesc"],
                                 "run",
                                 [None,
                                  ["LiteralExpr", "boz"],
                                  ["MethodCallExpr", ["NounExpr", "__makeList"],
                                   "run",
                                   [["MethodCallExpr",
                                     ["NounExpr", "__makeParamDesc"],
                                     "run",
                                     [["LiteralExpr", "d"],
                                      ["NounExpr", "any"]]]]],
                                  ["NounExpr", "float64"]]]]
                               ]]]]]])


    def test_try(self):
        self.assertEqual(self.parse("try { x } catch p { y }"),
                         ["KernelTry",
                          ["NounExpr", "x"],
                          ["FinalPattern", ["NounExpr", "p"], None],
                          ["NounExpr", "y"]])
        self.assertEqual(self.parse("try { x }"),
                         ["HideExpr", ["NounExpr", "x"]])

        self.assertEqual(self.parse("try { x } catch p { y } catch q { z }"),
                         ["KernelTry",
                          ["KernelTry",
                           ["NounExpr", "x"],
                           ["FinalPattern", ["NounExpr", "p"], None],
                           ["NounExpr", "y"]],
                          ["FinalPattern", ["NounExpr", "q"], None],
                          ["NounExpr", "z"]])

        self.assertEqual(self.parse("try { x } finally { y }"),
                         ["Finally", ["NounExpr", "x"],
                          ["NounExpr", "y"]])

        self.assertEqual(self.parse("try { x } catch p { y } finally { z }"),
                         ["Finally",
                          ["KernelTry",
                           ["NounExpr", "x"],
                           ["FinalPattern", ["NounExpr", "p"], None],
                           ["NounExpr", "y"]],
                          ["NounExpr", "z"]])


    def test_when(self):
        self.assertEqual(self.parse("when (x) -> { y }"),
                         ["HideExpr",
                          ["MethodCallExpr",
                             ["NounExpr", "Ref"],
                             "whenResolved",
                             [["NounExpr", "x"],
                             ["Object", "when-catch 'done' function",
                              ["IgnorePattern", None],
                              ["Script", None, None, [],
                               [["Method", None, "run",
                                 [["FinalPattern",
                                   ["NounExpr", "resolution__1"], None]],
                                 None,
                                 [["If", ["MethodCallExpr",
                                         ["NounExpr", "Ref"],
                                         "isBroken",
                                         [["NounExpr", "resolution__1"]]],
                                  ["MethodCallExpr",
                                   ["NounExpr", "Ref"],
                                   "broken",
                                   [["MethodCallExpr",
                                     ["NounExpr", "Ref"],
                                     "optProblem",
                                     [["NounExpr", "resolution__1"]]]]],
                                   ["NounExpr", "y"]]]]],
                               []]]]]])
        self.assertEqual(self.parse("when (x) -> { y } catch p { z }"),
                         ["HideExpr",
                          ["MethodCallExpr",
                             ["NounExpr", "Ref"],
                             "whenResolved",
                             [["NounExpr", "x"],
                             ["Object", "when-catch 'done' function",
                              ["IgnorePattern", None],
                              ["Script", None, None, [],
                               [["Method", None, "run",
                                 [["FinalPattern",
                                   ["NounExpr", "resolution__1"], None]],
                                 None,
                                   [["KernelTry",
                                     ["If", ["MethodCallExpr",
                                            ["NounExpr", "Ref"],
                                            "isBroken",
                                            [["NounExpr", "resolution__1"]]],
                                     ["MethodCallExpr",
                                      ["NounExpr", "Ref"],
                                      "broken",
                                      [["MethodCallExpr",
                                        ["NounExpr", "Ref"],
                                        "optProblem",
                                        [["NounExpr", "resolution__1"]]]]],
                                      ["NounExpr", "y"]],
                                     ["FinalPattern", ["NounExpr", "p"], None],
                                     ["NounExpr", "z"]]]]],
                                 []]]]]])

