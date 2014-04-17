from textwrap import dedent
from monte.test import unittest
from monte.runtime.base import toQuote
from monte.runtime.data import false, true, Integer, String
from monte.runtime.load import eval as monte_eval
from monte.runtime.scope import safeScope
from monte.runtime.tables import ConstList, ConstMap, FlexList
from monte.runtime.compiler_helpers import wrap


class NullPropertiesTest(unittest.TestCase):

    def test_equal(self):
        self.assertEqual(monte_eval("null == null"), true)

    def test_inequal(self):
        self.assertEqual(monte_eval("null != null"), false)


class EvalTest(unittest.TestCase):

    def test_base(self):
        self.assertEqual(monte_eval("3 + 4"), Integer(7))

    def test_string(self):
        self.assertEqual(monte_eval('"foo"'), String(u'foo'))

    def test_object(self):
        self.assertEqual(monte_eval(dedent(
            """
            def foo():
                return 3
            def baz():
                return 4
            foo() + baz()
            """)),
            Integer(7))

    def test_scope(self):
        self.assertEqual(monte_eval("if (true) {1} else {2}"), Integer(1))

    def test_comparer(self):
        self.assertEqual(monte_eval("1 < 2"), true)
        self.assertEqual(monte_eval("1 > 2"), false)
        self.assertEqual(monte_eval("3 >= 3"), true)
        self.assertEqual(monte_eval("3 <= 3"), true)
        self.assertEqual(monte_eval("3 <=> 4"), false)

    def test_list(self):
        self.assertEqual(monte_eval("[0, 1]"), ConstList((Integer(0), Integer(1))))

    def test_def(self):
        self.assertEqual(monte_eval("def x := 1; x"), Integer(1))

    def test_var(self):
        self.assertEqual(monte_eval("var x := 1; x := 2; x"), Integer(2))

    def test_for(self):
        self.assertEqual(monte_eval("var x := 0; for y in [1, 2] { x := y }; x"), Integer(2))
        self.assertEqual(monte_eval("var x := 0; for y in [1, 2] { x := y; break}; x"), Integer(1))
        self.assertEqual(monte_eval("for y in [1, 2] { break(3)}"), Integer(3))

    def test_listcomp(self):
        self.assertEqual(monte_eval("[x + 1 for x in [0, 1]]"), ConstList((Integer(1), Integer(2))))
        self.assertEqual(monte_eval("[k + v for k => v in [3, 4, 7]]"), ConstList((Integer(3), Integer(5), Integer(9))))

    def test_map(self):
        self.assertEqual(monte_eval('["a" => 3, "b" => 4]["a"]'), Integer(3))

    def test_mapcomp(self):
        self.assertEqual(monte_eval('[x => x + 1 for x in [1, 2]][2]'), Integer(3))

    def test_while(self):
        self.assertEqual(monte_eval('var x := 0; while (x <= 3) { x += 1}; x'), Integer(4))

    def test_tryDoesntCatchEjections(self):
        self.assertEqual(
            monte_eval(
                'var x := 0; escape e { try { e(1) } catch p { x := p } }; x'),
            Integer(0))

    def test_scopesDontOverlap(self):
        self.assertEqual(
            monte_eval(
                'def x := 1; if (true) { def x := 2}; x'),
            Integer(1))

    def test_verbFacet(self):
        self.assertEqual(monte_eval("def foo() { return 1 }; def x := foo.run; x()"), Integer(1))

    def test_matchsame(self):
        self.assertEqual(monte_eval("def ==1 := 1"), Integer(1))
        self.assertRaises(RuntimeError, monte_eval, "def ==1 := 2")

    def test_bind(self):
        self.assertEqual(monte_eval("def x; bind x := 1; x"), Integer(1))

    def test_map_patt(self):
        self.assertEqual(monte_eval('def ["a" => a, "b" => c] := ["a" => 1, "b" => 3]; c - a'), Integer(2))
#        self.assertEqual(monte_eval('def ["a" => a, "b" => c, "e" => e default {9}] := ["a" => 1, "b" => 3]; e'), Integer(9))
        self.assertRaises(RuntimeError, monte_eval,
                          'def ["a" => a, "b" => c] := ["a" => 1, "b" => 3, "e" => 4]')

        self.assertEqual(monte_eval(
            'def ["a" => a, "b" => c] | d := ["a" => 1, "b" => 3, "e" => 4]; d'),
                         ConstMap({String(u'e'): Integer(4)}))

    def test_list_patt(self):
        self.assertEqual(monte_eval('def [a, b, c] := [2, 3, 4]; c - a'), Integer(2))
        self.assertEqual(monte_eval('def [a, b, c] + d := [2, 3, 4, 7, 6]; d'), ConstList((Integer(7), Integer(6))))

    def test_suchthat(self):
        self.assertEqual(monte_eval('def a ? (a > 0) := 1; a'), Integer(1))
        self.assertRaises(RuntimeError, monte_eval, 'def a ? (a > 10) := 1')

    def test_switch(self):
        self.assertEqual(monte_eval('switch (1) { match ==0 { 1} match ==1 { 2}}'), Integer(2))
        self.assertRaises(RuntimeError, monte_eval, 'switch (2) { match ==0 { 1} match ==1 { 2}}')

    def test_coerce(self):
        self.assertEqual(monte_eval('true :boolean'), true)

    def test_simple_quasiParser_value(self):
        self.assertEqual(monte_eval('def x := 42; `($x)`'), String(u"(42)"))
        self.assertEqual(monte_eval('def x := 1; def y := [2, 3]; `one $x and $y and two`'),
                         String(u"one 1 and [2, 3] and two"))

    def test_simple_quasiParser_pattern(self):
        self.assertEqual(
            monte_eval('def `one @x and @y and two` := "one foo and bar and two"; [x, y]'),
            ConstList((String(u"foo"), String(u"bar"))))
        self.assertEqual(
            monte_eval('def `foo @x@y` := "foo baz"; [x, y]'),
            ConstList((String(u""), String(u"baz"))))
        self.assertEqual(
            monte_eval('def a := "baz"; def `foo @x$a` := "foo baz"; x'),
            String(u""))

    def test_and(self):
        self.assertEqual(monte_eval("true && false"), false)
        self.assertEqual(monte_eval("[(def x := true) && true, x]"), ConstList((true, true)))

    def test_or(self):
        self.assertEqual(monte_eval("true || false"), true)
        self.assertEqual(monte_eval("[(def x := true) || true, x]"), ConstList((true, true)))

    def test_binding(self):
        self.assertEqual(monte_eval("def x := 1; (&&x).get().get()"), Integer(1))

    def test_interface(self):
        self.assertEqual(monte_eval(
            "interface Foo { to doStuff(x)} ; object blee implements Foo {}; blee =~ _ :Foo"),
                         true)

    def test_interfaceGuards(self):
        self.assertEqual(monte_eval(dedent("""
            interface Foo guards FooStamp:
                to doStuff(x)
            object blee implements FooStamp:
                pass
            blee =~ _ :Foo
        """)),
                         true)

    def test_varParameters(self):
        self.assertEqual(monte_eval(dedent("""
            def foo(var x):
                x += 1
                return x
            foo(2)
        """)), Integer(3))

class EqualizerTest(unittest.TestCase):
    def test_prims(self):
        self.assertEqual(monte_eval("1 == 1"), true)
        self.assertEqual(monte_eval("1 == 2"), false)
        self.assertEqual(monte_eval("1 == 1.0"), false)
        self.assertEqual(monte_eval("'a' == 'a'"), true)
        self.assertEqual(monte_eval("'a' == 'b'"), false)
        self.assertEqual(monte_eval("'a' == 1"), false)
        self.assertEqual(monte_eval("3.14 == 3.14"), true)
        self.assertEqual(monte_eval("3.14 == 3.15"), false)
        self.assertEqual(monte_eval('"fred" == "fred"'), true)
        self.assertEqual(monte_eval('"fred" == "barney"'), false)
        self.assertEqual(monte_eval('true == false'), false)
        self.assertEqual(monte_eval('false == false'), true)

    def test_list(self):
        self.assertEqual(monte_eval("[] == []"), true)
        self.assertEqual(monte_eval("[1] == [1]"), true)
        self.assertEqual(monte_eval("[1] == []"), false)
        self.assertEqual(monte_eval("[1, 2] == [3, 4]"), false)
        self.assertEqual(monte_eval("[5, [6, 7]] == [5, [6, 7]]"), true)
        self.assertEqual(monte_eval("[5, [6, 7]] == [5, [8, 7]]"), false)

    def test_opaque(self):
        self.assertEqual(monte_eval("object x {}; x == x"), true)

    def test_map(self):
        self.assertEqual(monte_eval("[1 => 2, 3 => 4] == [1 => 2, 3 => 4]"), true)
        self.assertEqual(monte_eval("[1 => 2, 3 => 4] == [3 => 4, 1 => 2]"), false)
        self.assertEqual(monte_eval("[].asMap() == [].asMap()"), true)

    def test_cycle(self):
        self.assertEqual(monte_eval("def x := [1, x]; x == x[1]"), true)
        self.assertEqual(monte_eval("def x := [1, x]; def y := [1, y]; x == y"), true)
        self.assertEqual(monte_eval("def x := [1 => x]; def y := [1 => y]; x == y"), true)

    def test_mapAsKey(self):
        self.assertEqual(monte_eval(dedent(
            """
            def k := [1 => 2, 3 => 4]
            def x := [].asMap().diverge()
            x[k] := 1
            x[[1 => 2, 3 => 4]] == 1
            """)),
                         true)

    def test_cyclicListAsKey(self):
        self.assertEqual(monte_eval(dedent(
            """
            def k := [1, k]
            def x := [].asMap().diverge()
            x[k] := 1
            def j := [1, j]
            x[j] == 1
            """)),
                         true)

class PrinterTest(unittest.TestCase):

    def pr(self, s):
        return toQuote(monte_eval(s))

    def test_prims(self):
        self.assertEqual(self.pr("1"), "1")
        self.assertEqual(self.pr("1.5"), "1.5")
        self.assertEqual(self.pr("'a'"), "'a'")
        self.assertEqual(self.pr('"foo baz \\u03b5"'), '"foo baz \\u03b5"')
        self.assertEqual(self.pr('"foo baz \\u03b5"[8]'), "'\\u03b5'")

    def test_list(self):
        self.assertEqual(self.pr("[1, 2]"), "[1, 2]")
        self.assertEqual(self.pr("[1, [2, 3, []]]"), "[1, [2, 3, []]]")
        self.assertEqual(self.pr("def x := [1, x]"), "[1, <**CYCLE**>]")

    def test_map(self):
        self.assertEqual(self.pr("[].asMap()"), "[].asMap()")
        self.assertEqual(self.pr("[1 => 2]"), "[1 => 2]")
        self.assertEqual(self.pr("[1 => 2, 3 => 4]"), "[1 => 2, 3 => 4]")
        self.assertEqual(self.pr("def x := [1 => 2, 3 => x]"), "[1 => 2, 3 => <**CYCLE**>]")


class AuditingTest(unittest.TestCase):

    def setUp(self):
        self.output = []
        self.scope = safeScope.copy()
        self.scope['emit'] = self.output.append

    def eq_(self, src, result):
        self.assertEqual(monte_eval(dedent(src), self.scope), result)

    def test_auditCalled(self):
        self.eq_("""
            var timesCalled := 0
            object approver:
                to audit(audition):
                    timesCalled += 1
                    return true
            object auditSample implements approver {}
            object auditSample_as as approver {}
            timesCalled
        """,
                 Integer(2))

    def test_stamped(self):
        self.eq_("""
            object approver:
                to audit(audition):
                    return true
            object auditSample implements approver {}
            object auditSample_as as approver {}
            __auditedBy(approver, auditSample) && __auditedBy(approver, auditSample_as)
        """,
                 true)

    def test_unstamped(self):
        self.eq_("""
            object approver:
                to audit(audition):
                    return true
            __auditedBy(approver, 1)
        """,
                 false)

    def test_rejected(self):
        self.eq_("""
            object noop:
                to audit(audition):
                    return false
            __auditedBy(noop, object x implements noop {}) || __auditedBy(noop, object y as noop {})
        """,
                 false)

    def test_badReturn(self):
        self.assertRaises(
            RuntimeError,
            monte_eval,
            dedent("""
                object approver:
                    to audit(audition) :any:
                        return 43
                object auditSample implements approver {}
                __auditedBy(approver, auditSample)
            """),
            self.scope)

    def test_nonGozerian(self):
        self.eq_("""
            object approver:
                to audit(audition):
                    return true
            object x:
                match msg:
                    emit(msg)
            __auditedBy(approver, x)
        """,
                 false)
        self.assertEqual(self.output, [])

    def test_delegator(self):
        self.eq_("""
            object approver:
                to audit(audition):
                    return true
            object delegatingAuditor:
                to audit(audition):
                    audition.ask(approver)
                    return false
            object x implements delegatingAuditor:
                pass
            [__auditedBy(delegatingAuditor, x), __auditedBy(approver, x)] == [false, true]
        """,
                 true)


class BindingGuardTest(unittest.TestCase):
    def setUp(self):
        CheckGuard = monte_eval(dedent(
            """
            object CheckGuard:
                to get(noun, guard):
                    return object guardCheckingAuditor:
                        to audit(audition):
                            if (audition.getGuard(noun) == guard):
                                return true
                            else:
                                throw(`$noun: expected $guard, got ${audition.getGuard(noun)}`)
            """))
        self.scope = safeScope.copy()
        self.scope["CheckGuard"] = CheckGuard

    def test_doesNotGuard(self):
        err = self.assertRaises(
            RuntimeError,
            monte_eval,
            dedent(
                """
                def FinalSlot := __makeFinalSlot.asType()
                def x := 1
                object doesNotGuardX implements CheckGuard["x", FinalSlot[int]]:
                    to f():
                        return x
                """), self.scope)
        self.assertEqual(str(err), "x: expected FinalSlot[int], got FinalSlot[any]")

    def test_doesNotMention(self):
        err = self.assertRaises(
            RuntimeError,
            monte_eval,
            dedent(
                """
                def FinalSlot := __makeFinalSlot.asType()
                def x := 1
                object doesNotMentionX implements CheckGuard["x", FinalSlot[int]]:
                    to f():
                        return 0
                """), self.scope)
        self.assertEqual(str(err), '"x" is not a free variable in <__main$doesNotMentionX>')

    def test_final(self):
        monte_eval(dedent(
            """
            def FinalSlot := __makeFinalSlot.asType()
            def x :int := 1
            object guardsX implements CheckGuard["x", FinalSlot[int]]:
                to f():
                    return x
            """), self.scope)

    def test_var(self):
        monte_eval(dedent(
            """
            def VarSlot := __makeVarSlot.asType()
            var x := 1
            object guardsX implements CheckGuard["x", VarSlot[any]]:
                to f():
                    return x
            """), self.scope)

    def test_guardedVar(self):
        monte_eval(dedent(
            """
            def VarSlot := __makeVarSlot.asType()
            var x :int := 1
            object guardsX implements CheckGuard["x", VarSlot[int]]:
                to f():
                    return x
            """), self.scope)

    def test_objectFinal(self):
        monte_eval(dedent(
            """
            def FinalSlot := __makeFinalSlot.asType()
            object x {}
            object guardsX implements CheckGuard["x", FinalSlot[any]]:
                to f():
                    return x
            """), self.scope)

    def test_as(self):
        monte_eval(dedent(
            """
            def FinalSlot := __makeFinalSlot.asType()
            object approver:
                to audit(audition):
                    return true
            object x as approver {}
            object guardsX implements CheckGuard["x", FinalSlot[approver]]:
                to f():
                    return x
            """), self.scope)

    def test_slot(self):
        monte_eval(dedent(
            """
            def s := __makeFinalSlot(1)
            def &x := s
            object guardsX implements CheckGuard["x", any]:
                to f():
                    return x
            """), self.scope)

    def test_guardedSlot(self):
        monte_eval(dedent(
            """
            def s := __makeFinalSlot(1)
            object g extends any {}
            def &x :g := s
            object guardsX implements CheckGuard["x", g]:
                to f():
                    return x
            """), self.scope)


class ConstListTest(unittest.TestCase):

    def test_get(self):
        self.assertEqual(monte_eval("def x := [1, 2, 3]; x[1]"), Integer(2))

    def test_print(self):
        self.assertEqual(monte_eval("def x := [1, 2, 3]; M.toString(x)"),
                         String(u'[1, 2, 3]'))

    def test_size(self):
        self.assertEqual(monte_eval("def x := [1, 2, 3]; x.size()"),
                         Integer(3))

    def test_add(self):
        self.assertEqual(monte_eval("[1, 2] + [3, 4] == [1, 2, 3, 4]"),
                         true)

    def test_contains(self):
        self.assertEqual(monte_eval("[1, 2, 3].contains(2)"),
                         true)
        self.assertEqual(monte_eval("[1, 2, 3].contains(4)"),
                         false)

    def test_sort(self):
        self.assertEqual(monte_eval(
            "[4, 9, 1, 2, 3].sort() == [1, 2, 3, 4, 9]"),
                         true)

    def test_fetch(self):
        self.assertEqual(monte_eval(
            "[4, 9, 1].fetch(0, fn {99}) == 4"),
                         true)
        self.assertEqual(monte_eval(
            "[4, 9, 1].fetch(3, fn {99}) == 99"),
                         true)

    def test_last(self):
        self.assertEqual(monte_eval(
            "[4, 9, 1, 13].last()"),
                         Integer(13))

    def test_with(self):
        self.assertEqual(monte_eval(
            "[4, 9, 1, 13].with(11) == [4, 9, 1, 13, 11]"),
                         true)
        self.assertEqual(monte_eval(
            "[4, 9, 1, 13].with(1, 11) == [4, 11, 9, 1, 13]"),
            true)

    def test_multiply(self):
        self.assertEqual(monte_eval(
            "[4] * 3 == [4, 4, 4]"),
                        true)

    def test_asMap(self):
        self.assertEqual(monte_eval(
            "[4, 9, 1, 13].asMap() == [0 => 4, 1 => 9, 2 => 1, 3 => 13]"),
                         true)

    def test_asKeys(self):
        self.assertEqual(monte_eval(
            "[4, 9, 1, 13].asKeys() == [4 => null, 9 => null, 1 => null, 13 => null]"),
                         true)

    def test_slice(self):
        self.assertEqual(monte_eval(
            "[4, 9, 1, 13].slice(1) == [9, 1, 13]"),
                         true)
        self.assertEqual(monte_eval(
            "[4, 9, 1, 13].slice(0, 2) == [4, 9]"),
                         true)

    def test_diverge(self):
        self.assertEqual(monte_eval(
            "[4, 9, 1, 13].diverge()").__class__,
                         FlexList)


class FlexListTest(unittest.TestCase):

    def test_get(self):
        self.assertEqual(monte_eval("def x := [1, 2, 3].diverge(); x[1]"), Integer(2))

    def test_print(self):
        self.assertEqual(monte_eval("def x := [1, 2, 3].diverge(); M.toString(x)"),
                         String(u'[1, 2, 3].diverge()'))

    def test_size(self):
        self.assertEqual(monte_eval("def x := [1, 2, 3].diverge(); x.size()"),
                         Integer(3))

    def test_add(self):
        self.assertEqual(monte_eval("([1, 2].diverge() + [3, 4].diverge()).snapshot() == [1, 2, 3, 4]"),
                         true)

    def test_contains(self):
        self.assertEqual(monte_eval("[1, 2, 3].diverge().contains(2)"),
                         true)
        self.assertEqual(monte_eval("[1, 2, 3].diverge().contains(4)"),
                         false)

    def test_sort(self):
        self.assertEqual(monte_eval(
            "[4, 9, 1, 2, 3].diverge().sort() == [1, 2, 3, 4, 9]"),
                         true)

    def test_sortInPlace(self):
        self.assertEqual(monte_eval(
            "def x := [4, 9, 1, 2, 3].diverge(); x.sortInPlace(); x.snapshot() == [1, 2, 3, 4, 9]"),
                         true)

    def test_fetch(self):
        self.assertEqual(monte_eval(
            "[4, 9, 1].diverge().fetch(0, fn {99}) == 4"),
                         true)
        self.assertEqual(monte_eval(
            "[4, 9, 1].diverge().fetch(3, fn {99}) == 99"),
                         true)

    def test_last(self):
        self.assertEqual(monte_eval(
            "[4, 9, 1, 13].diverge().last()"),
                         Integer(13))

    def test_with(self):
        self.assertEqual(monte_eval(
            "[4, 9, 1, 13].diverge().with(11) == [4, 9, 1, 13, 11]"),
                         true)
        self.assertEqual(monte_eval(
            "[4, 9, 1, 13].diverge().with(1, 11) == [4, 11, 9, 1, 13]"),
            true)

    def test_multiply(self):
        self.assertEqual(monte_eval(
            "[4].diverge() * 3 == [4, 4, 4]"),
                        true)

    def test_asMap(self):
        self.assertEqual(monte_eval(
            "[4, 9, 1, 13].diverge().asMap() == [0 => 4, 1 => 9, 2 => 1, 3 => 13]"),
                         true)

    def test_asKeys(self):
        self.assertEqual(monte_eval(
            "[4, 9, 1, 13].diverge().asKeys() == [4 => null, 9 => null, 1 => null, 13 => null]"),
                         true)

    def test_slice(self):
        self.assertEqual(monte_eval(
            "[4, 9, 1, 13].diverge().slice(1) == [9, 1, 13]"),
                         true)
        self.assertEqual(monte_eval(
            "[4, 9, 1, 13].diverge().slice(0, 2) == [4, 9]"),
                         true)

    def test_push(self):
        self.assertEqual(monte_eval(
            "def x := [1].diverge(); x.push(3); x.snapshot() == [1, 3]"),
                        true)

    def test_pop(self):
        self.assertEqual(monte_eval(
            "def x := [1, 3].diverge(); def y := x.pop(); [x.snapshot(), y] == [[1], 3]"),
                        true)

    def test_setSlice(self):
        self.assertEqual(monte_eval(
            "def x := [1, 4, 3].diverge(); x.setSlice(1, 3, [7, 8]); x.snapshot() == [1, 7, 8]"),
                        true)

    def test_removeSlice(self):
        self.assertEqual(monte_eval(
            "def x := [1, 4, 2, 3].diverge(); x.removeSlice(1, 3); x.snapshot() == [1, 3]"),
                        true)

    def test_insert(self):
        self.assertEqual(monte_eval(
            "def x := [1, 4, 3].diverge(); x.insert(2, 9); x.snapshot() == [1, 4, 9, 3]"),
                        true)

    def test_put(self):
        self.assertEqual(monte_eval(
            "def x := [1, 4, 3].diverge(); x[1] := 5; x.snapshot() == [1, 5, 3]"),
                        true)

    def test_valueGuard(self):
        self.assertRaises(
            RuntimeError,
            monte_eval,
            "def x := [1, 4, 3, 'b'].diverge(int)")

        self.assertEqual(monte_eval(
            "def x := [1, 4, 3].diverge(int); x[1] := 5; x.snapshot() == [1, 5, 3]"),
                         true)

        self.assertEqual(monte_eval(
            "def x := [1, 4, 3].diverge(int); x.push(5); x.snapshot() == [1, 4, 3, 5]"),
                         true)

        self.assertRaises(
            RuntimeError,
            monte_eval,
            "def x := [1, 4, 3].diverge(int); x[1] := 'b'")

        self.assertRaises(
            RuntimeError,
            monte_eval,
            "def x := [1, 4, 3].diverge(int); x.push('b')")


class ConstMapTests(unittest.TestCase):
    def test_get(self):
        self.assertEqual(monte_eval(
            "def x := [1 => 3, 4 => 7]; x[4]"), Integer(7))

    def test_print(self):
        self.assertEqual(monte_eval(
            "def x := [1 => 3, 4 => 7]; M.toString(x)"),
                         String(u'[1 => 3, 4 => 7]'))

    def test_fetch(self):
        self.assertEqual(monte_eval(
            "def x := [1 => 3, 4 => 7]; x.fetch(4, fn {99})"), Integer(7))
        self.assertEqual(monte_eval(
            "def x := [1 => 3, 4 => 7]; x.fetch(3, fn {99})"), Integer(99))

    def test_size(self):
        self.assertEqual(monte_eval(
            "def x := [1 => 3, 4 => 7]; x.size()"), Integer(2))

    def test_or(self):
        self.assertEqual(monte_eval(
            "def x := [1 => 3, 4 => 7] | [4 => 6, 2 => 'b']; x == [4 => 7, 2 => 'b', 1 => 3]"),
                         true)

    def test_and(self):
        self.assertEqual(monte_eval(
            "def x := [1 => 3, 4 => 7] & [4 => 6, 2 => 'b']; x == [4 => 7]"),
                         true)

    def test_butNot(self):
        self.assertEqual(monte_eval(
            "def x := [1 => 3, 4 => 7] &! [4 => 6, 2 => 'b']; x == [1 => 3]"),
                         true)

    def test_maps(self):
        self.assertEqual(monte_eval(
            "def x := [1 => 3, 4 => 7]; x.maps(4) && !x.maps(5)"),
                         true)

    def test_with(self):
        self.assertEqual(monte_eval(
                    "def x := [1 => 3, 4 => 7]; x.with(5, 2) == [1 => 3, 4 => 7, 5 => 2]"),
                         true)

    def test_without(self):
        self.assertEqual(monte_eval(
                    "def x := [1 => 3, 4 => 7, 5 => 2, 9 => 6]; x.without(4) == [1 => 3, 9 => 6, 5 => 2]"),
                         true)

    def test_getKeys(self):
        self.assertEqual(monte_eval(
                    "def x := [1 => 3, 4 => 7, 5 => 2, 9 => 6]; x.getKeys() == [1, 4, 5, 9]"),
                         true)

    def test_sortKeys(self):
        self.assertEqual(monte_eval(
                    "def x := [4 => 7, 1 => 3,  9 => 6, 5 => 2]; x.sortKeys() == [1 => 3, 4 => 7, 5 => 2, 9 => 6]"),
                         true)

    def test_getValues(self):
        self.assertEqual(monte_eval(
                    "def x := [1 => 3, 4 => 7, 5 => 2, 9 => 6]; x.getValues() == [3, 7, 2, 6]"),
                         true)

    def test_getPair(self):
        self.assertEqual(monte_eval(
                    "def x := [1 => 3, 4 => 7, 5 => 2, 9 => 6]; x.getPair() == [[1, 4, 5, 9], [3, 7, 2, 6]]"),
                         true)


class FlexMapTests(unittest.TestCase):
    def test_get(self):
        self.assertEqual(monte_eval(
            "def x := [1 => 3, 4 => 7].diverge(); x[4]"), Integer(7))

    def test_print(self):
        self.assertEqual(monte_eval(
            "def x := [1 => 3, 4 => 7].diverge(); M.toString(x)"),
                         String(u'[1 => 3, 4 => 7].diverge()'))

    def test_fetch(self):
        self.assertEqual(monte_eval(
            "def x := [1 => 3, 4 => 7].diverge(); x.fetch(4, fn {99})"), Integer(7))
        self.assertEqual(monte_eval(
            "def x := [1 => 3, 4 => 7].diverge(); x.fetch(3, fn {99})"), Integer(99))

    def test_size(self):
        self.assertEqual(monte_eval(
            "def x := [1 => 3, 4 => 7].diverge(); x.size()"), Integer(2))

    def test_or(self):
        self.assertEqual(monte_eval(
            "def x := [1 => 3, 4 => 7].diverge() | [4 => 6, 2 => 'b']; x == [4 => 7, 2 => 'b', 1 => 3]"),
                         true)

    def test_and(self):
        self.assertEqual(monte_eval(
            "def x := [1 => 3, 4 => 7].diverge() & [4 => 6, 2 => 'b']; x == [4 => 7]"),
                         true)

    def test_butNot(self):
        self.assertEqual(monte_eval(
            "def x := [1 => 3, 4 => 7].diverge() &! [4 => 6, 2 => 'b']; x == [1 => 3]"),
                         true)

    def test_maps(self):
        self.assertEqual(monte_eval(
            "def x := [1 => 3, 4 => 7].diverge(); x.maps(4) && !x.maps(5)"),
                         true)

    def test_with(self):
        self.assertEqual(monte_eval(
                    "def x := [1 => 3, 4 => 7].diverge(); x.with(5, 2) == [1 => 3, 4 => 7, 5 => 2]"),
                         true)

    def test_without(self):
        self.assertEqual(monte_eval(
                    "def x := [1 => 3, 4 => 7, 5 => 2, 9 => 6].diverge(); x.without(4) == [1 => 3, 9 => 6, 5 => 2]"),
                         true)

    def test_getKeys(self):
        self.assertEqual(monte_eval(
                    "def x := [1 => 3, 4 => 7, 5 => 2, 9 => 6].diverge(); x.getKeys() == [1, 4, 5, 9]"),
                         true)

    def test_sortKeys(self):
        self.assertEqual(monte_eval(
                    "def x := [4 => 7, 1 => 3,  9 => 6, 5 => 2].diverge(); x.sortKeys() == [1 => 3, 4 => 7, 5 => 2, 9 => 6]"),
                         true)

    def test_getValues(self):
        self.assertEqual(monte_eval(
                    "def x := [1 => 3, 4 => 7, 5 => 2, 9 => 6].diverge(); x.getValues() == [3, 7, 2, 6]"),
                         true)

    def test_getPair(self):
        self.assertEqual(monte_eval(
                    "def x := [1 => 3, 4 => 7, 5 => 2, 9 => 6].diverge(); x.getPair() == [[1, 4, 5, 9], [3, 7, 2, 6]]"),
                         true)


    def test_removeKey(self):
        self.assertEqual(monte_eval(
                    "def x := [1 => 3, 4 => 7, 5 => 2, 9 => 6].diverge(); x.removeKey(4); x.snapshot() == [1 => 3, 9 => 6, 5 => 2]"),
                         true)

    def test_removeKeys(self):
        self.assertEqual(monte_eval(
            "def x := [1 => 3, 4 => 7].diverge(); x.removeKeys([4 => 6, 2 => 'b']); x.snapshot() == [1 => 3]"),
                         true)

    def test_put(self):
        self.assertEqual(monte_eval(
            "def x := [1 => 3, 4 => 7].diverge(); x[2] := 5; x.snapshot() == [1 => 3, 4 => 7, 2 => 5]"),
                         true)
        self.assertEqual(monte_eval(
            "def x := [1 => 3, 4 => 7].diverge(); x[1] := 5; x.snapshot() == [1 => 5, 4 => 7]"),
                         true)

    def test_putAll(self):
        self.assertEqual(monte_eval(
            "def x := [1 => 3, 4 => 7].diverge() ; x.putAll([4 => 6, 2 => 'b']); x.snapshot() == [ 1 => 3, 4 => 6, 2 => 'b']"),
                         true)

    def test_valueGuard(self):
        self.assertRaises(
            RuntimeError,
            monte_eval,
            "def x := [1 => 4, 3 => 'b'].diverge(int, char)")

        self.assertRaises(
            RuntimeError,
            monte_eval,
            "def x := [3.5 => 'a', 3 => 'b'].diverge(int, char)")

        self.assertEqual(monte_eval(
            "def x := [4 => 'a', 3 => 'b'].diverge(int, char); x[5] := 'c'; x.snapshot() == [4 => 'a', 3 => 'b', 5 => 'c']"),
                         true)

        self.assertRaises(
            RuntimeError,
            monte_eval,
            "def x := [4 => 'a', 3 => 'b'].diverge(int, char); x[4.5] := 'c'")

        self.assertRaises(
            RuntimeError,
            monte_eval,
            "def x := [4 => 'a', 3 => 'b'].diverge(int, char); x[5] := 9")


class ListGuardTests(unittest.TestCase):
    def test_plainConst(self):
        self.assertEqual(monte_eval(
            "escape e {def x :List exit e := [1 => 2]; 1} catch v {2}"),
                         Integer(2))
        self.assertEqual(monte_eval(
            "escape e {def x :List exit e := [3, 4]; 1} catch v {2}"),
                         Integer(1))

    def test_guardConst(self):
        self.assertEqual(monte_eval(
            "escape e {def x :List[int] exit e := [1 => 2]; 1} catch v {2}"),
                         Integer(2))
        self.assertEqual(monte_eval(
            "escape e {def x :List[int] exit e := [3, 'b']; 1} catch v {2}"),
                         Integer(2))
        self.assertEqual(monte_eval(
            "escape e {def x :List[int] exit e := [3, 4]; 1} catch v {2}"),
                         Integer(1))

    def test_var(self):
        self.assertEqual(monte_eval(
            "escape e {def x :List exit e := [3, 'b'].diverge(); 1} catch v {2}"),
                         Integer(2))
        self.assertEqual(monte_eval(
            "escape e {def x :List[int] exit e := [3, 4].diverge(); 1} catch v {2}"),
                         Integer(2))


class MapGuardTests(unittest.TestCase):
    def test_plainConst(self):
        self.assertEqual(monte_eval(
            "escape e {def x :Map exit e := [1 => 2]; 1} catch v {2}"),
                         Integer(1))
        self.assertEqual(monte_eval(
            "escape e {def x :Map exit e := [3, 4]; 1} catch v {2}"),
                         Integer(2))

    def test_guardConst(self):
        self.assertEqual(monte_eval(
            "escape e {def x :Map[int, char] exit e := [1 => 'b', 2 => 'x']; 1} catch v {2}"),
                         Integer(1))
        self.assertEqual(monte_eval(
            "escape e {def x :Map[int, char] exit e := [1 => 2, 3 => 'x']; 1} catch v {2}"),
                         Integer(2))
        self.assertEqual(monte_eval(
            "escape e {def x :Map[int, char] exit e := ['a' => 'b']; 1} catch v {2}"),
                         Integer(2))
        self.assertEqual(monte_eval(
            "escape e {def x :Map[int, char] exit e := 3; 1} catch v {2}"),
                         Integer(2))

    def test_var(self):
        self.assertEqual(monte_eval(
            "escape e {def x :Map exit e := [3 => 'b'].diverge(); 1} catch v {2}"),
                         Integer(2))
        self.assertEqual(monte_eval(
            "escape e {def x :Map[int, char] exit e := [3 => 'b'].diverge(); 1} catch v {2}"),
                         Integer(2))


class DeepFrozenGuardTests(unittest.TestCase):
    def test_prims(self):
        self.assertEqual(monte_eval("true =~ _ :DeepFrozen"), true)
        self.assertEqual(monte_eval("null =~ _ :DeepFrozen"), true)
        self.assertEqual(monte_eval("1 =~ _ :DeepFrozen"), true)
        self.assertEqual(monte_eval("3.5 =~ _ :DeepFrozen"), true)
        self.assertEqual(monte_eval("'a' =~ _ :DeepFrozen"), true)
        self.assertEqual(monte_eval('"bob" =~ _ :DeepFrozen'), true)

    def test_tables(self):
        self.assertEqual(monte_eval("[1] =~ _ :DeepFrozen"), true)
        self.assertEqual(monte_eval("[1].diverge() =~ _ :DeepFrozen"), false)
        self.assertEqual(monte_eval("[1 => 'a'] =~ _ :DeepFrozen"), true)
        self.assertEqual(monte_eval("[1 => 'a'].diverge() =~ _ :DeepFrozen"), false)

    def test_audited(self):
        self.assertEqual(monte_eval('object _ {} =~ _ :DeepFrozen'), false)
        self.assertEqual(monte_eval('object _ implements DeepFrozen {} =~ _ :DeepFrozen'), true)
        self.assertEqual(monte_eval(dedent("""
            var w := 0
            def x := 1
            def y :int := 1
            object foo implements DeepFrozen:
                to doStuff(z):
                    return y + z
                to doOther():
                    var a := null
                    return a
            foo =~ _ :DeepFrozen
            """)), true)
        self.assertEqual(monte_eval(dedent("""
            object baz as DeepFrozen {}
            object foo implements DeepFrozen:
                to doStuff(z):
                    return baz
            foo =~ _ :DeepFrozen
            """)), true)


    def test_rejected(self):
        self.assertRaises(
            RuntimeError,
            monte_eval,
            dedent("""
            var x :int := 0
            def y :int := 1
            object foo implements DeepFrozen:
                to doStuff(z):
                    return x + y
            """))

        self.assertRaises(
            RuntimeError,
            monte_eval,
            dedent("""
            interface Blee:
                pass
            object y as Blee {}
            object foo implements DeepFrozen:
                to doStuff(z):
                    y.push(z)
                    return y.pull()
            """))

        self.assertRaises(
            RuntimeError,
            monte_eval,
            dedent("""
            object baz implements DeepFrozen {}
            object foo implements DeepFrozen:
                to doStuff(z):
                    return baz
            """))


class IntegerGuardTests(unittest.TestCase):

    def test_type(self):
        monte_eval('def x :int := 1')
        self.assertRaises(RuntimeError, monte_eval, 'def x :int := "foo"')

    def test_lt(self):
        monte_eval('def x :(int < 5) := 1')
        self.assertRaises(RuntimeError, monte_eval, 'def x :(int < 5) := 10')

    def test_gt(self):
        monte_eval('def x :(int > 5) := 10')
        self.assertRaises(RuntimeError, monte_eval, 'def x :(int > 5) := 1')

    def test_gte(self):
        monte_eval('def x :(int >= 0) := 1')
        monte_eval('def x :(int >= 0) := 0')
        self.assertRaises(RuntimeError, monte_eval, 'def x :(int >= 0) := -1')

    def test_lte(self):
        monte_eval('def x :(int <= 9000) := 50')
        monte_eval('def x :(int <= 9000) := 9000')
        self.assertRaises(RuntimeError, monte_eval,
                          'def x :(int <= 9000) := 9001')

    def test_backwards(self):
        monte_eval('def x :(0 <= int) := 1')
        self.assertRaises(RuntimeError, monte_eval, 'def x :(0 <= int) := -1')

    def test_compound_fails(self):
        self.assertRaises(RuntimeError, monte_eval, '0 <= int <= 1')


class FloatGuardTests(unittest.TestCase):

    def test_type(self):
        monte_eval('def x :float := 1.0')
        self.assertRaises(RuntimeError, monte_eval, 'def x :float := "foo"')

    def test_lt(self):
        monte_eval('def x :(float < 5.0) := 1.0')
        self.assertRaises(RuntimeError, monte_eval,
                          'def x :(float < 5.0) := 10.0')

    def test_gt(self):
        monte_eval('def x :(float > 5.0) := 10.0')
        self.assertRaises(RuntimeError, monte_eval,
                          'def x :(float > 5.0) := 1.0')

    def test_gte(self):
        monte_eval('def x :(float >= 0.0) := 1.0')
        self.assertRaises(RuntimeError, monte_eval,
                          'def x :(float >= 0.0) := -1.0')

    def test_lte(self):
        monte_eval('def x :(float <= 9000.0) := 50.0')
        self.assertRaises(RuntimeError, monte_eval,
                          'def x :(float <= 9000.0) := 9001.0')

    def test_backwards(self):
        monte_eval('def x :(0.0 <= float) := 1.0')
        self.assertRaises(RuntimeError, monte_eval,
                          'def x :(1.0 <= float) := 0.5')

    def test_compound_fails(self):
        self.assertRaises(RuntimeError, monte_eval, '0.0 <= float <= 1.0')

    def test_integer_coercion(self):
        monte_eval('def x :(float < 1) := 0.5')
        self.assertRaises(RuntimeError, monte_eval,
                          'def x :(float < 1) := 2.0')


class StringTests(unittest.TestCase):

    def test_slice(self):
        self.assertEqual(monte_eval(dedent("""
            def x := "abcd"
            x.slice(1) == "bcd"
            """)), true)

class RefTests(unittest.TestCase):
    def test_print(self):
        self.assertEqual(repr(monte_eval("Ref.promise()[0]")), "<m: <Promise>>")

    def test_resolve(self):
        self.assertEqual(monte_eval(dedent("""
            def [p, r] := Ref.promise()
            r.resolve(3)
            p == 3
            """)), true)
