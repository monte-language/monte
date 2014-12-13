def files := pkg.readFiles(".")
def unittest := pkg.testCollector()

def [=> Tag, => makeTag, => optMakeTagFromData] := files["tag"]([=> unittest])
def [=> Term, => makeTerm, => termBuilder] := files["term"]([=> Tag, => makeTag, => optMakeTagFromData])
def [=> convertToTerm] := files["convertToTerm"]([=> makeTerm, => Term,
                                                  => makeTag, => optMakeTagFromData, => unittest])
def [=> termFactory] := files["termFactory"]([=> makeTerm, => makeTag, => optMakeTagFromData,
                                              => convertToTerm])
def [=> makeTermLexer] := files["termLexer"]([=> makeTag, => makeTerm, => termBuilder, => unittest])
def [=> makeQFunctor, => makeQTerm, => makeQSome, => makeQDollarHole, => makeQAtHole, => qEmptySeq, => makeQPairSeq] := files["quasiterm"]([=> convertToTerm, => makeTerm, => makeTag, => termBuilder, => Term, => optMakeTagFromData])
def [=> parseTerm, => term__quasiParser] := files["termParser"]([
    => makeTag, => makeTerm, => makeTermLexer, => convertToTerm, => makeQFunctor, => makeQTerm, => makeQSome, => makeQDollarHole, => makeQAtHole, => qEmptySeq, => makeQPairSeq, => termBuilder, => optMakeTagFromData, => unittest])
def terml := pkg.makeModule([=> Tag, => Term, => makeTag,
                             => makeTerm, => termFactory, => makeTermLexer,
                             => parseTerm])
terml
