def quadruple():
    trace("3... ")
    def triple():
        trace("2... ")
        def double():
            trace("1... ")
            def single():
                traceln("boom!")
            return single
        return double
    return triple

quadruple()()()()
