from monte.test import unittest
from monte.lexer import MonteLexer, StringFeeder, ParseError
from terml.nodes import Tag, Term

def lex(s):
    toks = list(MonteLexer(StringFeeder(s, '<test data>')))
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
        self.assertEqual(lex('-> {'),  [Term(Tag('->'), None, None, None),
                                        Term(Tag('{'), None, None, None)])

    def test_colon(self):
        self.assertEqual(lex(':x'),   [Term(Tag(':'), None, None, None),
                                       Term(Tag('IDENTIFIER'), 'x', None, None)])
        self.assertEqual(lex(':='),  [Term(Tag(':='), None, None, None)])
        self.assertEqual(lex('::'),  [Term(Tag('::'), None, None, None)])

    def test_crunch(self):
        self.assertEqual(lex('<'),   [Term(Tag('<'), None, None, None)])
        self.assertEqual(lex('<-'),  [Term(Tag('<-'), None, None, None)])
        self.assertEqual(lex('<='),  [Term(Tag('<='), None, None, None)])
        self.assertEqual(lex('<<='), [Term(Tag('<<='), None, None, None)])
        self.assertEqual(lex('<=>'), [Term(Tag('<=>'), None, None, None)])

    def test_zap(self):
        self.assertEqual(lex('1 >'),   [Term(Tag('.int.'), 1, None, None),
                                        Term(Tag('>'), None, None, None)])
        self.assertEqual(lex('1 >='),  [Term(Tag('.int.'), 1, None, None),
                                        Term(Tag('>='), None, None, None)])
        self.assertEqual(lex('1 >>='), [Term(Tag('.int.'), 1, None, None),
                                        Term(Tag('>>='), None, None, None)])

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
                         [Term(Tag('DOC_COMMENT'), ' hello ', None, None)])

    def test_comment(self):
        self.assertEqual(lex('# yes\n1'), [Term(Tag('#'), ' yes', None, None),
                                           Term(Tag('EOL'), None, None, None),
                                           Term(Tag('.int.'), 1, None, None)])

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


SIMPLE_INDENT = """
foo:
  baz
"""

ARROW_INDENT = """
foo ->
  baz
"""

SIMPLE_DEDENT = """
foo:
  baz
blee
"""
VERTICAL_SPACE = """
foo:

  baz


blee
"""

HORIZ_SPACE = """
foo:    
  baz
blee
"""

MULTI_INDENT = """
foo:
  baz:
     biz
blee
"""

UNBALANCED = """
foo:
  baz:
     biz
 blee
"""

UNBALANCED2 = """
foo:
  baz
   blee
"""

PARENS = """
(foo,
 baz:
  blee
 )
"""

#TODO decide whether to follow python's "no indent tokens inside
#parens" strategy or have ways to jump in/out of indentation-awareness
CONTINUATION = """
foo (
  baz
    biz
 )
blee
"""
class IndentLexerTests(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(lex(SIMPLE_INDENT),
                         [Term(Tag('EOL'), None, None, None),
                          Term(Tag('IDENTIFIER'), "foo", None, None),
                          Term(Tag(':'), None, None, None),
                          Term(Tag('EOL'), None, None, None),
                          Term(Tag('INDENT'), None, None, None),
                          Term(Tag('IDENTIFIER'), "baz", None, None),
                          Term(Tag('EOL'), None, None, None),
                          Term(Tag('EOL'), None, None, None),
                          Term(Tag('DEDENT'), None, None, None)])

    def test_arrow(self):
        self.assertEqual(lex(ARROW_INDENT),
                         [Term(Tag('EOL'), None, None, None),
                          Term(Tag('IDENTIFIER'), "foo", None, None),
                          Term(Tag('->'), None, None, None),
                          Term(Tag('EOL'), None, None, None),
                          Term(Tag('INDENT'), None, None, None),
                          Term(Tag('IDENTIFIER'), "baz", None, None),
                          Term(Tag('EOL'), None, None, None),
                          Term(Tag('EOL'), None, None, None),
                          Term(Tag('DEDENT'), None, None, None)])

    def test_dedent(self):
        self.assertEqual(lex(SIMPLE_DEDENT),
                         [Term(Tag('EOL'), None, None, None),
                          Term(Tag('IDENTIFIER'), "foo", None, None),
                          Term(Tag(':'), None, None, None),
                          Term(Tag('EOL'), None, None, None),
                          Term(Tag('INDENT'), None, None, None),
                          Term(Tag('IDENTIFIER'), "baz", None, None),
                          Term(Tag('EOL'), None, None, None),
                          Term(Tag('DEDENT'), None, None, None),
                          Term(Tag('IDENTIFIER'), "blee", None, None),
                          Term(Tag('EOL'), None, None, None)])

    def test_vertical(self):
        self.assertEqual(lex(VERTICAL_SPACE),
                         [Term(Tag('EOL'), None, None, None),
                          Term(Tag('IDENTIFIER'), "foo", None, None),
                          Term(Tag(':'), None, None, None),
                          Term(Tag('EOL'), None, None, None),
                          Term(Tag('EOL'), None, None, None),
                          Term(Tag('INDENT'), None, None, None),
                          Term(Tag('IDENTIFIER'), "baz", None, None),
                          Term(Tag('EOL'), None, None, None),
                          Term(Tag('EOL'), None, None, None),
                          Term(Tag('EOL'), None, None, None),
                          Term(Tag('DEDENT'), None, None, None),
                          Term(Tag('IDENTIFIER'), "blee", None, None),
                          Term(Tag('EOL'), None, None, None)])

    def test_horizontal(self):
        self.assertEqual(lex(SIMPLE_DEDENT), lex(HORIZ_SPACE))

    def test_multi(self):
        self.assertEqual(lex(MULTI_INDENT),
                         [Term(Tag('EOL'), None, None, None),
                          Term(Tag('IDENTIFIER'), "foo", None, None),
                          Term(Tag(':'), None, None, None),
                          Term(Tag('EOL'), None, None, None),
                          Term(Tag('INDENT'), None, None, None),
                          Term(Tag('IDENTIFIER'), "baz", None, None),
                          Term(Tag(':'), None, None, None),
                          Term(Tag('EOL'), None, None, None),
                          Term(Tag('INDENT'), None, None, None),
                          Term(Tag('IDENTIFIER'), "biz", None, None),
                          Term(Tag('EOL'), None, None, None),
                          Term(Tag('DEDENT'), None, None, None),
                          Term(Tag('DEDENT'), None, None, None),
                          Term(Tag('IDENTIFIER'), "blee", None, None),
                          Term(Tag('EOL'), None, None, None),])

    def test_unbalanced(self):
        e = self.assertRaises(ParseError, lex, UNBALANCED)
        self.assertIn("unindent does not match any outer indentation level",
                      str(e))

    def test_unbalanced2(self):
        e = self.assertRaises(ParseError, lex, UNBALANCED2)
        self.assertIn("Unexpected indent", str(e))

    def test_wacky_parens(self):
        e = self.assertRaises(ParseError, lex, PARENS)
        self.assertIn("Indented blocks only allowed in statement positions",
                      str(e))

    def test_continuation(self):
        self.assertEqual(lex(CONTINUATION),
                         [Term(Tag('EOL'), None, None, None),
                          Term(Tag('IDENTIFIER'), "foo", None, None),
                          Term(Tag('('), None, None, None),
                          Term(Tag('EOL'), None, None, None),
                          Term(Tag('IDENTIFIER'), "baz", None, None),
                          Term(Tag('EOL'), None, None, None),
                          Term(Tag('IDENTIFIER'), "biz", None, None),
                          Term(Tag('EOL'), None, None, None),
                          Term(Tag(')'), None, None, None),
                          Term(Tag('EOL'), None, None, None),
                          Term(Tag('IDENTIFIER'), "blee", None, None),
                          Term(Tag('EOL'), None, None, None)])
