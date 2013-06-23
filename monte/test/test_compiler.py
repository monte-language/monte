# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.
import textwrap

from twisted.trial import  unittest
from monte.compiler import ecompile, CompileError

class CompilerTest(unittest.TestCase):
    maxDiff = None
    def eq_(self, esrc, pysrc):
        self.assertMultiLineEqual(ecompile(textwrap.dedent(esrc).strip()),
                                  textwrap.dedent(pysrc).strip())

    def test_literal(self):
        self.assertEqual(ecompile("1"), "1")
        self.assertEqual(ecompile('"foo"'), "u'foo'")
        self.assertEqual(ecompile("'x'"), "_monte.Character('x')")
        self.assertEqual(ecompile("100_312"), "100312")
        self.assertEqual(ecompile('"\\u0061"'), "u'a'")

    # def test_noun(self):
    #     self.assertEqual(ecompile("foo"), "foo")
    #     self.assertEqual(ecompile('::"if"'), "_m_if")
    #     self.assertEqual(ecompile('_m_if'), "_m__m_if")
    #     self.assertEqual(ecompile('::"hello world!"'), "_m_hello_world_")

    def test_call(self):
        self.eq_("def x := 1; x.baz(2)",
                 """
                 x = 1
                 x.baz(2)
                 """)

    def test_def(self):
        self.eq_("def x := 1",
        """
        x = 1
        x
        """)

    def test_var(self):
        self.eq_("var x := 1",
        """
        x = _monte.VarSlot(None)
        _g_x1 = 1
        x.put(_g_x1)
        _g_x1
        """)
    def test_varNoun(self):
        self.eq_("var x := 1; x",
        """
        x = _monte.VarSlot(None)
        _g_x1 = 1
        x.put(_g_x1)
        x.get()
        """)

    def test_guardedVar(self):
        self.eq_("var x :(1..!10) := 1",
        """
        _g_guard1 = _monte.__makeOrderedSpace.op__till(1, 10)
        x = _monte.VarSlot(_g_guard1)
        _g_x2 = 1
        x.put(_g_x2)
        _g_x2
        """)

    def test_assign(self):
        self.eq_(
            "var x := 1; x := 2",
            """
            x = _monte.VarSlot(None)
            _g_x1 = 1
            x.put(_g_x1)
            _g_x2 = 2
            x.put(_g_x2)
            _g_x2
            """)
        self.assertRaises(CompileError, ecompile, "def x := 1; x := 2")
        self.assertRaises(CompileError, ecompile, "x := 2")

    def test_guardpattern(self):
        self.eq_("def x :float64 := 1",
                 """
                 _g_guard1 = _monte.float64
                 x = _g_guard1.coerce(1, _monte.throw)
                 x
                 """)

    def test_listpattern(self):
        self.eq_('def [x :float64, y :String, z] := "foo"',
                 """
                 _g_total_list1 = u'foo'
                 try:
                     _g_list2, _g_list3, _g_list4 = _g_total_list1
                 except ValueError, _g_e5:
                     _monte.throw(_g_e5)
                 _g_guard6 = _monte.float64
                 x = _g_guard6.coerce(_g_list2, _monte.throw)
                 _g_guard7 = _monte.String
                 y = _g_guard7.coerce(_g_list3, _monte.throw)
                 z = _g_list4
                 _g_total_list1
                 """)

        self.eq_('def ej := 1; def [x :float64, y :String, z] exit ej := "foo"',
                 """
                 ej = 1
                 _g_total_list1 = u'foo'
                 try:
                     _g_list2, _g_list3, _g_list4 = _g_total_list1
                 except ValueError, _g_e5:
                     ej(_g_e5)
                 _g_guard6 = _monte.float64
                 x = _g_guard6.coerce(_g_list2, ej)
                 _g_guard7 = _monte.String
                 y = _g_guard7.coerce(_g_list3, ej)
                 z = _g_list4
                 _g_total_list1
                 """)
        # self.eq_("def [x, y, z] + blee := foo.baz(a)",
        #          """
        #          _g_total_list1 = foo.baz(a)
        #          try:
        #              _g_list2, _g_list3, _g_list4 = _g_total_list1
        #          except ValueError, _g_e5:
        #              ej(_g_e5)
        #          x = _monte.float64.coerce(_g_list2, _monte.throw)
        #          y = _monte.String.coerce(_g_list3, _monte.throw)
        #          z = _g_list4
        #          _g_total_list1
        #          """)

    def test_trivialObject(self):
        self.eq_(
            'def foo { method baz(x, y) { x }}',
             """
             class _m_foo_Script(_monte.MonteObject):
                 def baz(foo, x, y):
                     return x

             foo = _m_foo_Script()
             foo
             """)

    def test_trivialNestedObject(self):
        self.eq_(
            '''
            def foo {
                method baz(x, y) {
                    def boz {
                        method blee() { 1 }
                    }
                }
            }''',
             """
             class _m_boz_Script(_monte.MonteObject):
                 def blee(boz):
                     return 1

             class _m_foo_Script(_monte.MonteObject):
                 def baz(foo, x, y):
                     boz = _m_boz_Script()
                     return boz

             foo = _m_foo_Script()
             foo
             """)

    def test_frameFinal(self):
        self.eq_(
            '''
            def foo {
                method baz(x :int, y) {
                    def a := 2
                    def b :(float64 >= 0) := 3.0
                    def boz {
                        method blee() { b.foo(a + x) }
                    }
                }
            }''',
             """
             class _m_boz_Script(_monte.MonteObject):
                 def __init__(boz, a_slot, b_slot, x_slot):
                     _monte.MonteObject.install(boz, 'a', a_slot)
                     _monte.MonteObject.install(boz, 'b', b_slot)
                     _monte.MonteObject.install(boz, 'x', x_slot)

                 def blee(boz):
                     return boz.b.foo(boz.a.add(boz.x))

             class _m_foo_Script(_monte.MonteObject):
                 def baz(foo, _g_Final1, y):
                     _g_guard2 = _monte.int
                     x = _g_guard2.coerce(_g_Final1, _monte.throw)
                     a = 2
                     _g_guard3 = _monte.__comparer.geq(_monte.float64, 0)
                     b = _g_guard3.coerce(3.0, _monte.throw)
                     boz = _m_boz_Script(_monte.FinalSlot(a, None), _monte.FinalSlot(b, _g_guard3), _monte.FinalSlot(x, _g_guard2))
                     return boz

             foo = _m_foo_Script()
             foo
             """)

    def test_sharedVar(self):
        self.eq_(
            '''
            def foo {
                method baz(x :int, y) {
                    var a := 1
                    var b :int := 0
                    def left {
                        method inc() { a += 1; b }
                    }
                    def right {
                        method dec() { b -= 1; a }
                    }
                    [left, right]
                }
            }''',
             """
             class _m_left_Script(_monte.MonteObject):
                 def __init__(left, a_slot, b_slot):
                     _monte.MonteObject.install(left, 'a', a_slot)
                     _monte.MonteObject.install(left, 'b', b_slot)

                 def inc(left):
                     _g_a6 = left.a.add(1)
                     left.a = _g_a6
                     return left.b

             class _m_right_Script(_monte.MonteObject):
                 def __init__(right, a_slot, b_slot):
                     _monte.MonteObject.install(right, 'a', a_slot)
                     _monte.MonteObject.install(right, 'b', b_slot)

                 def dec(right):
                     _g_b7 = right.b.subtract(1)
                     right.b = _g_b7
                     return right.a

             class _m_foo_Script(_monte.MonteObject):
                 def baz(foo, _g_Final1, y):
                     _g_guard2 = _monte.int
                     x = _g_guard2.coerce(_g_Final1, _monte.throw)
                     a = _monte.VarSlot(None)
                     _g_a3 = 1
                     a.put(_g_a3)
                     _g_guard4 = _monte.int
                     b = _monte.VarSlot(_g_guard4)
                     _g_b5 = 0
                     b.put(_g_b5)
                     left = _m_left_Script(a, b)
                     right = _m_right_Script(a, b)
                     return _monte.__makeList(left, right)

             foo = _m_foo_Script()
             foo
             """)

    def test_function(self):
        self.eq_(
            '''
            def foo(x) {
                return 1
            }
            ''',
            """
            class _m_foo_Script(_monte.MonteObject):
                def run(foo, x):
                    __return = _monte.ejector("__return")
                    try:
                        __return(1)
                        _g_escape2 = None
                    except __return._m_type, _g___return1:
                        _g_escape2 = _g___return1
                    return _g_escape2

            foo = _m_foo_Script()
            foo
            """
            # """
            # class _m_foo_Script(_monte.MonteObject):
            #     def run(self, x):
            #         return 1
            # """
        )

    def test_unusedEscape(self):
        self.eq_(
            '''
            var x := 1
            escape e {
                x := 2
            } catch e {
                x := 3
            }
            ''',
            """
            x = _monte.VarSlot(None)
            _g_x1 = 1
            x.put(_g_x1)
            _g_x2 = 2
            x.put(_g_x2)
            _g_x2
            """)
