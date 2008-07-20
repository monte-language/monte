from twisted.trial import unittest
from compiler import parse as python_parse
from pymeta.runtime import IterBuffer
from pymeta.builder import AstBuilder

class IterBufferTest(unittest.TestCase):

    def test_next(self):
        """
        IterBuffers are iterable and yield their contents.
        """
        d = "test data"
        i = IterBuffer(d)
        self.assertEqual(''.join(i), d)


    def test_rewind(self):
        """
        Rewinding an IterBuffer should reset it to a previous marked position
        in the iterator.
        """
        d = "test data"
        i1 = IterBuffer(d)
        i2 = IterBuffer(d)
        for _ in range(3):
            i1.next()
            i2.next()
        m = i1.mark()
        for _ in range(3):
            i1.next()
        i1.rewind(m)
        self.assertEqual(list(i1), list(i2))


    def test_rewindPush(self):
        """
        Rewinding an IterBuffer should reset it to a previous marked position
        in the iterator, even if args have been pushed to it.
        """
        d = "test data"
        i1 = IterBuffer(d)
        i2 = IterBuffer(d)
        for _ in range(3):
            i1.next()
            i2.next()
        m = i1.mark()
        for _ in range(3):
            i1.next()
        i1.push(7)
        i1.next()
        i1.rewind(m)
        self.assertEqual(list(i1), list(i2))



class AstBuilderTest(unittest.TestCase):
    """
    Tests for creating Python functions and classes.
    """

    def test_method(self):
        """
        C{compileAstMethod} creates a function with a single 'self' arg that
        returns the value of the given expression.
        """
        expr = python_parse("self.data[1] + 3", mode="eval").asList()[0]
        ab = AstBuilder("<test>", None)
        f = ab._compileAstMethod("rule_f", expr)
        class Foo:
            locals = {}
            data = [0, 2]
        self.assertEqual(f(Foo), 5)
