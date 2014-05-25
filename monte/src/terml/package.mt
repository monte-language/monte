def files := pkg.readFiles(".")
def unittest := pkg.testCollector()

def [=> Tag, => makeTag] := files["tag"]()
def [=> Term, => makeTerm] := files["term"]([=> Tag])
def [=> convertToTerm] := files["convertToTerm"]([=> makeTerm, => Term,
                                                  => makeTag])
def [=> termFactory] := files["termFactory"]([=> makeTerm, => makeTag,
                                              => convertToTerm])

def terml := pkg.makeModule([=> Tag, => Term, => makeTag, => makeTerm,
                             => termFactory])
terml
