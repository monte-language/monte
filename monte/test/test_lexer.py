from twisted.trial import unittest
from monte.lexer import ELexer, StringFeeder
from terml.nodes import Tag, Term

def lex(s):
    toks = list(ELexer(StringFeeder(s, '<test data>')))
    if toks[-1].tag.name == 'EOL':
        del toks[-1]
    return toks

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

    def test_holes(self):
        self.assertEqual(lex('${'),     [Term(Tag('${'), None, None, None)])
        self.assertEqual(lex('$blee'),  [Term(Tag('DOLLAR_IDENT'), "blee", None, None)])
        self.assertEqual(lex('@{'),     [Term(Tag('@{'), None, None, None)])
        self.assertEqual(lex('@fred'),  [Term(Tag('AT_IDENT'), "fred", None, None)])
        self.assertEqual(lex('@_fred'), [Term(Tag('AT_IDENT'), "_fred", None, None)])
        self.assertEqual(lex('@_'),     [Term(Tag('AT_IDENT'), "_", None, None)])

        self.assertEqual(lex('$0'), [Term(Tag('$'), None, None, None),
                                     Term(Tag(".int."), 0, None, None)])
        self.assertEqual(lex('@1'), [Term(Tag('@'), None, None, None),
                                     Term(Tag(".int."), 1, None, None)])

    def test_braces(self):
        self.assertEqual(lex('[a, 1]'),
                         [Term(Tag('['), None, None, None),
                          Term(Tag('IDENTIFIER'), 'a', None, None),
                          Term(Tag(','), None, None, None),
                          Term(Tag('.int.'), 1, None, None),
                          Term(Tag(']'), None, None, None)])

    def test_dot(self):
        self.assertEqual(lex('.'),   [Term(Tag('.'), None, None, None)])
        self.assertEqual(lex('..'),  [Term(Tag('..'), None, None, None)])
        self.assertEqual(lex('..!'), [Term(Tag('..!'), None, None, None)])

    def test_caret(self):
        self.assertEqual(lex('^'),   [Term(Tag('^'), None, None, None)])
        self.assertEqual(lex('^='),  [Term(Tag('^='), None, None, None)])

    def test_plus(self):
        self.assertEqual(lex('+'),   [Term(Tag('+'), None, None, None)])
        self.assertEqual(lex('+='),  [Term(Tag('+='), None, None, None)])

    def test_minus(self):
        self.assertEqual(lex('-'),   [Term(Tag('-'), None, None, None)])
        self.assertEqual(lex('-='),  [Term(Tag('-='), None, None, None)])
        self.assertEqual(lex('->'),  [Term(Tag('->'), None, None, None)])

    def test_colon(self):
        self.assertEqual(lex(':'),   [Term(Tag(':'), None, None, None)])
        self.assertEqual(lex(':='),  [Term(Tag(':='), None, None, None)])
        self.assertEqual(lex('::'),  [Term(Tag('::'), None, None, None)])

    def test_crunch(self):
        self.assertEqual(lex('<'),   [Term(Tag('<'), None, None, None)])
        self.assertEqual(lex('<-'),  [Term(Tag('<-'), None, None, None)])
        self.assertEqual(lex('<='),  [Term(Tag('<='), None, None, None)])
        self.assertEqual(lex('<<='), [Term(Tag('<<='), None, None, None)])
        self.assertEqual(lex('<=>'), [Term(Tag('<=>'), None, None, None)])

    def test_zap(self):
        self.assertEqual(lex('>'),   [Term(Tag('>'), None, None, None)])
        self.assertEqual(lex('>='),  [Term(Tag('>='), None, None, None)])
        self.assertEqual(lex('>>='), [Term(Tag('>>='), None, None, None)])

    def test_star(self):
        self.assertEqual(lex('*'),   [Term(Tag('*'), None, None, None)])
        self.assertEqual(lex('*='),  [Term(Tag('*='), None, None, None)])
        self.assertEqual(lex('**'),  [Term(Tag('**'), None, None, None)])
        self.assertEqual(lex('**='), [Term(Tag('**='), None, None, None)])

    def test_slash(self):
        self.assertEqual(lex('/'),   [Term(Tag('/'), None, None, None)])
        self.assertEqual(lex('/='),  [Term(Tag('/='), None, None, None)])
        self.assertEqual(lex('//'),  [Term(Tag('//'), None, None, None)])
        self.assertEqual(lex('//='), [Term(Tag('//='), None, None, None)])

    def test_doccomment(self):
        self.assertEqual(lex('/** hello */'),
                         [Term(Tag('/**'), ' hello ', None, None)])

    def test_comment(self):
        self.assertEqual(lex('# yes\n1'), [Term(Tag('#'), ' yes', None, None),
                                           Term(Tag('EOL'), None, None, None),
                                           Term(Tag('.int.'), 1, None, None)])

    def test_backslash(self):
        self.assertEqual(lex('foo\\\n   baz'), lex('foo baz'))

    def test_bang(self):
        self.assertEqual(lex('!'),   [Term(Tag('!'), None, None, None)])
        self.assertEqual(lex('!='),  [Term(Tag('!='), None, None, None)])
        self.assertEqual(lex('!~'),  [Term(Tag('!~'), None, None, None)])

    def test_eq(self):
        self.assertEqual(lex('=='),   [Term(Tag('=='), None, None, None)])
        self.assertEqual(lex('=~'),  [Term(Tag('=~'), None, None, None)])
        self.assertEqual(lex('=>'),  [Term(Tag('=>'), None, None, None)])

    def test_and(self):
        self.assertEqual(lex('&'),   [Term(Tag('&'), None, None, None)])
        self.assertEqual(lex('&='),  [Term(Tag('&='), None, None, None)])
        self.assertEqual(lex('&!'),  [Term(Tag('&!'), None, None, None)])
        self.assertEqual(lex('&&'),  [Term(Tag('&&'), None, None, None)])

    def test_or(self):
        self.assertEqual(lex('|'),   [Term(Tag('|'), None, None, None)])
        self.assertEqual(lex('|='),  [Term(Tag('|='), None, None, None)])
        self.assertEqual(lex('||'),  [Term(Tag('||'), None, None, None)])
