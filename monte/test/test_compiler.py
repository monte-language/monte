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
        _g_guard1 = _monte._m___makeOrderedSpace.op__till(1, 10)
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

    def test_trivialVarObject(self):
        self.eq_(
            'def var foo { method baz(x, y) { x }}',
             """
             class _m_foo_Script(_monte.MonteObject):
                 def __init__(_g_foo1, foo_slot):
                     _monte.MonteObject.install(_g_foo1, 'foo', foo_slot)

                 def baz(_g_foo1, x, y):
                     return x

             foo = _monte.VarSlot(None)
             _g_foo1 = _m_foo_Script(foo)
             foo.put(_g_foo1)
             _g_foo1
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
                     _g_guard3 = _monte._m___comparer.geq(_monte.float64, 0)
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
                     return _monte._m___makeList(left, right)

             foo = _m_foo_Script()
             foo
             """)

    def test_implements(self):
        self.eq_(
            '''
            def foo implements DeepFrozen, Data {}
            ''',
            """
            class _m_foo_Script(_monte.MonteObject):
                def __init__(foo, _m_auditors):
                    foo._m_audit(_m_auditors)

                _m_objectExpr = "eJzzT8pKTS7RyCvNydFRcMvMS8wJSCwpSS3K0/DLL81zrSgo0lBKy89X0tRRAKkBUsHJRZkFMB0QMhqh1iU1tcCtKL8qNQ+kBUk8sSRRSTMWqBaMNTUB+zEoKA=="

            foo = _m_foo_Script([_monte.DeepFrozen, _monte.Data])
            foo
            """)

    def test_simpleAs(self):
        self.eq_(
            '''
            def foo as Data implements DeepFrozen {}
            ''',
            """
            class _m_foo_Script(_monte.MonteObject):
                def __init__(foo, _m_auditors):
                    foo._m_audit(_m_auditors)

                _m_objectExpr = "eJzzT8pKTS7RyCvNydFRcMvMS8wJSCwpSS3K0/DLL81zrSgo0lBKy89X0tRRAKkBUsHJRZkFMB0IRS6JJYkgVdFIQqmpBW5F+VWpeUqasUAZMNbUBAD7syYh"

            _g_guard1 = _monte.Data
            foo = _g_guard1.coerce(_m_foo_Script([_monte.Data, _monte.DeepFrozen]), _monte.throw)
            foo
            """)

    def test_varAs(self):
        self.eq_(
            '''
            def var foo as Data implements DeepFrozen {}
            ''',
            """
            class _m_foo_Script(_monte.MonteObject):
                def __init__(_g_foo2, _m_auditors, foo_slot):
                    _g_foo2._m_audit(_m_auditors)
                    _monte.MonteObject.install(_g_foo2, 'foo', foo_slot)

                _m_objectExpr = "eJzzT8pKTS7RyCvNydFRCEssCkgsKUktytPwyy/Nc60oKNJQSsvPV9LUUQCpAFLByUWZBTD1CEUuiSWJIFXRSEKpqQVuRflVqXlKmrFAGTDW1AQApkAlYA=="

            _g_guard1 = _monte.Data
            foo = _monte.VarSlot(_g_guard1)
            _g_foo2 = _m_foo_Script([_monte.Data, _monte.DeepFrozen], foo)
            foo.put(_g_foo2)
            _g_foo2
            """)

    def test_methGuard(self):
        self.eq_(
            'def foo { method baz(x, y) :int { x }}',
             """
             class _m_foo_Script(_monte.MonteObject):
                 def __init__(foo, _m_methodGuards):
                     foo._m_guardMethods(_m_methodGuards)

                 def baz(foo, x, y):
                     return foo._m_guardForMethod('baz').coerce(x, _monte.throw)

             foo = _m_foo_Script({'baz': _monte.int})
             foo
             """)

    def test_matcher(self):
        self.eq_(
            'def foo { method baz(x, y) { x } match [verb1, args1] { verb1 } match etc { etc }}',
             """
             class _m_foo_Script(_monte.MonteObject):
                 _m_matcherNames = ['_g_matcher1', '_g_matcher2']
                 def baz(foo, x, y):
                     return x

                 def _g_matcher1(foo, _m_message):
                     _g_total_list3 = _m_message
                     try:
                         _g_list4, _g_list5 = _g_total_list3
                     except ValueError, _g_e6:
                         _monte.throw(_g_e6)
                     verb1 = _g_list4
                     args1 = _g_list5
                     return verb1

                 def _g_matcher2(foo, _m_message):
                     etc = _m_message
                     return etc

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
                    _m___return = _monte.ejector("__return")
                    try:
                        _m___return(1)
                        _g_escape2 = None
                    except _m___return._m_type, _g___return1:
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

    def test_metacontext(self):
        self.eq_(
            '''
            def foo {
                method baz(x, y) {
                    def a := 2
                    var b := 3
                    def boz {
                        method blee() { b := a; meta.context() }
                    }
                }
            }''',
             """
             class _m_boz_Script(_monte.MonteObject):
                 def __init__(boz, a_slot, b_slot):
                     _monte.MonteObject.install(boz, 'a', a_slot)
                     _monte.MonteObject.install(boz, 'b', b_slot)

                 def blee(boz):
                     _g_b2 = boz.a
                     boz.b = _g_b2
                     return _monte.StaticContext('__main$foo$boz', ['b', 'a'], _m_boz_Script._m_objectExpr)

                 _m_objectExpr = "eJzzT8pKTS7RyCvNydFRcMvMS8wJSCwpSS3K0/DLL81zrSgo0lBKyq9S0tRRAKkBUsHJRZkFMB0QMjoWiH1TSzLyU6DiSkk5qalKEBmISHBqIdi0aMfi4sx0FONBhiO4iUqaQD7QtEQNJef8vJLUihIlzVhNTZAdQAoAuNc5Rg=="

             class _m_foo_Script(_monte.MonteObject):
                 def baz(foo, x, y):
                     a = 2
                     b = _monte.VarSlot(None)
                     _g_b1 = 3
                     b.put(_g_b1)
                     boz = _m_boz_Script(_monte.FinalSlot(a, None), b)
                     return boz

             foo = _m_foo_Script()
             foo
             """)

    def test_metastate_empty(self):
        self.eq_(
            '''
            def _() :any { def x := 1; return meta.getState() }()
            ''',
            """
            class _m__g_ignore1_Script(_monte.MonteObject):
                def __init__(_g_ignore2, _m_methodGuards):
                    _g_ignore2._m_guardMethods(_m_methodGuards)

                def run(_g_ignore2):
                    _m___return = _monte.ejector("__return")
                    try:
                        x = 1
                        _m___return(_monte.Map(()))
                        _g_escape4 = None
                    except _m___return._m_type, _g___return3:
                        _g_escape4 = _g___return3
                    return _g_ignore2._m_guardForMethod('run').coerce(_g_escape4, _monte.throw)

            _g_ignore2 = _m__g_ignore1_Script({'run': _monte.any})
            _g_ignore2()
            """)

    def test_metastate(self):
        self.eq_(
            '''
            def foo() {
                def a := 1;
                var b := 2;
                var c := 3;
                return def boz {
                    method biz() {
                        def x := 17
                        meta.getState()
                    }
                    method baz() {
                        b += a
                    }
                }
            }
            ''',
            """
            class _m_boz_Script(_monte.MonteObject):
                def __init__(boz, a_slot, b_slot):
                    _monte.MonteObject.install(boz, 'a', a_slot)
                    _monte.MonteObject.install(boz, 'b', b_slot)

                def biz(boz):
                    x = 17
                    return _monte.Map((('&b', _monte.getSlot(boz, 'b')), ('&a', _monte.getSlot(boz, 'a'))))

                def baz(boz):
                    _g_b5 = boz.b.add(boz.a)
                    boz.b = _g_b5
                    return _g_b5

            class _m_foo_Script(_monte.MonteObject):
                def run(foo):
                    _m___return = _monte.ejector("__return")
                    try:
                        a = 1
                        b = _monte.VarSlot(None)
                        _g_b3 = 2
                        b.put(_g_b3)
                        c = _monte.VarSlot(None)
                        _g_c4 = 3
                        c.put(_g_c4)
                        boz = _m_boz_Script(_monte.FinalSlot(a, None), b)
                        _m___return(boz)
                        _g_escape2 = None
                    except _m___return._m_type, _g___return1:
                        _g_escape2 = _g___return1
                    return _g_escape2

            foo = _m_foo_Script()
            foo
            """)

    def test_finally(self):
        self.eq_(
            '''
            try { 1 } finally { 2 }
            ''',
            """
            try:
                _g_finally1 = 1
            finally:
                _g_finally1 = 2
            _g_finally1
            """)

    def test_catch(self):
        self.eq_(
            '''
            try { 1 } catch p { 2 }
            ''',
            """
            try:
                _g_catch1 = 1
            except Exception, _g_exception2:
                p = _g_exception2
                _g_catch1 = 2
            _g_catch1
            """)

    def test_hide(self):
        self.eq_(
            '''
            def x := 1; {def x := 2}
            ''',
            """
            x = 1
            _g_x1 = 2
            _g_x1
            """)

    def test_if(self):
        self.eq_(
            '''
            if (1) { 2 } else { 3 }
            ''',
            """
            if 1:
                _g_if1 = 2
            else:
                _g_if1 = 3
            _g_if1
            """)

    # def test_via(self):
    #     self.eq_(
    #         '''
    #         def a := 3
    #         def b := 4
    #         def x via (a) exit b := 1
    #         ''',
    #         """
    #         a = 3
    #         b = 4
    #         _g_via1 = 1
    #         x = a(_g_via1, b)
    #         _g_via1
    #         """)

    # def test_bindingexpr(self):
    #     self.eq_(
    #         '''
    #         var x := 1
    #         &&x
    #         ''',
    #         """
    #         x = _monte.VarSlot(None)
    #         _g_x1 = 1
    #         x.put(_g_x1)
    #         _monte.reifyBinding(x)
    #         """)

    # def test_bindingpatt(self):
    #     self.eq_(
    #         '''
    #         def &&x := 1
    #         ''',
    #         """
    #         _g_binding1 = 1
    #         x = _monte.slotFromBinding(_g_binding1)
    #         _g_binding1
    #         """)
