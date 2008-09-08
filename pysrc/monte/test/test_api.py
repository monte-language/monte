"""
Tests for the E/Python bridge.
"""
from twisted.trial import unittest
from monte import api

class EvalTest(unittest.TestCase):
    """
    Tests for evaluation of code.
    """

    def assertEvaluatesTo(self, expr, result):
        """
        Evaluate an E expression and compare the returned value to the given
        string.
        """
        [res, newScope] = api.eval(expr, api.e_privilegedScope)
        self.assertEqual(res.strip(), result)


    def test_scopeExtension(self):
        """
        C{eval} places new bindings into the scope it returns.
        """
        [res, newScope] = api.eval("def x := 1+1", api.e_privilegedScope)
        self.assertEqual(res.strip(), "2")
        [nextRes, nextScope] = api.eval("2 + x", newScope)
        self.assertEqual(nextRes.strip(), "4")


    def test_expression0(self):
       self.assertEvaluatesTo("1 + 1", "2")


    def test_expression1(self):
       self.assertEvaluatesTo("1 == 1", "true")


    def test_expression2(self):
       self.assertEvaluatesTo("def f(x) { return x + 1}; f(1)", "2")


    def test_expression3(self):
       self.assertEvaluatesTo("def f(a, b, c, d) { return c}; f(3, 1, 7, 9)", "7")


    def test_expression4(self):
       self.assertEvaluatesTo("var x := 0; def f(y) {x := y}; f(3); x", "3")


    def test_expression5(self):
       self.assertEvaluatesTo("var x := 0; def f(y) {x := __return}; f(3); x(1)", "Failed: ejector must be enabled")


    def test_expression6(self):
       self.assertEvaluatesTo('try { 1; throw ("oh no")} catch p { "done"}',
                              "done")


    def test_expression7(self):
       self.assertEvaluatesTo('try { 1; throw("oh no")} catch p {p}', "oh no")


    def test_expression8(self):
       self.assertEvaluatesTo('escape e1 { escape e2 { e1("yes") }}', "yes")


    def test_expression9(self):
       self.assertEvaluatesTo("escape e { try { 2 } finally { 1 } }", "2")


    def test_expression10(self):
       self.assertEvaluatesTo("def g(e, y) {e(y) + 1}; def f(x) { g(x, 2); return 4}; escape e {f(e); 3}", "2")


    def test_expression11(self):
       self.assertEvaluatesTo("var i := 0; while (i < 3) { i += 1}; i", "3")


    def test_expression12(self):
       self.assertEvaluatesTo("[1,2][1]", "2")


    def test_expression13(self):
       self.assertEvaluatesTo("def [a, b] := [1, 2]; a", "1")


    def test_expression14(self):
       self.assertEvaluatesTo("[3 => 4, 'a' => 2]['a']", "2")


    def test_expression15(self):
       self.assertEvaluatesTo("require(true)", "null")


    def test_expression16(self):
       self.assertEvaluatesTo("require(false)", "required condition failed")


    def test_expression17(self):
       self.assertEvaluatesTo('require(false, "oh no")', "oh no")


    def test_expression18(self):
       self.assertEvaluatesTo("var x := 0; for i in 1..10 { x += i }; x", "55")


    def test_expression19(self):
       self.assertEvaluatesTo("var x := 0; for i in 1..!11 { x += i }; x", "55")


    def test_expression20(self):
       self.assertEvaluatesTo("var x := 0; for i in 1..10 { x += 1; if (i == 4) { break;} }; x", "4")


    def test_expression21(self):
       self.assertEvaluatesTo("var x := 0; for i in (1..10).descending() { x += 1; if (i == 4) { break;} }; x", "7")


    def test_expression22(self):
       self.assertEvaluatesTo("(1..10).op__cmp(1..10)", "0.0")


    def test_expression23(self):
       self.assertEvaluatesTo("(1..10).op__cmp(3..7)", "1.0")


    def test_expression24(self):
       self.assertEvaluatesTo("(1..10).op__cmp(1..20)", "-1.0")


    def test_expression25(self):
       self.assertEvaluatesTo("(1..10).op__cmp(-10..10)", "-1.0")


    def test_expression26(self):
       self.assertEvaluatesTo("(1..10).op__cmp(20..30)", "NaN")


    def test_expression27(self):
       self.assertEvaluatesTo("(1..10).getEdges()[1]", "11")


    def test_expression28(self):
       self.assertEvaluatesTo("def i :int := 1", "1")


    def test_expression29(self):
       self.assertEvaluatesTo("def c :char := 'a'", "'a'")


    def test_expression30(self):
       self.assertEvaluatesTo("def f :float64 := 1.0", "1.0")


    def test_expression31(self):
       self.assertEvaluatesTo('def s :String := "foo"', "foo")


    def test_expression32(self):
       self.assertEvaluatesTo("def _ :__Test := true", "true")


    def test_expression33(self):
       self.assertEvaluatesTo("def _ :__Test := false", "<problem condition was false: false>")


    def test_expression34(self):
       self.assertEvaluatesTo("def x; bind x := 1; x", "1")


    def test_expression35(self):
       self.assertEvaluatesTo("switch (1) {match ==2 {'a'} match ==1 {'c'}}", "'c'")


    def test_expression36(self):
       self.assertEvaluatesTo("def x := 1.add; x(5)", "6")


    def test_expression37(self):
       self.assertEvaluatesTo("def x ? true := 3", "3")


    def test_expression38(self):
       self.assertEvaluatesTo("def x ? false := 3", "<problem such-that expression was: false>")


    def test_expression39(self):
       self.assertEvaluatesTo("def x := [3].diverge(); x[0]", "3")


    def test_expression40(self):
       self.assertEvaluatesTo("def x := [].diverge(); x.push(3); x[0]", "3")


    def test_expression41(self):
       self.assertEvaluatesTo("def x := [3].diverge(); x.pop(); x.size()", "0")


    def test_expression42(self):
       self.assertEvaluatesTo("def x := [3].diverge(); def y := x.snapshot();  x.pop(); y[0]", "3")


    def test_expression43(self):
       self.assertEvaluatesTo('def x := [].asMap().diverge(); x["a"] := "b"; x["a"]', "b")


    def test_expression44(self):
       self.assertEvaluatesTo("[1, 2].contains(2)", "true")


    def test_expression45(self):
       self.assertEvaluatesTo("[1, 2].contains(3)", "false")


    def test_expression46(self):
       self.assertEvaluatesTo("[1, 7, 9].lastIndexOf1(7)", "1")


    def test_expression47(self):
       self.assertEvaluatesTo("[7, 7, 7, 9].lastIndexOf1(7)", "2")


    def test_expression48(self):
       self.assertEvaluatesTo("[1, 7, 9].lastIndexOf1(13)", "-1")


    def test_expression49(self):
       self.assertEvaluatesTo("[].asSet()", "[].asSet()")


    def test_expression50(self):
       self.assertEvaluatesTo("def x := [].asSet(); def y := x.with(3); y.size()", "1")


    def test_expression51(self):
       self.assertEvaluatesTo("def x := [3, 4].asSet(); x.with(3).getElements().size()", "2")


    def test_expression52(self):
       self.assertEvaluatesTo("var y := 0; for x in [1, 3, 6] { y += x }; y", "10")


    def test_expression53(self):
       self.assertEvaluatesTo("[1, 5, 7].last()", "7")


    def test_expression54(self):
       self.assertEvaluatesTo("def x := [1 => 9, 17 => 42].getKeys(); x[0] + x[1]", "18")


    def test_expression55(self):
       self.assertEvaluatesTo("def x := [1 => 9, 17 => 42].getValues(); x[0] + x[1]", "51")


    def test_expression56(self):
       self.assertEvaluatesTo("[1 => 2].maps(1)", "true")


    def test_expression57(self):
       self.assertEvaluatesTo("[1 => 2].maps(2)", "false")


    def test_expression58(self):
       self.assertEvaluatesTo("[1 => 2].fetch(1, 3)", "2")


    def test_expression59(self):
       self.assertEvaluatesTo("[1 => 2].fetch(2, 3)", "3")


    def test_expression60(self):
       self.assertEvaluatesTo("def x := [4 => 2, 1 => 17, 12 => 3, 8 => 1].sortKeys().getKeys(); x[0] == 1 && x[1] == 4 && x[2] == 8 && x[3] == 12", "true")


    def test_expression61(self):
       self.assertEvaluatesTo("def x := (2**34).toByteArray(); x.size() == 5 && x[0] == 4 && x[1] == 0 && x[2] == 0 && x[3] == 0 && x[4] == 0", "true")


    def test_expression62(self):
       self.assertEvaluatesTo("var x := 1; escape e { throw.eject(e, 2); x := 2} catch p { x := 3}; x", "3")


    def test_expression63(self):
       self.assertEvaluatesTo("safeScope.getScopeLayout().getSynEnv().size()", "90")


    def test_expression64(self):
       self.assertEvaluatesTo("def y := 1; def x := \"yes\"; `$x hooray $y`", "yes hooray 1")


    def test_expression65(self):
       self.assertEvaluatesTo('[1, \"bob\", 3]', '[1, "bob", 3]')


    def test_expression66(self):
       self.assertEvaluatesTo("[1 => 2, \"three\" => '4']", "[1 => 2, \"three\" => '4']")


    def test_expression67(self):
       self.assertEvaluatesTo("[]", "[]")


    def test_expression68(self):
       self.assertEvaluatesTo("[].asMap()", "[].asMap()")


    def test_expression69(self):
       self.assertEvaluatesTo("[1, 2].asSet()", "[1, 2].asSet()")


    def test_expression70(self):
       self.assertEvaluatesTo("[].asMap().with(1, 2)", "[1 => 2]")


    def test_expression71(self):
       self.assertEvaluatesTo('def foo {to five() {return 5}}; foo.__respondsTo("five", 0)', "true")


    def test_expression72(self):
       self.assertEvaluatesTo('def foo {}; foo.__respondsTo("__respondsTo", 2)', "true")


    def test_expression73(self):
       self.assertEvaluatesTo("def foo {to baz(x) { return x + 1} match [name, [x, y]] {x+y}}; foo.boz(3, 4)", "7")


    def test_expression74(self):
       self.assertEvaluatesTo("def foo {match [_, [x]] {x*x} match [_, [x, y]] {x + y}}; foo.boz(3)", "9")


    def test_expression75(self):
       self.assertEvaluatesTo("def foo {match [_, [x]] {x*x} match [_, [x, y]] {x + y}}; foo.boz(3, 4)", "7")


    def test_expression76(self):
       self.assertEvaluatesTo("def m := [1 => 2, 2 => 4]; def foo extends m {}; foo[1] + 2", "4")


    def test_expression77(self):
       self.assertEvaluatesTo("[1, 2] + [3, 4]", "[1, 2, 3, 4]")


    def test_expression78(self):
       self.assertEvaluatesTo("(3.141592653589793).toHexString()", "0x1.921fb54442d18p+1")


    def test_expression79(self):
       self.assertEvaluatesTo("def ten := 0..10; ten.coerce(9, null)", "9")


    def test_expression80(self):
       self.assertEvaluatesTo("def ten:= 0..10; ten.coerce(11, null)", "<problem Value not in region: 11>")


    def test_expression81(self):
       self.assertEvaluatesTo("__makeMap.fromColumns(['a', 'b', 'c'], [1, 2, 3])", "['a' => 1, 'b' => 2, 'c' => 3]")


    def test_expression82(self):
       self.assertEvaluatesTo("def x := [4, 7, 2, 9].diverge(); x.insert(2, 3); x", "[4, 7, 3, 2, 9].diverge()")


    def test_expression83(self):
       self.assertEvaluatesTo("[1, 2] == [1, 2]", "true")


    def test_expression84(self):
       self.assertEvaluatesTo("[1, [2, 3]] == [1, [2, 3]]", "true")


    def test_expression85(self):
       self.assertEvaluatesTo("def x; def y := [1, x]; bind x := 2; y == [1, 2]", "true")


    def test_expression86(self):
       self.assertEvaluatesTo("def x := [].diverge(); ['a' => 1, 'b' => 3].iterate(fn k, v { x.push(k); x.push(v) }); x.snapshot()", "['a', 1, 'b', 3]")


    def test_expression87(self):
       self.assertEvaluatesTo("\"abcdefg\".run(2, 5)", "cde")


    def test_expression88(self):
        #XXX need a way to virtualize stdout
       self.assertEvaluatesTo("stdout.indent(\"yay> \").println([1, 2])",
                              "null")

    def test_esendonly(self):
        """
        C{E.sendOnly} delivers a message to an object, eventually.
        """
        [res, newScope] = api.eval("def x := [].diverge()",
                                   api.e_privilegedScope)
        [res2, scope2] = api.eval('E.sendOnly(x, "push", [1])',
                                  newScope)
        [res3, scope3] = api.eval('x', scope2)
        self.assertEqual(res3.strip(), "[1].diverge()")


    def test_esend(self):
        """
        C{E.send} delivers a message to an object, eventually, and returns a
        promise which resolves to the result.
        """
        [res, newScope] = api.eval("def x := []",
                                   api.e_privilegedScope)
        [res2, scope2] = api.eval('def y := E.send(x, "with", [1])',
                                  newScope)
        [res3, scope3] = api.eval('y == [1]', scope2)
        self.assertEqual(res3.strip(), "true")
