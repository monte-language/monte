
import "unittest" =~ [=> unittest]
exports ()

def mockFileResource(path):
    var contents := b``
    return object fileResource:
        to setContents(bs :Bytes):
            contents := bs
        to getContents() :Bytes:
            def [p, r] := Ref.promise()
            r <- resolve(contents)
            return p


# auditors

unittest([
    
])


# block-expr

def testblock_expr_0(assert):
    object example:
        method test():
            "doc"
            if (2 < 3) { "expected" } else { "unexpected" }
            

    def actual := example.test()
    assert.equal(actual, "expected")


def testblock_expr_1(assert):
    object example:
        method test():
            "doc"
            def x := 5
            def y := 10
            if (x < y) { "less" } else if (x > y) { "greater" } else { "neither" }
            

    def actual := example.test()
    assert.equal(actual, "less")


def testblock_expr_2(assert):
    object example:
        method test():
            "doc"
            def state := "day"
            
            switch (state) {
                match =="day" {"night"}
                match =="night" {"day"}
            }
            

    def actual := example.test()
    assert.equal(actual, "night")


def testblock_expr_3(assert):
    object example:
        method test():
            "doc"
            m`switch (specimen) { match pat1 { expr1 } }`.expand()
            

    def actual := example.test().canonical()
    assert.equal(actual, m`{ def specimen_1 := specimen; escape ej_2 { def pat1 exit ej_2 := specimen_1; expr1 } catch failure_3 { _switchFailed.run(specimen_1, failure_3) } }`.canonical())


def testblock_expr_4(assert):
    object example:
        method test():
            "doc"
            try { 3 < "3" } catch _ { "ouch! no order defined" }
            

    def actual := example.test()
    assert.equal(actual, "ouch! no order defined")


def testblock_expr_5(assert):
    object example:
        method test():
            "doc"
            escape hatch { def x :Int exit hatch := 1.0 }
            

    def actual := example.test()
    assert.equal(actual, "1.000000 does not conform to <IntGuard>")


unittest([
    testblock_expr_0,
    testblock_expr_1,
    testblock_expr_2,
    testblock_expr_3,
    testblock_expr_4,
    testblock_expr_5
])


# brands

unittest([
    
])


# custom-guards

unittest([
    
])


# design

unittest([
    
])


# faq

unittest([
    
])


# glossary

unittest([
    
])


# guards

def testguards_0(assert):
    object example:
        method test():
            "doc"
            def x :Int := 1
            x
            

    def actual := example.test()
    assert.equal(actual, 1)


def testguards_1(assert):
    object example:
        method test():
            "doc"
            def halves(s) :Pair[Str, Str]:
                return s.split(",")
            halves("A,B")
            

    def actual := example.test()
    assert.equal(actual, ["A", "B"])


def testguards_2(assert):
    object example:
        method test():
            "doc"
            def y := -5
            escape oops {
                def x :(Int > 0) exit oops := y
            }
            

    def actual := example.test()
    assert.equal(actual, "-5 is not in <(0, ∞) <IntGuard> region>")


def testguards_3(assert):
    object example:
        method test():
            "doc"
            def x :('a'..'z' | 'A'..'Z') := 'c'
            def y :(Double >= 4.2) := 7.0
            def z :(Int < 5) := 3
            [x, y, z]
            

    def actual := example.test()
    assert.equal(actual, ['c', 7.0, 3])


def testguards_4(assert):
    object example:
        method test():
            "doc"
            def ints :List[Int] := [1, 2, 4, 6, 8]
            def setOfUppercaseChars :Set['A'..'Z'] := ['A', 'C', 'E', 'D', 'E', 'C', 'A', 'D', 'E'].asSet()
            def scores :Map[Str, Int] := ["Alice" => 10, "Bob" => 5]
            
            [ints.contains(4), setOfUppercaseChars.contains('B'), scores.contains("Bob")]
            

    def actual := example.test()
    assert.equal(actual, [true, false, true])


unittest([
    testguards_0,
    testguards_1,
    testguards_2,
    testguards_3,
    testguards_4
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
            

    def actual := example.test()
    assert.equal(actual, 2)


def testintro_1(assert):
    object example:
        method test():
            "doc"
            "abc".size()
            

    def actual := example.test()
    assert.equal(actual, 3)


unittest([
    testintro_0,
    testintro_1
])


# iteration

def testiteration_0(assert):
    object example:
        method test():
            "doc"
            for i => each in (["a", "b"]):
                traceln(`Index: $i Value: $each`)
            

    def actual := example.test()
    assert.equal(actual, null)


def testiteration_1(assert):
    object example:
        method test():
            "doc"
            { def i := 3; if (i % 2 == 0) { "yes" } else { "no" } }
            

    def actual := example.test()
    assert.equal(actual, "no")


def testiteration_2(assert):
    object example:
        method test():
            "doc"
            def evens := [for number in (1..10) if (number % 2 == 0) number]
            evens
            

    def actual := example.test()
    assert.equal(actual, [2, 4, 6, 8, 10])


unittest([
    testiteration_0,
    testiteration_1,
    testiteration_2
])


# miranda

unittest([
    
])


# modules

def testmodules_0(assert):
    object example:
        method test():
            "doc"
            m`1 + 1`.expand()
            

    def actual := example.test().canonical()
    assert.equal(actual, m`1.add(1)`.canonical())


unittest([
    testmodules_0
])


# montefesto

unittest([
    
])


# operators

def testoperators_0(assert):
    object example:
        method test():
            "doc"
            { 4; "x"; "y" }
            

    def actual := example.test()
    assert.equal(actual, "y")


def testoperators_1(assert):
    object example:
        method test():
            "doc"
            def color := ["red", "green", "blue"].diverge()
            def c := color[1] := "yellow"
            c
            

    def actual := example.test()
    assert.equal(actual, "yellow")


def testoperators_2(assert):
    object example:
        method test():
            "doc"
            m`x[i] := 1`.expand()
            

    def actual := example.test().canonical()
    assert.equal(actual, m`x.put(i, def ares_1 := 1); ares_1`.canonical())


def testoperators_3(assert):
    object example:
        method test():
            "doc"
            { var x := "augmenting "; x += "addition!"; x }
            

    def actual := example.test()
    assert.equal(actual, "augmenting addition!")


def testoperators_4(assert):
    object example:
        method test():
            "doc"
            m`x += "addition!"`.expand()
            

    def actual := example.test().canonical()
    assert.equal(actual, m`x := x.add("addition!")`.canonical())


def testoperators_5(assert):
    object example:
        method test():
            "doc"
            { var l := []; for i in (1..10) { l with= (i) }; l }
            

    def actual := example.test()
    assert.equal(actual, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])


def testoperators_6(assert):
    object example:
        method test():
            "doc"
            { var x := 7; x modPow= (129, 3) }
            

    def actual := example.test()
    assert.equal(actual, 1)


def testoperators_7(assert):
    object example:
        method test():
            "doc"
            var x := 5; [ x += 2, x -= 1, x *= 2, x **= 3 ]
            

    def actual := example.test()
    assert.equal(actual, [7, 6, 12, 1728])


def testoperators_8(assert):
    object example:
        method test():
            "doc"
            var x := 50; [ x //= 3, x %= 7, x /= 4]
            

    def actual := example.test()
    assert.equal(actual, [16, 2, 0.500000])


def testoperators_9(assert):
    object example:
        method test():
            "doc"
            var x := 5; [ x ^= 3, x |= 15, x &= 7, x <<= 3, x >>= 2]
            

    def actual := example.test()
    assert.equal(actual, [6, 15, 7, 56, 14])


def testoperators_10(assert):
    object example:
        method test():
            "doc"
            false || true
            

    def actual := example.test()
    assert.equal(actual, true)


def testoperators_11(assert):
    object example:
        method test():
            "doc"
            {((1 =~ x) || (2 =~ x)); x}
            

    def actual := example.test()
    assert.equal(actual, 1)


def testoperators_12(assert):
    object example:
        method test():
            "doc"
            {((1 =~ [x, y]) || (2 =~ x)); x}
            

    def actual := example.test()
    assert.equal(actual, 2)


def testoperators_13(assert):
    object example:
        method test():
            "doc"
            m`a || b`.expand()
            

    def actual := example.test().canonical()
    assert.equal(actual, m`if (a) { true } else if (b) { true } else { false }`.canonical())


def testoperators_14(assert):
    object example:
        method test():
            "doc"
            m`a && b`.expand()
            

    def actual := example.test().canonical()
    assert.equal(actual, m`if (a) { if (b) { true } else { false } } else { false }`.canonical())


def testoperators_15(assert):
    object example:
        method test():
            "doc"
            false == true
            

    def actual := example.test()
    assert.equal(actual, false)


def testoperators_16(assert):
    object example:
        method test():
            "doc"
            false != true
            

    def actual := example.test()
    assert.equal(actual, true)


def testoperators_17(assert):
    object example:
        method test():
            "doc"
            [1, "x"] =~ [_ :Int, _ :Str]
            

    def actual := example.test()
    assert.equal(actual, true)


def testoperators_18(assert):
    object example:
        method test():
            "doc"
            [1, 2] =~ [a, b]; b
            

    def actual := example.test()
    assert.equal(actual, 2)


def testoperators_19(assert):
    object example:
        method test():
            "doc"
            "<p>" =~ `<@tag>`; tag
            

    def actual := example.test()
    assert.equal(actual, "p")


def testoperators_20(assert):
    object example:
        method test():
            "doc"
            "<p>" !~ `</@tag>`
            

    def actual := example.test()
    assert.equal(actual, true)


def testoperators_21(assert):
    object example:
        method test():
            "doc"
            3 == "3"
            

    def actual := example.test()
    assert.equal(actual, false)


def testoperators_22(assert):
    object example:
        method test():
            "doc"
            1 + 1 == 2.0
            

    def actual := example.test()
    assert.equal(actual, false)


def testoperators_23(assert):
    object example:
        method test():
            "doc"
            true &! false
            

    def actual := example.test()
    assert.equal(actual, true)


def testoperators_24(assert):
    object example:
        method test():
            "doc"
            false & true
            

    def actual := example.test()
    assert.equal(actual, false)


def testoperators_25(assert):
    object example:
        method test():
            "doc"
            false | true
            

    def actual := example.test()
    assert.equal(actual, true)


def testoperators_26(assert):
    object example:
        method test():
            "doc"
            false ^ true
            

    def actual := example.test()
    assert.equal(actual, true)


def testoperators_27(assert):
    object example:
        method test():
            "doc"
            m`x == y`.expand()
            

    def actual := example.test().canonical()
    assert.equal(actual, m`_equalizer.sameEver(x, y)`.canonical())


def testoperators_28(assert):
    object example:
        method test():
            "doc"
            m`x != y`.expand()
            

    def actual := example.test().canonical()
    assert.equal(actual, m`_equalizer.sameEver(x, y).not()`.canonical())


def testoperators_29(assert):
    object example:
        method test():
            "doc"
            m`"value" =~ pattern`.expand()
            

    def actual := example.test().canonical()
    assert.equal(actual, m`def sp_1 := "value"; def [ok_2, &&pattern] := escape fail_3 { def pattern exit fail_3 := sp_1; _makeList.run(true, &&pattern) } catch problem_4 { def via (_slotToBinding) &&broken_5 := Ref.broken(problem_4); _makeList.run(false, &&broken_5) }; ok_2`.canonical())


def testoperators_30(assert):
    object example:
        method test():
            "doc"
            m`"value" !~ pattern`.expand()
            

    def actual := example.test().canonical()
    assert.equal(actual, m`(def sp_1 := "value"; def [ok_2, &&pattern] := escape fail_3 { def pattern exit fail_3 := sp_1; _makeList.run(true, &&pattern) } catch problem_4 { def via (_slotToBinding) &&broken_5 := Ref.broken(problem_4); _makeList.run(false, &&broken_5) }; ok_2).not()`.canonical())


def testoperators_31(assert):
    object example:
        method test():
            "doc"
            m`x ^ y`.expand()
            

    def actual := example.test().canonical()
    assert.equal(actual, m`x.xor(y)`.canonical())


def testoperators_32(assert):
    object example:
        method test():
            "doc"
            m`x & y`.expand()
            

    def actual := example.test().canonical()
    assert.equal(actual, m`x.and(y)`.canonical())


def testoperators_33(assert):
    object example:
        method test():
            "doc"
            m`x | y`.expand()
            

    def actual := example.test().canonical()
    assert.equal(actual, m`x.or(y)`.canonical())


def testoperators_34(assert):
    object example:
        method test():
            "doc"
            m`x &! y`.expand()
            

    def actual := example.test().canonical()
    assert.equal(actual, m`x.butNot(y)`.canonical())


def testoperators_35(assert):
    object example:
        method test():
            "doc"
            3 < 2
            

    def actual := example.test()
    assert.equal(actual, false)


def testoperators_36(assert):
    object example:
        method test():
            "doc"
            3 > 2
            

    def actual := example.test()
    assert.equal(actual, true)


def testoperators_37(assert):
    object example:
        method test():
            "doc"
            3 < 3
            

    def actual := example.test()
    assert.equal(actual, false)


def testoperators_38(assert):
    object example:
        method test():
            "doc"
            3 <= 3
            

    def actual := example.test()
    assert.equal(actual, true)


def testoperators_39(assert):
    object example:
        method test():
            "doc"
            try { 3 < "3" } catch _ { "ouch! no order defined" }
            

    def actual := example.test()
    assert.equal(actual, "ouch! no order defined")


def testoperators_40(assert):
    object example:
        method test():
            "doc"
            2.0 <=> 1 + 1
            

    def actual := example.test()
    assert.equal(actual, true)


def testoperators_41(assert):
    object example:
        method test():
            "doc"
            2 + 1 <=> 3.0
            

    def actual := example.test()
    assert.equal(actual, true)


def testoperators_42(assert):
    object example:
        method test():
            "doc"
            m`3 < 2`.expand()
            

    def actual := example.test().canonical()
    assert.equal(actual, m`_comparer.lessThan(3, 2)`.canonical())


def testoperators_43(assert):
    object example:
        method test():
            "doc"
            m`2.0 <=> 1 + 1`.expand()
            

    def actual := example.test().canonical()
    assert.equal(actual, m`_comparer.asBigAs(2.000000, 1.add(1))`.canonical())


def testoperators_44(assert):
    object example:
        method test():
            "doc"
            [for x in (1..!4) x * 2]
            

    def actual := example.test()
    assert.equal(actual, [2, 4, 6])


def testoperators_45(assert):
    object example:
        method test():
            "doc"
            [for x in (1..4) x * 2]
            

    def actual := example.test()
    assert.equal(actual, [2, 4, 6, 8])


def testoperators_46(assert):
    object example:
        method test():
            "doc"
            (0..!10) <=> (0..9)
            

    def actual := example.test()
    assert.equal(actual, true)


def testoperators_47(assert):
    object example:
        method test():
            "doc"
            m`lo..hi`.expand()
            

    def actual := example.test().canonical()
    assert.equal(actual, m`_makeOrderedSpace.op__thru(lo, hi)`.canonical())


def testoperators_48(assert):
    object example:
        method test():
            "doc"
            m`lo..!hi`.expand()
            

    def actual := example.test().canonical()
    assert.equal(actual, m`_makeOrderedSpace.op__till(lo, hi)`.canonical())


def testoperators_49(assert):
    object example:
        method test():
            "doc"
            m`i << bits`.expand()
            

    def actual := example.test().canonical()
    assert.equal(actual, m`i.shiftLeft(bits)`.canonical())


def testoperators_50(assert):
    object example:
        method test():
            "doc"
            m`i >> bits`.expand()
            

    def actual := example.test().canonical()
    assert.equal(actual, m`i.shiftRight(bits)`.canonical())


def testoperators_51(assert):
    object example:
        method test():
            "doc"
            [1, 2] + [3, 4]
            

    def actual := example.test()
    assert.equal(actual, [1, 2, 3, 4])


def testoperators_52(assert):
    object example:
        method test():
            "doc"
            "abc" + "def"
            

    def actual := example.test()
    assert.equal(actual, "abcdef")


def testoperators_53(assert):
    object example:
        method test():
            "doc"
            ["square" => 4] | ["triangle" => 3]
            

    def actual := example.test()
    assert.equal(actual, ["square" => 4, "triangle" => 3])


def testoperators_54(assert):
    object example:
        method test():
            "doc"
            def sides := ["square" => 4, "triangle" => 3]
            sides.without("square")
            

    def actual := example.test()
    assert.equal(actual, ["triangle" => 3])


def testoperators_55(assert):
    object example:
        method test():
            "doc"
            m`x + y`.expand()
            

    def actual := example.test().canonical()
    assert.equal(actual, m`x.add(y)`.canonical())


def testoperators_56(assert):
    object example:
        method test():
            "doc"
            m`x - y`.expand()
            

    def actual := example.test().canonical()
    assert.equal(actual, m`x.subtract(y)`.canonical())


def testoperators_57(assert):
    object example:
        method test():
            "doc"
            2 * 3
            

    def actual := example.test()
    assert.equal(actual, 6)


def testoperators_58(assert):
    object example:
        method test():
            "doc"
            5 ** 3 % 13
            

    def actual := example.test()
    assert.equal(actual, 8)


def testoperators_59(assert):
    object example:
        method test():
            "doc"
            m`base ** exp % mod`.expand()
            

    def actual := example.test().canonical()
    assert.equal(actual, m`base.modPow(exp, mod)`.canonical())


def testoperators_60(assert):
    object example:
        method test():
            "doc"
            2 ** 3
            

    def actual := example.test()
    assert.equal(actual, 8)


def testoperators_61(assert):
    object example:
        method test():
            "doc"
            m`2 ** 3`.expand()
            

    def actual := example.test().canonical()
    assert.equal(actual, m`2.pow(3)`.canonical())


def testoperators_62(assert):
    object example:
        method test():
            "doc"
            - (1 + 3)
            

    def actual := example.test()
    assert.equal(actual, -4)


def testoperators_63(assert):
    object example:
        method test():
            "doc"
            ~ 0xff
            

    def actual := example.test()
    assert.equal(actual, -256)


def testoperators_64(assert):
    object example:
        method test():
            "doc"
            ! true
            

    def actual := example.test()
    assert.equal(actual, false)


def testoperators_65(assert):
    object example:
        method test():
            "doc"
            m`! false`.expand()
            

    def actual := example.test().canonical()
    assert.equal(actual, m`false.not()`.canonical())


def testoperators_66(assert):
    object example:
        method test():
            "doc"
            1 :Int
            

    def actual := example.test()
    assert.equal(actual, 1)


def testoperators_67(assert):
    object example:
        method test():
            "doc"
            { def x := 2; def result := x.add(3) }
            

    def actual := example.test()
    assert.equal(actual, 5)


def testoperators_68(assert):
    object example:
        method test():
            "doc"
            { def x; def prom := x<-message(3); null }
            

    def actual := example.test()
    when (actual) ->
        assert.equal(actual, null)


def testoperators_69(assert):
    object example:
        method test():
            "doc"
            { def x := 2; def xplus := x.add; xplus(4) }
            

    def actual := example.test()
    assert.equal(actual, 6)


def testoperators_70(assert):
    object example:
        method test():
            "doc"
            m`f(x)`.expand()
            

    def actual := example.test().canonical()
    assert.equal(actual, m`f.run(x)`.canonical())


def testoperators_71(assert):
    object example:
        method test():
            "doc"
            { object parity { to get(n) { return n % 2 }}; parity[3] }
            

    def actual := example.test()
    assert.equal(actual, 1)


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
    testoperators_44,
    testoperators_45,
    testoperators_46,
    testoperators_47,
    testoperators_48,
    testoperators_49,
    testoperators_50,
    testoperators_51,
    testoperators_52,
    testoperators_53,
    testoperators_54,
    testoperators_55,
    testoperators_56,
    testoperators_57,
    testoperators_58,
    testoperators_59,
    testoperators_60,
    testoperators_61,
    testoperators_62,
    testoperators_63,
    testoperators_64,
    testoperators_65,
    testoperators_66,
    testoperators_67,
    testoperators_68,
    testoperators_69,
    testoperators_70,
    testoperators_71
])


# ordinary-programming

def testordinary_programming_0(assert):
    object example:
        method test():
            "doc"
            object origin:
                to getX():
                    return 0
                to getY():
                    return 0
            # Now invoke the methods
            origin.getY()
            

    def actual := example.test()
    assert.equal(actual, 0)


def testordinary_programming_1(assert):
    object example:
        method test():
            "doc"
            def square(x):
                return x * x
            square.run(4)
            

    def actual := example.test()
    assert.equal(actual, 16)


def testordinary_programming_2(assert):
    object example:
        method test():
            "doc"
            object square:
                to run(x):
                    return x * x
            square(4)
            

    def actual := example.test()
    assert.equal(actual, 16)


def testordinary_programming_3(assert):
    object example:
        method test():
            "doc"
            def makeCounter(var value :Int):
                return object counter:
                    to increment() :Int:
                        return value += 1
                    to makeOffsetCounter(delta :Int):
                        return makeCounter(value + delta)
            
            def c1 := makeCounter(1)
            c1.increment()
            def c2 := c1.makeOffsetCounter(10)
            c1.increment()
            c2.increment()
            [c1.increment(), c2.increment()]
            

    def actual := example.test()
    assert.equal(actual, [4, 14])


def testordinary_programming_4(assert):
    object example:
        method test():
            "doc"
            def makeMafia(var players :Set):
                def mafiosoCount :Int := players.size() // 3
                var mafiosos :Set := players.slice(0, mafiosoCount)
                var innocents :Set := players.slice(mafiosoCount)
            
                return object mafia:
                    to getWinner():
                        if (mafiosos.size() == 0):
                            return "village"
                        if (mafiosos.size() >= innocents.size()):
                            return "mafia"
                        return null
            
                    to lynch(victim):
                        players without= (victim)
                        mafiosos without= (victim)
                        innocents without= (victim)
            
            def game1 := makeMafia(["Alice", "Bob", "Charlie"].asSet())
            game1.lynch("Bob")
            game1.lynch("Charlie")
            game1.getWinner()
            

    def actual := example.test()
    assert.equal(actual, "mafia")


def testordinary_programming_5(assert):
    object example:
        method test():
            "doc"
            -3.5 // 1
            

    def actual := example.test()
    assert.equal(actual, -4)


unittest([
    testordinary_programming_0,
    testordinary_programming_1,
    testordinary_programming_2,
    testordinary_programming_3,
    testordinary_programming_4,
    testordinary_programming_5
])


# patterns

def testpatterns_0(assert):
    object example:
        method test():
            "doc"
            def players := [object alice{}, object bob{}]
            
            object game:
                to vote(player ? (players.contains(player)),
                        choice ? (players.contains(choice))) :
                   return "voted"
            
            def t1 := game.vote(players[0], players[1])
            def t2 := try { game.vote(object alice{}, "bob") } catch _ { "BZZT!" }
            [t1, t2]
            

    def actual := example.test()
    assert.equal(actual, ["voted", "BZZT!"])


def testpatterns_1(assert):
    object example:
        method test():
            "doc"
            m`def patt ? (condition) := value`.expand()
            

    def actual := example.test().canonical()
    assert.equal(actual, m`def via (_suchThat) [patt, via (_suchThat.run(condition)) _] := value`.canonical())


def testpatterns_2(assert):
    object example:
        method test():
            "doc"
            def [x, y] := [5, 10]; x
            

    def actual := example.test()
    assert.equal(actual, 5)


def testpatterns_3(assert):
    object example:
        method test():
            "doc"
            def [first] + rest := [1, 2, 3, 4]
            rest
            

    def actual := example.test()
    assert.equal(actual, [2, 3, 4])


def testpatterns_4(assert):
    object example:
        method test():
            "doc"
            def sides := ["square" => 4, "triangle" => 3]
            def shape := "triangle"
            
            def ["square" => squareSides, (shape) => qty1] := sides
            
            def ["triangle" => qty2] | _ := sides
            
            [squareSides, shape, qty1, qty2]
            

    def actual := example.test()
    assert.equal(actual, [4, "triangle", 3, 3])


def testpatterns_5(assert):
    object example:
        method test():
            "doc"
            def sides := ["square" => 4, "triangle" => 3]
            
            def ["octogon" => octoSides := 8] | _ := sides
            octoSides
            

    def actual := example.test()
    assert.equal(actual, 8)


def testpatterns_6(assert):
    object example:
        method test():
            "doc"
            def sides := ["square" => 4, "triangle" => 3]
            
            def [=> triangle, => square] := sides
            [triangle, square]
            

    def actual := example.test()
    assert.equal(actual, [3, 4])


def testpatterns_7(assert):
    object example:
        method test():
            "doc"
            m`def [item1, item2] + rest := stuff`.expand()
            

    def actual := example.test().canonical()
    assert.equal(actual, m`def via (_splitList.run(2)) [item1, item2, rest] := stuff`.canonical())


def testpatterns_8(assert):
    object example:
        method test():
            "doc"
            m`def ["key" => patt] := data`.expand()
            

    def actual := example.test().canonical()
    assert.equal(actual, m`def via (_mapExtract.run("key")) [patt, _ :_mapEmpty] := data`.canonical())


def testpatterns_9(assert):
    object example:
        method test():
            "doc"
            m`def ["key1" => patt1] | rest := data`.expand()
            

    def actual := example.test().canonical()
    assert.equal(actual, m`def via (_mapExtract.run("key1")) [patt1, rest] := data`.canonical())


def testpatterns_10(assert):
    object example:
        method test():
            "doc"
            m`def ["key1" => patt1 := fallback] := data`.expand()
            

    def actual := example.test().canonical()
    assert.equal(actual, m`def via (_mapExtract.withDefault("key1", fallback)) [patt1, _ :_mapEmpty] := data`.canonical())


def testpatterns_11(assert):
    object example:
        method test():
            "doc"
            def state := "night"
            
            switch (state) {
                match =="day" {"night"}
                match =="night" {"day"}
            }
            

    def actual := example.test()
    assert.equal(actual, "day")


def testpatterns_12(assert):
    object example:
        method test():
            "doc"
            m`def ==specimen := value`.expand()
            

    def actual := example.test().canonical()
    assert.equal(actual, m`def via (_matchSame.run(specimen)) _ := value`.canonical())


def testpatterns_13(assert):
    object example:
        method test():
            "doc"
            m`def !=specimen := value`.expand()
            

    def actual := example.test().canonical()
    assert.equal(actual, m`def via (_matchSame.different(specimen)) _ := value`.canonical())


def testpatterns_14(assert):
    object example:
        method test():
            "doc"
            "The cat and the hat." =~ simple`The cat and the @what.`
            

    def actual := example.test()
    assert.equal(actual, true)


def testpatterns_15(assert):
    object example:
        method test():
            "doc"
            "The cat and the hat." =~ `The cat and the @{what :Str}.`; what
            

    def actual := example.test()
    assert.equal(actual, "hat")


def testpatterns_16(assert):
    object example:
        method test():
            "doc"
            "The cat and the hat." =~ simple`The cat and the @{what :Int}.`
            

    def actual := example.test()
    assert.equal(actual, false)


def testpatterns_17(assert):
    object example:
        method test():
            "doc"
            m`def ``quasi @@patt`` := value`.expand()
            

    def actual := example.test().canonical()
    assert.equal(actual, m`def via (_quasiMatcher.run(simple__quasiParser.matchMaker(_makeList.run("quasi ", simple__quasiParser.patternHole(0), "")), _makeList.run())) [patt] := value`.canonical())


def testpatterns_18(assert):
    object example:
        method test():
            "doc"
            def via (_splitList.run(1)) [x, xs] := [1, 2, 3]
            [x, xs]
            

    def actual := example.test()
    assert.equal(actual, [1, [2, 3]])


def testpatterns_19(assert):
    object example:
        method test():
            "doc"
            def x := 1
            x
            

    def actual := example.test()
    assert.equal(actual, 1)


def testpatterns_20(assert):
    object example:
        method test():
            "doc"
            def ::"hello, world" := [1, 2]
            ::"hello, world"
            

    def actual := example.test()
    assert.equal(actual, [1, 2])


def testpatterns_21(assert):
    object example:
        method test():
            "doc"
            m`def bind x := 2`.expand()
            

    def actual := example.test().canonical()
    assert.equal(actual, m`def via (_bind.run(x_Resolver, null)) _ := 2`.canonical())


def testpatterns_22(assert):
    object example:
        method test():
            "doc"
            m`def &x := 1`.expand()
            

    def actual := example.test().canonical()
    assert.equal(actual, m`def via (_slotToBinding) &&x := 1`.canonical())


unittest([
    testpatterns_0,
    testpatterns_1,
    testpatterns_2,
    testpatterns_3,
    testpatterns_4,
    testpatterns_5,
    testpatterns_6,
    testpatterns_7,
    testpatterns_8,
    testpatterns_9,
    testpatterns_10,
    testpatterns_11,
    testpatterns_12,
    testpatterns_13,
    testpatterns_14,
    testpatterns_15,
    testpatterns_16,
    testpatterns_17,
    testpatterns_18,
    testpatterns_19,
    testpatterns_20,
    testpatterns_21,
    testpatterns_22
])


# prim-expr

def testprim_expr_0(assert):
    object example:
        method test():
            "doc"
            4 + 2 * 3
            

    def actual := example.test()
    assert.equal(actual, 10)


def testprim_expr_1(assert):
    object example:
        method test():
            "doc"
            (4 + 2) * 3
            

    def actual := example.test()
    assert.equal(actual, 18)


def testprim_expr_2(assert):
    object example:
        method test():
            "doc"
            Int
            

    def actual := example.test()
    assert.equal(actual, Int)


def testprim_expr_3(assert):
    object example:
        method test():
            "doc"
            _equalizer
            

    def actual := example.test()
    assert.equal(actual, _equalizer)


def testprim_expr_4(assert):
    object example:
        method test():
            "doc"
            { def ::"hello, world" := 1; ::"hello, world" }
            

    def actual := example.test()
    assert.equal(actual, 1)


def testprim_expr_5(assert):
    object example:
        method test():
            "doc"
            ['I', "love", "Monte", 42, 0.5][3]
            

    def actual := example.test()
    assert.equal(actual, 42)


def testprim_expr_6(assert):
    object example:
        method test():
            "doc"
            { def l := ['I', "love", "Monte", 42, 0.5].diverge(); l[3] := 0 }
            

    def actual := example.test()
    assert.equal(actual, 0)


def testprim_expr_7(assert):
    object example:
        method test():
            "doc"
            m`[]`.expand()
            

    def actual := example.test().canonical()
    assert.equal(actual, m`_makeList.run()`.canonical())


def testprim_expr_8(assert):
    object example:
        method test():
            "doc"
            { def m := ["roses" => "red", "violets" => "blue"]; m["roses"] }
            

    def actual := example.test()
    assert.equal(actual, "red")


def testprim_expr_9(assert):
    object example:
        method test():
            "doc"
            { def m := ["roses" => "red", "violets" => "blue"].diverge(); m["roses"] := 3 }
            

    def actual := example.test()
    assert.equal(actual, 3)


def testprim_expr_10(assert):
    object example:
        method test():
            "doc"
            [ "a" => 1, "b" => 2] == [ "b" => 2, "a" => 1]
            

    def actual := example.test()
    assert.equal(actual, false)


def testprim_expr_11(assert):
    object example:
        method test():
            "doc"
            [ "a" => 1, "b" => 2].sortKeys() == [ "b" => 2, "a" => 1].sortKeys()
            

    def actual := example.test()
    assert.equal(actual, true)


unittest([
    testprim_expr_0,
    testprim_expr_1,
    testprim_expr_2,
    testprim_expr_3,
    testprim_expr_4,
    testprim_expr_5,
    testprim_expr_6,
    testprim_expr_7,
    testprim_expr_8,
    testprim_expr_9,
    testprim_expr_10,
    testprim_expr_11
])


# promises

unittest([
    
])


# quasiparsers

def testquasiparsers_0(assert):
    object example:
        method test():
            "doc"
            def x := 3
            `Value of x is: $x`
            

    def actual := example.test()
    assert.equal(actual, "Value of x is: 3")


unittest([
    testquasiparsers_0
])


# quick_ref

def testquick_ref_0(assert):
    object example:
        method test():
            "doc"
            def a := 2 + 3
            var a2 := 4
            a2 += 1
            def b := `answer: $a`
            traceln(b)
            b
            

    def actual := example.test()
    assert.equal(actual, "answer: 5")


def testquick_ref_1(assert):
    object example:
        method test():
            "doc"
            if ('a' == 'b'):
               "match"
            else:
               "no match"
            

    def actual := example.test()
    assert.equal(actual, "no match")


def testquick_ref_2(assert):
    object example:
        method test():
            "doc"
            var a := 0; def b := 4
            while (a < b):
                a += 1
            a
            

    def actual := example.test()
    assert.equal(actual, 4)


def testquick_ref_3(assert):
    object example:
        method test():
            "doc"
            var resource := "reserved"
            try:
                3 // 0
            catch err:
                `error!`
            finally:
                resource := "released"
            resource
            

    def actual := example.test()
    assert.equal(actual, "released")


def testquick_ref_4(assert):
    object example:
        method test():
            "doc"
            def x := [].diverge()
            for next in (1..3):
                x.push([next, next])
            x.snapshot()
            

    def actual := example.test()
    assert.equal(actual, [[1, 1], [2, 2], [3, 3]])


def testquick_ref_5(assert):
    object example:
        method test():
            "doc"
            def map := ['a' => 65, 'b' => 66]
            var sum := 0
            for key => value in (map):
                sum += value
            sum
            

    def actual := example.test()
    assert.equal(actual, 131)


def testquick_ref_6(assert):
    object example:
        method test():
            "doc"
            def addTwoPrint(number):
                traceln(number + 2)
                return number + 2
            
            def twoPlusThree := addTwoPrint(3)
            twoPlusThree
            

    def actual := example.test()
    assert.equal(actual, 5)


def testquick_ref_7(assert):
    object example:
        method test():
            "doc"
            object adder:
                to add1(number):
                    return number + 1
                to add2(number):
                    return number + 2
            def result := adder.add1(3)
            result
            

    def actual := example.test()
    assert.equal(actual, 4)


def testquick_ref_8(assert):
    object example:
        method test():
            "doc"
            def makeOperator(baseNum):
                def instanceValue := 3
                object operator:
                    to addBase(number):
                        return baseNum + number
                    to multiplyBase(number):
                        return baseNum * number
                return operator
            def threeHandler := makeOperator(3)
            def threeTimes2 := threeHandler.multiplyBase(2)
            threeTimes2
            

    def actual := example.test()
    assert.equal(actual, 6)


def testquick_ref_9(assert):
    object example:
        method test():
            "doc"
            def makeExtendedFile(myFile):
                return object extendedFile extends myFile:
                    to append(text):
                        var current := myFile.getText()
                        current := current + text
                        myFile.setText(current)
            
            makeExtendedFile(object _ {})._respondsTo("append", 1)
            

    def actual := example.test()
    assert.equal(actual, true)


def testquick_ref_10(assert):
    object example:
        method test():
            "doc"
            def main(argv, => makeFileResource):
                def fileA := makeFileResource("fileA")
                fileA <- setContents(b`abc\ndef`)
                def contents := fileA <- getContents()
                when (contents) ->
                    for line in (contents.split("\n")):
                        traceln(line)
            
            main._respondsTo("run", 1)
            

    def actual := example.test()
    when (actual) ->
        assert.equal(actual, true)


def testquick_ref_11(assert):
    object example:
        method test():
            "doc"
            var a := [8, 6, "a"]
            a[2]
            

    def actual := example.test()
    assert.equal(actual, "a")


def testquick_ref_12(assert):
    object example:
        method test():
            "doc"
            var a := [8, 6, "a"]
            a.size()
            

    def actual := example.test()
    assert.equal(actual, 3)


def testquick_ref_13(assert):
    object example:
        method test():
            "doc"
            var a := [8, 6, "a"]
            for i in (a):
                traceln(i)
            a := a + ["b"]
            a.slice(0, 2)
            

    def actual := example.test()
    assert.equal(actual, [8, 6])


def testquick_ref_14(assert):
    object example:
        method test():
            "doc"
            def m := ["c" => 5]
            m["c"]
            

    def actual := example.test()
    assert.equal(actual, 5)


def testquick_ref_15(assert):
    object example:
        method test():
            "doc"
            ["c" => 5].size()
            

    def actual := example.test()
    assert.equal(actual, 1)


def testquick_ref_16(assert):
    object example:
        method test():
            "doc"
            def m := ["c" => 5]
            for key => value in (m):
                traceln(value)
            def flexM := m.diverge()
            flexM["d"] := 6
            flexM.size()
            

    def actual := example.test()
    assert.equal(actual, 2)


def testquick_ref_17(assert):
    object example:
        method test():
            "doc"
            def flexA := [8, 6, "a", "b"].diverge()
            flexA.extend(["b"])
            flexA.push("b")
            def constA := flexA.snapshot()
            

    def actual := example.test()
    assert.equal(actual, [8, 6, "a", "b", "b", "b"])


def testquick_ref_18(assert):
    object example:
        method test():
            "doc"
            def m := ["c" => 5]
            def flexM := m.diverge()
            flexM["b"] := 2
            flexM.removeKey("b")
            def constM := flexM.snapshot()
            

    def actual := example.test()
    assert.equal(actual, ["c" => 5])


def testquick_ref_19(assert):
    object example:
        method test():
            "doc"
            def abacus := object mock { to add(x, y) { return x + y } }
            var out := null
            
            def answer := abacus <- add(1, 2)
            when (answer) ->
                out := `computation complete: $answer`
            catch problem:
                traceln(`promise broken $problem `)
            

    def actual := example.test()
    when (actual) ->
        assert.equal(actual, 3)


def testquick_ref_20(assert):
    object example:
        method test():
            "doc"
            def makeCarRcvr := fn autoMake { `shiny $autoMake` }
            
            def carRcvr := makeCarRcvr <- ("Mercedes")
            Ref.whenBroken(carRcvr, def lost(brokenRef) {
                traceln("Lost connection to carRcvr")
            })
            carRcvr
            

    def actual := example.test()
    when (actual) ->
        assert.equal(actual, "shiny Mercedes")


def testquick_ref_21(assert):
    object example:
        method test():
            "doc"
            def [resultVow, resolver] := Ref.promise()
            
            when (resultVow) ->
                traceln(resultVow)
            catch prob:
                traceln(`oops: $prob`)
            
            resolver.resolve("this text is the answer")
            resultVow
            

    def actual := example.test()
    when (actual) ->
        assert.equal(actual, "this text is the answer")


unittest([
    testquick_ref_0,
    testquick_ref_1,
    testquick_ref_2,
    testquick_ref_3,
    testquick_ref_4,
    testquick_ref_5,
    testquick_ref_6,
    testquick_ref_7,
    testquick_ref_8,
    testquick_ref_9,
    testquick_ref_10,
    testquick_ref_11,
    testquick_ref_12,
    testquick_ref_13,
    testquick_ref_14,
    testquick_ref_15,
    testquick_ref_16,
    testquick_ref_17,
    testquick_ref_18,
    testquick_ref_19,
    testquick_ref_20,
    testquick_ref_21
])


# runtime

unittest([
    
])


# semantics

unittest([
    
])


# slots

unittest([
    
])


# symbols

def testsymbols_0(assert):
    object example:
        method test():
            "doc"
            DEF x := 1
            

    def actual := example.test()
    assert.equal(actual, 1)


def testsymbols_1(assert):
    object example:
        method test():
            "doc"
            5
            

    def actual := example.test()
    assert.equal(actual, 5)


def testsymbols_2(assert):
    object example:
        method test():
            "doc"
            0xF
            

    def actual := example.test()
    assert.equal(actual, 15)


def testsymbols_3(assert):
    object example:
        method test():
            "doc"
            128 ** 20
            

    def actual := example.test()
    assert.equal(actual, 1393796574908163946345982392040522594123776)


def testsymbols_4(assert):
    object example:
        method test():
            "doc"
            5 + 2
            

    def actual := example.test()
    assert.equal(actual, 7)


def testsymbols_5(assert):
    object example:
        method test():
            "doc"
            def x :Double := 1.0
            

    def actual := example.test()
    assert.equal(actual, 1.000000)


def testsymbols_6(assert):
    object example:
        method test():
            "doc"
            4.0.floor()
            

    def actual := example.test()
    assert.equal(actual, 4)


def testsymbols_7(assert):
    object example:
        method test():
            "doc"
            4 * 1.0
            

    def actual := example.test()
    assert.equal(actual, 4.000000)


def testsymbols_8(assert):
    object example:
        method test():
            "doc"
            '☃'
            

    def actual := example.test()
    assert.equal(actual, '☃')


def testsymbols_9(assert):
    object example:
        method test():
            "doc"
            '\u23b6'
            

    def actual := example.test()
    assert.equal(actual, '⎶')


def testsymbols_10(assert):
    object example:
        method test():
            "doc"
            "Hello World!".replace("World", "Monte hackers")
            

    def actual := example.test()
    assert.equal(actual, "Hello Monte hackers!")


def testsymbols_11(assert):
    object example:
        method test():
            "doc"
            "¿Dónde aquí habla Monte o español?".size()
            

    def actual := example.test()
    assert.equal(actual, 34)


def testsymbols_12(assert):
    object example:
        method test():
            "doc"
            def price := 10.00
            `The price is $$$price.`
            

    def actual := example.test()
    assert.equal(actual, "The price is $10.000000.")


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
    testsymbols_12
])


# taste

def testtaste_0(assert):
    object example:
        method test():
            "doc"
            def helloWeb(request) { return [200, "hello"]; }
            helloWeb("/")
            

    def actual := example.test()
    assert.equal(actual, [200, "hello"])


unittest([
    testtaste_0
])


# tools

unittest([
    
])


# tubes

unittest([
    
])


# vats

unittest([
    
])


# wizard

unittest([
    
])

