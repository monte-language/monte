
# custom-guards

unittest([
    
])


# design

unittest([
    
])


# faq

unittest([
    
])


# guards

unittest([
    
])


# index

unittest([
    
])


# interfaces

unittest([
    
])


# intro

def testintro_0(assert):
    object example:
        method test():
            "doc"
            1 + 1
            

    assert.equal(example.test(), 2)


def testintro_1(assert):
    object example:
        method test():
            "doc"
            "abc".size()
            

    assert.equal(example.test(), 3)


unittest([
    testintro_0,
    testintro_1
])


# iteration

def testiteration_0(assert):
    object example:
        method test():
            "doc"
            object helloThere:
                to greet(whom):
                    return `Hello, my dear $whom!`
            
            helloThere.greet("Student")
            

    assert.equal(example.test(), "Hello, my dear Student!")


def testiteration_1(assert):
    object example:
        method test():
            "doc"
            def makeSalutation(time):
                return object helloThere:
                    to greet(whom):
                        return `Good $time, my dear $whom!`
            
            def hi := makeSalutation("morning")
            
            hi.greet("Student")
            

    assert.equal(example.test(), "Good morning, my dear Student!")


unittest([
    testiteration_0,
    testiteration_1
])


# miranda

unittest([
    
])


# modules

unittest([
    
])


# montefesto

unittest([
    
])


# operators

def testoperators_0(assert):
    object example:
        method test():
            "doc"
            { var v := 6; v := 12; v - 4 }
            

    assert.equal(example.test(), 8)


def testoperators_1(assert):
    object example:
        method test():
            "doc"
            { def [x, y] := [1, 2]; x }
            

    assert.equal(example.test(), 1)


def testoperators_2(assert):
    object example:
        method test():
            "doc"
            { def x := 2; def result := x.add(3) }
            

    assert.equal(example.test(), 5)


def testoperators_3(assert):
    object example:
        method test():
            "doc"
            { def x; def prom := x<-message(3); null }
            

    assert.equal(example.test(), null)


def testoperators_4(assert):
    object example:
        method test():
            "doc"
            m`f(x)`.expand()
            

    assert.equal(example.test().canonical(), m`f.run(x)`.canonical())


def testoperators_5(assert):
    object example:
        method test():
            "doc"
            { object parity { to get(n) { return n % 2 }}; parity[3] }
            

    assert.equal(example.test(), 1)


def testoperators_6(assert):
    object example:
        method test():
            "doc"
            { def x := 2; def xplus := x.add; xplus(4) }
            

    assert.equal(example.test(), 6)


def testoperators_7(assert):
    object example:
        method test():
            "doc"
            3 < 2
            

    assert.equal(example.test(), false)


def testoperators_8(assert):
    object example:
        method test():
            "doc"
            3 > 2
            

    assert.equal(example.test(), true)


def testoperators_9(assert):
    object example:
        method test():
            "doc"
            3 < 3
            

    assert.equal(example.test(), false)


def testoperators_10(assert):
    object example:
        method test():
            "doc"
            3 <= 3
            

    assert.equal(example.test(), true)


def testoperators_11(assert):
    object example:
        method test():
            "doc"
            m`x == y`.expand()
            

    assert.equal(example.test().canonical(), m`__equalizer.sameEver(x, y)`.canonical())


def testoperators_12(assert):
    object example:
        method test():
            "doc"
            m`3 < 2`.expand()
            

    assert.equal(example.test().canonical(), m`_comparer.lessThan(3, 2)`.canonical())


def testoperators_13(assert):
    object example:
        method test():
            "doc"
            3 == "3"
            

    assert.equal(example.test(), false)


def testoperators_14(assert):
    object example:
        method test():
            "doc"
            1 + 1 == 2.0
            

    assert.equal(example.test(), false)


def testoperators_15(assert):
    object example:
        method test():
            "doc"
            2.0 <=> 1 + 1
            

    assert.equal(example.test(), true)


def testoperators_16(assert):
    object example:
        method test():
            "doc"
            2 + 1 <=> 3.0
            

    assert.equal(example.test(), true)


def testoperators_17(assert):
    object example:
        method test():
            "doc"
            m`2.0 <=> 1 + 1`.expand()
            

    assert.equal(example.test().canonical(), m`_comparer.asBigAs(2.000000, 1.add(1))`.canonical())


def testoperators_18(assert):
    object example:
        method test():
            "doc"
            [1, 2] =~ [a, b]
            

    assert.equal(example.test(), true)


def testoperators_19(assert):
    object example:
        method test():
            "doc"
            [1, "x"] =~ [_ :Int, _ :Str]
            

    assert.equal(example.test(), true)


def testoperators_20(assert):
    object example:
        method test():
            "doc"
            "abc" =~ `a@rest`
            

    assert.equal(example.test(), true)


def testoperators_21(assert):
    object example:
        method test():
            "doc"
            "xbc" =~ `a@rest`
            

    assert.equal(example.test(), false)


def testoperators_22(assert):
    object example:
        method test():
            "doc"
            "xbc" !~ `a@rest`
            

    assert.equal(example.test(), true)


def testoperators_23(assert):
    object example:
        method test():
            "doc"
            { def i := 3; if (i % 2 == 0) { "yes" } else { "no" } }
            

    assert.equal(example.test(), "no")


def testoperators_24(assert):
    object example:
        method test():
            "doc"
            true && true
            

    assert.equal(example.test(), true)


def testoperators_25(assert):
    object example:
        method test():
            "doc"
            true &! false
            

    assert.equal(example.test(), true)


def testoperators_26(assert):
    object example:
        method test():
            "doc"
            m`x &! y`.expand()
            

    assert.equal(example.test().canonical(), m`x.butNot(y)`.canonical())


def testoperators_27(assert):
    object example:
        method test():
            "doc"
            2 ** 3
            

    assert.equal(example.test(), 8)


def testoperators_28(assert):
    object example:
        method test():
            "doc"
            2 * 3
            

    assert.equal(example.test(), 6)


def testoperators_29(assert):
    object example:
        method test():
            "doc"
            [for x in (1..!4) x * 2]
            

    assert.equal(example.test(), [2, 4, 6])


def testoperators_30(assert):
    object example:
        method test():
            "doc"
            1..4
            

    assert.equal(example.test(), 1..!5)


def testoperators_31(assert):
    object example:
        method test():
            "doc"
            [for x in (1..4) x * 2]
            

    assert.equal(example.test(), [2, 4, 6, 8])


def testoperators_32(assert):
    object example:
        method test():
            "doc"
            { var x := "augmenting "; x += "addition!"; x }
            

    assert.equal(example.test(), "augmenting addition!")


def testoperators_33(assert):
    object example:
        method test():
            "doc"
            { var x := "augmenting "; x := x.add("addition!") }
            

    assert.equal(example.test(), "augmenting addition!")


def testoperators_34(assert):
    object example:
        method test():
            "doc"
            { var l := []; for i in 1..10 { l with= (i) }; l }
            

    assert.equal(example.test(), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])


def testoperators_35(assert):
    object example:
        method test():
            "doc"
            { var x := 7; x modPow= (129, 3) }
            

    assert.equal(example.test(), 1)


def testoperators_36(assert):
    object example:
        method test():
            "doc"
            { 4; "x"; "y" }
            

    assert.equal(example.test(), "y")


def testoperators_37(assert):
    object example:
        method test():
            "doc"
            4 + 2 * 3
            

    assert.equal(example.test(), 10)


def testoperators_38(assert):
    object example:
        method test():
            "doc"
            (4 + 2) * 3
            

    assert.equal(example.test(), 18)


def testoperators_39(assert):
    object example:
        method test():
            "doc"
            Int
            

    assert.equal(example.test(), Int)


def testoperators_40(assert):
    object example:
        method test():
            "doc"
            { def ::"hello, world" := 1; ::"hello, world" }
            

    assert.equal(example.test(), 1)


def testoperators_41(assert):
    object example:
        method test():
            "doc"
            - (1 + 3)
            

    assert.equal(example.test(), -4)


def testoperators_42(assert):
    object example:
        method test():
            "doc"
            ~ 0xff
            

    assert.equal(example.test(), -256)


def testoperators_43(assert):
    object example:
        method test():
            "doc"
            ! true
            

    assert.equal(example.test(), false)


def testoperators_44(assert):
    object example:
        method test():
            "doc"
            1 :Int
            

    assert.equal(example.test(), 1)


unittest([
    testoperators_0,
    testoperators_1,
    testoperators_2,
    testoperators_3,
    testoperators_4,
    testoperators_5,
    testoperators_6,
    testoperators_7,
    testoperators_8,
    testoperators_9,
    testoperators_10,
    testoperators_11,
    testoperators_12,
    testoperators_13,
    testoperators_14,
    testoperators_15,
    testoperators_16,
    testoperators_17,
    testoperators_18,
    testoperators_19,
    testoperators_20,
    testoperators_21,
    testoperators_22,
    testoperators_23,
    testoperators_24,
    testoperators_25,
    testoperators_26,
    testoperators_27,
    testoperators_28,
    testoperators_29,
    testoperators_30,
    testoperators_31,
    testoperators_32,
    testoperators_33,
    testoperators_34,
    testoperators_35,
    testoperators_36,
    testoperators_37,
    testoperators_38,
    testoperators_39,
    testoperators_40,
    testoperators_41,
    testoperators_42,
    testoperators_43,
    testoperators_44
])


# patterns

def testpatterns_0(assert):
    object example:
        method test():
            "doc"
            m`def bind x := 2`.expand()
            

    assert.equal(example.test().canonical(), m`def via (_bind.run(x_Resolver, null)) _ := 2`.canonical())


def testpatterns_1(assert):
    object example:
        method test():
            "doc"
            m`def &x := 1`.expand()
            

    assert.equal(example.test().canonical(), m`def via (__slotToBinding) &&x := 1`.canonical())


unittest([
    testpatterns_0,
    testpatterns_1
])


# quasiparsers

unittest([
    
])


# symbols

def testsymbols_0(assert):
    object example:
        method test():
            "doc"
            5
            

    assert.equal(example.test(), 5)


def testsymbols_1(assert):
    object example:
        method test():
            "doc"
            0xF
            

    assert.equal(example.test(), 15)


def testsymbols_2(assert):
    object example:
        method test():
            "doc"
            128 ** 20
            

    assert.equal(example.test(), 1393796574908163946345982392040522594123776)


def testsymbols_3(assert):
    object example:
        method test():
            "doc"
            5 + 2
            

    assert.equal(example.test(), 7)


def testsymbols_4(assert):
    object example:
        method test():
            "doc"
            def x :Double := 1.0
            

    assert.equal(example.test(), 1.000000)


def testsymbols_5(assert):
    object example:
        method test():
            "doc"
            4.0.floor()
            

    assert.equal(example.test(), 4)


def testsymbols_6(assert):
    object example:
        method test():
            "doc"
            4 * 1.0
            

    assert.equal(example.test(), 4.000000)


def testsymbols_7(assert):
    object example:
        method test():
            "doc"
            false || true
            

    assert.equal(example.test(), true)


def testsymbols_8(assert):
    object example:
        method test():
            "doc"
            {((1 =~ x) || (2 =~ x)); x}
            

    assert.equal(example.test(), 1)


def testsymbols_9(assert):
    object example:
        method test():
            "doc"
            {((1 =~ [x, y]) || (2 =~ x)); x}
            

    assert.equal(example.test(), 2)


def testsymbols_10(assert):
    object example:
        method test():
            "doc"
            false && true
            

    assert.equal(example.test(), false)


def testsymbols_11(assert):
    object example:
        method test():
            "doc"
            false == true
            

    assert.equal(example.test(), false)


def testsymbols_12(assert):
    object example:
        method test():
            "doc"
            false != true
            

    assert.equal(example.test(), true)


def testsymbols_13(assert):
    object example:
        method test():
            "doc"
            false & true
            

    assert.equal(example.test(), false)


def testsymbols_14(assert):
    object example:
        method test():
            "doc"
            false | true
            

    assert.equal(example.test(), true)


def testsymbols_15(assert):
    object example:
        method test():
            "doc"
            false ^ true
            

    assert.equal(example.test(), true)


def testsymbols_16(assert):
    object example:
        method test():
            "doc"
            ! false
            

    assert.equal(example.test(), true)


def testsymbols_17(assert):
    object example:
        method test():
            "doc"
            m`! false`.expand()
            

    assert.equal(example.test().canonical(), m`false.not()`.canonical())


def testsymbols_18(assert):
    object example:
        method test():
            "doc"
            m`false & true`.expand()
            

    assert.equal(example.test().canonical(), m`false.and(true)`.canonical())


def testsymbols_19(assert):
    object example:
        method test():
            "doc"
            '☃'
            

    assert.equal(example.test(), '☃')


def testsymbols_20(assert):
    object example:
        method test():
            "doc"
            '\u23b6'
            

    assert.equal(example.test(), '⎶')


def testsymbols_21(assert):
    object example:
        method test():
            "doc"
            "Hello World!".replace("World", "Monte hackers")
            

    assert.equal(example.test(), "Hello Monte hackers!")


def testsymbols_22(assert):
    object example:
        method test():
            "doc"
            "¿Dónde aquí habla Monte o español?".size()
            

    assert.equal(example.test(), 34)


def testsymbols_23(assert):
    object example:
        method test():
            "doc"
            ['I', "love", "Monte", 42, 0.5][3]
            

    assert.equal(example.test(), 42)


def testsymbols_24(assert):
    object example:
        method test():
            "doc"
            { def l := ['I', "love", "Monte", 42, 0.5].diverge(); l[3] := 0 }
            

    assert.equal(example.test(), 0)


def testsymbols_25(assert):
    object example:
        method test():
            "doc"
            { def m := ["roses" => "red", "violets" => "blue"]; m["roses"] }
            

    assert.equal(example.test(), "red")


def testsymbols_26(assert):
    object example:
        method test():
            "doc"
            { def m := ["roses" => "red", "violets" => "blue"].diverge(); m["roses"] := 3 }
            

    assert.equal(example.test(), 3)


def testsymbols_27(assert):
    object example:
        method test():
            "doc"
            [ "a" => 1, "b" => 2] == [ "b" => 2, "a" => 1]
            

    assert.equal(example.test(), false)


def testsymbols_28(assert):
    object example:
        method test():
            "doc"
            [ "a" => 1, "b" => 2].sortKeys() == [ "b" => 2, "a" => 1].sortKeys()
            

    assert.equal(example.test(), true)


unittest([
    testsymbols_0,
    testsymbols_1,
    testsymbols_2,
    testsymbols_3,
    testsymbols_4,
    testsymbols_5,
    testsymbols_6,
    testsymbols_7,
    testsymbols_8,
    testsymbols_9,
    testsymbols_10,
    testsymbols_11,
    testsymbols_12,
    testsymbols_13,
    testsymbols_14,
    testsymbols_15,
    testsymbols_16,
    testsymbols_17,
    testsymbols_18,
    testsymbols_19,
    testsymbols_20,
    testsymbols_21,
    testsymbols_22,
    testsymbols_23,
    testsymbols_24,
    testsymbols_25,
    testsymbols_26,
    testsymbols_27,
    testsymbols_28
])


# tools

unittest([
    
])


# tubes

unittest([
    
])


# wizard

def testwizard_0(assert):
    object example:
        method test():
            "doc"
            def f(x) { def y := x * x; return y }
            f(4)
            

    assert.equal(example.test(), 16)


def testwizard_1(assert):
    object example:
        method test():
            "doc"
            def f(x):
                def y := x * x
                return y
            f(5)
            

    assert.equal(example.test(), 25)


def testwizard_2(assert):
    object example:
        method test():
            "doc"
            m`1 + 1`.expand()
            

    assert.equal(example.test().canonical(), m`1.add(1)`.canonical())


unittest([
    testwizard_0,
    testwizard_1,
    testwizard_2
])

