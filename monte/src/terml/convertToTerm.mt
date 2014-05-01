module makeTerm, Term, makeTag
export (convertToTerm)

def mkt(name, data, args) as DeepFrozen:
    return makeTerm(makeTag(null, name, null), data, args, null)

def convertToTerm(val, ej) as DeepFrozen:
    switch (val):
        match _ :Term:
            return val
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
        match v :str:
            return mkt(".String.", v, null)
        match v :char:
            return mkt(".char.", v, null)
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
