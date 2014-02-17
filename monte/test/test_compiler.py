# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.
import textwrap

from twisted.trial import  unittest
from monte.compiler import ecompile, CompileError, mangleIdent, safeScopeNames

fakeScope = dict.fromkeys(safeScopeNames)

class CompilerTest(unittest.TestCase):
    maxDiff = None
    def eq_(self, esrc, pysrc):
        self.assertMultiLineEqual(ecompile(textwrap.dedent(esrc).strip(), fakeScope),
                                  textwrap.dedent(pysrc).strip())

    def test_mangle(self):
        self.assertEqual(mangleIdent("foo"), "foo")
        self.assertEqual(mangleIdent("while"), "_m_while")
        self.assertEqual(mangleIdent("_g_x"), "_m__g_x")
        self.assertEqual(mangleIdent("_m_x"), "_m__m_x")
        self.assertEqual(mangleIdent("__foo"), "_m___foo")
        self.assertEqual(mangleIdent("x1"), "x1")
        self.assertEqual(mangleIdent("__x1"), "_m___x49")
        self.assertEqual(mangleIdent("jim bob"), "_m_jim32bob")
        self.assertEqual(mangleIdent("9lives"), "_m_57lives")
        self.assertEqual(mangleIdent("jim!bob"), "_m_jim33bob")

    def test_literal(self):
        self.assertEqual(ecompile("1", {}), "_monte.wrap(1)")
        self.assertEqual(ecompile('"foo"', {}), "_monte.wrap(u'foo')")
        self.assertEqual(ecompile("'x'", {}), "_monte.Character('x')")
        self.assertEqual(ecompile("100_312", {}), "_monte.wrap(100312)")
        self.assertEqual(ecompile('"\\u0061"', {}), "_monte.wrap(u'a')")

    def test_noun(self):
         self.assertEqual(ecompile("foo", {'foo': None}), '_m_outerScope["foo"]')
         self.assertEqual(ecompile('::"if"', {'if': None}),  '_m_outerScope["if"]')
         self.assertEqual(ecompile('::"hello world!"', {'hello world!': None}),
                          '_m_outerScope["hello world!"]')

    def test_call(self):
        self.eq_("def x := 1; x.baz(2)",
                 """
                 x = _monte.wrap(1)
                 x.baz(_monte.wrap(2))
                 """)

    def test_def(self):
        self.eq_("def x := 1",
        """
        x = _monte.wrap(1)
        x
        """)

    def test_var(self):
        self.eq_("var x := 1",
        """
        _g_x1 = _monte.wrap(1)
        x = _monte.VarSlot(None, _g_x1, _monte.throw)
        _g_x1
        """)
    def test_varNoun(self):
        self.eq_("var x := 1; x",
        """
        _g_x1 = _monte.wrap(1)
        x = _monte.VarSlot(None, _g_x1, _monte.throw)
        x.get()
        """)

    def test_guardedVar(self):
        self.eq_("var x :(1..!10) := 1",
        """
        _g_guard1 = _m_outerScope["__makeOrderedSpace"].op__till(_monte.wrap(1), _monte.wrap(10))
        _g_x2 = _monte.wrap(1)
        x = _monte.VarSlot(_g_guard1, _g_x2, _monte.throw)
        _g_x2
        """)

    def test_assign(self):
        self.eq_(
            "var x := 1; x := 2",
            """
            _g_x1 = _monte.wrap(1)
            x = _monte.VarSlot(None, _g_x1, _monte.throw)
            _g_x2 = _monte.wrap(2)
            x.put(_g_x2)
            _g_x2
            """)
        self.assertRaises(CompileError, ecompile, "def x := 1; x := 2", {})
        self.assertRaises(CompileError, ecompile, "x := 2", {})

    def test_guardpattern(self):
        self.eq_("def x :float64 := 1",
                 """
                 _g_guard1 = _m_outerScope["float64"]
                 x = _g_guard1.coerce(_monte.wrap(1), _monte.throw)
                 x
                 """)

    def test_listpattern(self):
        self.eq_('def [x] := "a"',
                 """
                 _g_total_list1 = _monte.wrap(u'a')
                 try:
                     _g_list2, = _g_total_list1
                 except ValueError, _g_e3:
                     _monte.throw(_g_e3)
                     raise RuntimeError("Ejector did not exit")
                 x = _g_list2
                 _g_total_list1
                 """)

        self.eq_('def [x :float64, y :String, z] := "foo"',
                 """
                 _g_total_list1 = _monte.wrap(u'foo')
                 try:
                     _g_list2, _g_list3, _g_list4, = _g_total_list1
                 except ValueError, _g_e5:
                     _monte.throw(_g_e5)
                     raise RuntimeError("Ejector did not exit")
                 _g_guard6 = _m_outerScope["float64"]
                 x = _g_guard6.coerce(_g_list2, _monte.throw)
                 _g_guard7 = _m_outerScope["String"]
                 y = _g_guard7.coerce(_g_list3, _monte.throw)
                 z = _g_list4
                 _g_total_list1
                 """)

        self.eq_('def ej := 1; def [x :float64, y :String, z] exit ej := "foo"',
                 """
                 ej = _monte.wrap(1)
                 _g_total_list1 = _monte.wrap(u'foo')
                 try:
                     _g_list2, _g_list3, _g_list4, = _g_total_list1
                 except ValueError, _g_e5:
                     ej(_g_e5)
                     raise RuntimeError("Ejector did not exit")
                 _g_guard6 = _m_outerScope["float64"]
                 x = _g_guard6.coerce(_g_list2, ej)
                 _g_guard7 = _m_outerScope["String"]
                 y = _g_guard7.coerce(_g_list3, ej)
                 z = _g_list4
                 _g_total_list1
                 """)

    def test_trivialObject(self):
        self.eq_(
            'object foo { method baz(x, y) { x }}',
             """
             class _m_foo_Script(_monte.MonteObject):
                 _m_fqn = '__main$foo'
                 def baz(foo, x, y):
                     return x

             foo = _m_foo_Script()
             foo
             """)

    def test_trivialVarObject(self):
        self.eq_(
            'object var foo { method baz(x, y) { x }}',
             """
             class _m_foo_Script(_monte.MonteObject):
                 _m_fqn = '__main$foo'
                 def __init__(_g_foo1, foo_slot):
                     _monte.MonteObject._m_install(_g_foo1, 'foo', foo_slot)

                 def baz(_g_foo1, x, y):
                     return x

             foo = _monte.VarSlot(None)
             _g_foo1 = _m_foo_Script(foo)
             foo._m_init(_g_foo1, _monte.throw)
             _g_foo1
             """)

    def test_trivialNestedObject(self):
        self.eq_(
            '''
            object foo {
                method baz(x, y) {
                    object boz {
                        method blee() { 1 }
                    }
                }
            }''',
             """
             class _m_boz_Script(_monte.MonteObject):
                 _m_fqn = '__main$foo$boz'
                 def blee(boz):
                     return _monte.wrap(1)

             class _m_foo_Script(_monte.MonteObject):
                 _m_fqn = '__main$foo'
                 def baz(foo, x, y):
                     boz = _m_boz_Script()
                     return boz

             foo = _m_foo_Script()
             foo
             """)

    def test_tripleNest(self):
        self.eq_(
            '''
            object outer:
                method run(f):
                    object o:
                        method inner(x):
                            object q:
                                method do():
                                    f
                            q.do()
            outer(0).inner(1)
            ''',
            """
            class _m_q_Script(_monte.MonteObject):
                _m_fqn = '__main$outer$o$q'
                def __init__(q, f_slot):
                    _monte.MonteObject._m_install(q, 'f', f_slot)

                def do(q):
                    return q.f

            class _m_o_Script(_monte.MonteObject):
                _m_fqn = '__main$outer$o'
                def __init__(o, f_slot):
                    _monte.MonteObject._m_install(o, 'f', f_slot)

                def inner(o, x):
                    q = _m_q_Script(_monte.FinalSlot(o.f, _monte.getGuard(o, "f")))
                    return q.do()

            class _m_outer_Script(_monte.MonteObject):
                _m_fqn = '__main$outer'
                def run(outer, f):
                    o = _m_o_Script(_monte.FinalSlot(f, None))
                    return o

            outer = _m_outer_Script()
            outer(_monte.wrap(0)).inner(_monte.wrap(1))
            """)

    def test_frameFinal(self):
        self.eq_(
            '''
            object foo {
                method baz(x :int, y) {
                    def a := 2
                    def b :(float64 >= 0) := 3.0
                    object boz {
                        method blee() { b.foo(a + x) }
                    }
                }
            }''',
             """
             class _m_boz_Script(_monte.MonteObject):
                 _m_fqn = '__main$foo$boz'
                 def __init__(boz, a_slot, b_slot, x_slot):
                     _monte.MonteObject._m_install(boz, 'a', a_slot)
                     _monte.MonteObject._m_install(boz, 'b', b_slot)
                     _monte.MonteObject._m_install(boz, 'x', x_slot)

                 def blee(boz):
                     return boz.b.foo(boz.a.add(boz.x))

             class _m_foo_Script(_monte.MonteObject):
                 _m_fqn = '__main$foo'
                 def baz(foo, _g_Final1, y):
                     _g_guard2 = _m_outerScope["int"]
                     x = _g_guard2.coerce(_g_Final1, _monte.throw)
                     a = _monte.wrap(2)
                     _g_guard3 = _m_outerScope["__comparer"].geq(_m_outerScope["float64"], _monte.wrap(0))
                     b = _g_guard3.coerce(_monte.wrap(3.0), _monte.throw)
                     boz = _m_boz_Script(_monte.FinalSlot(a, None), _monte.FinalSlot(b, _g_guard3), _monte.FinalSlot(x, _g_guard2))
                     return boz

             foo = _m_foo_Script()
             foo
             """)

    def test_sharedVar(self):
        self.eq_(
            '''
            object foo {
                method baz(x :int, y) {
                    var a := 1
                    var b :int := 0
                    object left {
                        method inc() { a += 1; b }
                    }
                    object right {
                        method dec() { b -= 1; a }
                    }
                    [left, right]
                }
            }''',
             """
             class _m_left_Script(_monte.MonteObject):
                 _m_fqn = '__main$foo$left'
                 def __init__(left, a_slot, b_slot):
                     _monte.MonteObject._m_install(left, 'a', a_slot)
                     _monte.MonteObject._m_install(left, 'b', b_slot)

                 def inc(left):
                     _g_a6 = left.a.add(_monte.wrap(1))
                     left.a = _g_a6
                     return left.b

             class _m_right_Script(_monte.MonteObject):
                 _m_fqn = '__main$foo$right'
                 def __init__(right, a_slot, b_slot):
                     _monte.MonteObject._m_install(right, 'a', a_slot)
                     _monte.MonteObject._m_install(right, 'b', b_slot)

                 def dec(right):
                     _g_b7 = right.b.subtract(_monte.wrap(1))
                     right.b = _g_b7
                     return right.a

             class _m_foo_Script(_monte.MonteObject):
                 _m_fqn = '__main$foo'
                 def baz(foo, _g_Final1, y):
                     _g_guard2 = _m_outerScope["int"]
                     x = _g_guard2.coerce(_g_Final1, _monte.throw)
                     _g_a3 = _monte.wrap(1)
                     a = _monte.VarSlot(None, _g_a3, _monte.throw)
                     _g_guard4 = _m_outerScope["int"]
                     _g_b5 = _monte.wrap(0)
                     b = _monte.VarSlot(_g_guard4, _g_b5, _monte.throw)
                     left = _m_left_Script(a, b)
                     right = _m_right_Script(a, b)
                     return _m_outerScope["__makeList"](left, right)

             foo = _m_foo_Script()
             foo
             """)

    def test_implements(self):
        self.eq_(
            '''
            object foo implements DeepFrozen, Data {}
            ''',
            """
            class _m_foo_Script(_monte.MonteObject):
                _m_fqn = '__main$foo'
                def __init__(foo, _m_auditors):
                    foo._m_audit(_m_auditors)

                _m_objectExpr = "eJzzT8pKTS7RyCvNydFRcMvMS8wJSCwpSS3K0/DLL81zrSgo0lBKy89X0tRRAKkBUsHJRZkFMB0QMhqh1iU1tcCtKL8qNQ+kBUk8sSRRSTMWqBaMNTUB+zEoKA=="

            foo = _m_foo_Script([_m_outerScope["DeepFrozen"], _m_outerScope["Data"]])
            foo
            """)

    def test_simpleAs(self):
        self.eq_(
            '''
            object foo as Data implements DeepFrozen {}
            ''',
            """
            class _m_foo_Script(_monte.MonteObject):
                _m_fqn = '__main$foo'
                def __init__(foo, _m_auditors):
                    foo._m_audit(_m_auditors)

                _m_objectExpr = "eJzzT8pKTS7RyCvNydFRcMvMS8wJSCwpSS3K0/DLL81zrSgo0lBKy89X0tRRAKkBUsHJRZkFMB0IRS6JJYkgVdFIQqmpBW5F+VWpeUqasUAZMNbUBAD7syYh"

            _g_guard1 = _m_outerScope["Data"]
            foo = _g_guard1.coerce(_m_foo_Script([_m_outerScope["Data"], _m_outerScope["DeepFrozen"]]), _monte.throw)
            foo
            """)

    def test_varAs(self):
        self.eq_(
            '''
            object var foo as Data implements DeepFrozen {}
            ''',
            """
            class _m_foo_Script(_monte.MonteObject):
                _m_fqn = '__main$foo'
                def __init__(_g_foo2, _m_auditors, foo_slot):
                    _g_foo2._m_audit(_m_auditors)
                    _monte.MonteObject._m_install(_g_foo2, 'foo', foo_slot)

                _m_objectExpr = "eJzzT8pKTS7RyCvNydFRCEssCkgsKUktytPwyy/Nc60oKNJQSsvPV9LUUQCpAFLByUWZBTD1CEUuiSWJIFXRSEKpqQVuRflVqXlKmrFAGTDW1AQApkAlYA=="

            _g_guard1 = _m_outerScope["Data"]
            foo = _monte.VarSlot(_g_guard1)
            _g_foo2 = _m_foo_Script([_m_outerScope["Data"], _m_outerScope["DeepFrozen"]], foo)
            foo._m_init(_g_foo2, _monte.throw)
            _g_foo2
            """)

    def test_methGuard(self):
        self.eq_(
            'object foo { method baz(x, y) :int { x }}',
             """
             class _m_foo_Script(_monte.MonteObject):
                 _m_fqn = '__main$foo'
                 def __init__(foo, _m_methodGuards):
                     foo._m_guardMethods(_m_methodGuards)

                 def baz(foo, x, y):
                     return foo._m_guardForMethod('baz').coerce(x, _monte.throw)

             foo = _m_foo_Script({'baz': _m_outerScope["int"]})
             foo
             """)

    def test_matcher(self):
        self.eq_(
            'object foo { method baz(x, y) { x } match [verb1, args1] { verb1 } match etc { etc }}',
             """
             class _m_foo_Script(_monte.MonteObject):
                 _m_fqn = '__main$foo'
                 _m_matcherNames = ['_g_matcher1', '_g_matcher2']
                 def baz(foo, x, y):
                     return x

                 def _g_matcher1(foo, _m_message):
                     _g_total_list3 = _m_message
                     try:
                         _g_list4, _g_list5, = _g_total_list3
                     except ValueError, _g_e6:
                         _monte.matcherFail(_g_e6)
                         raise RuntimeError("Ejector did not exit")
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
                _m_fqn = '__main$foo'
                def run(foo, x):
                    _m___return = _monte.ejector("__return")
                    try:
                        _m___return(_monte.wrap(1))
                        _g_escape2 = None
                    except _m___return._m_type, _g___return1:
                        _g_escape2 = _g___return1.args[0]
                    finally:
                        _m___return.disable()
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

    def test_selfReference(self):
        self.eq_(
            '''
            def foo(x) {
                return foo(x)
            }
            ''',
            """
            class _m_foo_Script(_monte.MonteObject):
                _m_fqn = '__main$foo'
                def run(foo, x):
                    _m___return = _monte.ejector("__return")
                    try:
                        _m___return(foo(x))
                        _g_escape2 = None
                    except _m___return._m_type, _g___return1:
                        _g_escape2 = _g___return1.args[0]
                    finally:
                        _m___return.disable()
                    return _g_escape2

            foo = _m_foo_Script()
            foo
            """
        )

    def test_varSelfReference(self):
        self.eq_(
            'object var foo { method baz(x, y) { foo := 1; x }}',
             """
             class _m_foo_Script(_monte.MonteObject):
                 _m_fqn = '__main$foo'
                 def __init__(_g_foo1, foo_slot):
                     _monte.MonteObject._m_install(_g_foo1, 'foo', foo_slot)

                 def baz(_g_foo1, x, y):
                     _g_foo2 = _monte.wrap(1)
                     _g_foo1.put(_g_foo2)
                     return x

             foo = _monte.VarSlot(None)
             _g_foo1 = _m_foo_Script(foo)
             foo._m_init(_g_foo1, _monte.throw)
             _g_foo1
             """)

    def test_escape(self):
        self.eq_(
            '''
            var x := 1
            escape e {
              e(2)
            } catch v {
              x := v
            }
            ''',
            """
            _g_x1 = _monte.wrap(1)
            x = _monte.VarSlot(None, _g_x1, _monte.throw)
            e = _monte.ejector("e")
            try:
                _g_escape3 = e(_monte.wrap(2))
            except e._m_type, _g_e2:
                v = _g_e2.args[0]
                _g_x4 = v
                x.put(_g_x4)
                _g_escape3 = _g_x4
            finally:
                e.disable()
            _g_escape3
            """)

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
            _g_x1 = _monte.wrap(1)
            x = _monte.VarSlot(None, _g_x1, _monte.throw)
            _g_x2 = _monte.wrap(2)
            x.put(_g_x2)
            _g_x2
            """)

    def test_metacontext(self):
        self.eq_(
            '''
            object foo {
                method baz(x, y) {
                    def a := 2
                    var b := 3
                    object boz {
                        method blee() { b := a; meta.context() }
                    }
                }
            }''',
             """
             class _m_boz_Script(_monte.MonteObject):
                 _m_fqn = '__main$foo$boz'
                 def __init__(boz, a_slot, b_slot):
                     _monte.MonteObject._m_install(boz, 'a', a_slot)
                     _monte.MonteObject._m_install(boz, 'b', b_slot)

                 def blee(boz):
                     _g_b2 = boz.a
                     boz.b = _g_b2
                     return _monte.StaticContext('__main$foo$boz', ['b', 'a'], _m_boz_Script._m_objectExpr)

                 _m_objectExpr = "eJzzT8pKTS7RyCvNydFRcMvMS8wJSCwpSS3K0/DLL81zrSgo0lBKyq9S0tRRAKkBUsHJRZkFMB0QMjoWiH1TSzLyU6DiSkk5qalKEBmISHBqIdi0aMfi4sx0FONBhiO4iUqaQD7QtEQNJef8vJLUihIlzVhNTZAdQAoAuNc5Rg=="

             class _m_foo_Script(_monte.MonteObject):
                 _m_fqn = '__main$foo'
                 def baz(foo, x, y):
                     a = _monte.wrap(2)
                     _g_b1 = _monte.wrap(3)
                     b = _monte.VarSlot(None, _g_b1, _monte.throw)
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
                _m_fqn = '__main$_'
                def __init__(_g_ignore2, _m_methodGuards):
                    _g_ignore2._m_guardMethods(_m_methodGuards)

                def run(_g_ignore2):
                    _m___return = _monte.ejector("__return")
                    try:
                        x = _monte.wrap(1)
                        _m___return(_monte.Map(()))
                        _g_escape4 = None
                    except _m___return._m_type, _g___return3:
                        _g_escape4 = _g___return3.args[0]
                    finally:
                        _m___return.disable()
                    return _g_ignore2._m_guardForMethod('run').coerce(_g_escape4, _monte.throw)

            _g_ignore2 = _m__g_ignore1_Script({'run': _m_outerScope["any"]})
            _g_ignore2()
            """)

    def test_metastate(self):
        self.eq_(
            '''
            def foo() {
                def a := 1;
                var b := 2;
                var c := 3;
                return object boz {
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
                _m_fqn = '__main$foo$boz'
                def __init__(boz, a_slot, b_slot):
                    _monte.MonteObject._m_install(boz, 'a', a_slot)
                    _monte.MonteObject._m_install(boz, 'b', b_slot)

                def biz(boz):
                    x = _monte.wrap(17)
                    return _monte.Map((('&b', _monte.getSlot(boz, 'b')), ('&a', _monte.getSlot(boz, 'a'))))

                def baz(boz):
                    _g_b5 = boz.b.add(boz.a)
                    boz.b = _g_b5
                    return _g_b5

            class _m_foo_Script(_monte.MonteObject):
                _m_fqn = '__main$foo'
                def run(foo):
                    _m___return = _monte.ejector("__return")
                    try:
                        a = _monte.wrap(1)
                        _g_b3 = _monte.wrap(2)
                        b = _monte.VarSlot(None, _g_b3, _monte.throw)
                        _g_c4 = _monte.wrap(3)
                        c = _monte.VarSlot(None, _g_c4, _monte.throw)
                        boz = _m_boz_Script(_monte.FinalSlot(a, None), b)
                        _m___return(boz)
                        _g_escape2 = None
                    except _m___return._m_type, _g___return1:
                        _g_escape2 = _g___return1.args[0]
                    finally:
                        _m___return.disable()
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
                _g_finally1 = _monte.wrap(1)
            finally:
                _monte.wrap(2)
            _g_finally1
            """)

    def test_catch(self):
        self.eq_(
            '''
            try { 1 } catch p { 2 }
            ''',
            """
            try:
                _g_catch1 = _monte.wrap(1)
            except _monte.MonteEjection:
                raise
            except BaseException, _g_exception2:
                p = _g_exception2
                _g_catch1 = _monte.wrap(2)
            _g_catch1
            """)

    def test_hide(self):
        self.eq_(
            '''
            def x := 1; {def x := 2}
            ''',
            """
            x = _monte.wrap(1)
            _g_x1 = _monte.wrap(2)
            _g_x1
            """)

    def test_if(self):
        self.eq_(
            '''
            if (1) { 2 } else { 3 }
            ''',
            """
            if _monte.booleanGuard.coerce(_monte.wrap(1), None):
                _g_if1 = _monte.wrap(2)
            else:
                _g_if1 = _monte.wrap(3)
            _g_if1
            """)

    def test_oneArmedIf(self):
        self.eq_(
            '''
            if (1) { 2 }
            ''',
            """
            if _monte.booleanGuard.coerce(_monte.wrap(1), None):
                _g_if1 = _monte.wrap(2)
            else:
                _g_if1 = None
            _g_if1
            """)

    def test_via(self):
        self.eq_(
            '''
            def a := 3
            def b := 4
            def via (a + 1) x exit b := 2
            ''',
            """
            a = _monte.wrap(3)
            b = _monte.wrap(4)
            x = a.add(_monte.wrap(1))(_monte.wrap(2), _monte.wrapEjector(b))
            _monte.wrap(2)
            """)

    def test_bindingexpr_local(self):
        self.eq_(
            '''
            var x := 1
            &&x
            ''',
            """
            _g_x1 = _monte.wrap(1)
            x = _monte.VarSlot(None, _g_x1, _monte.throw)
            _monte.reifyBinding(x)
            """)

    def test_bindingexpr_frame(self):
        self.eq_(
            '''
            var x := 1
            object foo {
              method baz() {
                &&x
              }
            }
            ''',
            """
            class _m_foo_Script(_monte.MonteObject):
                _m_fqn = '__main$foo'
                def __init__(foo, x_slot):
                    _monte.MonteObject._m_install(foo, 'x', x_slot)

                def baz(foo):
                    return _monte.getBinding(foo, 'x')

            _g_x1 = _monte.wrap(1)
            x = _monte.VarSlot(None, _g_x1, _monte.throw)
            foo = _m_foo_Script(x)
            foo

            """)

    def test_bindingpatt(self):
        self.eq_(
            '''
            def a := 1
            def &&x := &&a
            ''',
            """
            a = _monte.wrap(1)
            x = _monte.slotFromBinding(_monte.reifyBinding(_monte.FinalSlot(a)))
            x
            """)
