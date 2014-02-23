# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

from twisted.trial import unittest
from monte.parser import makeParser
from terml.nodes import Tag

class Listifier(object):
    def leafData(self, data, span):
        return data
    def leafTag(self, tag, span):
        return tag
    def term(self, tag, args):
        if isinstance(tag, Tag): #argh
            if tag.name == 'null':
                return None
            if tag.name == '.tuple.':
                return args
            return [tag.name] + args
        else:
            return tag

def serialize(term):
    return term.build(Listifier())

class ParserTest(unittest.TestCase):
    """
    Test Monte parser rules.
    """


    def getParser(self, rule):
        def parse(src):
            p = makeParser(src)
            r, e = p.apply(rule)
            return serialize(r)
        return parse


    def test_literal(self):
        """
        Literals are parsed to LiteralExprs.
        """
        parse = self.getParser("literal")
        self.assertEqual(parse(u'"foo bar"'), ["LiteralExpr", u"foo bar"])
        self.assertEqual(parse('"foo bar"'), ["LiteralExpr", "foo bar"])
        self.assertEqual(parse("'z'"), ["LiteralExpr", ["Character", "z"]])
        self.assertEqual(parse("0xDECAFC0FFEEBAD"), ["LiteralExpr", 0xDECAFC0FFEEBAD])
        self.assertEqual(parse("3.14159E17"), ["LiteralExpr", 3.14159E17])
        self.assertEqual(parse("1e9"), ["LiteralExpr", 1e9])
        self.assertEqual(parse("0"), ["LiteralExpr", 0])
        self.assertEqual(parse("7"), ["LiteralExpr", 7])
        self.assertEqual(parse("3_000"), ["LiteralExpr", 3000])
        self.assertEqual(parse("0.91"), ["LiteralExpr", 0.91])
        self.assertEqual(parse("3e-2"), ["LiteralExpr", 3e-2])
        self.assertEqual(parse("'\\n'"), ["LiteralExpr", ["Character", "\n"]])
        self.assertEqual(parse('"foo\\nbar"'), ["LiteralExpr", "foo\nbar"])
        self.assertEqual(parse("'\\u0061'"), ["LiteralExpr", ["Character", u"a"]])
        self.assertEqual(parse('"foo\\\nbar"'), ["LiteralExpr", "foobar"])


    def test_noun(self):
        """
        Nouns and URL expressions can be parsed.
        """
        parse = self.getParser("expr")
        self.assertEqual(parse("foo"), ["NounExpr", "foo"])
        self.assertEqual(parse("<unsafe>"), ["URIGetter", "unsafe"])
        self.assertEqual(parse("::length"), ["NounExpr", "length"])
        self.assertEqual(parse('::"if"'), ["NounExpr", "if"])
        self.assertEqual(parse("iffy"), ["NounExpr", "iffy"])


    def test_uri(self):
        """
        URI literals.
        """
        parse = self.getParser("prim")
        self.assertEqual(parse("<import:foo.makeBaz>"),
                         ["URIExpr", "import", "foo.makeBaz"])

    def test_holes(self):
        """
        Value and pattern holes are recognized and checked.
        """
        p = makeParser("${0}")
        self.assertEqual(serialize(p.apply("noun")[0]), ["QuasiLiteralExpr", 0])
        p = makeParser("${3}")
        self.assertEqual(serialize(p.apply("noun")[0]), ["QuasiLiteralExpr", 3])
        p = makeParser("@{0}")
        self.assertEqual(serialize(p.apply("noun")[0]), ["QuasiPatternExpr", 0])
        p = makeParser("@{7}")
        self.assertEqual(serialize(p.apply("noun")[0]), ["QuasiPatternExpr", 7])

    def test_quasiliterals(self):
        """
        Quasiliterals are recognized and collected by the parser.
        """

        parse = self.getParser("prim")

        self.assertEqual(parse("`foo`"), ["QuasiExpr", None, [["QuasiText", "foo"]]])
        self.assertEqual(parse("bob`foo`"), ["QuasiExpr", "bob", [["QuasiText", "foo"]]])
        self.assertEqual(parse("bob`foo`` $x baz`"), ["QuasiExpr", "bob", [["QuasiText", "foo` "], ["QuasiExprHole", ["NounExpr", "x"]], ["QuasiText", " baz"]]])

    def test_quasiliteralsParens(self):
        """
        Parentheses should not be eaten by the parser incorrectly.
        """

        parse = self.getParser("prim")

        self.assertEqual(parse("`($x)`"),
                         ["QuasiExpr", None, [
                             ["QuasiText", "("],
                             ["QuasiExprHole", ["NounExpr", "x"]],
                             ["QuasiText", ")"]]])

    def test_quasiliteralsBraces(self):
        """
        Test that quasiliterals and braces don't smash each other up.
        """
        parse = self.getParser("seq")
        self.assertEqual(parse("{`${x}`}; 1"), ["SeqExpr", [["HideExpr", ["QuasiExpr", None, [["QuasiExprHole", ["NounExpr", "x"]], ["QuasiText", '']]]], ["LiteralExpr", 1]]])

    def test_collections(self):
        """
        List and map syntax.
        """
        parse = self.getParser("prim")
        self.assertEqual(parse("[]"), ["ListExpr", []])
        self.assertEqual(parse("[1, a]"), ["ListExpr", [["LiteralExpr", 1], ["NounExpr", "a"]]])
        self.assertEqual(parse("[1=> a, 2 => b]"), ["MapExpr", [["MapExprAssoc", ["LiteralExpr", 1], ["NounExpr", "a"]], ["MapExprAssoc", ["LiteralExpr", 2], ["NounExpr", "b"]]]])
        self.assertEqual(parse("[1=> a, => &x, => y]"), ["MapExpr", [["MapExprAssoc", ["LiteralExpr", 1], ["NounExpr", "a"]], ["MapExprExport", ["SlotExpr", ["NounExpr", "x"]]], ["MapExprExport", ["NounExpr", "y"]]]])

    def test_body(self):
        """
        Braces in the right places.
        """
        parse = self.getParser("prim")
        self.assertEqual(parse("{1}"), ["HideExpr", ["LiteralExpr", 1]]);
        self.assertEqual(parse("{}"), ["HideExpr", ["SeqExpr", []]]);

    def test_call(self):
        """
        Method calls and sends of various stripes.
        """
        parse = self.getParser("call")
        self.assertEqual(parse("x.y()"), ["MethodCallExpr", ["NounExpr", "x"], "y", []])
        self.assertEqual(parse("x.y"), ["VerbCurryExpr", ["NounExpr", "x"], "y"])
        self.assertEqual(parse("x()"), ["FunctionCallExpr", ["NounExpr", "x"], []])
        self.assertEqual(parse("{1}.x()"), ["MethodCallExpr", ["HideExpr", ["LiteralExpr", 1]], "x", []])
        self.assertEqual(parse("x(a, b)"), ["FunctionCallExpr", ["NounExpr", "x"], [["NounExpr", "a"], ["NounExpr", "b"]]])
        self.assertEqual(parse("x.foo(a, b)"), ["MethodCallExpr", ["NounExpr", "x"], "foo", [["NounExpr", "a"], ["NounExpr", "b"]]])
        self.assertEqual(parse("x(a, b)"), ["FunctionCallExpr", ["NounExpr", "x"], [["NounExpr", "a"], ["NounExpr", "b"]]])
        self.assertEqual(parse("x <- (a, b)"), ["FunctionSendExpr", ["NounExpr", "x"], [["NounExpr", "a"], ["NounExpr", "b"]]])
        self.assertEqual(parse("x <- foo(a, b)"), ["MethodSendExpr", ["NounExpr", "x"], "foo", [["NounExpr", "a"], ["NounExpr", "b"]]])
        self.assertEqual(parse("x <- foo"), ["SendCurryExpr", ["NounExpr", "x"], "foo"])
        self.assertEqual(parse("x[a, b]"), ["GetExpr", ["NounExpr", "x"], [["NounExpr", "a"], ["NounExpr", "b"]]])
        self.assertEqual(parse("x[a, b].foo(c)"), ["MethodCallExpr", ["GetExpr", ["NounExpr", "x"], [["NounExpr", "a"], ["NounExpr", "b"]]], "foo", [["NounExpr", "c"]]])

    def test_prefix(self):
        """
        Prefix operators work and have the right precedence.
        """
        parse = self.getParser("prefix")
        self.assertEqual(parse("!x.a()"), ["LogicalNot", ["MethodCallExpr", ["NounExpr", "x"], "a", []]])
        self.assertEqual(parse("~17"), ["BinaryNot", ["LiteralExpr", 17]])
        self.assertEqual(parse("&x"), ["SlotExpr", ["NounExpr", "x"]])
        self.assertEqual(parse("&&x"), ["BindingExpr", ["NounExpr" ,"x"]])
        self.assertEqual(parse("-(3.pow(2))"), ["Minus", ["MethodCallExpr", ["LiteralExpr", 3], "pow", [["LiteralExpr", 2]]]])
        self.assertEqual(parse("-(3.14.pow(2))"), ["Minus", ["MethodCallExpr", ["LiteralExpr", 3.14], "pow", [["LiteralExpr", 2]]]])

    def test_pattern(self):
        """
        Pattern parsing.
        """
        parse = self.getParser("pattern")
        self.assertEqual(parse("a"), ["FinalPattern", ["NounExpr", "a"], None])
        self.assertEqual(parse("[]"), ["ListPattern", [], None])
        self.assertEqual(parse("[a]"), ["ListPattern", [["FinalPattern", ["NounExpr", "a"], None]], None])
        self.assertEqual(parse("[a, b]"), ["ListPattern", [["FinalPattern", ["NounExpr", "a"], None], ["FinalPattern", ["NounExpr", "b"], None]], None])
        self.assertEqual(parse("[a] + b"), ["ListPattern", [["FinalPattern", ["NounExpr", "a"], None]], ["FinalPattern", ["NounExpr", "b"], None]])
        self.assertEqual(parse("[]"), ["ListPattern", [], None])
        self.assertEqual(parse('["a" => aa, (b) => bb]'), ["MapPattern", [["MapPatternRequired", ["MapPatternAssoc", ["LiteralExpr", "a"], ["FinalPattern", ["NounExpr", "aa"], None]]], ["MapPatternRequired", ["MapPatternAssoc", ["NounExpr", "b"], ["FinalPattern", ["NounExpr", "bb"], None]]]], None])
        self.assertEqual(parse('["a" => aa := 1]'), ["MapPattern", [["MapPatternOptional", ["MapPatternAssoc", ["LiteralExpr", "a"], ["FinalPattern", ["NounExpr", "aa"], None]], ["LiteralExpr", 1]]], None])
        self.assertEqual(parse("[=> aa := 1]"), ["MapPattern", [["MapPatternOptional", ["MapPatternImport", ["FinalPattern", ["NounExpr", "aa"], None]], ["LiteralExpr", 1]]], None])
        self.assertEqual(parse("[=> a]"), ["MapPattern", [["MapPatternRequired", ["MapPatternImport", ["FinalPattern", ["NounExpr", "a"], None]]]], None])
        self.assertEqual(parse('["a" => b] | c'), ["MapPattern", [["MapPatternRequired", ["MapPatternAssoc", ["LiteralExpr", "a"], ["FinalPattern", ["NounExpr", "b"], None]]]], ["FinalPattern", ["NounExpr", "c"], None]])
        self.assertEqual(parse("_"), ["IgnorePattern", None])
        self.assertEqual(parse("__foo"), ["FinalPattern", ["NounExpr", "__foo"], None])
        self.assertEqual(parse("a :int"), ["FinalPattern", ["NounExpr", "a"], ["Guard", ["NounExpr", "int"], []]])
        self.assertEqual(parse("a :List[int]"), ["FinalPattern", ["NounExpr", "a"], ["Guard", ["NounExpr", "List"], [[["NounExpr", "int"]]]]])
        self.assertEqual(parse("`foo`"), ["QuasiPattern", None, [["QuasiText", "foo"]]])
        self.assertEqual(parse("baz`foo`"), ["QuasiPattern", "baz", [["QuasiText", "foo"]]])
        self.assertEqual(parse("==1"), ["SamePattern", ["LiteralExpr", 1]])
        self.assertEqual(parse("==x"), ["SamePattern", ["NounExpr", "x"]])
        self.assertEqual(parse("!=x"), ["NotSamePattern", ["NounExpr", "x"]])
        self.assertEqual(parse("var x"), ["VarPattern", ["NounExpr", "x"], None])
        self.assertEqual(parse("bind y"), ["BindPattern", ["NounExpr", "y"], None])
        self.assertEqual(parse("&z"), ["SlotPattern", ["NounExpr", "z"], None])
        self.assertEqual(parse("&&z"), ["BindingPattern", ["NounExpr", "z"]])
        self.assertEqual(parse("var x :int"), ["VarPattern", ["NounExpr", "x"], ["Guard", ["NounExpr", "int"], []]])
        self.assertEqual(parse("bind y :float64"), ["BindPattern", ["NounExpr", "y"], ["Guard", ["NounExpr", "float64"], []]])
        self.assertEqual(parse("&z :Foo"), ["SlotPattern", ["NounExpr", "z"], ["Guard", ["NounExpr", "Foo"], []]])
        self.assertEqual(parse("via (foo) [x]"), ["ViaPattern", ["NounExpr", "foo"], ["ListPattern" ,[["FinalPattern", ["NounExpr", "x"], None]], None]])
        self.assertEqual(parse("x ? (y)"), ["SuchThatPattern", ["FinalPattern", ["NounExpr", "x"], None], ["NounExpr", "y"]])

    def test_match(self):
        """
        Match and don't-match operators.
        """
        parse = self.getParser("expr")
        self.assertEqual(parse("x =~ [a, b]"), ["MatchBind", ["NounExpr", "x"], ["ListPattern", [["FinalPattern", ["NounExpr", "a"], None] ,["FinalPattern", ["NounExpr", "b"], None]], None]])
        self.assertEqual(parse("x !~ y :String"), ["Mismatch", ["NounExpr", "x"], ["FinalPattern", ["NounExpr", "y"], ["Guard", ["NounExpr", "String"], []]]])

    def test_operators(self):
        parse = self.getParser("expr")
        self.assertEqual(parse("x ** -y"), ["Pow", ["NounExpr", "x"], ["Minus", ["NounExpr", "y"]]])
        self.assertEqual(parse("x * y"), ["Multiply", ["NounExpr", "x"], ["NounExpr", "y"]])
        self.assertEqual(parse("x / y"), ["Divide", ["NounExpr", "x"], ["NounExpr", "y"]])
        self.assertEqual(parse("x // y"), ["FloorDivide", ["NounExpr", "x"], ["NounExpr", "y"]])
        self.assertEqual(parse("x % y"), ["Remainder", ["NounExpr", "x"], ["NounExpr", "y"]])
        self.assertEqual(parse("x %% y"), ["Mod", ["NounExpr", "x"], ["NounExpr", "y"]])
        self.assertEqual(parse("x + y"), ["Add", ["NounExpr", "x"], ["NounExpr", "y"]])
        self.assertEqual(parse("(x + y) + z"), ["Add", ["Add", ["NounExpr", "x"], ["NounExpr", "y"]], ["NounExpr", "z"]])
        self.assertEqual(parse("1 + 1"), ["Add", ["LiteralExpr", 1], ["LiteralExpr", 1]])
        self.assertEqual(parse("x - y"), ["Subtract", ["NounExpr", "x"], ["NounExpr", "y"]])
        self.assertEqual(parse("x - y + z"), ["Add", ["Subtract", ["NounExpr", "x"], ["NounExpr", "y"]], ["NounExpr", "z"]])
        self.assertEqual(parse("x..y"), ["Thru", ["NounExpr", "x"], ["NounExpr", "y"]])
        self.assertEqual(parse("x..!y"), ["Till", ["NounExpr", "x"], ["NounExpr", "y"]])
        self.assertEqual(parse("x < y"), ["LessThan", ["NounExpr", "x"], ["NounExpr", "y"]])
        self.assertEqual(parse("x <= y"), ["LessThanEqual", ["NounExpr", "x"], ["NounExpr", "y"]])
        self.assertEqual(parse("x <=> y"), ["AsBigAs", ["NounExpr", "x"], ["NounExpr", "y"]])
        self.assertEqual(parse("x >= y"), ["GreaterThanEqual", ["NounExpr", "x"], ["NounExpr", "y"]])
        self.assertEqual(parse("x > y"), ["GreaterThan", ["NounExpr", "x"], ["NounExpr", "y"]])
        self.assertEqual(parse("x :y"), ["Coerce",  ["NounExpr", "x"], ["Guard", ["NounExpr", "y"], []]])
        self.assertEqual(parse("x :y[z, a]"), ["Coerce",  ["NounExpr", "x"], ["Guard", ["NounExpr", "y"], [[["NounExpr", "z"], ["NounExpr", "a"]]]]])
        self.assertEqual(parse("x << y"), ["ShiftLeft", ["NounExpr", "x"], ["NounExpr", "y"]])
        self.assertEqual(parse("x >> y"), ["ShiftRight", ["NounExpr", "x"], ["NounExpr", "y"]])
        self.assertEqual(parse("x << y >> z"), ["ShiftRight", ["ShiftLeft", ["NounExpr", "x"], ["NounExpr", "y"]], ["NounExpr", "z"]])
        self.assertEqual(parse("x == y"), ["Same", ["NounExpr", "x"], ["NounExpr", "y"]])
        self.assertEqual(parse("x != y"), ["NotSame", ["NounExpr", "x"], ["NounExpr", "y"]])
        self.assertEqual(parse("x &! y"), ["ButNot", ["NounExpr", "x"], ["NounExpr", "y"]])
        self.assertEqual(parse("x ^ y"), ["BinaryXor", ["NounExpr", "x"], ["NounExpr", "y"]])
        self.assertEqual(parse("x & y"), ["BinaryAnd", ["NounExpr", "x"], ["NounExpr", "y"]])
        self.assertEqual(parse("x & y & z"), ["BinaryAnd", ["BinaryAnd", ["NounExpr", "x"], ["NounExpr", "y"]], ["NounExpr", "z"]])
        self.assertEqual(parse("x | y"), ["BinaryOr", ["NounExpr", "x"], ["NounExpr", "y"]])
        self.assertEqual(parse("x | y | z"), ["BinaryOr", ["BinaryOr", ["NounExpr", "x"], ["NounExpr", "y"]], ["NounExpr", "z"]])
        self.assertEqual(parse("x and y"), ["LogicalAnd", ["NounExpr", "x"], ["NounExpr", "y"]])
        self.assertEqual(parse("x and y and  z"), ["LogicalAnd", ["NounExpr", "x"], ["LogicalAnd", ["NounExpr", "y"], ["NounExpr", "z"]]])
        self.assertEqual(parse("x or y"), ["LogicalOr", ["NounExpr", "x"], ["NounExpr", "y"]])
        self.assertEqual(parse("x or y or z"), ["LogicalOr", ["NounExpr", "x"], ["LogicalOr", ["NounExpr", "y"], ["NounExpr", "z"]]])

    def test_precedence(self):
        parse = self.getParser("expr")
        self.assertEqual(parse("x and y or z"),  parse("(x and y) or z"))
        self.assertEqual(parse("x or y and z"),  parse("x or (y and z)"))
        self.assertEqual(parse("x =~ a or y == b and z != c"),
                         parse("(x =~ a) or ((y == b) and (z != c))"))
        self.assertEqual(parse("x | y > z"),  parse("x | (y > z)"))
        self.assertEqual(parse("x < y | y > z"),  parse("(x < y) | (y > z)"))
        self.assertEqual(parse("x & y > z"),  parse("x & (y > z)"))
        self.assertEqual(parse("x < y & y > z"),  parse("(x < y) & (y > z)"))
        self.assertEqual(parse("x..y <=> a..!b"),  parse("(x..y) <=> (a..!b)"))
        self.assertEqual(parse("a << b..y >> z"),  parse("(a << b) .. (y >> z)"))
        self.assertEqual(parse("x.y() :List[int] > a..!b"),
                         parse("(x.y() :List[int]) > a..!b"))
        self.assertEqual(parse("a + b >> z"),  parse("(a + b) >> z"))
        self.assertEqual(parse("a >> b + z"),  parse("a >> (b + z)"))
        self.assertEqual(parse("a + b * c"), parse("a + (b * c)"))
        self.assertEqual(parse("a - b + c * d"), parse("(a - b) + (c * d)"))
        self.assertEqual(parse("a / b + c - d"), parse("((a / b) + c) - d"))
        self.assertEqual(parse("a / b * !c ** ~d"), parse("(a / b) * ((!c) ** (~d))"))

    def test_assign(self):
        """
        Assignment expressions.
        """
        parse = self.getParser("expr")
        self.assertEqual(parse("x := y"), ["Assign", ["NounExpr", "x"], ["NounExpr", "y"]])
        self.assertEqual(parse("x := y := z"), ["Assign", ["NounExpr", "x"], ["Assign", ["NounExpr", "y"], ["NounExpr", "z"]]])
        self.assertEqual(parse("x foo= y"), ["VerbAssign", "foo", ["NounExpr", "x"], [["NounExpr", "y"]]])
        self.assertEqual(parse("x foo= (y)"), ["VerbAssign", "foo", ["NounExpr", "x"], [["NounExpr", "y"]]])
        self.assertEqual(parse("x foo= (y, z)"), ["VerbAssign", "foo", ["NounExpr", "x"], [["NounExpr", "y"], ["NounExpr", "z"]]])
        self.assertEqual(parse("x[i] := y"), ["Assign", ["GetExpr", ["NounExpr", "x"], [["NounExpr", "i"]]], ["NounExpr", "y"]])
        self.assertEqual(parse("x(i) := y"), ["Assign", ["FunctionCallExpr", ["NounExpr", "x"], [["NounExpr", "i"]]], ["NounExpr", "y"]])
        self.assertEqual(parse("x += y"), ["AugAssign", "Add", ["NounExpr", "x"], ["NounExpr", "y"]])
        self.assertEqual(parse("x -= y"), ["AugAssign", "Subtract", ["NounExpr", "x"], ["NounExpr", "y"]])
        self.assertEqual(parse("x *= y"), ["AugAssign", "Multiply", ["NounExpr", "x"], ["NounExpr", "y"]])
        self.assertEqual(parse("x /= y"), ["AugAssign", "Divide", ["NounExpr", "x"], ["NounExpr", "y"]])
        self.assertEqual(parse("x //= y"), ["AugAssign", "FloorDivide", ["NounExpr", "x"], ["NounExpr", "y"]])
        self.assertEqual(parse("x %= y"), ["AugAssign", "Remainder", ["NounExpr", "x"], ["NounExpr", "y"]])
        self.assertEqual(parse("x %%= y"), ["AugAssign", "Mod", ["NounExpr", "x"], ["NounExpr", "y"]])
        self.assertEqual(parse("x **= y"), ["AugAssign", "Pow", ["NounExpr", "x"], ["NounExpr", "y"]])
        self.assertEqual(parse("x >>= y"), ["AugAssign", "ShiftRight", ["NounExpr", "x"], ["NounExpr", "y"]])
        self.assertEqual(parse("x <<= y"), ["AugAssign", "ShiftLeft", ["NounExpr", "x"], ["NounExpr", "y"]])
        self.assertEqual(parse("x &= y"), ["AugAssign", "BinaryAnd", ["NounExpr", "x"], ["NounExpr", "y"]])
        self.assertEqual(parse("x |= y"), ["AugAssign", "BinaryOr", ["NounExpr", "x"], ["NounExpr", "y"]])
        self.assertEqual(parse("x ^= y"), ["AugAssign", "BinaryXor", ["NounExpr", "x"], ["NounExpr", "y"]])

    def test_def(self):
        """
        Variable declaration expressions.
        """
        parse = self.getParser("blockExpr")
        self.assertEqual(parse("def x := 1"), ["Def", ["FinalPattern", ["NounExpr", "x"], None], None, ["LiteralExpr", 1]])
        self.assertEqual(parse("def x exit e := 1"), ["Def", ["FinalPattern", ["NounExpr", "x"], None], ["NounExpr", "e"], ["LiteralExpr", 1]])
        self.assertEqual(parse("def [a, b] := 1"), ["Def", ["ListPattern", [["FinalPattern", ["NounExpr", "a"], None],["FinalPattern", ["NounExpr", "b"], None]], None], None, ["LiteralExpr", 1]])
        self.assertEqual(parse("def x"), ["Forward", ["NounExpr", "x"]])
        self.assertEqual(parse("var x := 1"), ["Def", ["VarPattern", ["NounExpr", "x"], None], None, ["LiteralExpr", 1]])
        self.assertEqual(parse("bind x := 1"), ["Def", ["BindPattern", ["NounExpr", "x"], None], None, ["LiteralExpr", 1]])

    def test_object(self):
        """
        Object expressions.
        """
        parse = self.getParser("blockExpr")
        self.assertEqual(parse("object foo {}"), ["Object", None, ["FinalPattern", ["NounExpr", "foo"], None], ["Script", None, None, [], [], []]])
        self.assertEqual(parse("object foo:\n pass"), ["Object", None, ["FinalPattern", ["NounExpr", "foo"], None], ["Script", None, None, [], [], []]])
        self.assertEqual(parse("object _:\n pass"), ["Object", None, ["IgnorePattern", None], ["Script", None, None, [], [], []]])
        self.assertEqual(parse("object _ {}"), ["Object", None, ["IgnorePattern", None], ["Script", None, None, [], [], []]])
        self.assertEqual(parse("object bind foo {}"), ["Object", None, ["BindPattern", ["NounExpr", "foo"], None], ["Script", None, None, [], [], []]])
        self.assertEqual(parse("object bind foo:\n pass"), ["Object", None, ["BindPattern", ["NounExpr", "foo"], None], ["Script", None, None, [], [], []]])
        self.assertEqual(parse("object var foo {}"), ["Object", None, ["VarPattern", ["NounExpr", "foo"], None], ["Script", None, None, [], [], []]])
        self.assertEqual(parse("object var foo:\n pass"), ["Object", None, ["VarPattern", ["NounExpr", "foo"], None], ["Script", None, None, [], [], []]])
        self.assertEqual(parse("bind foo {}"), ["Object", None, ["BindPattern", ["NounExpr", "foo"], None], ["Script", None, None, [], [], []]])
        self.assertEqual(parse("bind foo:\n pass"), ["Object", None, ["BindPattern", ["NounExpr", "foo"], None], ["Script", None, None, [], [], []]])
        self.assertEqual(parse("var foo {}"), ["Object", None, ["VarPattern", ["NounExpr", "foo"], None], ["Script", None, None, [], [], []]])
        self.assertEqual(parse("var foo:\n pass"), ["Object", None, ["VarPattern", ["NounExpr", "foo"], None], ["Script", None, None, [], [], []]])
        self.assertEqual(parse("/** yes */ object foo {}"),  ["Object", "yes", ["FinalPattern", ["NounExpr", "foo"], None], ["Script", None, None, [], [], []]])
        self.assertEqual(parse("object foo implements A {}"),  ["Object", None, ["FinalPattern", ["NounExpr", "foo"], None], ["Script", None, None, [["NounExpr", "A"]], [], []]])
        self.assertEqual(parse("object foo implements A:\n pass"),  ["Object", None, ["FinalPattern", ["NounExpr", "foo"], None], ["Script", None, None, [["NounExpr", "A"]], [], []]])
        self.assertEqual(parse("object foo extends B {}"),  ["Object", None, ["FinalPattern", ["NounExpr", "foo"], None], ["Script", ["NounExpr", "B"], None, [], [], []]])
        self.assertEqual(parse("object foo extends B:\n pass"),  ["Object", None, ["FinalPattern", ["NounExpr", "foo"], None], ["Script", ["NounExpr", "B"], None, [], [], []]])
        self.assertEqual(parse("object foo extends B implements A {}"),  ["Object", None, ["FinalPattern", ["NounExpr", "foo"], None], ["Script", ["NounExpr", "B"], None, [["NounExpr", "A"]], [], []]])
        self.assertEqual(parse("object foo extends B implements A:\n pass"),  ["Object", None, ["FinalPattern", ["NounExpr", "foo"], None], ["Script", ["NounExpr", "B"], None, [["NounExpr", "A"]], [], []]])
        self.assertEqual(parse("object foo as X implements A, B {}"),  ["Object", None, ["FinalPattern", ["NounExpr", "foo"], None], ["Script", None, ["NounExpr", "X"], [["NounExpr", "A"], ["NounExpr", "B"]], [], []]])
        self.assertEqual(parse("object foo as X implements A, B:\n pass"),  ["Object", None, ["FinalPattern", ["NounExpr", "foo"], None], ["Script", None, ["NounExpr", "X"], [["NounExpr", "A"], ["NounExpr", "B"]], [], []]])
        self.assertEqual(parse("object foo {to baz(x) {1}}"), ["Object", None, ["FinalPattern", ["NounExpr", "foo"], None], ["Script", None, None, [], [["To", None, "baz", [["FinalPattern", ["NounExpr", "x"], None]], None, ["LiteralExpr", 1]]], []]])
        self.assertEqual(parse("object foo:\n to baz(x):\n  1"), ["Object", None, ["FinalPattern", ["NounExpr", "foo"], None], ["Script", None, None, [], [["To", None, "baz", [["FinalPattern", ["NounExpr", "x"], None]], None, ["LiteralExpr", 1]]], []]])
        self.assertEqual(parse("object foo {/** woot */ to baz(x) {1}}"), ["Object", None, ["FinalPattern", ["NounExpr", "foo"], None], ["Script", None, None, [], [["To", "woot", "baz", [["FinalPattern", ["NounExpr", "x"], None]], None, ["LiteralExpr", 1]]], []]])
        self.assertEqual(parse("object foo:\n /** woot */\n to baz(x):\n  1"), ["Object", None, ["FinalPattern", ["NounExpr", "foo"], None], ["Script", None, None, [], [["To", "woot", "baz", [["FinalPattern", ["NounExpr", "x"], None]], None, ["LiteralExpr", 1]]], []]])
        self.assertEqual(parse("object foo {\nto baz(x) {\n1}}"), ["Object", None, ["FinalPattern", ["NounExpr", "foo"], None], ["Script", None, None, [], [["To", None, "baz", [["FinalPattern", ["NounExpr", "x"], None]], None, ["LiteralExpr", 1]]], []]])
        self.assertEqual(parse("object foo {\nto baz() {\n1}}"), ["Object", None, ["FinalPattern", ["NounExpr", "foo"], None], ["Script", None, None, [], [["To", None, "baz", [], None, ["LiteralExpr", 1]]], []]])
        self.assertEqual(parse("object foo {method baz(x) {1}}"), ["Object", None, ["FinalPattern", ["NounExpr", "foo"], None], ["Script", None, None, [], [["Method", None, "baz", [["FinalPattern", ["NounExpr", "x"], None]], None, ["LiteralExpr", 1]]], []]])
        self.assertEqual(parse("object foo:\n method baz(x):\n  1"), ["Object", None, ["FinalPattern", ["NounExpr", "foo"], None], ["Script", None, None, [], [["Method", None, "baz", [["FinalPattern", ["NounExpr", "x"], None]], None, ["LiteralExpr", 1]]], []]])
        self.assertEqual(parse("object foo {match [verb, args] {1}}"), ["Object", None, ["FinalPattern", ["NounExpr", "foo"], None], ["Script", None, None, [], [], [["Matcher", ["ListPattern", [["FinalPattern", ["NounExpr", "verb"], None], ["FinalPattern", ["NounExpr", "args"], None]], None], ["LiteralExpr", 1]]]]])
        self.assertEqual(parse("object foo:\n match [verb, args]:\n  1"), ["Object", None, ["FinalPattern", ["NounExpr", "foo"], None], ["Script", None, None, [], [], [["Matcher", ["ListPattern", [["FinalPattern", ["NounExpr", "verb"], None], ["FinalPattern", ["NounExpr", "args"], None]], None], ["LiteralExpr", 1]]]]])
        self.assertEqual(parse("def foo(x) {}"), ["Object", None, ["FinalPattern", ["NounExpr", "foo"], None], ["Function", [["FinalPattern", ["NounExpr", "x"], None]], None, [], ["SeqExpr", []]]])
        self.assertEqual(parse("def foo(x):\n pass"), ["Object", None, ["FinalPattern", ["NounExpr", "foo"], None], ["Function", [["FinalPattern", ["NounExpr", "x"], None]], None, [], ["SeqExpr", []]]])
        self.assertEqual(parse("bind foo {method baz(x) {1}}"), ["Object", None, ["BindPattern", ["NounExpr", "foo"], None], ["Script", None, None, [], [["Method", None, "baz", [["FinalPattern", ["NounExpr", "x"], None]], None, ["LiteralExpr", 1]]], []]])
        self.assertEqual(parse("bind foo:\n method baz(x):\n  1\n"), ["Object", None, ["BindPattern", ["NounExpr", "foo"], None], ["Script", None, None, [], [["Method", None, "baz", [["FinalPattern", ["NounExpr", "x"], None]], None, ["LiteralExpr", 1]]], []]])
        self.assertEqual(parse("var foo {method baz(x) {1}}"), ["Object", None, ["VarPattern", ["NounExpr", "foo"], None], ["Script", None, None, [], [["Method", None, "baz", [["FinalPattern", ["NounExpr", "x"], None]], None, ["LiteralExpr", 1]]], []]])
        self.assertEqual(parse("var foo:\n method baz(x):\n  1"), ["Object", None, ["VarPattern", ["NounExpr", "foo"], None], ["Script", None, None, [], [["Method", None, "baz", [["FinalPattern", ["NounExpr", "x"], None]], None, ["LiteralExpr", 1]]], []]])
        self.assertEqual(parse("object foo {to baz(x) :any {1}}"), ["Object", None, ["FinalPattern", ["NounExpr", "foo"], None], ["Script", None, None, [], [["To", None, "baz", [["FinalPattern", ["NounExpr", "x"], None]], ["Guard", ["NounExpr", "any"], []], ["LiteralExpr", 1]]], []]])
        self.assertEqual(parse("object foo:\n to baz(x) :any:\n  1"), ["Object", None, ["FinalPattern", ["NounExpr", "foo"], None], ["Script", None, None, [], [["To", None, "baz", [["FinalPattern", ["NounExpr", "x"], None]], ["Guard", ["NounExpr", "any"], []], ["LiteralExpr", 1]]], []]])

    def test_interface(self):
        """
        Interface expressions.
        """
        parse = self.getParser("blockExpr")
        self.assertEqual(parse("/** yes */ interface foo {}"), ["Interface", "yes", ["FinalPattern", ["NounExpr", "foo"], None], None, [], [], []])
        self.assertEqual(parse("/** yes */\ninterface foo:\n pass\n"), ["Interface", "yes", ["FinalPattern", ["NounExpr", "foo"], None], None, [], [], []])
        self.assertEqual(parse("interface foo {}"), ["Interface", None, ["FinalPattern", ["NounExpr", "foo"], None], None, [], [], []])
        self.assertEqual(parse("interface foo:\n pass"), ["Interface", None, ["FinalPattern", ["NounExpr", "foo"], None], None, [], [], []])
        self.assertEqual(parse("interface foo extends baz {}"), ["Interface", None, ["FinalPattern", ["NounExpr", "foo"], None], None, [["NounExpr", "baz"]], [], []])
        self.assertEqual(parse("interface foo extends baz:\n pass"), ["Interface", None, ["FinalPattern", ["NounExpr", "foo"], None], None, [["NounExpr", "baz"]], [], []])
        self.assertEqual(parse("interface foo implements bar {}"), ["Interface", None, ["FinalPattern", ["NounExpr", "foo"], None], None, [], [["NounExpr", "bar"]], []])
        self.assertEqual(parse("interface foo implements bar:\n pass\n"), ["Interface", None, ["FinalPattern", ["NounExpr", "foo"], None], None, [], [["NounExpr", "bar"]], []])
        self.assertEqual(parse("interface foo extends boz, biz implements bar {}"), ["Interface", None, ["FinalPattern", ["NounExpr", "foo"], None], None, [["NounExpr", "boz"], ["NounExpr", "biz"]], [["NounExpr", "bar"]], []])
        self.assertEqual(parse("interface foo extends boz, biz implements bar:\n pass\n"), ["Interface", None, ["FinalPattern", ["NounExpr", "foo"], None], None, [["NounExpr", "boz"], ["NounExpr", "biz"]], [["NounExpr", "bar"]], []])
        self.assertEqual(parse("interface foo guards FooStamp extends boz, biz implements bar {}"), ["Interface", None, ["FinalPattern", ["NounExpr", "foo"], None], ["FinalPattern", ["NounExpr", "FooStamp"], None], [["NounExpr", "boz"], ["NounExpr", "biz"]], [["NounExpr", "bar"]], []])
        self.assertEqual(parse("interface foo guards FooStamp extends boz, biz implements bar:\n pass"), ["Interface", None, ["FinalPattern", ["NounExpr", "foo"], None], ["FinalPattern", ["NounExpr", "FooStamp"], None], [["NounExpr", "boz"], ["NounExpr", "biz"]], [["NounExpr", "bar"]], []])
        self.assertEqual(parse("interface foo {to run(a :int, b :float64) :any}"), ["Interface", None, ["FinalPattern", ["NounExpr", "foo"], None], None, [], [], [["MessageDesc", None, "to", "run", [["ParamDesc", ["NounExpr", "a"], ["Guard", ["NounExpr", "int"], []]], ["ParamDesc", ["NounExpr", "b"], ["Guard", ["NounExpr", "float64"], []]]], ["Guard", ["NounExpr", "any"], []]]]])
        self.assertEqual(parse("interface foo:\n to run(a :int, b :float64) :any"), ["Interface", None, ["FinalPattern", ["NounExpr", "foo"], None], None, [], [], [["MessageDesc", None, "to", "run", [["ParamDesc", ["NounExpr", "a"], ["Guard", ["NounExpr", "int"], []]], ["ParamDesc", ["NounExpr", "b"], ["Guard", ["NounExpr", "float64"], []]]], ["Guard", ["NounExpr", "any"], []]]]])
        self.assertEqual(parse("interface foo(a :int, b :float64) :any"), ["Interface", None, ["FinalPattern", ["NounExpr", "foo"], None], None, [], [], ["InterfaceFunction", [["ParamDesc", ["NounExpr", "a"], ["Guard", ["NounExpr", "int"], []]], ["ParamDesc", ["NounExpr", "b"], ["Guard", ["NounExpr", "float64"], []]]], ["Guard", ["NounExpr", "any"], []]]])
        self.assertEqual(parse("interface a guards b ? c () {}"), ["Interface", None, ["FinalPattern", ["NounExpr", "a"], None], ["SuchThatPattern", ["FinalPattern", ["NounExpr", "b"], None], ["FunctionCallExpr", ["NounExpr", "c"], []]], [], [], []])
        self.assertEqual(parse("interface a guards b ? c ():\n pass"), ["Interface", None, ["FinalPattern", ["NounExpr", "a"], None], ["SuchThatPattern", ["FinalPattern", ["NounExpr", "b"], None], ["FunctionCallExpr", ["NounExpr", "c"], []]], [], [], []])

    def test_ejector(self):
        """
        Special ejector-invoking expressions.
        """
        parse = self.getParser("expr")
        self.assertEqual(parse("return x + y"), ["Return", ["Add", ["NounExpr", "x"], ["NounExpr", "y"]]])
        self.assertEqual(parse("return(x + y)"), ["Return", ["Add", ["NounExpr", "x"], ["NounExpr", "y"]]])
        self.assertEqual(parse("return()"), ["Return", None])
        self.assertEqual(parse("return"), ["Return", None])
        self.assertEqual(parse("continue x + y"), ["Continue", ["Add", ["NounExpr", "x"], ["NounExpr", "y"]]])
        self.assertEqual(parse("continue(x + y)"), ["Continue", ["Add", ["NounExpr", "x"], ["NounExpr", "y"]]])
        self.assertEqual(parse("continue()"), ["Continue", None])
        self.assertEqual(parse("continue"), ["Continue", None])
        self.assertEqual(parse("break x + y"), ["Break", ["Add", ["NounExpr", "x"], ["NounExpr", "y"]]])
        self.assertEqual(parse("break(x + y)"), ["Break", ["Add", ["NounExpr", "x"], ["NounExpr", "y"]]])
        self.assertEqual(parse("break()"), ["Break", None])
        self.assertEqual(parse("break"), ["Break", None])
        self.assertEqual(parse("breaks"), ["NounExpr", "breaks"])


    def test_try(self):
        """
        Try/catch and try/finally blocks.
        """
        parse = self.getParser("blockExpr")
        self.assertEqual(parse("try {1} finally {2}"), ["Try", ["LiteralExpr", 1], [], ["LiteralExpr", 2]])
        self.assertEqual(parse("try:\n 1\nfinally:\n 2"), ["Try", ["LiteralExpr", 1], [], ["LiteralExpr", 2]])
        self.assertEqual(parse("try {1} catch p {2}"), ["Try", ["LiteralExpr", 1], [["Catch", ["FinalPattern", ["NounExpr", "p"], None], ["LiteralExpr", 2]]], None])
        self.assertEqual(parse("try:\n 1\ncatch p:\n 2"), ["Try", ["LiteralExpr", 1], [["Catch", ["FinalPattern", ["NounExpr", "p"], None], ["LiteralExpr", 2]]], None])
        self.assertEqual(parse("try {1} catch p {2} finally {3}"), ["Try", ["LiteralExpr", 1], [["Catch", ["FinalPattern", ["NounExpr", "p"], None], ["LiteralExpr", 2]]], ["LiteralExpr", 3]])
        self.assertEqual(parse("try:\n 1\ncatch p:\n 2\nfinally:\n 3"), ["Try", ["LiteralExpr", 1], [["Catch", ["FinalPattern", ["NounExpr", "p"], None], ["LiteralExpr", 2]]], ["LiteralExpr", 3]])
        self.assertEqual(parse("try {1} catch p {2} catch q {3}"), ["Try", ["LiteralExpr", 1], [["Catch", ["FinalPattern", ["NounExpr", "p"], None], ["LiteralExpr", 2]], ["Catch", ["FinalPattern", ["NounExpr", "q"], None], ["LiteralExpr", 3]]], None])
        self.assertEqual(parse("try:\n 1\ncatch p:\n 2\ncatch q:\n 3"), ["Try", ["LiteralExpr", 1], [["Catch", ["FinalPattern", ["NounExpr", "p"], None], ["LiteralExpr", 2]], ["Catch", ["FinalPattern", ["NounExpr", "q"], None], ["LiteralExpr", 3]]], None])

    def test_switch(self):
        """
        Switch expression.
        """
        parse = self.getParser("blockExpr")
        self.assertEqual(parse("switch (1) { match ==1 {2}}"), ["Switch", ["LiteralExpr", 1], [["Matcher", ["SamePattern", ["LiteralExpr", 1]], ["LiteralExpr", 2]]]])
        self.assertEqual(parse("switch (1):\n match ==1:\n  2"), ["Switch", ["LiteralExpr", 1], [["Matcher", ["SamePattern", ["LiteralExpr", 1]], ["LiteralExpr", 2]]]])

    def test_lambda(self):
        """
        Lambda expression.
        """
        parse = self.getParser("blockExpr")
        self.assertEqual(parse("/** foo */ fn a, [b,c] {1}"), ["Lambda", "foo", [["FinalPattern", ["NounExpr", "a"], None], ["ListPattern", [["FinalPattern", ["NounExpr", "b"], None], ["FinalPattern", ["NounExpr", "c"], None]], None]], ["LiteralExpr", 1]])

    def test_while(self):
        """
        While expression.
        """
        parse = self.getParser("blockExpr")
        self.assertEqual(parse("while (true) {1}"), ["While", ["NounExpr", "true"], ["LiteralExpr", 1], None])
        self.assertEqual(parse("while (true):\n 1"), ["While", ["NounExpr", "true"], ["LiteralExpr", 1], None])

    def test_when(self):
        """
        When expression.
        """
        parse = self.getParser("blockExpr")
        self.assertEqual(parse("when (d) -> {1}"), ["When", [["NounExpr", "d"]], ["LiteralExpr", 1], [], None])
        self.assertEqual(parse("when (d) ->\n 1"), ["When", [["NounExpr", "d"]], ["LiteralExpr", 1], [], None])
        self.assertEqual(parse("when (d) ->\n 1\ncatch p:\n 2"), ["When", [["NounExpr", "d"]], ["LiteralExpr", 1], [["Catch", ["FinalPattern", ["NounExpr", "p"], None], ["LiteralExpr", 2]]], None])
        self.assertEqual(parse("when (d) -> {1} finally {3}"), ["When", [["NounExpr", "d"]], ["LiteralExpr", 1], [], ["LiteralExpr", 3]])
        self.assertEqual(parse("when (d) ->\n 1\nfinally:\n 3"), ["When", [["NounExpr", "d"]], ["LiteralExpr", 1], [], ["LiteralExpr", 3]])
        self.assertEqual(parse("when (e, d) -> {1}"), ["When", [["NounExpr", "e"], ["NounExpr", "d"]], ["LiteralExpr", 1], [], None])
        self.assertEqual(parse("when (e, d) ->\n 1"), ["When", [["NounExpr", "e"], ["NounExpr", "d"]], ["LiteralExpr", 1], [], None])

    def test_listcomp(self):
        parse = self.getParser("expr")
        self.assertEqual(parse("[1 for k => v in x]"), ["ListComp", ["FinalPattern", ["NounExpr", "k"], None], ["FinalPattern", ["NounExpr", "v"], None], ["NounExpr", "x"], None, ["LiteralExpr", 1]])
        self.assertEqual(parse("[1 for v in x]"), ["ListComp", None, ["FinalPattern", ["NounExpr", "v"], None], ["NounExpr", "x"], None, ["LiteralExpr", 1]])
        self.assertEqual(parse("[1 for v in x][0]"), ["GetExpr", ["ListComp", None, ["FinalPattern", ["NounExpr", "v"], None], ["NounExpr", "x"], None, ["LiteralExpr", 1]], [["LiteralExpr", 0]]])
        self.assertEqual(parse("[1 for v in x if y]"), ["ListComp", None, ["FinalPattern", ["NounExpr", "v"], None], ["NounExpr", "x"], ["NounExpr", "y"], ["LiteralExpr", 1]])

    def test_mapcomp(self):
        parse = self.getParser("expr")
        self.assertEqual(parse("[1 => 2 for k => v in x]"), ["MapComp", ["FinalPattern", ["NounExpr", "k"], None], ["FinalPattern", ["NounExpr", "v"], None], ["NounExpr", "x"], None, ["LiteralExpr", 1], ["LiteralExpr", 2]])
        self.assertEqual(parse("[1 => 2 for v in x]"), ["MapComp", None, ["FinalPattern", ["NounExpr", "v"], None], ["NounExpr", "x"], None, ["LiteralExpr", 1], ["LiteralExpr", 2]])
        self.assertEqual(parse("[1 => 2 for v in x if y]"), ["MapComp", None, ["FinalPattern", ["NounExpr", "v"], None], ["NounExpr", "x"], ["NounExpr", "y"], ["LiteralExpr", 1], ["LiteralExpr", 2]])

    def test_for(self):
        """
        For-loop expression.
        """
        parse = self.getParser("blockExpr")
        self.assertEqual(parse("for k => v in x {}"), ["For", ["FinalPattern", ["NounExpr", "k"], None], ["FinalPattern", ["NounExpr", "v"], None], ["NounExpr", "x"], ["SeqExpr", []], None])
        self.assertEqual(parse("for k => v in x:\n pass"), ["For", ["FinalPattern", ["NounExpr", "k"], None], ["FinalPattern", ["NounExpr", "v"], None], ["NounExpr", "x"], ["SeqExpr", []], None])
        self.assertEqual(parse("for v in x {}"), ["For", None, ["FinalPattern", ["NounExpr", "v"], None], ["NounExpr", "x"], ["SeqExpr", []], None])
        self.assertEqual(parse("for v in x:\n pass"), ["For", None, ["FinalPattern", ["NounExpr", "v"], None], ["NounExpr", "x"], ["SeqExpr", []], None])
        self.assertEqual(parse("for v in x {1} catch p {2}"), ["For", None, ["FinalPattern", ["NounExpr", "v"], None], ["NounExpr", "x"], ["LiteralExpr", 1], ["Catch", ["FinalPattern", ["NounExpr", "p"], None], ["LiteralExpr", 2]]])
        self.assertEqual(parse("for v in x:\n 1\ncatch p:\n 2"), ["For", None, ["FinalPattern", ["NounExpr", "v"], None], ["NounExpr", "x"], ["LiteralExpr", 1], ["Catch", ["FinalPattern", ["NounExpr", "p"], None], ["LiteralExpr", 2]]])

    def test_if(self):
        """
        If expression.
        """
        parse = self.getParser("blockExpr")
        self.assertEqual(parse("if (true) {1}"), ["If", ["NounExpr", "true"], ["LiteralExpr", 1], None])
        self.assertEqual(parse("if (true):\n 1"), ["If", ["NounExpr", "true"], ["LiteralExpr", 1], None])
        self.assertEqual(parse("if (true) {1} else {2}"), ["If", ["NounExpr", "true"], ["LiteralExpr", 1], ["LiteralExpr", 2]])

        self.assertEqual(parse("if (true):\n 1\nelse:\n 2"), ["If", ["NounExpr", "true"], ["LiteralExpr", 1], ["LiteralExpr", 2]])

    def test_escape(self):
        """
        Escape expression.
        """
        parse = self.getParser("blockExpr")
        self.assertEqual(parse("escape e {1}"), ["Escape", ["FinalPattern", ["NounExpr", "e"], None], ["LiteralExpr", 1], None])
        self.assertEqual(parse("escape e {1} catch p {2}"), ["Escape", ["FinalPattern", ["NounExpr", "e"], None], ["LiteralExpr", 1], ["Catch", ["FinalPattern", ["NounExpr", "p"], None], ["LiteralExpr", 2]]])
        self.assertEqual(parse("escape e:\n 1"), ["Escape", ["FinalPattern", ["NounExpr", "e"], None], ["LiteralExpr", 1], None])
        self.assertEqual(parse("escape e:\n 1\ncatch p:\n 2"), ["Escape", ["FinalPattern", ["NounExpr", "e"], None], ["LiteralExpr", 1], ["Catch", ["FinalPattern", ["NounExpr", "p"], None], ["LiteralExpr", 2]]])

    def test_updoc(self):
        """
        Updoc should get ignored real good.
        """
        parse = self.getParser("start")
        self.assertEqual(parse("? 1 + 1\n1\n"), ["SeqExpr", [["LiteralExpr", 1]]])


    def test_topseq(self):
        """
        Sequence at the top level too.
        """
        parse = self.getParser("start")
        self.assertEqual(parse("x := 1; y"), ["SeqExpr", [["Assign", ["NounExpr", "x"], ["LiteralExpr", 1]], ["NounExpr", "y"]]])
        self.assertEqual(parse("def foo():\n return 3\ndef baz():\n return 4\nfoo() + baz()"),
                         ['SeqExpr',
                          [['Object',
                            None,
                            ['FinalPattern', ['NounExpr', 'foo'], None],
                            ['Function', [], None, [], ['Return', ['LiteralExpr', 3]]]],
                           ['Object',
                            None,
                            ['FinalPattern', ['NounExpr', 'baz'], None],
                            ['Function', [], None, [], ['Return', ['LiteralExpr', 4]]]],
                           ['Add',
                            ['FunctionCallExpr', ['NounExpr', 'foo'], []],
                            ['FunctionCallExpr', ['NounExpr', 'baz'], []]]]])

    def test_meta(self):
        """
        Meta expressions.
        """
        parse = self.getParser("expr")
        self.assertEqual(parse("meta.getState()"), ["Meta", "State"])
        self.assertEqual(parse("meta.scope()"), ["Meta", "Scope"])
        self.assertEqual(parse("meta.context()"), ["Meta", "Context"])
