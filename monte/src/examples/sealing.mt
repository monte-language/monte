module unittest
export (makeBrandPair)

/** makeBrandPair -- Rights Amplification
 cf http://www.erights.org/elib/capability/ode/ode-capabilities.html#rights-amp
 cribbed from wiki.erights.org/wiki/Walnut/Secure_Distributed_Computing/Capability_Patterns#Sealers_and_Unsealers
 */
def makeBrandPair(nickname):
    object noObject:
        pass

    var shared := noObject

    def makeSealedBox(obj):
        object box:
            to shareContent():
                shared := obj
            to _printOn(t):
                t.print(`<$nickname sealed box>`)
        return box

    object sealer:
        to seal(obj):
            return makeSealedBox(obj)

        to _printOn(t):
            t.print(`<$nickname sealer>`)

    object unsealer:
        to unseal(box):
            shared := noObject
            box.shareContent()
            if (shared == noObject):
                throw("invalid box")
            def contents := shared
            shared := noObject
            return contents
        to _printOn(t):
            t.print(`<$nickname unsealer>`)

    return [sealer, unsealer]


def t(assert):
    def happy():
        def [s, u] := makeBrandPair("bob")
        assert.equal(`$s`, "<bob sealer>")
        assert.equal(`$u`, "<bob unsealer>")

        def x := s.seal("abc")
        assert.equal(`$x`, "<bob sealed box>")
        assert.equal(u.unseal(x), "abc")

    def evil():
        def [s, u] := makeBrandPair("bob")
        def x := s.seal("abc")

        def [ss, uu] := makeBrandPair("evil")

        assert.raises(def _(fail){
            uu.unseal(x)
        })

    return [happy, evil]

unittest([t])
