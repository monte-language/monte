def unittest := pkg.testCollector()
def files := pkg.readFiles(".")

def [=> OrderedSpaceMaker,
     => OrderedRegionMaker] := files["regions"]([=> unittest])

def [=> __makeOrderedSpace,
     => charSpace,
     => intSpace,
     => floatSpace] := files["primSpaces"]([=> OrderedSpaceMaker])

#all this should go in terml/package.mt probably
def terml_files := pkg.readFiles("./terml")
def [=> Tag, => makeTag, => optMakeTagFromData] := terml_files["tag"]([=> unittest])
def [=> Term, => makeTerm, => termBuilder] := terml_files["term"]([=> Tag, => makeTag, => optMakeTagFromData])
def [=> convertToTerm] := terml_files["convertToTerm"]([=> makeTerm, => Term,
                                                  => makeTag, => optMakeTagFromData, => unittest])
def [=> termFactory] := terml_files["termFactory"]([=> makeTerm, => makeTag, => optMakeTagFromData,
                                              => convertToTerm])
def [=> makeTermLexer] := terml_files["termLexer"]([=> __makeOrderedSpace, => makeTag, => makeTerm, => termBuilder, => unittest])
def [=> makeQFunctor, => makeQTerm, => makeQSome, => makeQDollarHole, => makeQAtHole, => qEmptySeq, => makeQPairSeq] := terml_files["quasiterm"]([=> __makeOrderedSpace, => convertToTerm, => makeTerm, => makeTag, => termBuilder, => Term, => optMakeTagFromData])
def [=> parseTerm, => quasitermParser] := terml_files["termParser"]([
    => __makeOrderedSpace, => makeTag, => makeTerm, => makeTermLexer, => convertToTerm, => makeQFunctor, => makeQTerm, => makeQSome, => makeQDollarHole, => makeQAtHole, => qEmptySeq, => makeQPairSeq, => termBuilder, => optMakeTagFromData, => unittest])

pkg.makeModule([
    => __makeOrderedSpace,
    "Char" => charSpace,
    "Int" => intSpace,
    "Double" => floatSpace,
    "term__quasiParser" => quasitermParser,
    ])
