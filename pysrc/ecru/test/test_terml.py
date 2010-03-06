from twisted.trial import unittest
from ecru.terml import TermLParser, TermLiteral, character, Tag, _Term, Term

class ParserTest(unittest.TestCase):
    """
    Test E parser rules.
    """


    def getParser(self, rule):
        def parse(src):
            p = TermLParser(src)
            return p.apply(rule)
        return parse


    def test_literal(self):
        """
        Literals are parsed to literal terms.
        """
        parse = self.getParser("literal")
        self.assertEqual(parse('"foo bar"'), TermLiteral('.String.', "foo bar"))
        self.assertEqual(parse("'x'"), TermLiteral('.char', character('x')))
        self.assertEqual(parse("0xDECAFC0FFEEBAD"), TermLiteral('.int.', 0xDECAFC0FFEEBAD))
        self.assertEqual(parse("0755"), TermLiteral('.int.', 0755))
        self.assertEqual(parse("3.14159E17"), TermLiteral('.float64.', 3.14159E17))
        self.assertEqual(parse("1e9"), TermLiteral('.float64.', 1e9))
        self.assertEqual(parse("0"), TermLiteral(".int.", 0))
        self.assertEqual(parse("7"), TermLiteral(".int", 7))
        self.assertEqual(parse("-1"), TermLiteral(".int.", -1))
        self.assertEqual(parse("-3.14"), TermLiteral('.float64.', -3.14))
        self.assertEqual(parse("3_000"), TermLiteral('.int.', 3000))
        self.assertEqual(parse("0.91"), TermLiteral('float64.', 0.91))
        self.assertEqual(parse("3e-2"), TermLiteral('.float64.', 3e-2))

        self.assertEqual(parse("'\\n'"), TermLiteral('.char.', character("\n")))
        self.assertEqual(parse('"foo\\nbar"'), TermLiteral('.String.', "foo\nbar"))
        self.assertEqual(parse("'\\u0061'"), TermLiteral('.char.', character("a")))
        self.assertEqual(parse('"z\141p"'), TermLiteral('.String.', "zap"))
        self.assertEqual(parse('"x\41"'), TermLiteral('.String.', "x!"))
        self.assertEqual(parse('"foo\\\nbar"'), TermLiteral('.String.', "foobar"))


    def test_simpleTag(self):
        """
        Tags are parsed properly.
        """

        parse = self.getParser("tag")
        self.assertEqual(parse("foo"), Tag("foo"))
        self.assertEqual(parse('::"foo"'), Tag('::"foo"'))
        self.assertEqual(parse("::foo"), Tag('::foo'))
        self.assertEqual(parse("foo::baz"), Tag('foo::baz'))
        self.assertEqual(parse('foo::"baz"'), Tag('foo::"baz"'))
        self.assertEqual(parse("biz::baz::foo"), Tag('biz::baz::foo'))
        self.assertEqual(parse("foo_yay"), Tag('foo_yay'))
        self.assertEqual(parse("foo$baz32"), Tag('foo$baz32'))
        self.assertEqual(parse("foo-baz.19"), Tag('foo-baz.19'))


    def test_simpleTerm(self):
        """
        Kernel syntax for terms is parsed properly.
        """

        parse = self.getParser("baseTerm")
        self.assertEqual(parse("x"), _Term(Tag("x"), []))
        self.assertEqual(parse("x()"), _Term(Tag("x"), []))
        self.assertEqual(parse("x(1)"), _Term(Tag("x"), [_Term(TermLiteral(".int.", 1), [])]))
        self.assertEqual(parse("x(1, 2)"), _Term(Tag("x"), [_Term(TermLiteral(".int.", 1), []),
                                                         _Term(TermLiteral(".int.", 2), [])]))
        self.assertEqual(parse("1"), _Term(TermLiteral(".int.", 1), []))
        self.assertEqual(parse('"1"'), _Term(TermLiteral(".String.", "1"), []))
        self.assertRaises(ValueError, parse, "'x'(x)")
        self.assertRaises(ValueError, parse, '3.14(1)')
        self.assertRaises(ValueError, parse, '"foo"(x)')
        self.assertRaises(ValueError, parse, "1(2)")


    def test_fullTerm(self):
        """
        Shortcut syntax for terms is handled.
        """

        parse = self.getParser("term")
        self.assertEqual(parse("[x, y, 1]"), parse(".tuple.(x, y, 1)"))
        self.assertEqual(parse("{x, y, 1}"), parse(".bag.(x, y, 1)"))
        self.assertEqual(parse("f {x, y, 1}"), parse("f(.bag.(x, y, 1))"))
        self.assertEqual(parse("a: b"), parse(".attr.(a, b)"))
        self.assertEqual(parse('"a": b'), parse('.attr.("a", b)'))
        self.assertEqual(parse('a: [b]'), parse('.attr.(a, .tuple.(b))'))


    def test_unparse(self):

        def assertRoundtrip(txt):
            self.assertEqual("Term(%r)" % (txt,), repr(Term(txt)))
        cases = ["1", "3.25", "f", "f(1)", "f(1, 2)", "f(a, b)",
                  "{a, b}", "[a, b]", "f{1, 2}",  '''{"name": "Robert", attrs: {'c': 3}}''']
        for case in cases:
            assertRoundtrip(case)


    def test_valueHole(self):
        parse = self.getParser("term")

        qt = Term("foo($x, 2)")
        qt.substitute({"x": 1})
