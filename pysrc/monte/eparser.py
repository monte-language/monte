from pymeta.grammar import OMetaGrammar, OMeta
from pymeta.runtime import ParseError

from monte.nodes import (Character, LiteralExpr, URIExpr, URIGetter, NounExpr, QuasiLiteralExpr, QuasiPatternExpr, QuasiText, QuasiExprHole, QuasiPatternHole, Slot, MapExpr, ListExpr, MapExprAssoc, MapExprExport, QuasiExpr, HideExpr, SeqExpr, MethodCallExpr, VerbCurryExpr, GetExpr, FunctionCallExpr, FunctionSendExpr, MethodSendExpr, SendCurryExpr, Minus, LogicalNot, BinaryNot, Pow, Multiply, Divide, FloorDivide, Remainder, Mod, Add, Subtract, ShiftLeft, ShiftRight, Till, Thru, GreaterThan, GreaterThanEqual, AsBigAs, LessThanEqual, LessThan, Coerce, MatchBind, Mismatch, Same, NotSame, ButNot, BinaryOr, BinaryAnd, BinaryXor, LogicalAnd, LogicalOr, Def, Forward, Assign, AugAssign, VerbAssign, Break, Continue, Return, Guard, IgnorePattern, QuasiPattern, SamePattern, VarPattern, BindPattern, FinalPattern, SlotPattern, MapPatternAssoc, MapPatternImport, MapPatternOptional, MapPatternRequired, MapPattern, ListPattern, ViaPattern, SuchThatPattern, Interface, InterfaceFunction, MessageDesc, ParamDesc, Object, Script, Function, Matcher, To, Method, Catch, Accum, AccumFor, AccumIf, AccumWhile, AccumOp, AccumCall, Escape, For, If, Lambda, Meta, Switch, Try, While, When, Pragma)
import string

#first, make double quotes do tokens
metagrammar = """
string ::= <token '"'> (~('"') <anything>)*:c '"' => self.builder.apply("tokenBR", self.name, repr(''.join(c)))
"""
OMetaGrammarEx = OMetaGrammar.makeGrammar(metagrammar, {})
class OMetaEx(OMeta):
    metagrammarClass = OMetaGrammarEx

    def rule_tokenBR(self):
        """
        Match and return the given string, consuming any preceding or trailing whitespace.
        """
        tok = self.input.head()

        m = self.input = self.input.tail()
        try:
            self.eatWhitespace()
            for c in tok:
                self.exactly(c)
            self.apply("br")
            return tok
        except ParseError:
            self.input = m
            raise

egrammar = r"""
spaces ::= (' '|'\t'|'\f'|('#' (~<eol> <anything>)*))*

number ::= <spaces> <barenumber>
barenumber ::= ('0' (('x'|'X') <hexdigit>*:hs => int(''.join(hs), 16)
                    |<floatPart '0'>
                    |<octaldigit>*:ds => int('0'+''.join(ds), 8))
               |<decdigits>:ds <floatPart ds>
               |<decdigits>:ds => int(''.join(ds)))
floatPart :ds ::= ('.' <decdigits>:fs (<exponent>:e => float(ds+"."+fs+e)
                                                   | => float(ds+"."+fs))
                               | <exponent>:e => float(ds+e))
exponent ::= ('e' | 'E'):e ('+' | '-' | => ''):s <decdigits>:ds => e+s+ds
decdigits ::= <digit>:d ((:x ?(x in string.digits) => x) | '_' => '')*:ds => d + ''.join(ds)
octaldigit ::= :x ?(x in string.octdigits) => x
hexdigit ::= :x ?(x in string.hexdigits) => x

string ::= <token '"'> (<escapedChar> | ~('"') <anything>)*:c '"' => ''.join(c)
character ::= <token "'"> (<escapedChar> | ~('\''|'\n'|'\r'|'\\') <anything>):c '\'' => Character(c)
escapedChar ::= '\\' ('n' => "\n"
                     |'r' => "\r"
                     |'t' => "\t"
                     |'b' => "\b"
                     |'f' => "\f"
                     |'"' => '"'
                     |'\'' => "'"
                     |'?' => "?"
                     |'\\' => "\\"
                     | <escapedUnicode>
                     | <escapedOctal>
                     | <spaces> <eol> => '')
escapedUnicode ::= ('u' <hexdigit>:a <hexdigit>:b <hexdigit>:c <hexdigit>:d => unichr(int(a+b+c+d, 16))
                   |'U' (<hexdigit>:a <hexdigit>:b <hexdigit>:c <hexdigit>:d
                         <hexdigit>:e <hexdigit>:f <hexdigit>:g <hexdigit>:h => unichr(int(a+b+c+d+e+f+g+h, 16))))

escapedOctal ::= ((:a ?(a in '0123')) (<octdigit>:b  (<octdigit>:c (=> int(a+b+c, 8)) | (=> int(a+b, 8))| => int(a, 8)))
                 | :a ?(a in '4567') (<octdigit>:b (=> int(a+b, 8)) | => int(a, 8)))
updocLine ::= ('?'|'#'|'>'):y (~('\n' | '\r') <anything>)*:ys <eol> => [y] + ys
updoc ::= ('?' (~('\n' | '\r') <anything>)*:xs
              ((<eol> (<eol>
                      |<updocLine>)*)
              (<spaces> | <updocLine>))?)

eol ::= <spaces> ('\r' '\n'|'\r' | '\n')
eolplus ::= <eol> <updoc>?
linesep ::= <eolplus>+:xs => xs

br ::= (<spaces> <eolplus> | <eolplus>)*

literal ::= (<string> | <character> | <number>):x => LiteralExpr(x)

identifier ::= <spaces> (<letter> | '_'):x (<letterOrDigit> | '_')*:xs => x+''.join(xs)
uri ::= "<" <uriScheme>:s ':' <uriBody>:b '>' => URIExpr(s, b)
uriGetter ::= "<" <uriScheme>:s '>' => URIGetter(s)
uriScheme ::= <letter>:x (<letterOrDigit> | '_' | '+' | '-' | '.')*:xs => x+''.join(xs)
uriBody ::= (<letterOrDigit> |';'|'/'|'?'|':'|'@'|'&'|'='|'+'|'$'|','|'-'|'.'|'!'|'~'|'*'|'\''|'('|')'|'%'|'\\'|'|'|'#')+:x => ''.join(x)
noun ::= <sourceHole> | <justNoun>
justNoun ::= ((<identifier>:id => self.keywordCheck(id) and id
              | ("::" (<string> | <identifier>):x => x)):n  => NounExpr.fromSource(n)
              | <uriGetter>)
sourceHole ::= ("$" (=> self.valueHole()):v '{' <digit>+:ds '}' => QuasiLiteralExpr(v)
               |"@" (=> self.patternHole()):v '{' <digit>+:ds '}' => QuasiPatternExpr(v))

quasiString ::= "`" (<exprHole> | <pattHole> | <quasiText>)*:qs '`' => qs

quasiText ::= (~('`'|'$'|'@') <anything> | '`' '`' | '$' '$' | ('$' | '@') '\\' <escapedChar> | '@' '@')+:qs => QuasiText(''.join(qs))

exprHole ::= '$' ('{' <br> <seq>:s '}' => QuasiExprHole(s)
                 |'_' !(self.noIgnoreExpressionHole())
                 |<identifier>:n !(self.keywordError(n) if n in self.keywords else None) => QuasiExprHole(NounExpr(n)))
pattHole ::= '@' ('{' <br> <pattern>:s '}' => QuasiPatternHole(s)
                 |'_' !(self.noIgnorePatternHole())
                 |<identifier>:n !(self.throwSemanticHere("Unexpected keyword %r in quasi hole" % (n,)) if n in self.keywords else None) => QuasiPatternHole(FinalPattern(NounExpr(n), None)))

slotExpr ::= "&" <verb>:v => Slot(v)
verb ::= <identifier> | <string>

listAndMap ::= "[" (<assoc>:x ("," <assoc>)*:xs ","? ']' => MapExpr([x]+xs)
                   |(<seq>:s ("," <seq>)*:ss ","? ']')=> ListExpr([s]+ss)
                   | ']' => ListExpr([]))
assoc ::= (<seq>:k "=>" <seq>:v => MapExprAssoc(k, v)
          |"=>" (<noun> | <slotExpr>):n => MapExprExport(n)
                | "def" <noun>:n ~":=" !(self.throwSemanticHere("Reserved syntax: forward export")))


prim ::= ( <literal>
         | <basic>
         | <identifier>?:n <quasiString>:qs => QuasiExpr(n, qs)
         | <noun>
         | <uri>
         | <parenExpr>:p (<quasiString>:qs => QuasiExpr(p, qs)
                         | => p)
         | <block>:b => HideExpr(b)
         | <listAndMap>
         )

parenExpr ::= "(" <seq>:s <token ')'> => s
block ::= "{" (<seq> |=> SeqExpr([])):s <token '}'> => s

seqSep ::= (";"| <linesep>)+
seq ::= <expr>:e ((<seqSep> <expr>)+:es <seqSep>? => SeqExpr([e]+es)
                 |<seqSep>? => e)
parenArgs ::= "(" <args>:a <token ')'> => a
args ::= (<seq>:s ("," <seq>)*:ss => [s]+ss
         |=> [])

call ::= (<call>:c ("." <verb>:v (<parenArgs>:x => MethodCallExpr(c, v, x)
                                  | => VerbCurryExpr(c, v))
                    |"[" <args>:a <token ']'> => GetExpr(c, a)
                    |<parenArgs>:x => FunctionCallExpr(c, x)
                    | "<-" (<parenArgs>:x => FunctionSendExpr(c, x)
                           |<verb>:v (<parenArgs>:x => MethodSendExpr(c, v, x)
                                     | => SendCurryExpr(c, v)))
                    )
         |<prim>
         )

prefix ::= (<call>
           | "-" <call>:c => Minus(c)
           | "!" <call>:c => LogicalNot(c)
           | "~" <call>:c => BinaryNot(c)
           | <slotExpr>
           | "&" <call> !(self.throwSemanticHere("reserved: unary prefix '&' applied to non-noun lValue")))

pow ::= <prefix>:x ("**" <prefix>:y => Pow(x, y)
                   | => x)
mult ::= (<mult>:x ("*" <pow>:y => Multiply(x, y)
                 |"/" <pow>:y => Divide(x, y)
                 |"//" <pow>:y => FloorDivide(x, y)
                 |"%" <pow>:y => Remainder(x, y)
                 |"%%" <pow>:y => Mod(x, y))
         |<pow>)

add ::= (<add>:x ("+" <mult>:y => Add(x, y)
                 |"-" <mult>:y => Subtract(x, y))
        | <mult>)

shift ::= (<shift>:x ("<<" <add>:y => ShiftLeft(x, y)
                     |">>" <add>:y => ShiftRight(x, y))
          |<add>)

interval ::= <shift>:x ("..!" <shift>:y => Till(x, y)
                       |".." <shift>:y => Thru(x, y)
                       | => x)

order ::= <interval>:x (">" <interval>:y => GreaterThan(x, y)
                       | ">=" <interval>:y => GreaterThanEqual(x, y)
                       | "<=>" <interval>:y => AsBigAs(x, y)
                       | "<=" <interval>:y => LessThanEqual(x, y)
                       | "<" <interval>:y => LessThan(x, y)
                       | ":" <guard>:g => Coerce(x, g)
                       | => x)

logical ::= (<band>
            |<bor>
            |(<order>:x ("=~" <pattern>:p => MatchBind(x, p)
                        |"!~" <pattern>:p => Mismatch(x, p)
                        |"==" <order>:y => Same(x, y)
                        |"!=" <order>:y => NotSame(x, y)
                        |"&!" <order>:y => ButNot(x, y)
                        |"^" <order>:y => BinaryXor(x, y)
                        | => x)))

band ::= (<band>:x ~("&&" | "&!") "&" <order>:y => BinaryAnd(x, y)
         |<order>:x ~("&&" | "&!") "&" <order>:y => BinaryAnd(x, y))

bor ::= (<bor>:x "|" <order>:y => BinaryOr(x, y)
        |<order>:x "|" <order>:y => BinaryOr(x, y))

condAnd ::= <logical>:x (("&&" <condAnd>):y => LogicalAnd(x, y)
                        | => x)
cond ::= <condAnd>:x (("||" <cond>):y => LogicalOr(x, y)
                     | => x)
assign ::= (~<objectExpr> "def" (<pattern>:p ("exit" <order>)?:e ":=" <assign>:a => Def(p, e, a)
                  |<noun>:n (~~<seqSep> | <end>)=> Forward(n))
           |<keywordPattern>:p ":=" <assign>:a => Def(p, None, a)
           |<cond>:x (":=" <assign>:y => Assign(x, y)
                    |<assignOp>:o <assign>:y => AugAssign(o, x, y)
                    |<identifier>:v '=' (<parenArgs>:y => VerbAssign(v, x, y)
                                        |<assign>:y => VerbAssign(v, x, [y]))
                    | => x))

assignOp ::= ("+=" => "Add"
             |"-=" => "Subtract"
             |"*=" => "Multiply"
             |"/=" => "Divide"
             |"%=" => "Remainder"
             |"%%=" => "Mod"
             |"**=" => "Pow"
             |"//=" => "FloorDivide"
             |">>=" => "ShiftRight"
             |"<<=" => "ShiftLeft"
             |"&=" => "BinaryAnd"
             |"|=" => "BinaryOr"
             |"^=" => "BinaryXor")

expr ::=  <ejector> | <assign>
ejector ::= ((<token "break"> (=> Break) | <token "continue"> (=> Continue) | <token "return"> (=> Return)):ej
             (("(" <token ")"> => None) | <assign>)?:val => ej(val))

guard ::= (<noun> | <parenExpr>):e ("[" <args>:x <token ']'> => x)*:xs => Guard(e, xs)
optGuard ::= (":" <guard>)?
eqPattern ::= (<token '_'> <optGuard>:e => IgnorePattern(e)
              |<identifier>?:n <quasiString>:q => QuasiPattern(n, q)
              |<namePattern>
              |"==" <prim>:p => SamePattern(p)
              |"!=" <prim>:p => self.throwSemanticHere("reserved: not-same pattern")
              )

patterns ::= (<pattern>:p ("," <pattern>)*:ps =>[p] + ps
             | => [])
key ::= (<parenExpr> | <literal>):x <br> => x

keywordPattern ::= (<token "var"> <noun>:n <optGuard>:g => VarPattern(n, g)
                   |<token "bind"> <noun>:n <optGuard>:g => BindPattern(n, g))
namePattern ::= (<keywordPattern>
                |<noun>:n <optGuard>:g => FinalPattern(n, g)
                |"&" <noun>:n <optGuard>:g => SlotPattern(n, g))

mapPatternAddressing ::= (<key>:k "=>" <pattern>:v => MapPatternAssoc(k, v)
                         |"=>" <namePattern>:p => MapPatternImport(p))

mapPattern ::= <mapPatternAddressing>:a (":=" <order>:d => MapPatternOptional(a, d)
                                        | => MapPatternRequired(a))
mapPatts ::= <mapPattern>:m ("," <mapPattern>)*:ms => [m] + ms

listPatternInner ::= (<mapPatts>:ms <br> <token ']'> ("|" <listPattern>)?:t => MapPattern(ms, t)
                     |<patterns>:ps <br> <token ']'> ("+" <listPattern>)?:t => ListPattern(ps, t))
listPattern ::= (
                "via" <parenExpr>:e <listPattern>:p => ViaPattern(e, p)
                | <eqPattern>
                | "[" <listPatternInner>)
pattern ::= <listPattern>:p ("?" <order>:e => SuchThatPattern(p, e)
                            | => p)

basic ::= <docoDef> | <accumExpr> | <escapeExpr> | <forExpr> | <ifExpr> | <lambdaExpr> | <metaExpr> | <switchExpr> | <tryExpr> | <whileExpr> | <whenExpr>

docoDef ::= <doco>?:doc (<objectExpr>:o => Object(doc, *o)
                       |<interfaceExpr>:i => Interface(doc, *i))
doco ::= <token "/**"> (~('*' '/') <anything>)*:doc '*' '/' => ''.join(doc).strip()
objectExpr ::= ((<token "def"> <objectName>:n) | <keywordPattern>:n) <objectTail>:t => [n, t]
objectName ::= (<token '_'> <optGuard>:e => IgnorePattern(e)
               |<namePattern>)
objectTail ::= (<functionTail>
               |((<token "extends"> <br> <order>)?:e <oImplements>:oi <scriptPair>:s
                  => Script(e, oi, *s)))
oImplements ::= (<token "implements"> <br> <order>:x ("," <order>)*:xs => [x] + xs
                | => [])
functionTail ::= <parenParamList>:ps <optResultGuard>:g <oImplements>:fi <block>:b => Function(ps, g, fi, b)
parenParamList ::= "(" (<pattern>:p ("," <pattern>)*:ps <token ")"> => [p] + ps
                       | <token ")"> => [])
optResultGuard ::= (":" <guard>)?
scriptPair ::= "{" <method>*:methods <matcher>*:matchers <token "}"> => [methods, matchers]
method ::= (<doco>?:doc ((<token "to"> => To) | <token "method"> => Method):t <verb>?:v <parenParamList>:ps <optResultGuard>:g <block>:b => t(doc, v, ps, g, b))
matcher ::= <token "match"> <pattern>:p <block>:b => Matcher(p, b)

interfaceExpr ::= (<token "interface"> <objectName>:n <iguards>?:g ((<multiExtends>:es <oImplements>:oi <iscript>:s => [n, g, es, oi, s])
                       |<parenParamDescList>:ps <optGuard>:rg => [n, g, [], [], InterfaceFunction(ps, rg)]))
iguards ::= <token "guards"> <pattern>
multiExtends ::= (<token "extends"> <br> <order>:x ("," <order>)*:xs => [x] + xs
                 | => [])
iscript ::= "{" (<messageDesc>:m <br> => m)*:ms <token "}"> => ms
messageDesc ::= (<doco>?:doc (<token "to"> | <token "method">):t <verb>?:v <parenParamDescList>:ps <optGuard>:g
                => MessageDesc(doc, t, v, ps, g))
paramDesc ::= (<justNoun> | <token '_'> => None):n <optGuard>:g => ParamDesc(n, g)
parenParamDescList ::= "(" <paramDesc>:p ("," <paramDesc>)*:ps <token ")"> => [p] + ps

accumExpr ::= <token "accum"> <call>:c <accumulator>:a => Accum(c, a)
accumulator ::= ((<token "for"> <forPattern>:p <token "in"> <logical>:a <accumBody>:b <catcher>?:c => AccumFor(*(p + [a, b, c])))
                |(<token "if"> <parenExpr>:e <accumBody>:a => AccumIf(e, a))
                |(<token "while"> <parenExpr>:e <accumBody>:a <catcher>?:c => AccumWhile(e, a, c)))

accumBody ::= "{" (<token '_'> (<accumOp>:op <assign>:a => AccumOp(op, a)
                               |"." <verb>:v <parenArgs>:ps => AccumCall(v, ps))
                  | <accumulator>):ab <br> <token "}"> => ab
accumOp ::= ("+" => "Add"
            |"*" => "Multiply"
            |"&" => "BinaryAnd"
            |"|" => "BinaryOr")

escapeExpr ::= <token "escape"> <pattern>:p <block>:b <catcher>?:c => Escape(p, b, c)

forExpr ::= <token "for"> <forPattern>:p <token "in"> <br> <assign>:a <block>:b <catcher>?:c => For(*(p + [a, b, c]))

forPattern ::= <pattern>:p (<br> "=>" <pattern>:px => [p, px]
                           | => [None, p])

ifExpr ::= <token "if"> <parenExpr>:p <br> <block>:b (<token "else"> (<ifExpr> | <block>) | => None):e => If(p, b, e)

lambdaExpr ::= <doco>?:doc <token "fn"> <patterns>:ps <block>:b => Lambda(doc, ps, b)

metaExpr ::= <token "meta"> "." (<token "getState"> => "State"
                                |<token "scope"> => "Scope"
                                |<token "context"> => "Context"):s "(" <token ")"> => Meta(s)
switchExpr ::= <token "switch"> <parenExpr>:e "{" (<matcher>:m <br> => m)*:ms <token "}"> => Switch(e, ms)

tryExpr ::= <token "try"> <block>:tb <catcher>*:cs (<token "finally"> <block>)?:fb => Try(tb, cs, fb)
catcher ::= <token "catch"> <pattern>:p <block>:b => Catch(p, b)

whileExpr ::= <token "while"> <parenExpr>:e <block>:b <catcher>?:c => While(e, b, c)

whenExpr ::= <token "when"> <parenArgs>:a <br> "->" <block>:b <catcher>*:cs (<token "finally"> <block>)?:fb => When(a, b, cs, fb)

topSeq ::= <topExpr>:x (<seqSep> <topExpr>)*:xs <seqSep>? => SeqExpr(filter(None, [x] + xs))
pragma ::= <token "pragma"> "." <verb>:v "(" <string>:s <token ")"> => Pragma(v, s)
topExpr ::= (<pragma> => NounExpr("null")) | <expr>
start ::= <updoc>? <br> <topSeq>?

"""

try:
    from eparser_generated import BaseEParser
except ImportError:
    BaseEParser = OMetaEx.makeGrammar(egrammar, globals(), "BaseEParser")

class EParser(BaseEParser):
    """
    A parser for E.
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

    def keywordCheck(self, ident):
        """
        Ensure an identifier isn't a keyword or reserved word.
        """
        if ident in self.reserved:
            raise ParseError(ident + " is a reserved word")
        elif ident in self.basicKeywords:
            raise ParseError(ident + " is a keyword")
        else:
            return True
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

    def throwSemanticHere(self, arg):
        """
        Raise an error when invalid source is parsed.
        """
        raise ValueError(arg)

