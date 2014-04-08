def makeTerm := import("terml.makeTerm")
def makeTag := import("terml.makeTag")

#XXX obviously bad, replace with interface/guard
# def TermType := unsafeType(makeTerm(makeTag(null, "x", null), null, null, null))
interface Term:
    pass

def mkt(name, data, args):
    return makeTerm(makeTag(null, name, null), data, args, null)

def convertToTerm(val, ej):
    switch (val):
        match v :Term:
            return v
        match ==null:
            return mkt("null", null, null)
        match ==true:
            return mkt("true", null, null)
        match ==false:
            return mkt("false", null, null)
        match v :int:
            return mkt(".int.", v, null)
        match v :float:
            return mkt(".float.", v, null)
        match v :char:
            return mkt(".char.", v, null)
        match v :str:
            return mkt(".String.", v, null)
        match v :List:
            def l := [convertToTerm(item, ej) for item in v]
            return mkt(".tuple.", null, l)
        # match v :set:
        #   return mkt(".bag.", null, [convertToTerm(item) for item in v])
        match m :Map:
            return mkt(".bag.", null,
                       [mkt(".attr.", null, [convertToTerm(k, ej),
                       convertToTerm(v, ej)])
                        for k => v in m])
        match _:
            throw.eject(ej, `Could not coerce $val to term`)

[convertToTerm, Term]
