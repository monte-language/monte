# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.
import textwrap

from twisted.trial import  unittest
from monte.compiler import ecompile, CompileError, mangleIdent
from monte.runtime.scope import safeScope

class CompilerTest(unittest.TestCase):
    maxDiff = None
    def eq_(self, esrc, pysrc):
        self.assertMultiLineEqual(ecompile(textwrap.dedent(esrc).strip(), safeScope),
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
        self.assertEqual(ecompile("'x'", {}), "_monte.makeCharacter('x')")
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
        x = _monte.VarSlot(_monte.null, _g_x1, _monte.throw)
        _g_x1
        """)
    def test_varNoun(self):
        self.eq_("var x := 1; x",
        """
        _g_x1 = _monte.wrap(1)
        x = _monte.VarSlot(_monte.null, _g_x1, _monte.throw)
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
            x = _monte.VarSlot(_monte.null, _g_x1, _monte.throw)
            _g_x2 = _monte.wrap(2)
            x.put(_g_x2)
            _g_x2
            """)
        self.assertRaises(CompileError, ecompile, "def x := 1; x := 2", {})
        self.assertRaises(CompileError, ecompile, "x := 2", {})

    def test_guardpattern(self):
        self.eq_("def x :float := 1",
                 """
                 _g_guard1 = _m_outerScope["float"]
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

        self.eq_('def [x :float, y :str, z] := "foo"',
                 """
                 _g_total_list1 = _monte.wrap(u'foo')
                 try:
                     _g_list2, _g_list3, _g_list4, = _g_total_list1
                 except ValueError, _g_e5:
                     _monte.throw(_g_e5)
                     raise RuntimeError("Ejector did not exit")
                 _g_guard6 = _m_outerScope["float"]
                 x = _g_guard6.coerce(_g_list2, _monte.throw)
                 _g_guard7 = _m_outerScope["str"]
                 y = _g_guard7.coerce(_g_list3, _monte.throw)
                 z = _g_list4
                 _g_total_list1
                 """)

        self.eq_('def ej := 1; def [x :float, y :str, z] exit ej := "foo"',
                 """
                 ej = _monte.wrap(1)
                 _g_total_list1 = _monte.wrap(u'foo')
                 try:
                     _g_list2, _g_list3, _g_list4, = _g_total_list1
                 except ValueError, _g_e5:
                     ej(_g_e5)
                     raise RuntimeError("Ejector did not exit")
                 _g_guard6 = _m_outerScope["float"]
                 x = _g_guard6.coerce(_g_list2, ej)
                 _g_guard7 = _m_outerScope["str"]
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

    def test_noMethodCollision(self):
        self.eq_("""
            def x := 42
            object test:
                method x():
                    x

            test.x()
            """,
            """
            class _m_test_Script(_monte.MonteObject):
                _m_fqn = '__main$test'
                _g_x1 = _monte._SlotDescriptor('x')
                def __init__(test, x_slotPair):
                    test._m_slots = {
                        'x': x_slotPair,
                    }

                def x(test):
                    return test._g_x1

            x = _monte.wrap(42)
            test = _m_test_Script((_monte.FinalSlot(x, _monte.null, unsafe=True), _monte.FinalSlot.asType().get(_monte.null)))
            test.x()
            """)
    def test_trivialVarObject(self):
        self.eq_(
            'object var foo { method baz(x, y) { x }}',
             """
             class _m_foo_Script(_monte.MonteObject):
                 _m_fqn = '__main$foo'
                 foo = _monte._SlotDescriptor('foo')
                 def __init__(foo, foo_slotPair):
                     foo._m_slots = {
                         'foo': foo_slotPair,
                     }

                 def baz(foo, x, y):
                     return x

             foo = _monte.VarSlot(_monte.null)
             _g_foo1 = _m_foo_Script((foo, _monte.VarSlot.asType().get(_monte.null)))
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
                f = _monte._SlotDescriptor('f')
                def __init__(q, f_slotPair):
                    q._m_slots = {
                        'f': f_slotPair,
                    }

                def do(q):
                    return q.f

            class _m_o_Script(_monte.MonteObject):
                _m_fqn = '__main$outer$o'
                f = _monte._SlotDescriptor('f')
                def __init__(o, f_slotPair):
                    o._m_slots = {
                        'f': f_slotPair,
                    }

                def inner(o, x):
                    q = _m_q_Script((_monte.FinalSlot(o.f, None, unsafe=True), o._m_slots["f"][1]))
                    return q.do()

            class _m_outer_Script(_monte.MonteObject):
                _m_fqn = '__main$outer'
                def run(outer, f):
                    o = _m_o_Script((_monte.FinalSlot(f, _monte.null, unsafe=True), _monte.FinalSlot.asType().get(_monte.null)))
                    return o

            outer = _m_outer_Script()
            outer(_monte.wrap(0)).inner(_monte.wrap(1))
            """)

    def test_classGensym(self):
        self.eq_(
            '''
            object foo:
                method x():
                    object baz:
                        pass
                method y():
                    object baz:
                        pass
             ''',
             """
             class _m_baz_Script(_monte.MonteObject):
                 _m_fqn = '__main$foo$baz'
             class _g_baz1_Script(_monte.MonteObject):
                 _m_fqn = '__main$foo$baz'
             class _m_foo_Script(_monte.MonteObject):
                 _m_fqn = '__main$foo'
                 def x(foo):
                     baz = _m_baz_Script()
                     return baz

                 def y(foo):
                     baz = _g_baz1_Script()
                     return baz

             foo = _m_foo_Script()
             foo
             """)


    def test_frameFinal(self):
        self.eq_(
            '''
            object foo {
                method baz(x :int, y) {
                    def a := 2
                    def b :(float >= 0) := 3.0
                    object boz {
                        method blee() { b.foo(a + x) }
                    }
                }
            }''',
             """
             class _m_boz_Script(_monte.MonteObject):
                 _m_fqn = '__main$foo$boz'
                 a = _monte._SlotDescriptor('a')
                 b = _monte._SlotDescriptor('b')
                 x = _monte._SlotDescriptor('x')
                 def __init__(boz, a_slotPair, b_slotPair, x_slotPair):
                     boz._m_slots = {
                         'a': a_slotPair,
                         'b': b_slotPair,
                         'x': x_slotPair,
                     }

                 def blee(boz):
                     return boz.b.foo(boz.a.add(boz.x))

             class _m_foo_Script(_monte.MonteObject):
                 _m_fqn = '__main$foo'
                 def baz(foo, _g_Final1, y):
                     _g_guard2 = _m_outerScope["int"]
                     x = _g_guard2.coerce(_g_Final1, _monte.throw)
                     a = _monte.wrap(2)
                     _g_guard3 = _m_outerScope["__comparer"].geq(_m_outerScope["float"], _monte.wrap(0))
                     b = _g_guard3.coerce(_monte.wrap(3.0), _monte.throw)
                     boz = _m_boz_Script((_monte.FinalSlot(a, _monte.null, unsafe=True), _monte.FinalSlot.asType().get(_monte.null)), (_monte.FinalSlot(b, _g_guard3, unsafe=True), _monte.FinalSlot.asType().get(_g_guard3)), (_monte.FinalSlot(x, _g_guard2, unsafe=True), _monte.FinalSlot.asType().get(_g_guard2)))
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
                 a = _monte._SlotDescriptor('a')
                 b = _monte._SlotDescriptor('b')
                 def __init__(left, a_slotPair, b_slotPair):
                     left._m_slots = {
                         'a': a_slotPair,
                         'b': b_slotPair,
                     }

                 def inc(left):
                     _g_a6 = left.a.add(_monte.wrap(1))
                     left.a = _g_a6
                     return left.b

             class _m_right_Script(_monte.MonteObject):
                 _m_fqn = '__main$foo$right'
                 a = _monte._SlotDescriptor('a')
                 b = _monte._SlotDescriptor('b')
                 def __init__(right, a_slotPair, b_slotPair):
                     right._m_slots = {
                         'a': a_slotPair,
                         'b': b_slotPair,
                     }

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
                     a = _monte.VarSlot(_monte.null, _g_a3, _monte.throw)
                     _g_guard4 = _m_outerScope["int"]
                     _g_b5 = _monte.wrap(0)
                     b = _monte.VarSlot(_g_guard4, _g_b5, _monte.throw)
                     left = _m_left_Script((a, _monte.VarSlot.asType().get(_monte.null)), (b, _monte.VarSlot.asType().get(_g_guard4)))
                     right = _m_right_Script((a, _monte.VarSlot.asType().get(_monte.null)), (b, _monte.VarSlot.asType().get(_g_guard4)))
                     return _m_outerScope["__makeList"](left, right)

             foo = _m_foo_Script()
             foo
             """)

    def test_doubleNestVar(self):
        self.eq_(
            '''
            object a:
                to go():
                    var x := 0
                    return object b:
                        method do():
                          return object c:
                              method it():
                                  x
            ''',
            '''
            class _m_c_Script(_monte.MonteObject):
                _m_fqn = '__main$a$b$c'
                x = _monte._SlotDescriptor('x')
                def __init__(c, x_slotPair):
                    c._m_slots = {
                        'x': x_slotPair,
                    }

                def it(c):
                    return c.x

            class _m_b_Script(_monte.MonteObject):
                _m_fqn = '__main$a$b'
                _m___return = _monte._SlotDescriptor('__return')
                x = _monte._SlotDescriptor('x')
                def __init__(b, _m___return_slotPair, x_slotPair):
                    b._m_slots = {
                        '__return': _m___return_slotPair,
                        'x': x_slotPair,
                    }

                def do(b):
                    c = _m_c_Script((b._m_slots["x"][0], b._m_slots["x"][1]))
                    return b._m___return(c)

            class _m_a_Script(_monte.MonteObject):
                _m_fqn = '__main$a'
                def go(a):
                    _m___return = _monte.ejector("__return")
                    try:
                        _g_x3 = _monte.wrap(0)
                        x = _monte.VarSlot(_monte.null, _g_x3, _monte.throw)
                        b = _m_b_Script((_monte.FinalSlot(_m___return, _monte.null, unsafe=True), _monte.FinalSlot.asType().get(_monte.null)), (x, _monte.VarSlot.asType().get(_monte.null)))
                        _m___return(b)
                        _g_escape2 = _monte.null
                    except _m___return._m_type, _g___return1:
                        _g_escape2 = _g___return1.args[0]
                    finally:
                        _m___return.disable()
                    return _g_escape2

            a = _m_a_Script()
            a
            '''
            )



    def test_implements(self):
        self.eq_(
            '''
            object foo implements DeepFrozen, Data {}
            ''',
            """
            class _m_foo_Script(_monte.MonteObject):
                _m_fqn = '__main$foo'
                def __init__(foo, _m_auditors):
                    foo._m_slots = {}
                    foo._m_outers = {
                        'Data': _monte.deepFrozenGuard,
                        'DeepFrozen': _monte.deepFrozenGuard,
                    }
                    foo._m_audit(_m_auditors, _monte.safeScope)

                _m_objectExpr = "0 :)!   #foo '# )!   *DeepFrozen)!   $Data1 ' ' "

            foo = _m_foo_Script([_m_outerScope["DeepFrozen"], _m_outerScope["Data"]])
            foo
            """)

    def test_auditBindingGuards(self):
        self.eq_(
            '''
            def x :int := 1
            def y := 2
            var z :float := 0
            def &w := __makeFinalSlot(9)
            object foo implements DeepFrozen, Data {
                method run() {
                    [x, y, z, w]
                }
            }
            ''',
            """
            class _m_foo_Script(_monte.MonteObject):
                _m_fqn = '__main$foo'
                w = _monte._SlotDescriptor('w')
                x = _monte._SlotDescriptor('x')
                y = _monte._SlotDescriptor('y')
                z = _monte._SlotDescriptor('z')
                def __init__(foo, _m_auditors, w_slotPair, x_slotPair, y_slotPair, z_slotPair):
                    foo._m_slots = {
                        'w': w_slotPair,
                        'x': x_slotPair,
                        'y': y_slotPair,
                        'z': z_slotPair,
                    }
                    foo._m_outers = {
                        '__makeList': _monte.deepFrozenGuard,
                        'Data': _monte.deepFrozenGuard,
                        'DeepFrozen': _monte.deepFrozenGuard,
                    }
                    foo._m_audit(_m_auditors, _monte.safeScope)

                def run(foo):
                    return _m_outerScope["__makeList"](foo.x, foo.y, foo.z, foo.w.slot.get())

                _m_objectExpr = "0 :)!   #foo '# )!   *DeepFrozen)!   $Data1 '!2 !   #run'  ,)!   *__makeList!   #run'$)!   !x)!   !y)!   !z)!   !w' "

            _g_guard1 = _m_outerScope["int"]
            x = _g_guard1.coerce(_monte.wrap(1), _monte.throw)
            y = _monte.wrap(2)
            _g_guard2 = _m_outerScope["float"]
            _g_z3 = _monte.wrap(0)
            z = _monte.VarSlot(_g_guard2, _g_z3, _monte.throw)
            w = _m_outerScope["__slotToBinding"](_m_outerScope["__makeFinalSlot"](_monte.wrap(9)), _monte.wrapEjector(_monte.throw))
            foo = _m_foo_Script([_m_outerScope["DeepFrozen"], _m_outerScope["Data"]], (w.slot, w.guard), (_monte.FinalSlot(x, _g_guard1, unsafe=True), _monte.FinalSlot.asType().get(_g_guard1)), (_monte.FinalSlot(y, _monte.null, unsafe=True), _monte.FinalSlot.asType().get(_monte.null)), (z, _monte.VarSlot.asType().get(_g_guard2)))
            foo
            """)

    def test_simpleAs(self):
        self.eq_(
            '''
            object foo as Data implements DeepFrozen {}
            ''',
            r"""
            class _m_foo_Script(_monte.MonteObject):
                _m_fqn = '__main$foo'
                def __init__(foo, _m_auditors):
                    foo._m_slots = {}
                    foo._m_outers = {
                        'DeepFrozen': _monte.deepFrozenGuard,
                        'Data': _monte.deepFrozenGuard,
                    }
                    foo._m_audit(_m_auditors, _monte.safeScope)

                _m_objectExpr = '0 :)!   #foo \'")!   $Data)!   *DeepFrozen1 \' \' '

            foo = _m_foo_Script([_m_outerScope["Data"], _m_outerScope["DeepFrozen"]])
            foo
            """)

    def test_varAs(self):
        self.eq_(
            '''
            object var foo as Data implements DeepFrozen {}
            ''',
            r"""
            class _m_foo_Script(_monte.MonteObject):
                _m_fqn = '__main$foo'
                foo = _monte._SlotDescriptor('foo')
                def __init__(foo, _m_auditors, foo_slotPair):
                    foo._m_slots = {
                        'foo': foo_slotPair,
                    }
                    foo._m_outers = {
                        'DeepFrozen': _monte.deepFrozenGuard,
                        'Data': _monte.deepFrozenGuard,
                    }
                    foo._m_audit(_m_auditors, _monte.safeScope)

                _m_objectExpr = '0 <)!   #foo \'")!   $Data)!   *DeepFrozen1 \' \' '

            foo = _monte.VarSlot(_monte.null)
            _g_foo1 = _m_foo_Script([_m_outerScope["Data"], _m_outerScope["DeepFrozen"]], (foo, _monte.VarSlot.asType().get(_m_outerScope["Data"])))
            foo._m_init(_g_foo1, _monte.throw)
            _g_foo1
            """)

    def test_methGuard(self):
        self.eq_(
            'object foo { method baz(x, y) :int { x }}',
             """
             class _m_foo_Script(_monte.MonteObject):
                 _m_fqn = '__main$foo'
                 def __init__(foo, _m_methodGuards):
                     foo._m_guardMethods(_m_methodGuards)
                     foo._m_slots = {}

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
                        _g_escape2 = _monte.null
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
                        _g_escape2 = _monte.null
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
                 foo = _monte._SlotDescriptor('foo')
                 def __init__(foo, foo_slotPair):
                     foo._m_slots = {
                         'foo': foo_slotPair,
                     }

                 def baz(foo, x, y):
                     _g_foo2 = _monte.wrap(1)
                     foo.foo.put(_g_foo2)
                     return x

             foo = _monte.VarSlot(_monte.null)
             _g_foo1 = _m_foo_Script((foo, _monte.VarSlot.asType().get(_monte.null)))
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
            x = _monte.VarSlot(_monte.null, _g_x1, _monte.throw)
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
            x = _monte.VarSlot(_monte.null, _g_x1, _monte.throw)
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
            r"""
             class _m_boz_Script(_monte.MonteObject):
                 _m_fqn = '__main$foo$boz'
                 a = _monte._SlotDescriptor('a')
                 b = _monte._SlotDescriptor('b')
                 def __init__(boz, a_slotPair, b_slotPair):
                     boz._m_slots = {
                         'a': a_slotPair,
                         'b': b_slotPair,
                     }

                 def blee(boz):
                     _g_b2 = boz.a
                     boz.b = _g_b2
                     return _monte.StaticContext('__main$foo$boz', ['a', 'b'], _m_boz_Script._m_objectExpr)

                 _m_objectExpr = '0 :)!   #boz \'! 1 \'!2 !   $blee\'  +\'"4)!   !b)!   !a9!   \'Context\' '

             class _m_foo_Script(_monte.MonteObject):
                 _m_fqn = '__main$foo'
                 def baz(foo, x, y):
                     a = _monte.wrap(2)
                     _g_b1 = _monte.wrap(3)
                     b = _monte.VarSlot(_monte.null, _g_b1, _monte.throw)
                     boz = _m_boz_Script((_monte.FinalSlot(a, _monte.null, unsafe=True), _monte.FinalSlot.asType().get(_monte.null)), (b, _monte.VarSlot.asType().get(_monte.null)))
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
                def __init__(_g_ignore1, _m_methodGuards):
                    _g_ignore1._m_guardMethods(_m_methodGuards)
                    _g_ignore1._m_slots = {}

                def run(_g_ignore1):
                    _m___return = _monte.ejector("__return")
                    try:
                        x = _monte.wrap(1)
                        _m___return(_monte.Map(()))
                        _g_escape4 = _monte.null
                    except _m___return._m_type, _g___return3:
                        _g_escape4 = _g___return3.args[0]
                    finally:
                        _m___return.disable()
                    return _g_ignore1._m_guardForMethod('run').coerce(_g_escape4, _monte.throw)

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
                a = _monte._SlotDescriptor('a')
                b = _monte._SlotDescriptor('b')
                def __init__(boz, a_slotPair, b_slotPair):
                    boz._m_slots = {
                        'a': a_slotPair,
                        'b': b_slotPair,
                    }

                def biz(boz):
                    x = _monte.wrap(17)
                    return _monte.Map((('&a', _monte.getSlot(boz, 'a')), ('&b', _monte.getSlot(boz, 'b'))))

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
                        b = _monte.VarSlot(_monte.null, _g_b3, _monte.throw)
                        _g_c4 = _monte.wrap(3)
                        c = _monte.VarSlot(_monte.null, _g_c4, _monte.throw)
                        boz = _m_boz_Script((_monte.FinalSlot(a, _monte.null, unsafe=True), _monte.FinalSlot.asType().get(_monte.null)), (b, _monte.VarSlot.asType().get(_monte.null)))
                        _m___return(boz)
                        _g_escape2 = _monte.null
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
            if _monte.booleanGuard.coerce(_monte.wrap(1), _monte.null):
                _g_if1 = _monte.wrap(2)
            else:
                _g_if1 = _monte.wrap(3)
            _g_if1
            """)


    def test_indent(self):
        self.eq_(
            '''
            if (1):
                # comment
                2
            else:

                3
            ''',
            """
            if _monte.booleanGuard.coerce(_monte.wrap(1), _monte.null):
                _g_if1 = _monte.wrap(2)
            else:
                _g_if1 = _monte.wrap(3)
            _g_if1
            """)

    def test_elseif(self):
        self.eq_(
            '''
            if (1):
                2
            else if (3):
                4
            else:
                5
            ''',
            """
            if _monte.booleanGuard.coerce(_monte.wrap(1), _monte.null):
                _g_if1 = _monte.wrap(2)
            else:
                if _monte.booleanGuard.coerce(_monte.wrap(3), _monte.null):
                    _g_if2 = _monte.wrap(4)
                else:
                    _g_if2 = _monte.wrap(5)
                _g_if1 = _g_if2
            _g_if1
            """)


    def test_oneArmedIf(self):
        self.eq_(
            '''
            if (1) { 2 }
            ''',
            """
            if _monte.booleanGuard.coerce(_monte.wrap(1), _monte.null):
                _g_if1 = _monte.wrap(2)
            else:
                _g_if1 = _monte.null
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
            x = _monte.VarSlot(_monte.null, _g_x1, _monte.throw)
            _monte.Binding(_monte.VarSlot.asType().get(_monte.null), x)
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
                x = _monte._SlotDescriptor('x')
                def __init__(foo, x_slotPair):
                    foo._m_slots = {
                        'x': x_slotPair,
                    }

                def baz(foo):
                    return _monte.getBinding(foo, 'x')

            _g_x1 = _monte.wrap(1)
            x = _monte.VarSlot(_monte.null, _g_x1, _monte.throw)
            foo = _m_foo_Script((x, _monte.VarSlot.asType().get(_monte.null)))
            foo

            """)

    def test_bindingpatt(self):
        self.eq_(
            '''
            def a :int := 1
            def &&x := &&a
            x
            ''',
            """
            _g_guard1 = _m_outerScope["int"]
            a = _g_guard1.coerce(_monte.wrap(1), _monte.throw)
            x = _monte.Binding(_monte.FinalSlot.asType().get(_g_guard1), _monte.FinalSlot(a))
            x.slot.get()
            """)

    def test_module(self):
        self.eq_(
            '''
            module x, y
            x.foo(y)
            ''',
            """
            def _g_module1(x, y):
                x.foo(y)
                return {}
            _g_module1
            """)

        self.eq_(
            '''
            module x, y
            export (a)
            def b := x.foo(y)
            def a := 1
            ''',
            """
            def _g_module1(x, y):
                b = x.foo(y)
                a = _monte.wrap(1)
                a
                return {'a': a}
            _g_module1
            """)
