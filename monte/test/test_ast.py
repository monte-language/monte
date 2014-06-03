from terml.nodes import termMaker as t
from monte.test import unittest
from monte import ast

class ASCIIShiftTests(unittest.TestCase):
    def test_encode(self):
        bs = [0, 17, 64, 250, 224, 239]
        encoded = ast.asciiShift(''.join(chr(b) for b in bs))
        self.assertEqual(encoded, ' 1`\x1a\x00\x0f')

    def test_decode(self):
        decoded = ast.asciiUnshift(' 1`\x1a\x00\x0f')
        self.assertEqual([ord(b) for b in decoded],
                         [0, 17, 64, 250, 224, 239])



class CodecTests(unittest.TestCase):
    def check(self, term):
        self.assertEqual(ast.load(ast.dump(term)), term)

    def test_null(self):
        self.check(t.null())

    def test_int(self):
        self.check(t.LiteralExpr(0))
        self.check(t.LiteralExpr(-255))
        self.check(t.LiteralExpr(1048369))

    def test_bigint(self):
        self.check(t.LiteralExpr(0x100000001))
        self.check(t.LiteralExpr(443464870465066586048))
        self.check(t.LiteralExpr(-443464870465066586048))

    def test_float(self):
        self.check(t.LiteralExpr(0.0))
        self.check(t.LiteralExpr(-1.0))
        self.check(t.LiteralExpr(3.14))

    def test_string(self):
        self.check(t.LiteralExpr(u''))
        self.check(t.LiteralExpr(u'yes'))
        self.check(t.LiteralExpr(u'\N{SNOWMAN}'))

    def test_compound(self):
        self.check(t.If(t.LiteralExpr(u"a"), t.LiteralExpr(1), t.null()))

    def test_seq(self):
        self.check(t.SeqExpr([t.LiteralExpr(1), t.NounExpr("true"),
                              t.NounExpr("false")]))

    def test_call(self):
        self.check(t.MethodCallExpr(t.NounExpr("__makeList"), "run",
                                    [t.NounExpr("null"), t.NounExpr("true")]))

    def test_object(self):
        term = t.SeqExpr([
            t.Object(t.null(),
                     t.FinalPattern(t.NounExpr("foo"), t.null()),
                     [t.null()],
                     t.Script(t.null(),
                              [
                                  t.Method(t.null(), "baz",
                                           [t.FinalPattern(t.NounExpr("x"), t.null()),
                                            t.FinalPattern(t.NounExpr("y"), t.null())],
                                           t.null(),
                                           t.NounExpr("x"))],
                              [t.Matcher(t.ListPattern([
                                  t.FinalPattern(t.NounExpr("verb1"), t.null()),
                                  t.FinalPattern(t.NounExpr("args1"), t.null())],
                                                       t.null()),
                                         t.NounExpr("verb1")),
                               t.Matcher(t.FinalPattern(t.NounExpr("etc"), t.null()),
                                         t.NounExpr("etc"))]))])
        self.check(term)

    def test_module(self):
        self.check(t.Module("unittest", "foo", "bar"))
