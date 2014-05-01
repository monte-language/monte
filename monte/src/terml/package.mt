def mos := pkg.require("__makeOrderedSpace")
def files := pkg.loadFiles(".")
def unittest := pkg.testCollector()

def [=> Tag, => makeTag] := files["tag"]()
def [=> makeLexer] := files["lexer"](mos)
def [=> Term, => makeTerm] := files["term"](Tag)
def [=> convertToTerm] := files["convertToTerm"](makeTerm, Term, makeTag)
def [=> readHole, => value, => pattern] := files["readHole"](unittest)
def [=> termFactory] := files["termFactory"](makeTerm, makeTag, convertToTerm)

def terml := pkg.makeModule([=> Tag, => Term, => makeTag, => makeTerm,
                             => termFactory])
terml
