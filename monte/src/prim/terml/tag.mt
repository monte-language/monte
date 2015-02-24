module unittest
export (Tag, makeTag, optMakeTagFromData)

interface Tag :DeepFrozen guards TagStamp :DeepFrozen:
    pass

object makeTag as DeepFrozen:
    to asType():
        return Tag
    to run(code :nullOk[int], name :str, dataGuard :DeepFrozen):
        return object tag implements Selfless, Transparent, TagStamp:
            to _uncall():
                return [makeTag, "run", [code, name, dataGuard]]

            to _printOn(out):
                out.print("<")
                out.print(name)
                if (code != null):
                    out.print(":")
                    out.print(code)
                if (dataGuard != null):
                    out.print(":")
                    out.print(dataGuard)
                out.print(">")

            to getCode():
                return code

            to getName():
                return name

            to getDataGuard():
                return dataGuard

            to isTagForData(data) :boolean:
                if (data == null):
                    return true
                if (dataGuard == null):
                    return false

                return data =~ _ :dataGuard

            to op__cmp(other):
                return name.op__cmp(other.getName())

def optMakeTagFromData(val, mkt):
    switch (val):
        match ==null:
            return mkt("null", null)
        match ==true:
            return mkt("true", null)
        match ==false:
            return mkt("false", null)
        match v :int:
            return mkt(".int.", v)
        match v :float:
            return mkt(".float64.", v)
        match v :str:
            return mkt(".String.", v)
        match v :char:
            return mkt(".char.", v)
        match _:
            return null

def testPrint(assert):
    def t1 := makeTag(1, "foo", int)
    assert.equal(M.toString(t1), "<foo:1:int>")

    def t2 := makeTag(null, "foo", null)
    assert.equal(M.toString(t2), "<foo>")

unittest([testPrint])
