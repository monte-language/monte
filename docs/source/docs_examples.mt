
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
            for i => each in (["a", "b"]):
                traceln(`Index: $i Value: $each`)
            

    assert.equal(example.test(), null)


def testiteration_1(assert):
    object example:
        method test():
            "doc"
            { def i := 3; if (i % 2 == 0) { "yes" } else { "no" } }
            

    assert.equal(example.test(), "no")


def testiteration_2(assert):
    object example:
        method test():
            "doc"
            def evens := [for number in (1..10) if (number % 2 == 0) number]
            evens
            

    assert.equal(example.test(), [2, 4, 6, 8, 10])


unittest([
    testiteration_0,
    testiteration_1,
    testiteration_2
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
            

    assert.equal(example.test().canonical(), m`_equalizer.sameEver(x, y)`.canonical())


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
            true && true
            

    assert.equal(example.test(), true)


def testoperators_24(assert):
    object example:
        method test():
            "doc"
            true &! false
            

    assert.equal(example.test(), true)


def testoperators_25(assert):
    object example:
        method test():
            "doc"
            m`x &! y`.expand()
            

    assert.equal(example.test().canonical(), m`x.butNot(y)`.canonical())


def testoperators_26(assert):
    object example:
        method test():
            "doc"
            2 ** 3
            

    assert.equal(example.test(), 8)


def testoperators_27(assert):
    object example:
        method test():
            "doc"
            2 * 3
            

    assert.equal(example.test(), 6)


def testoperators_28(assert):
    object example:
        method test():
            "doc"
            [for x in (1..!4) x * 2]
            

    assert.equal(example.test(), [2, 4, 6])


def testoperators_29(assert):
    object example:
        method test():
            "doc"
            [for x in (1..4) x * 2]
            

    assert.equal(example.test(), [2, 4, 6, 8])


def testoperators_30(assert):
    object example:
        method test():
            "doc"
            { var x := "augmenting "; x += "addition!"; x }
            

    assert.equal(example.test(), "augmenting addition!")


def testoperators_31(assert):
    object example:
        method test():
            "doc"
            { var x := "augmenting "; x := x.add("addition!") }
            

    assert.equal(example.test(), "augmenting addition!")


def testoperators_32(assert):
    object example:
        method test():
            "doc"
            { var l := []; for i in (1..10) { l with= (i) }; l }
            

    assert.equal(example.test(), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])


def testoperators_33(assert):
    object example:
        method test():
            "doc"
            { var x := 7; x modPow= (129, 3) }
            

    assert.equal(example.test(), 1)


def testoperators_34(assert):
    object example:
        method test():
            "doc"
            { 4; "x"; "y" }
            

    assert.equal(example.test(), "y")


def testoperators_35(assert):
    object example:
        method test():
            "doc"
            4 + 2 * 3
            

    assert.equal(example.test(), 10)


def testoperators_36(assert):
    object example:
        method test():
            "doc"
            (4 + 2) * 3
            

    assert.equal(example.test(), 18)


def testoperators_37(assert):
    object example:
        method test():
            "doc"
            Int
            

    assert.equal(example.test(), Int)


def testoperators_38(assert):
    object example:
        method test():
            "doc"
            { def ::"hello, world" := 1; ::"hello, world" }
            

    assert.equal(example.test(), 1)


def testoperators_39(assert):
    object example:
        method test():
            "doc"
            - (1 + 3)
            

    assert.equal(example.test(), -4)


def testoperators_40(assert):
    object example:
        method test():
            "doc"
            ~ 0xff
            

    assert.equal(example.test(), -256)


def testoperators_41(assert):
    object example:
        method test():
            "doc"
            ! true
            

    assert.equal(example.test(), false)


def testoperators_42(assert):
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
    testoperators_42
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
            

    assert.equal(example.test(), 0)


def testordinary_programming_1(assert):
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
            

    assert.equal(example.test(), [4, 14])


def testordinary_programming_2(assert):
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
            

    assert.equal(example.test(), "mafia")


def testordinary_programming_3(assert):
    object example:
        method test():
            "doc"
            def square(x):
                return x * x
            square.run(4)
            

    assert.equal(example.test(), 16)


def testordinary_programming_4(assert):
    object example:
        method test():
            "doc"
            object square:
                to run(x):
                    return x * x
            square(4)
            

    assert.equal(example.test(), 16)


def testordinary_programming_5(assert):
    object example:
        method test():
            "doc"
            -3.5 // 1
            

    assert.equal(example.test(), -4)


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
            m`def bind x := 2`.expand()
            

    assert.equal(example.test().canonical(), m`def via (_bind.run(x_Resolver, null)) _ := 2`.canonical())


def testpatterns_1(assert):
    object example:
        method test():
            "doc"
            m`def &x := 1`.expand()
            

    assert.equal(example.test().canonical(), m`def via (_slotToBinding) &&x := 1`.canonical())


unittest([
    testpatterns_0,
    testpatterns_1
])


# prim-expr

unittest([
    
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
            

    assert.equal(example.test(), "Value of x is: 3")


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
            

    assert.equal(example.test(), "answer: 5")


def testquick_ref_1(assert):
    object example:
        method test():
            "doc"
            if ('a' == 'b'):
               traceln("match")
            else:
               traceln("no match")
            

    assert.equal(example.test(), null)


def testquick_ref_2(assert):
    object example:
        method test():
            "doc"
            var a := 0; def b := 4
            while (a < b):
                a += 1
            a
            

    assert.equal(example.test(), 4)


def testquick_ref_3(assert):
    object example:
        method test():
            "doc"
            try:
                3 // 0
            catch err:
                traceln(`error: $err`)
            finally:
                traceln("always")
            

    assert.equal(example.test(), null)


def testquick_ref_4(assert):
    object example:
        method test():
            "doc"
            for next in (1..3):
                traceln(next)
            

    assert.equal(example.test(), null)


def testquick_ref_5(assert):
    object example:
        method test():
            "doc"
            def map := ['a' => 65, 'b' => 66]
            for key => value in (map):
                traceln("got pair")
            

    assert.equal(example.test(), null)


def testquick_ref_6(assert):
    object example:
        method test():
            "doc"
            def addTwoPrint(number):
                traceln(number + 2)
                return number + 2
            
            def twoPlusThree := addTwoPrint(3)
            twoPlusThree
            

    assert.equal(example.test(), 5)


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
            

    assert.equal(example.test(), 4)


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
            

    assert.equal(example.test(), 6)


def testquick_ref_9(assert):
    object example:
        method test():
            "doc"
            def makeRadio(car):
                # define radios
            def makeCar(name):
                var x := 0
                var y := 0
                def car # using def with no assignment
                def myWeatherRadio := makeRadio(car)
                bind car:
                    to receiveWeatherAlert():
                        # ....process the weather report....
                        # myWeatherRadio.foo(...)
                    to getX():
                        return x
                    to getY():
                        return y
                    # ....list the rest of the car methods....
                return car
            makeCar("ferrari").getX()
            

    assert.equal(example.test(), 0)


def testquick_ref_10(assert):
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
            

    assert.equal(example.test(), true)


def testquick_ref_11(assert):
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
            

    assert.equal(example.test(), true)


def testquick_ref_12(assert):
    object example:
        method test():
            "doc"
            var a := [8, 6, "a"]
            a[2]
            

    assert.equal(example.test(), "a")


def testquick_ref_13(assert):
    object example:
        method test():
            "doc"
            var a := [8, 6, "a"]
            a.size()
            

    assert.equal(example.test(), 3)


def testquick_ref_14(assert):
    object example:
        method test():
            "doc"
            var a := [8, 6, "a"]
            for i in (a):
                traceln(i)
            a := a + ["b"]
            a.slice(0, 2)
            

    assert.equal(example.test(), [8, 6])


def testquick_ref_15(assert):
    object example:
        method test():
            "doc"
            def m := ["c" => 5]
            m["c"]
            

    assert.equal(example.test(), 5)


def testquick_ref_16(assert):
    object example:
        method test():
            "doc"
            ["c" => 5].size()
            

    assert.equal(example.test(), 1)


def testquick_ref_17(assert):
    object example:
        method test():
            "doc"
            def m := ["c" => 5]
            for key => value in (m):
                traceln(value)
            def flexM := m.diverge()
            

    assert.equal(example.test(), ["c" => 5].diverge())


def testquick_ref_18(assert):
    object example:
        method test():
            "doc"
            def flexA := [8, 6, "a", "b"].diverge()
            flexA.extend(["b"])
            flexA.push("b")
            def constA := flexA.snapshot()
            

    assert.equal(example.test(), [8, 6, "a", "b", "b", "b"])


def testquick_ref_19(assert):
    object example:
        method test():
            "doc"
            def m := ["c" => 5]
            def flexM := m.diverge()
            flexM["b"] := 2
            flexM.removeKey("b")
            def constM := flexM.snapshot()
            

    assert.equal(example.test(), ["c" => 5])


def testquick_ref_20(assert):
    object example:
        method test():
            "doc"
            def abacus := object mock {}
            
            abacus <- add(1, 2)
            
            def answer := abacus <- add(1, 2)
            when (answer) ->
                traceln(`computation complete: $answer`)
            catch problem:
                traceln(`promise broken $problem `)
            finally:
                traceln("always")
            

    assert.equal(example.test(), null)


def testquick_ref_21(assert):
    object example:
        method test():
            "doc"
            def makeCarRcvr := object mock {}
            
            def carRcvr := makeCarRcvr <- ("Mercedes")
            Ref.whenBroken(carRcvr, def lost(brokenRef) {
                traceln("Lost connection to carRcvr")
            })
            def [resultVow, resolver] := Ref.promise()
            when (resultVow) -> {
                traceln(resultVow)
            } catch prob {
                traceln(`oops: $prob`)
            }
            resolver.resolve("this text is the answer")
            

    assert.equal(example.test(), true)


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

def testruntime_0(assert):
    object example:
        method test():
            "doc"
            [true, false, null, NaN, Infinity]
            

    assert.equal(example.test(), [true, false, null, NaN, Infinity])


def testruntime_1(assert):
    object example:
        method test():
            "doc"
            M.call(1, "add", [2])
            

    assert.equal(example.test(), 3)


def testruntime_2(assert):
    object example:
        method test():
            "doc"
            throw
            

    assert.equal(example.test(), throw)


def testruntime_3(assert):
    object example:
        method test():
            "doc"
            def l := [].diverge()
            _loop([1,2,3], fn k, v { l.push(v) })
            l.snapshot()
            

    assert.equal(example.test(), [1, 2, 3])


def testruntime_4(assert):
    object example:
        method test():
            "doc"
            trace("str")
            

    assert.equal(example.test(), null)


def testruntime_5(assert):
    object example:
        method test():
            "doc"
            traceln("str")
            

    assert.equal(example.test(), null)


def testruntime_6(assert):
    object example:
        method test():
            "doc"
            _makeList(1, 2, 3)
            

    assert.equal(example.test(), [1, 2, 3])


def testruntime_7(assert):
    object example:
        method test():
            "doc"
            _makeMap.fromPairs([['k', 'v']])
            

    assert.equal(example.test(), ['k' => 'v'])


def testruntime_8(assert):
    object example:
        method test():
            "doc"
            _makeInt("1")
            

    assert.equal(example.test(), 1)


def testruntime_9(assert):
    object example:
        method test():
            "doc"
            [_makeFinalSlot, _makeVarSlot]
            

    assert.equal(example.test(), [_makeFinalSlot, _makeVarSlot])


def testruntime_10(assert):
    object example:
        method test():
            "doc"
            _makeOrderedSpace
            

    assert.equal(example.test(), _makeOrderedSpace)


def testruntime_11(assert):
    object example:
        method test():
            "doc"
            [Any, Void]
            

    assert.equal(example.test(), [Any, Void])


def testruntime_12(assert):
    object example:
        method test():
            "doc"
            [Bool, Str, Char, Double, Int]
            

    assert.equal(example.test(), [Bool, Str, Char, Double, Int])


def testruntime_13(assert):
    object example:
        method test():
            "doc"
            [List, Map, Set]
            

    assert.equal(example.test(), [List, Map, Set])


def testruntime_14(assert):
    object example:
        method test():
            "doc"
            "abc" :NullOk[Str]
            

    assert.equal(example.test(), "abc")


def testruntime_15(assert):
    object example:
        method test():
            "doc"
            [_makeMessageDesc, _makeParamDesc, _makeProtocolDesc]
            

    assert.equal(example.test(), [_makeMessageDesc, _makeParamDesc, _makeProtocolDesc])


def testruntime_16(assert):
    object example:
        method test():
            "doc"
            [simple__quasiParser, m__quasiParser]
            

    assert.equal(example.test(), [simple__quasiParser, m__quasiParser])


def testruntime_17(assert):
    object example:
        method test():
            "doc"
            simple`sum: ${1+1}`
            

    assert.equal(example.test(), "sum: 2")


def testruntime_18(assert):
    object example:
        method test():
            "doc"
            m`1 + 1`.expand()
            

    assert.equal(example.test().canonical(), m`1.add(1)`.canonical())


def testruntime_19(assert):
    object example:
        method test():
            "doc"
            [_accumulateList, _accumulateMap]
            

    assert.equal(example.test(), [_accumulateList, _accumulateMap])


def testruntime_20(assert):
    object example:
        method test():
            "doc"
            _bind
            

    assert.equal(example.test(), _bind)


def testruntime_21(assert):
    object example:
        method test():
            "doc"
            [_booleanFlow, _comparer, _equalizer]
            

    assert.equal(example.test(), [_booleanFlow, _comparer, _equalizer])


def testruntime_22(assert):
    object example:
        method test():
            "doc"
            [_mapEmpty, _mapExtract]
            

    assert.equal(example.test(), [_mapEmpty, _mapExtract])


def testruntime_23(assert):
    object example:
        method test():
            "doc"
            [_matchSame, _quasiMatcher]
            

    assert.equal(example.test(), [_matchSame, _quasiMatcher])


def testruntime_24(assert):
    object example:
        method test():
            "doc"
            _slotToBinding
            

    assert.equal(example.test(), _slotToBinding)


def testruntime_25(assert):
    object example:
        method test():
            "doc"
            [_splitList, _suchThat]
            

    assert.equal(example.test(), [_splitList, _suchThat])


def testruntime_26(assert):
    object example:
        method test():
            "doc"
            _switchFailed
            

    assert.equal(example.test(), _switchFailed)


def testruntime_27(assert):
    object example:
        method test():
            "doc"
            _validateFor
            

    assert.equal(example.test(), _validateFor)


unittest([
    testruntime_0,
    testruntime_1,
    testruntime_2,
    testruntime_3,
    testruntime_4,
    testruntime_5,
    testruntime_6,
    testruntime_7,
    testruntime_8,
    testruntime_9,
    testruntime_10,
    testruntime_11,
    testruntime_12,
    testruntime_13,
    testruntime_14,
    testruntime_15,
    testruntime_16,
    testruntime_17,
    testruntime_18,
    testruntime_19,
    testruntime_20,
    testruntime_21,
    testruntime_22,
    testruntime_23,
    testruntime_24,
    testruntime_25,
    testruntime_26,
    testruntime_27
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


# taste

def testtaste_0(assert):
    object example:
        method test():
            "doc"
            def helloWeb(request) { def reply := [200]; return reply }
            helloWeb("/")
            

    assert.equal(example.test(), [200])


def testtaste_1(assert):
    object example:
        method test():
            "doc"
            def helloWeb(request):
                def reply := [200]
                return reply
            helloWeb("/page1")
            

    assert.equal(example.test(), [200])


unittest([
    testtaste_0,
    testtaste_1
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

def testwizard_0(assert):
    object example:
        method test():
            "doc"
            m`1 + 1`.expand()
            

    assert.equal(example.test().canonical(), m`1.add(1)`.canonical())


unittest([
    testwizard_0
])

