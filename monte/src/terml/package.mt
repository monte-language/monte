def files := pkg.readFiles(".")
def unittest := pkg.testCollector()

def [=> Tag, => makeTag] := files["tag"]([=> unittest])
def [=> Term, => makeTerm] := files["term"]([=> Tag])
def [=> convertToTerm] := files["convertToTerm"]([=> makeTerm, => Term,
                                                  => makeTag, => unittest])
def [=> termFactory] := files["termFactory"]([=> makeTerm, => makeTag,
                                              => convertToTerm])
def [=> makeTermLexer] := files["termLexer"]([=> makeTag, => makeTerm, => unittest])
def [=> parseTerm, => term__quasiParser] := files["termParser"]([
    => makeTag, => makeTerm, => makeTermLexer, => convertToTerm, => unittest])
def terml := pkg.makeModule([=> Tag, => Term, => makeTag,
                             => makeTerm, => termFactory, => makeTermLexer,
                             => parseTerm])
terml
