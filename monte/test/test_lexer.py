from twisted.trial import unittest
from monte.lexer import ELexer, StringFeeder
from terml.nodes import Tag, Term

def lex(s):
    return list(ELexer(StringFeeder(s, '<test data>')))[:-1]

class LexerTests(unittest.TestCase):

    def test_ident(self):
        self.assertEqual(lex("foo_bar9"),     [Term(Tag("IDENTIFIER"), "foo_bar9", None, None)])
        self.assertEqual(lex("foo"),          [Term(Tag("IDENTIFIER"), "foo", None, None)])

    def test_char(self):
        self.assertEqual(lex("'z'"),          [Term(Tag(".char."), "z", None, None)])
        self.assertEqual(lex("'\\n'"),        [Term(Tag(".char."), "\n", None, None)])
        self.assertEqual(lex("'\\u0061'"),    [Term(Tag(".char."), "a", None, None)])

    def test_string(self):
        self.assertEqual(lex('"foo\\\nbar"'), [Term(Tag(".String."), 'foobar', None, None)])
        self.assertEqual(lex('"foo"'),        [Term(Tag(".String."), 'foo', None, None)])
        self.assertEqual(lex('"foo bar 9"'),  [Term(Tag(".String."), 'foo bar 9', None, None)])
        self.assertEqual(lex('"foo\\nbar"'),  [Term(Tag(".String."), 'foo\nbar', None, None)])

    def test_integer(self):
        self.assertEqual(lex('0'),          [Term(Tag(".int."), 0, None, None)])
        self.assertEqual(lex('7'),          [Term(Tag(".int."), 7, None, None)])
        self.assertEqual(lex('3_000'),      [Term(Tag(".int."), 3000, None, None)])
        self.assertEqual(lex('0xABad1dea'), [Term(Tag(".int."), 0xABad1dea, None, None)])

    def test_float(self):
        self.assertEqual(lex('1e9'),       [Term(Tag(".float64."), 1e9, None, None)])
        self.assertEqual(lex('3.1415E17'), [Term(Tag(".float64."), 3.1415E17, None, None)])
        self.assertEqual(lex('0.91'),      [Term(Tag(".float64."), 0.91, None, None)])
        self.assertEqual(lex('3e-2'),      [Term(Tag(".float64."), 3e-2, None, None)])

    def test_uri(self):
        self.assertEqual(lex('<unsafe>'),[Term(Tag("URI_GETTER"), "unsafe", None, None)])
        self.assertEqual(lex('<import:foo.makeBaz>'),
                         [Term(Tag("URI"), "import:foo.makeBaz", None, None)])
