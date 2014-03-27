def makeTerm := import("terml.makeTerm")
def makeTag := import("terml.makeTag")

#XXX obviously bad, replace with interface/guard
def TermType := unsafeType(makeTerm(makeTag(null, "x", null), null, null, null))

def mkt(name, data, args):
    return makeTerm(makeTag(null, name, null), data, args, null)

def convertToTerm(val, ej):
    switch (val):
        match v ? (unsafeType(v) == TermType):
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
        match v :list:
            return mkt(".tuple.", null, [convertToTerm(item) for item in v])
        # match v :set:
        #   return mkt(".bag.", null, [convertToTerm(item) for item in v])
        match m :map:
            return mkt(".bag.", null,
                       [mkt(".attr.", null, [convertToTerm(k), convertToTerm(v)])
                        for k => v in m])
        match _:
            throw.eject(ej, `Could not coerce $val to term`)
