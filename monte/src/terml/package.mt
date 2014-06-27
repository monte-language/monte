def files := pkg.readFiles(".")
def unittest := pkg.testCollector()

def [=> Tag, => makeTag] := files["tag"]([=> unittest])
def [=> Term, => makeTerm] := files["term"]([=> Tag])
def [=> convertToTerm] := files["convertToTerm"]([=> makeTerm, => Term,
                                                  => makeTag, => unittest])
def [=> termFactory] := files["termFactory"]([=> makeTerm, => makeTag,
                                              => convertToTerm])
def [=> baseSchema] := files["schema"]([=> convertToTerm, => termFactory,
                                        => unittest])

def terml := pkg.makeModule([=> Tag, => Term, => baseSchema, => makeTag,
                             => makeTerm, => termFactory])
terml
