from twisted.trial import unittest
from monte.eparser import EParser
from monte.nodes import KernelENodeCopier, ParseError, SubNode

class ExpanderTest(unittest.TestCase):

    def parse(self, txt):
        SubNode.tempCounter = 1 #XXX hack

        ast = EParser(txt).apply("expr")
        return ast.expand().serialize()


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
        self.assertEqual(self.parse("x[i] foo= y"), ["SeqExpr", [["Def", ["FinalPattern", ["NounExpr", "recip__1"], None], None, ["NounExpr", "x"]], ["Def", ["FinalPattern", ["NounExpr", "arg__3"], None], None, ["NounExpr", "i"]], ["MethodCallExpr", ["NounExpr", "recip__1"], "put", [["NounExpr", "arg__3"], ["Def", ["FinalPattern", ["NounExpr", "ares__5"], None], None, ["MethodCallExpr", ["MethodCallExpr", ["NounExpr", "recip__1"], "get", [["NounExpr", "arg__3"]]], "foo", [["NounExpr", "y"]]]]]], ["NounExpr", "ares__5"]]])
        self.assertEqual(self.parse("x(a) foo= y"), ["SeqExpr", [["Def", ["FinalPattern", ["NounExpr", "recip__1"], None], None, ["NounExpr", "x"]], ["Def", ["FinalPattern", ["NounExpr", "arg__3"], None], None, ["NounExpr", "a"]], ["MethodCallExpr", ["NounExpr", "recip__1"], "setRun", [["NounExpr", "arg__3"], ["Def", ["FinalPattern", ["NounExpr", "ares__5"], None], None, ["MethodCallExpr", ["MethodCallExpr", ["NounExpr", "recip__1"], "run", [["NounExpr", "arg__3"]]], "foo", [["NounExpr", "y"]]]]]], ["NounExpr", "ares__5"]]])

        self.assertEqual(self.parse("x[i] += y"), ["SeqExpr", [["Def", ["FinalPattern", ["NounExpr", "recip__1"], None], None, ["NounExpr", "x"]], ["Def", ["FinalPattern", ["NounExpr", "arg__3"], None], None, ["NounExpr", "i"]], ["MethodCallExpr", ["NounExpr", "recip__1"], "put", [["NounExpr", "arg__3"], ["Def", ["FinalPattern", ["NounExpr", "ares__5"], None], None, ["MethodCallExpr", ["MethodCallExpr", ["NounExpr", "recip__1"], "get", [["NounExpr", "arg__3"]]], "add", [["NounExpr", "y"]]]]]], ["NounExpr", "ares__5"]]])
        self.assertEqual(self.parse("x(a) += y"), ["SeqExpr", [["Def", ["FinalPattern", ["NounExpr", "recip__1"], None], None, ["NounExpr", "x"]], ["Def", ["FinalPattern", ["NounExpr", "arg__3"], None], None, ["NounExpr", "a"]], ["MethodCallExpr", ["NounExpr", "recip__1"], "setRun", [["NounExpr", "arg__3"], ["Def", ["FinalPattern", ["NounExpr", "ares__5"], None], None, ["MethodCallExpr", ["MethodCallExpr", ["NounExpr", "recip__1"], "run", [["NounExpr", "arg__3"]]], "add", [["NounExpr", "y"]]]]]], ["NounExpr", "ares__5"]]])


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
        self.assertEqual(self.parse("def [x, y] := [1, x]"), ["SeqExpr", [["Def", ["ListPattern", [["FinalPattern", ["NounExpr", "x__1"], None], ["FinalPattern", ["NounExpr", "xR__3"], None]], None], None, ["MethodCallExpr", ["NounExpr", "Ref"], "promise", []]], ["Def", ["FinalPattern", ["NounExpr", "res__5"], None], None, ["Def", ["ListPattern", [["FinalPattern", ["NounExpr", "x"], None], ["FinalPattern", ["NounExpr", "y"], None]], None], None, ["MethodCallExpr", ["NounExpr", "__makeList"], "run", [["LiteralExpr", 1], ["NounExpr", "x__1"]]]]], ["MethodCallExpr", ["NounExpr", "xR__3"], "resolve", [["NounExpr", "x"]]], ["NounExpr", "res__5"]]])


    def test_forward(self):
        self.assertEqual(self.parse("def x"), ["SeqExpr", [["Def", ["ListPattern", [["FinalPattern", ["NounExpr", "x"], None], ["FinalPattern", ["NounExpr", "x__Resolver"], None]], None], None, ["MethodCallExpr", ["NounExpr", "Ref"], "promise", []]], ["NounExpr", "x__Resolver"]]])

    def test_noun(self):
        self.assertEqual(self.parse("x"), ["NounExpr", 'x'])
        self.assertEqual(self.parse("<x>"), ["NounExpr", 'x__uriGetter'])
        #parens since we're using 'expr' instead of 'start'
        self.assertEqual(self.parse("(x[i] := y; ares__1)"),
                         ["SeqExpr", [["MethodCallExpr", ["NounExpr", "x"], "put", [["NounExpr", "i"], ["Def", ["FinalPattern", ["NounExpr", "ares__1"], None], None, ["NounExpr", "y"]]]], ["NounExpr", "ares__1"], ["NounExpr", "ares__2"]]])


    def test_ejector(self):
        self.assertEqual(self.parse("return"), ["MethodCallExpr", ["NounExpr", "__return"], "run", []])
        self.assertEqual(self.parse("continue"), ["MethodCallExpr", ["NounExpr", "__continue"], "run", []])
        self.assertEqual(self.parse("break"), ["MethodCallExpr", ["NounExpr", "__break"], "run", []])

        self.assertEqual(self.parse("return 1"), ["MethodCallExpr", ["NounExpr", "__return"], "run", [["LiteralExpr", 1]]])
        self.assertEqual(self.parse("continue 2"), ["MethodCallExpr", ["NounExpr", "__continue"], "run", [["LiteralExpr", 2]]])
        self.assertEqual(self.parse("break 3"), ["MethodCallExpr", ["NounExpr", "__break"], "run", [["LiteralExpr", 3]]])

    def test_and(self):
        #XXX tests w/ export
        #value
        self.assertEqual(self.parse("x && y"),
                         ["Escape", ["FinalPattern", ["NounExpr", "ej__1"], None],
                          ["SeqExpr", [["Def", ["IgnorePattern", ["NounExpr", "__Test"]],
                                        ["NounExpr", "ej__1"], ["NounExpr", "x"]],
                                       ["Def", ["IgnorePattern", ["NounExpr", "__Test"]],
                                        ["NounExpr", "ej__1"], ["NounExpr", "y"]],
                                       ["NounExpr", "true"]]],
                          ["Catch", ["IgnorePattern", None],
                           ["NounExpr", "false"]]])
        #fxOnly
        self.assertEqual(self.parse("(x && y; 2)"),
                         ["SeqExpr",
                          [["Escape", ["FinalPattern", ["NounExpr", "ej__1"], None],
                            ["SeqExpr", [["Def", ["IgnorePattern", ["NounExpr", "__Test"]],
                                          ["NounExpr", "ej__1"], ["NounExpr", "x"]],
                                         ["Def", ["IgnorePattern", ["NounExpr", "__Test"]],
                                          ["NounExpr", "ej__1"], ["NounExpr", "y"]]]],
                            None],
                           ["LiteralExpr", 2]]])
        #control
        self.assertEqual(self.parse("if (x && y) { a } else { b }"),
                         ["Escape", ["FinalPattern", ["NounExpr", "ej__1"], None],
                          ["SeqExpr", [["Def", ["IgnorePattern", ["NounExpr", "__Test"]],
                                        ["NounExpr", "ej__1"], ["NounExpr", "x"]],
                                       ["Def", ["IgnorePattern", ["NounExpr", "__Test"]],
                                        ["NounExpr", "ej__1"], ["NounExpr", "y"]],
                                       ["NounExpr", "a"]]],
                          ["Catch", ["IgnorePattern", None],
                           ["NounExpr", "b"]]])

    def test_or(self):
        #XXX tests w/ export
        #value
        self.assertEqual(self.parse("x || y"),
                         ["Escape", ["FinalPattern", ["NounExpr", "ej__1"], None],
                          ["SeqExpr",
                           [["Escape", ["FinalPattern", ["NounExpr", "ej__3"], None],
                             ["Def", ["IgnorePattern", ["NounExpr", "__Test"]],
                              ["NounExpr", "ej__3"], ["NounExpr", "x"]],
                             ["Catch", ["IgnorePattern", None],
                              ["Def", ["IgnorePattern", ["NounExpr", "__Test"]],
                               ["NounExpr", "ej__1"], ["NounExpr", "y"]]]],
                            ["NounExpr", "true"]]],
                          ["Catch", ["IgnorePattern", None],
                           ["NounExpr", "false"]]])
        #fxOnly
        self.assertEqual(self.parse("(x || y; 2)"),
                         ["SeqExpr",
                          [["Escape", ["FinalPattern", ["NounExpr", "ej__1"], None],
                           ["Escape", ["FinalPattern", ["NounExpr", "ej__3"], None],
                            ["Def", ["IgnorePattern", ["NounExpr", "__Test"]],
                            ["NounExpr", "ej__3"], ["NounExpr", "x"]],
                           ["Catch", ["IgnorePattern", None],
                            ["Def", ["IgnorePattern", ["NounExpr", "__Test"]],
                             ["NounExpr", "ej__1"], ["NounExpr", "y"]]]],
                            None],
                           ["LiteralExpr", 2]]])
        #control
        self.assertEqual(self.parse("if (x || y) { a } else { b }"),
                         ["Escape", ["FinalPattern", ["NounExpr", "ej__1"], None],
                          ["SeqExpr",
                           [["Escape", ["FinalPattern", ["NounExpr", "ej__3"], None],
                             ["Def", ["IgnorePattern", ["NounExpr", "__Test"]],
                              ["NounExpr", "ej__3"], ["NounExpr", "x"]],
                             ["Catch", ["IgnorePattern", None],
                              ["Def", ["IgnorePattern", ["NounExpr", "__Test"]],
                               ["NounExpr", "ej__1"], ["NounExpr", "y"]]]],
                            ["NounExpr", "a"]]],
                          ["Catch", ["IgnorePattern", None],
                           ["NounExpr", "b"]]])

    def test_matchbind(self):
        #value
        self.assertEqual(self.parse("x =~ y"),
                         ["SeqExpr",
                          [["Def", ["ListPattern",
                                    [["FinalPattern", ["NounExpr", "rs__7"],
                                      None],
                                     ["SlotPattern", ["NounExpr", "y"], None]],
                                    None],
                            None,
                            ["Escape",
                             ["FinalPattern", ["NounExpr", "ej__1"], None],
                             ["SeqExpr",
                              [["Def", ["FinalPattern", ["NounExpr", "y"],
                                        None],
                                ["NounExpr", "ej__1"],
                                ["NounExpr", "x"]],
                               ["MethodCallExpr", ["NounExpr", "__makeList"],
                                "run",
                                [["NounExpr", "true"], ["Slot", "y"]]]]],
                             ["Catch", ["FinalPattern", ["NounExpr", "ex__3"],
                                        None],
                              ["SeqExpr",
                               [["Def", ["FinalPattern", ["NounExpr", "br__5"],
                                         None],
                                 None,
                                 ["MethodCallExpr", ["NounExpr", "Ref"],
                                  "broken",
                                  [["NounExpr", "ex__3"]]]],
                                ["MethodCallExpr", ["NounExpr", "__makeList"],
                                 "run",
                                 [["NounExpr", "false"], ["NounExpr", "br__5"]
                                  ]]]]]]],
                           ["NounExpr", "rs__7"]]])
        #fxOnly
        self.assertEqual(self.parse("(x =~ y; 2)"),
                         ["SeqExpr",
                          [["Def", ["ListPattern",
                                    [["SlotPattern", ["NounExpr", "y"], None]],
                                    None],
                            None,
                            ["Escape",
                             ["FinalPattern", ["NounExpr", "ej__1"], None],
                             ["SeqExpr",
                              [["Def", ["FinalPattern", ["NounExpr", "y"],
                                        None],
                                ["NounExpr", "ej__1"],
                                ["NounExpr", "x"]],
                               ["MethodCallExpr", ["NounExpr", "__makeList"],
                                "run",
                                [["Slot", "y"]]]]],
                             ["Catch", ["FinalPattern", ["NounExpr", "ex__3"],
                                        None],
                              ["SeqExpr",
                               [["Def", ["FinalPattern", ["NounExpr", "br__5"],
                                         None],
                                 None,
                                 ["MethodCallExpr", ["NounExpr", "Ref"],
                                  "broken",
                                  [["NounExpr", "ex__3"]]]],
                                ["MethodCallExpr", ["NounExpr", "__makeList"],
                                 "run",
                                 [["NounExpr", "br__5"]
                                  ]]]]]]],
                           ["LiteralExpr", 2]]])
        #control
        self.assertEqual(self.parse("if (x =~ y) { a } else { b }"),
                         ["Escape",
                          ["FinalPattern", ["NounExpr", "ej__1"], None],
                          ["SeqExpr",
                           [["Def", ["FinalPattern", ["NounExpr", "y"], None],
                             ["NounExpr", "ej__1"],
                             ["NounExpr", "x"]],
                            ["NounExpr", "a"]]],
                          ["Catch", ["IgnorePattern", None],
                           ["NounExpr", "b"]]])


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
                              ["Script", None, [],
                               [["Method", None,
                                 "run",
                                 [["FinalPattern", ["NounExpr", "key__3"],
                                   None],
                                  ["FinalPattern", ["NounExpr", "value__5"],
                                   None]],
                                 None,
                                 ["SeqExpr",
                                  [["MethodCallExpr", ["NounExpr", "require"],
                                    "run", [["NounExpr", "validFlag__1"],
                                            ["LiteralExpr",
                                             "For-loop body isn't valid "
                                             "after for-loop exits."]]],
                                   ["Escape", ["FinalPattern",
                                               ["NounExpr", "ej__7"], None],
                                    ["SeqExpr",
                                     [["Def", ["IgnorePattern", None],
                                       ["NounExpr", "ej__7"],
                                       ["NounExpr", "key__3"]],
                                      ["Def", ["FinalPattern",
                                               ["NounExpr", "x"], None],
                                       ["NounExpr", "ej__7"],
                                       ["NounExpr", "value__5"]],
                                      ["Escape", ["FinalPattern",
                                                  ["NounExpr", "__continue"],
                                                  None],
                                       ["SeqExpr",
                                        [["NounExpr", "z"],
                                         ["NounExpr", "null"]]],
                                       None]]],
                                       ["Catch",
                                        ["IgnorePattern", None],
                                        ["NounExpr", "null"]]]]]
                                 ]], []]]]],
                            ["Assign", ["NounExpr", "validFlag__1"],
                             ["NounExpr", "false"]]],
                           ["NounExpr", "null"]]],
                          None])

    def test_accum(self):
        self.assertEqual(
            self.parse(
                    "accum a for x in y { _.foo() }"),
                    ["SeqExpr",
                     [["Def", ["VarPattern", ["NounExpr", "accum__1"], None],
                       None, ["NounExpr", "a"]],
                      ["Escape", ["FinalPattern", ["NounExpr", "__break"],
                                     None],
                          ["SeqExpr",
                           [["Def", ["VarPattern",
                                    ["NounExpr", "validFlag__3"],
                                    None],
                            None,
                                   ["NounExpr", "true"]],
                           ["Finally",
                            ["MethodCallExpr", ["NounExpr", "y"], "iterate",
                             [["Object", "For-loop body",
                              ["IgnorePattern", None],
                              ["Script", None, [],
                               [["Method", None,
                                 "run",
                                 [["FinalPattern", ["NounExpr", "key__5"],
                                   None],
                                  ["FinalPattern", ["NounExpr", "value__7"],
                                   None]],
                                 None,
                                 ["SeqExpr",
                                  [["MethodCallExpr", ["NounExpr", "require"],
                                    "run", [["NounExpr", "validFlag__3"],
                                            ["LiteralExpr",
                                             "For-loop body isn't valid "
                                             "after for-loop exits."]]],
                                   ["Escape", ["FinalPattern",
                                               ["NounExpr", "ej__9"], None],
                                    ["SeqExpr",
                                     [["Def", ["IgnorePattern", None],
                                       ["NounExpr", "ej__9"],
                                       ["NounExpr", "key__5"]],
                                      ["Def", ["FinalPattern",
                                               ["NounExpr", "x"], None],
                                       ["NounExpr", "ej__9"],
                                       ["NounExpr", "value__7"]],
                                      ["Escape", ["FinalPattern",
                                                  ["NounExpr", "__continue"],
                                                  None],
                                       ["SeqExpr",
                                        [["Assign", ["NounExpr", "accum__1"],
                                          ["MethodCallExpr",
                                           ["NounExpr", "accum__1"],
                                           "foo", []]],
                                         ["NounExpr", "null"]]],
                                       None]]],
                                       ["Catch",
                                        ["IgnorePattern", None],
                                        ["NounExpr", "null"]]]]]
                                 ]], []]]]],
                            ["Assign", ["NounExpr", "validFlag__3"],
                             ["NounExpr", "false"]]],
                           ["NounExpr", "null"]]],
                          None],
                      ["NounExpr", "accum__1"]]])

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
                          ["Script", None, [],
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
                ["Script", None, [],
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
                      [["SlotPattern", ["NounExpr", "b"], None],
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
                 [["LiteralExpr", "&b"], ["Slot", "b"]]]]]]])


    def test_object(self):
        self.assertEqual(self.parse("def foo {}"),
                         ["Object", None,
                          ["FinalPattern", ["NounExpr", "foo"], None],
                          ["Script", None, [],
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
                              ["Script", None, [],
                               [],
                               [["Matcher",
                                 ["FinalPattern", ["NounExpr", "pair__1"], None],
                                 ["MethodCallExpr", ["NounExpr", "E"],
                                  "callWithPair",
                                  [["NounExpr", "super"],
                                   ["NounExpr", "pair__1"]]]]]]]]]]])

        self.assertEqual(self.parse("var foo extends baz {}"),
                         ["SeqExpr",
                          [["Def", ["SlotPattern", ["NounExpr", "foo"], None],
                            None,
                            ["HideExpr",
                             ["SeqExpr",
                              [["Def", ["FinalPattern", ["NounExpr", "super"],
                                        None],
                                None,
                                ["NounExpr", "baz"]],
                               ["Object", None,
                                ["VarPattern", ["NounExpr", "foo"], None],
                                ["Script", None, [],
                                 [],
                                 [["Matcher",
                                   ["FinalPattern", ["NounExpr", "pair__1"],
                                    None],
                                   ["MethodCallExpr", ["NounExpr", "E"],
                                    "callWithPair",
                                    [["NounExpr", "super"],
                                     ["NounExpr", "pair__1"]]]]]]],
                               ["Slot", "foo"]]]]],
                            ["NounExpr", "foo"]]])

        self.assertEqual(self.parse("bind foo extends baz {}"),
                         ["Def", ["ViaPattern",
                                    ["MethodCallExpr",
                                     ["NounExpr", "__bind"],
                                     "run",
                                      [["NounExpr", "foo__Resolver"]]],
                                    ["IgnorePattern", None]],
                            None,
                          ["HideExpr",
                           ["Def",
                            ["FinalPattern", ["NounExpr", "foo"], None],
                            None,
                            ["HideExpr",
                             ["SeqExpr",
                              [["Def", ["FinalPattern", ["NounExpr", "super"],
                                        None],
                                None,
                                ["NounExpr", "baz"]],
                               ["Object", None,
                                ["FinalPattern", ["NounExpr", "foo"], None],
                                ["Script", None, [],
                                 [],
                                 [["Matcher",
                                   ["FinalPattern", ["NounExpr", "pair__1"],
                                    None],
                                   ["MethodCallExpr", ["NounExpr", "E"],
                                    "callWithPair",
                                    [["NounExpr", "super"],
                                     ["NounExpr", "pair__1"]]]]]]]]]]]]])

    def test_to(self):
        self.assertEqual(self.parse("def foo { to baz() { x } }"),
                         ["Object", None,
                          ["FinalPattern", ["NounExpr", "foo"], None],
                          ["Script", None, [],
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
                          ["Script", None, [],
                           [["Method", None, "baz",
                             [["FinalPattern", ["NounExpr", "x"], None]], None,
                             ["NounExpr", "y"]]],
                             []]])

    def test_matcher(self):
        self.assertEqual(self.parse("def foo { match x { y } }"),
                         ["Object", None,
                          ["FinalPattern", ["NounExpr", "foo"], None],
                          ["Script", None, [], [],
                           [["Matcher", ["FinalPattern",
                                         ["NounExpr", "x"], None],
                             ["NounExpr", "y"]]]]])

    def test_function(self):
        self.assertEqual(self.parse("def foo() { y }"),
                         ["Object", None,
                          ["FinalPattern", ["NounExpr", "foo"], None],
                          ["Script", None, [],
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
                          ["Script", None, [],
                           [["Method", None, "run",
                             [["FinalPattern", ["NounExpr", "x"], None]], None,
                             ["NounExpr", "y"]]],
                             []]])


    def test_samePattern(self):
        self.assertEqual(self.parse("def ==x := y"),
                         ["Def",
                          ["ViaPattern",
                           ["MethodCallExpr",
                           ["NounExpr", "__is"],
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
                ["Escape", ["FinalPattern", ["NounExpr", "ej__5"], None],
                 ["SeqExpr",
                  [["Def", ["ListPattern",
                            [["FinalPattern", ["NounExpr", "a"], None],
                             ["FinalPattern", ["NounExpr", "b"], None]],
                            None],
                    ["NounExpr", "ej__5"],
                    ["NounExpr", "specimen__1"]],
                    ["NounExpr", "c"]]],
                 ["Catch", ["IgnorePattern", None],
                ["Escape", ["FinalPattern", ["NounExpr", "ej__3"], None],
                 ["SeqExpr",
                  [["Def", ["FinalPattern", ["NounExpr", "x"], None],
                    ["NounExpr", "ej__3"],
                    ["NounExpr", "specimen__1"]],
                    ["NounExpr", "y"]]],
                 ["Catch", ["IgnorePattern", None],
                  ["MethodCallExpr", ["NounExpr", "throw"],
                   "run",
                   [["MethodCallExpr", ["LiteralExpr", "no match: "],
                     "add", [["NounExpr", "specimen__1"]]]]]]]]]]]])

    def test_switch2(self):
        self.assertEqual(
            self.parse("switch (1) {match ==2 {'a'} match ==1 {'c'}}"),
            ["HideExpr",
             ["SeqExpr",
              [["Def", ["FinalPattern", ["NounExpr", "specimen__1"], None],
                None, ["LiteralExpr", 1]],
                ["Escape", ["FinalPattern", ["NounExpr", "ej__5"], None],
                 ["SeqExpr",
                  [["Def", ["ViaPattern",
                            ["MethodCallExpr", ["NounExpr", "__is"],
                             "run", [["LiteralExpr", 2]]],
                            ["IgnorePattern", None]],
                    ["NounExpr", "ej__5"],
                    ["NounExpr", "specimen__1"]],
                    ["LiteralExpr", ["Character", "a"]]]],
                 ["Catch", ["IgnorePattern", None],
                ["Escape", ["FinalPattern", ["NounExpr", "ej__3"], None],
                 ["SeqExpr",
                  [["Def",
                    ["ViaPattern",
                     ["MethodCallExpr", ["NounExpr", "__is"],
                      "run", [["LiteralExpr", 1]]],
                     ["IgnorePattern", None]],
                    ["NounExpr", "ej__3"],
                    ["NounExpr", "specimen__1"]],
                    ["LiteralExpr", ["Character", "c"]]]],
                 ["Catch", ["IgnorePattern", None],
                  ["MethodCallExpr", ["NounExpr", "throw"],
                   "run",
                   [["MethodCallExpr", ["LiteralExpr", "no match: "],
                     "add", [["NounExpr", "specimen__1"]]]]]]]]]]]])


    def test_interface(self):
        self.assertEqual(self.parse("interface foo {}"),
                         ["Def", ["FinalPattern", ["NounExpr", "foo"], None],
                          None,
                          ["HideExpr",
                           ["MethodCallExpr",
                            ["NounExpr", "__makeProtocolDesc"],
                            "run",
                            [["LiteralExpr", ""],
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
                                 [["LiteralExpr", ""],
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
                          ["NounExpr", "x"],
                          ["FinalPattern", ["NounExpr", "specimen__1"], None],
                          ["Escape", ["FinalPattern",
                                      ["NounExpr", "ej__5"], None],
                           ["SeqExpr",
                            [["Def", ["FinalPattern",
                                    ["NounExpr", "p"], None],
                              ["NounExpr", "ej__5"],
                              ["NounExpr", "specimen__1"]],
                             ["NounExpr", "y"]]],
                           ["Catch",
                            ["IgnorePattern", None],
                            ["Escape", ["FinalPattern",
                                        ["NounExpr", "ej__3"], None],
                             ["SeqExpr",
                              [["Def", ["FinalPattern",
                                        ["NounExpr", "q"], None],
                                ["NounExpr", "ej__3"],
                                ["NounExpr", "specimen__1"]],
                               ["NounExpr", "z"]]],
                             ["Catch",
                              ["IgnorePattern", None],
                               ["MethodCallExpr",
                                 ["NounExpr", "throw"],
                                 "run",
                                 [["MethodCallExpr",
                                   ["LiteralExpr", "no match: "],
                                   "add",
                                   [["NounExpr", "specimen__1"]]]]]]]]]])

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
                              ["Script", None, [],
                               [["Method", None, "run",
                                 [["FinalPattern",
                                   ["NounExpr", "resolution__3"], None]],
                                 None,
                                 ["KernelTry",
                                  ["SeqExpr",
                                   [["Def", ["IgnorePattern", None],
                                     None,
                                     ["MethodCallExpr",
                                      ["NounExpr", "Ref"],
                                      "fulfillment",
                                      [["NounExpr", "resolution__3"]]]],
                                    ["NounExpr", "y"]]],
                                  ["FinalPattern", ["NounExpr", "ex__1"],
                                   None],
                                  ["MethodCallExpr", ["NounExpr", "throw"],
                                   "run",
                                   [["NounExpr", "ex__1"]]]]]],
                               []]]]]])
        self.assertEqual(self.parse("when (x) -> { y } catch p { z }"),
                         ["HideExpr",
                          ["MethodCallExpr",
                             ["NounExpr", "Ref"],
                             "whenResolved",
                             [["NounExpr", "x"],
                             ["Object", "when-catch 'done' function",
                              ["IgnorePattern", None],
                              ["Script", None, [],
                               [["Method", None, "run",
                                 [["FinalPattern",
                                   ["NounExpr", "resolution__1"], None]],
                                 None,
                                 ["KernelTry",
                                  ["SeqExpr",
                                   [["Def", ["IgnorePattern", None],
                                     None,
                                     ["MethodCallExpr",
                                      ["NounExpr", "Ref"],
                                      "fulfillment",
                                      [["NounExpr", "resolution__1"]]]],
                                    ["NounExpr", "y"]]],
                                   ["FinalPattern", ["NounExpr", "p"],
                                    None],
                                   ["NounExpr", "z"]]]],
                               []]]]]])
