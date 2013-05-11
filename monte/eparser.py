# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.
import string
from parsley import ParseError, makeGrammar

from terml.nodes import termMaker as t

egrammar = r"""
hspace = (' '|'\t'|'\f'|('#' (~eol anything)*))
ws = ('\r' '\n'|'\r' | '\n' | hspace)*

number = ws barenumber
barenumber = '-'?:sign ('0' (('x'|'X') <hexdigit*>:hs
                                        -> int((sign or '') + hs, 16)
                        |floatPart(sign '0')
                        |<octaldigit*>:ds -> int((sign or '') + '0' + ds, 8))
               |decdigits:ds floatPart(sign ds)
               |decdigits:ds -> int((sign or '') + ds))

exponent = <('e' | 'E') ('+' | '-')? decdigits>
floatPart :sign :ds = <('.' decdigits exponent?) | exponent>:tail
                    -> float((sign or '') + ds + tail)
decdigits = digit:d ((:x ?(x.isdigit()) -> x) | '_' -> "")*:ds
          -> d + ''.join(ds)
octaldigit = :x ?(x in string.octdigits) -> x
hexdigit = :x ?(x in string.hexdigits) -> x

string = ws '"' (escapedChar | ~('"') anything)*:c '"' -> ''.join(c)
character = ws '\'' (escapedChar | ~('\''|'\n'|'\r'|'\\') anything):c '\''
          -> t.Character(c)
escapedUnicode = ('u' <hexdigit hexdigit hexdigit hexdigit>:hs
                -> unichr(int(hs, 16))
               |'U' <hexdigit hexdigit hexdigit hexdigit
                     hexdigit hexdigit hexdigit hexdigit>:hs
                -> unichr(int(hs, 16)))

escapedOctal = ( <:a ?(a in "0123") octdigit? octdigit?>
                 | <:a ?(a in "4567") octdigit?>):os -> int(os, 8)

escapedChar = '\\' ('n' -> '\n'
                     |'r' -> '\r'
                     |'t' -> '\t'
                     |'b' -> '\b'
                     |'f' -> '\f'
                     |'"' -> '"'
                     |'\'' -> '\''
                     |'?' -> '?'
                     |'\\' -> '\\'
                     | escapedUnicode
                     | escapedOctal
                     | eol -> "")

eol = hspace* ('\r' '\n'|'\r' | '\n')

uriBody = <(letterOrDigit|'_'|';'|'/'|'?'|':'|'@'|'&'|'='|'+'|'$'|','|'-'|'.'
            |'!'|'~'|'*'|'\''|'('|')'|'%'|'\\'|'|'|'#')+>


updocLine = <('?'|'#'|'>') (~('\n' | '\r') anything)*>:txt eol -> txt
updoc = ('?' (~('\n' | '\r') anything)*
             ((eol (eol | updocLine)*) (spaces | updocLine))?
        )

eolplus = eol updoc?
linesep = eolplus+

br = (spaces eolplus | eolplus)*

literal = (string | character | number):x -> t.LiteralExpr(x)
identifier = spaces <(letter | '_') (letterOrDigit | '_')*>
uri = "<" uriScheme:s ':' uriBody:b '>' -> t.URIExpr(s, b)
uriGetter = "<" uriScheme:s '>' -> t.URIGetter(s)
uriScheme = <letter (letterOrDigit | '_' | '+' | '-' | '.')*>

noun = sourceHole | justNoun
justNoun = ((identifier:id -> self.keywordCheck(id)
              | ("::" (string | identifier):x -> x)):n  -> t.NounExpr(n)
              | uriGetter)
sourceHole = ("$" (-> self.valueHole()):v '{' digit+:ds '}'
              -> t.QuasiLiteralExpr(v)
               |"@" (-> self.patternHole()):v '{' digit+:ds '}'
              -> t.QuasiPatternExpr(v))

quasiString = "`" (exprHole | pattHole | quasiText)*:qs '`' -> qs

quasiText = <(~('`'|'$'|'@') anything | '`' '`' | '$' '$'
            | ('$' | '@') '\\' escapedChar | '@' '@')+>:qs
          -> t.QuasiText(qs.replace("``", "`"))

exprHole = '$' ('{' br seq:s '}' -> t.QuasiExprHole(s)
                 |'_' !(noIgnoreExpressionHole())
                 |identifier:n !(exprHoleKeywordCheck(n))
         -> t.QuasiExprHole(t.NounExpr(n)))
pattHole = '@' ('{' br pattern:s '}' -> t.QuasiPatternHole(s)
                 |'_' !(noIgnorePatternHole())
                 |identifier:n !(quasiHoleKeywordCheck(n))
                  -> t.QuasiPatternHole(t.FinalPattern(t.NounExpr(n), None)))

reifyExpr = ("&&" verb:v -> t.BindingExpr(v)
            |"&" verb:v -> t.SlotExpr(v))

verb = identifier | string

listAndMap = "[" (assoc:x ("," assoc)*:xs ","? ']' -> t.MapExpr([x] + xs)
                   |(seq:s ("," seq)*:ss ","? ']')-> t.ListExpr([s] + ss)
                   | ']' -> t.ListExpr([]))
assoc = (seq:k "=>" seq:v -> t.MapExprAssoc(k, v)
          |"=>" (noun | reifyExpr):n -> t.MapExprExport(n)
                | "def" noun:n ~":="
                  !(throwSemanticHere("Reserved syntax: forward export")))


prim = ( literal
         | basic
         | identifier?:n quasiString:qs -> t.QuasiExpr(n, qs)
         | noun
         | uri
         | parenExpr:p (quasiString:qs -> t.QuasiExpr(p, qs)
                         | -> p)
         | block:b -> t.HideExpr(b)
         | listAndMap
         )

parenExpr = "(" seq:s ws ')' -> s
block = "{" (seq |-> t.SeqExpr([])):s ws '}' -> s

seqSep = (";"| linesep)+
seq = expr:e ((seqSep expr)+:es seqSep? -> t.SeqExpr(filter(None, [e] + es))
                 |seqSep? -> e)
parenArgs = "(" args:a ws ')' -> a
args = (seq:s ("," seq)*:ss -> [s] + ss
         |-> [])

call = (call:c ("." verb:v (parenArgs:x -> t.MethodCallExpr(c, v, x)
                                  | -> t.VerbCurryExpr(c, v))
                    |"[" args:a ws ']' -> t.GetExpr(c, a)
                    |parenArgs:x -> t.FunctionCallExpr(c, x)
                    | "<-" (parenArgs:x -> t.FunctionSendExpr(c, x)
                           |verb:v (parenArgs:x -> t.MethodSendExpr(c, v, x)
                                     | -> t.SendCurryExpr(c, v)))
                    )
         |prim
         )

prefix = (call
           | "-" call:c -> t.Minus(c)
           | "!" call:c -> t.LogicalNot(c)
           | "~" call:c -> t.BinaryNot(c)
           | reifyExpr
           | "&" call !(throwSemanticHere("reserved: unary prefix '&' applied to non-noun lValue")))

pow = prefix:x ("**" prefix:y -> t.Pow(x, y)
                   | -> x)
mult = (mult:x ("*" pow:y -> t.Multiply(x, y)
                 |"/" pow:y -> t.Divide(x, y)
                 |"//" pow:y -> t.FloorDivide(x, y)
                 |"%" pow:y -> t.Remainder(x, y)
                 |"%%" pow:y -> t.Mod(x, y))
         |pow)

add = (add:x ("+" mult:y -> t.Add(x, y)
                 |"-" mult:y -> t.Subtract(x, y))
        | mult)

shift = (shift:x ("<<" add:y -> t.ShiftLeft(x, y)
                     |">>" add:y -> t.ShiftRight(x, y))
          |add)

interval = shift:x ("..!" shift:y -> t.Till(x, y)
                       |".." shift:y -> t.Thru(x, y)
                       | -> x)

order = interval:x (">" interval:y -> t.GreaterThan(x, y)
                       | ">=" interval:y -> t.GreaterThanEqual(x, y)
                       | "<=>" interval:y -> t.AsBigAs(x, y)
                       | "<=" interval:y -> t.LessThanEqual(x, y)
                       | "<" interval:y -> t.LessThan(x, y)
                       | ":" guard:g -> t.Coerce(x, g)
                       | -> x)

logical = (band
            |bor
            |(order:x ("=~" pattern:p -> t.MatchBind(x, p)
                        |"!~" pattern:p -> t.Mismatch(x, p)
                        |"==" order:y -> t.Same(x, y)
                        |"!=" order:y -> t.NotSame(x, y)
                        |"&!" order:y -> t.ButNot(x, y)
                        |"^" order:y -> t.BinaryXor(x, y)
                        | -> x)))

band = (band:x ~("&&" | "&!") "&" order:y -> t.BinaryAnd(x, y)
         |order:x ~("&&" | "&!") "&" order:y -> t.BinaryAnd(x, y))

bor = (bor:x "|" order:y -> t.BinaryOr(x, y)
        |order:x "|" order:y -> t.BinaryOr(x, y))

condAnd = logical:x (("&&" condAnd):y -> t.LogicalAnd(x, y)
                        | -> x)
cond = condAnd:x (("||" cond):y -> t.LogicalOr(x, y)
                     | -> x)
assign = (~objectExpr "def" (pattern:p ("exit" order)?:e ":=" assign:a -> t.Def(p, e, a)
                  |noun:n (~~seqSep | end)-> t.Forward(n))
           |keywordPattern:p ":=" assign:a -> t.Def(p, None, a)
           |cond:x (":=" assign:y -> t.Assign(x, y)
                    |assignOp:o assign:y -> t.AugAssign(o, x, y)
                    |identifier:v '=' (parenArgs:y -> t.VerbAssign(v, x, y)
                                        |assign:y -> t.VerbAssign(v, x, [y]))
                    | -> x))

assignOp = ("+=" -> "Add"
             |"-=" -> "Subtract"
             |"*=" -> "Multiply"
             |"/=" -> "Divide"
             |"%=" -> "Remainder"
             |"%%=" -> "Mod"
             |"**=" -> "Pow"
             |"//=" -> "FloorDivide"
             |">>=" -> "ShiftRight"
             |"<<=" -> "ShiftLeft"
             |"&=" -> "BinaryAnd"
             |"|=" -> "BinaryOr"
             |"^=" -> "BinaryXor")

expr =  assign | ejector
ejector = ws ('break' -> t.Break
             | 'continue' -> t.Continue
             | 'return' -> t.Return):ej
             (("(" ws ')' -> None) | assign)?:val -> ej(val)

guard = (noun | parenExpr):e ("[" args:x ws ']' -> x)*:xs -> t.Guard(e, xs)
optGuard = (":" guard)?
eqPattern = (ws '_' ~(letterOrDigit | '_') optGuard:e -> t.IgnorePattern(e)
              |identifier?:n quasiString:q -> t.QuasiPattern(n, q)
              |namePattern
              |"==" prim:p -> t.SamePattern(p)
              |"!=" prim:p -> throwSemanticHere("reserved: not-same pattern")
              )

patterns = (pattern:p ("," pattern)*:ps -> [p] + ps
             | -> [])
key = (parenExpr | literal):x br -> x

keywordPattern = (ws 'var' noun:n optGuard:g -> t.VarPattern(n, g)
                   |ws 'bind' noun:n optGuard:g -> t.BindPattern(n, g))
namePattern = (keywordPattern
              |noun:n optGuard:g -> t.FinalPattern(n, g)
              |reifyPattern)

reifyPattern = ("&&" noun:n optGuard:g -> t.BindingPattern(n, g)
               |"&" noun:n optGuard:g -> t.SlotPattern(n, g))

mapPatternAddressing = (key:k "=>" pattern:v -> t.MapPatternAssoc(k, v)
                         |"=>" namePattern:p -> t.MapPatternImport(p))

mapPattern = mapPatternAddressing:a (":=" order:d -> t.MapPatternOptional(a, d)
                                        | -> t.MapPatternRequired(a))
mapPatts = mapPattern:m ("," mapPattern)*:ms -> [m] + ms

listPatternInner = (mapPatts:ms br ws ']' ("|" listPattern)?:tail -> t.MapPattern(ms, tail)
                     |patterns:ps br ws ']' ("+" listPattern)?:tail -> t.ListPattern(ps, tail))
listPattern = (
                "via" parenExpr:e listPattern:p -> t.ViaPattern(e, p)
                | eqPattern
                | "[" listPatternInner)
pattern = listPattern:p ("?" order:e -> t.SuchThatPattern(p, e)
                            | -> p)

basic = docoDef | accumExpr | escapeExpr | forExpr | ifExpr | lambdaExpr | metaExpr | switchExpr | tryExpr | whileExpr | whenExpr

docoDef = doco?:doc (objectExpr:o -> t.Object(doc, *o)
                       |interfaceExpr:i -> t.Interface(doc, *i))
doco = ws '/**' <(~('*' '/') anything)*>:doc '*' '/' -> doc.strip()
objectExpr = ((ws 'def' objectName:n) | keywordPattern:n) objectTail:tail -> [n, tail]
objectName = (ws '_' optGuard:e -> t.IgnorePattern(e)
               |namePattern)
objectTail = (functionTail
               |((ws 'extends' br order)?:e oAs?:g oImplements:oi scriptPair:s
                  -> t.Script(e, g, oi, *s)))
oAs = ws 'as' br order
oImplements = (ws 'implements' br order:x ("," order)*:xs -> [x] + xs
               | -> [])
functionTail = parenParamList:ps optResultGuard:g oImplements:fi block:b -> t.Function(ps, g, fi, b)
parenParamList = "(" (pattern:p ("," pattern)*:ps ws ')' -> [p] +  ps
                       | ws ')' -> [])
optResultGuard = (":" guard)?
scriptPair = "{" method*:methods matcher*:matchers ws '}' -> [methods, matchers]
method = (doco?:doc ((ws 'to' -> t.To) | ws 'method' -> t.Method):to verb?:v parenParamList:ps optResultGuard:g block:b -> to(doc, v, ps, g, b))
matcher = ws 'match' pattern:p block:b -> t.Matcher(p, b)

interfaceExpr = (ws 'interface' objectName:n iguards?:g ((multiExtends:es oImplements:oi iscript:s -> [n, g, es, oi, s])
                       |parenParamDescList:ps optGuard:rg -> [n, g, [], [], t.InterfaceFunction(ps, rg)]))
iguards = ws 'guards' pattern
multiExtends = ((ws 'extends' br order:x ("," order)*:xs -> [x] + xs)
                 | -> [])
iscript = "{" (messageDesc:m br -> m)*:ms ws '}' -> ms
messageDesc = (doco?:doc (ws 'to' | ws 'method'):to verb?:v parenParamDescList:ps optGuard:g
                -> t.MessageDesc(doc, to, v, ps, g))
paramDesc = (justNoun | (ws '_') -> None):n optGuard:g -> t.ParamDesc(n, g)
parenParamDescList = "(" paramDesc:p ("," paramDesc)*:ps ws ')' -> [p] +  ps

accumExpr = ws 'accum' call:c accumulator:a -> t.Accum(c, a)
accumulator = (((ws 'for' forPattern:p ws 'in' logical:a accumBody:b catcher?:c -> t.AccumFor(*(p + [a, b, c]))))
                |(ws 'if' parenExpr:e accumBody:a -> t.AccumIf(e, a))
                |(ws 'while' parenExpr:e accumBody:a catcher?:c -> t.AccumWhile(e, a, c)))

accumBody = "{" (ws '_' (accumOp:op assign:a -> t.AccumOp(op, a)
                               |"." verb:v parenArgs:ps -> t.AccumCall(v, ps))
                  | accumulator):ab br ws '}' -> ab
accumOp = ("+" -> "Add"
            |"*" -> "Multiply"
            |"&" -> "BinaryAnd"
            |"|" -> "BinaryOr")

escapeExpr = ws 'escape' pattern:p block:b catcher?:c -> t.Escape(p, b, c)

forExpr = ws 'for' forPattern:p ws 'in' br assign:a block:b catcher?:c -> t.For(*(p + [a, b, c]))

forPattern = pattern:p (br "=>" pattern:px -> [p, px]
                           | -> [None, p])

ifExpr = ws 'if' parenExpr:p br block:b (ws 'else' (ifExpr | block) | -> None):e -> t.If(p, b, e)

lambdaExpr = doco?:doc ws 'fn' patterns:ps block:b -> t.Lambda(doc, ps, b)

metaExpr = ws 'meta' "." (ws 'getState' -> "State"
                                |ws 'scope' -> "Scope"
                                |ws 'context' -> "Context"):s "(" ws ')' -> t.Meta(s)
switchExpr = ws 'switch' parenExpr:e "{" (matcher:m br -> m)*:ms ws '}' -> t.Switch(e, ms)

tryExpr = ws 'try' block:tb catcher*:cs (ws 'finally' block)?:fb -> t.Try(tb, cs, fb)
catcher = ws 'catch' pattern:p block:b -> t.Catch(p, b)

whileExpr = ws 'while' parenExpr:e block:b catcher?:c -> t.While(e, b, c)

whenExpr = ws 'when' parenArgs:a br "->" block:b catcher*:cs (ws 'finally' block)?:fb -> t.When(a, b, cs, fb)

topSeq = topExpr:x (seqSep topExpr)*:xs seqSep? -> t.SeqExpr([x] + xs)
pragma = ws 'pragma' "." verb:v "(" string:s ws ')' -> t.Pragma(v, s)
topExpr = (pragma -> t.NounExpr("null")) | expr
start = updoc? br topSeq?
"""


reserved = set(["delegate", "module", "abstract", "an", "as", "assert", "attribute",
           "be", "begin", "behalf", "belief", "believe", "believes", "case",
           "class", "const", "constructor", "declare", "default", "define",
           "defmacro", "delicate", "deprecated", "dispatch", "do", "encapsulate",
           "encapsulated", "encapsulates", "end", "ensure", "enum", "eventual",
           "eventually", "export", "facet", "forall", "function", "given",
           "hidden", "hides", "inline", "is", "know", "knows", "lambda", "let",
           "methods", "namespace", "native", "obeys", "octet", "oneway",
           "operator", "package", "private", "protected", "public",
           "raises", "reliance", "reliant", "relies", "rely", "reveal", "sake",
           "signed", "static", "struct", "suchthat", "supports", "suspect",
           "suspects", "synchronized", "this", "transient", "truncatable",
           "typedef", "unsigned", "unum", "uses", "using", "utf8", "utf16",
           "virtual", "volatile", "wstring"])
basicKeywords = set(["bind", "break", "catch", "continue", "def", "else", "escape", "exit",
           "extends", "finally", "fn", "for", "guards", "if", "implements", "in",
           "interface", "match", "meta", "method", "pragma", "return", "switch",
           "to", "try", "var", "via", "when", "while", "accum", "module", "on",
           "select", "throws", "thunk"])

keywords = reserved | basicKeywords
def quasiHoleKeywordCheck(n):
    if n in keywords:
        raise ValueError("Unexpected keyword %r in quasi hole" % (n,))
    else:
        return None

def exprHoleKeywordCheck(n):
    if n in keywords:
        raise ValueError("Unexpected keyword %r in quasi hole" % (n,))
    else:
        return None

def throwSemanticHere(arg):
    """
    Raise an error when invalid source is parsed.
    """
    raise ValueError(arg)

def noIgnorePatternHole():
    raise RuntimeError()

def noIgnoreExpressionHole():
    raise RuntimeError()


BaseEParser = makeGrammar(egrammar,  {}, "BaseEParser", unwrap=True)

class EParser(BaseEParser):
    """
    A parser for E.
    """
    
    def rule_tokenBR(self):
        """
        Match and return the given string, consuming any preceding or trailing
        whitespace.
        """
        tok, _ = self.input.head()

        m = self.input = self.input.tail()
        try:
            self.eatWhitespace()
            for c  in tok:
                self.exactly(c)
            _, e = self.apply("br")
            return tok, e
        except ParseError:
            self.input = m
            raise


    def keywordCheck(self, ident):
        """
        Ensure an identifier isn't a keyword or reserved word.
        """
        if ident in reserved:
            raise ParseError(self.input, self.input.position, ident + " is a reserved word")
        elif ident in basicKeywords:
            raise ParseError(self.input, self.input.position, ident + " is a keyword")
        else:
            return ident

    def valueHole(self):
        """
        Look up a value hole in the table and return its position.
        """
        try:
            return self.valueHoles.index(self.input.position - 1)
        except ValueError:
            raise ValueError("A literal $ is not meaningful in E source.")

    def patternHole(self):
        """
        Look up a pattern hole in the table and return its position.
        """
        try:
            return self.patternHoles.index(self.input.position - 1)
        except ValueError:
            raise ValueError("A literal @ is not meaningful in E source.")

EParser.globals = {}
EParser.globals.update(globals())
