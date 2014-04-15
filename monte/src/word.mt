def _makeGuard(mod):
    return object ModGuard:
        to coerce(x, ej) :any:
            if (x =~ i :int):
                return i %% mod
            else:
                throw.eject(ej, `Not an integer: $x`)
        to makeSlot(x :ModGuard) :any:
            var v := x
            return object slot:
                to getValue() :any:
                    return v
                to setValue(x :ModGuard) :void:
                    v := x

object Word:
    to get(width):
        def mod := 2 ** width
        return _makeGuard(mod)

object Mod:
    to get(mod):
        return _makeGuard(mod)

def testWord(assert):
    def word8Final():
        def fortyTwo :Word[8] := 42
        assert.equal(fortyTwo, 42)
    def word8FinalOverflow():
        def fortyTwo :Word[8] := 42 + 256
        assert.equal(fortyTwo, 42)
    def mod13Final():
        def twelve :Mod[13] := 12
        assert.equal(twelve, 12)
    def mod13FinalOverflow():
        def twelve :Mod[13] := 25
        assert.equal(twelve, 12)
    return [
        word8Final,
        word8FinalOverflow,
        mod13Final,
        mod13FinalOverflow,
    ]

def unittest := import("unittest")
unittest([
    testWord,
])

Word
