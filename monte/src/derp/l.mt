def consToList := import("hands.consToList")
def [makeDerp, ex, oneOf] := import("derp")
def ["oneOrMore" => oneOrMore] | _ := import("derp.combiners")
# def convertToTerm := import ("terml.convertToTerm")
# def makeTag := import ("terml.makeTag")

def letter := oneOf("abcdefghijklmnoprstuvwxyzABCDEFHIJKLMNOPQRSUVWXYZ")

def identifier := oneOrMore(letter | ex('_')) % consToList

def count(l):
    return l.size()

def space := ex(' ')
def spaces := oneOrMore(space) % consToList % count
def nl := ex('\n')

def colon := ex(':')

var lexer := identifier | spaces | nl | colon
lexer := lexer.repeated() % consToList
lexer := lexer.compacted()

traceln(`Lexer: $lexer, size ${lexer.size()}`)
def lexed := identifier.feedMany("object").results()
traceln(`Results: $lexed`)
#def lexed := lexer.feedMany("object test:\n return null").results()
#traceln(`Results: $lexed`)
