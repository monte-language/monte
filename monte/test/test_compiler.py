# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.
import textwrap

from twisted.trial import unittest
from ometa.runtime import ParseError
from monte.compiler import ecompile

class CompilerTest(unittest.TestCase):
    def test_literal(self):
        self.assertEqual(ecompile("1"), "1")
        self.assertEqual(ecompile('"foo"'), "u'foo'")
        self.assertEqual(ecompile("'x'"), "_monte.Character('x')")
        self.assertEqual(ecompile("100_312"), "100312")
        self.assertEqual(ecompile('"\\u0061"'), "u'a'")

    def test_noun(self):
        self.assertEqual(ecompile("foo"), "foo")
        self.assertEqual(ecompile('::"if"'), "_m_if")
        self.assertEqual(ecompile('_m_if'), "_m__m_if")
        self.assertEqual(ecompile('::"hello world!"'), "_m_hello_world_")

    def test_trivialObject(self):
        self.assertEqual(
            ecompile('def foo { method baz(x, y) { x }}'),
            textwrap.dedent("""
             class _m_foo_Script(_monte.MonteObject):
                 def baz(self, x, y):
                     return x
             foo = _m_foo_Script()""").strip())
