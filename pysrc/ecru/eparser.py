from pymeta.grammar import OMetaGrammar, PortableOMeta, OMeta, ActionNoun, ActionCall, ActionLiteral
from pymeta.runtime import ParseError

from ecru import nodes
import string


egrammar = r"""
spaces ::= (' '|'\t'|'\f'|('#' (~<eol> <anything>)*))*

number ::= <spaces> <barenumber>
barenumber ::= ('0' (('x'|'X') <hexdigit>*:hs => makeHex(hs)
                    |<floatPart '0'>
                    |<octaldigit>*:ds => makeOctal(ds))
               |<decdigits>:ds <floatPart ds>
               |<decdigits>:ds => int(join(ds)))


exponent ::= ('e' | 'E'):e ('+' | '-' | => ""):s <decdigits>:ds => concat(e, s, join(ds))


floatPart :ds ::= ('.' <decdigits>:fs <exponent>?:e => makeFloat(ds, fs, e)
                               | <exponent>:e => float(concat(ds, e)))

decdigits ::= <digit>:d ((:x ?(isDigit(x)) => x) | '_' => "")*:ds => concat(d, join(ds))
octaldigit ::= :x ?(isOctDigit(x)) => x
hexdigit ::= :x ?(isHexDigit(x)) => x

string ::= <token '"'> (<escapedChar> | ~('"') <anything>)*:c '"' => join(c)
character ::= <token "'"> (<escapedChar> | ~('\''|'\n'|'\r'|'\\') <anything>):c '\'' => Character(c)
escapedUnicode ::= ('u' <hexdigit>:a <hexdigit>:b <hexdigit>:c <hexdigit>:d => unichr(int(concat(a, b, c, d), 16))
                   |'U' (<hexdigit>:a <hexdigit>:b <hexdigit>:c <hexdigit>:d
                         <hexdigit>:e <hexdigit>:f <hexdigit>:g <hexdigit>:h => unichr(int(concat(a, b, c, d, e, f, g, h), 16))))

escapedOctal ::= ((:a ?(contains("0123", a))) (<octdigit>:b  (<octdigit>:c (=> int(concat(a, b, c), 8)) | (=> int(concat(a, b), 8))| => int(a, 8)))
                 | :a ?(contains("4567", a)) (<octdigit>:b (=> int(concat(a, b), 8)) | => int(a, 8)))

updocLine ::= ('?'|'#'|'>'):y (~('\n' | '\r') <anything>)*:ys <eol> => cons(y, ys)
updoc ::= ('?' (~('\n' | '\r') <anything>)*:xs
              ((<eol> (<eol>
                      |<updocLine>)*)
              (<spaces> | <updocLine>))?)

eol ::= <spaces> ('\r' '\n'|'\r' | '\n')
eolplus ::= <eol> <updoc>?
linesep ::= <eolplus>+:xs => xs

br ::= (<spaces> <eolplus> | <eolplus>)*

literal ::= (<string> | <character> | <number>):x => LiteralExpr(x)

identifier ::= <spaces> (<letter> | '_'):x (<letterOrDigit> | '_')*:xs => concat(x, join(xs))
uri ::= "<" <uriScheme>:s ':' <uriBody>:b '>' => URIExpr(s, b)
uriGetter ::= "<" <uriScheme>:s '>' => URIGetter(s)
uriScheme ::= <letter>:x (<letterOrDigit> | '_' | '+' | '-' | '.')*:xs => concat(x, join(xs))
escapedChar ::= '\\' ('n' => '\n'
                     |'r' => '\r'
                     |'t' => '\t'
                     |'b' => '\b'
                     |'f' => '\f'
                     |'"' => '"'
                     |'\'' => '\''
                     |'?' => '?'
                     |'\\' => '\\'
                     | <escapedUnicode>
                     | <escapedOctal>
                     | <spaces> <eol> => "")
uriBody ::= (<letterOrDigit> |';'|'/'|'?'|':'|'@'|'&'|'='|'+'|'$'|','|'-'|'.'|'!'|'~'|'*'|'\''|'('|')'|'%'|'\\'|'|'|'#')+:x => join(x)
noun ::= <sourceHole> | <justNoun>
justNoun ::= ((<identifier>:id => keywordCheck(id)
              | ("::" (<string> | <identifier>):x => x)):n  => nounExprFromSource(n)
              | <uriGetter>)
sourceHole ::= ("$" (=> valueHole()):v '{' <digit>+:ds '}' => QuasiLiteralExpr(v)
               |"@" (=> patternHole()):v '{' <digit>+:ds '}' => QuasiPatternExpr(v))

quasiString ::= "`" (<exprHole> | <pattHole> | <quasiText>)*:qs '`' => qs

quasiText ::= (~('`'|'$'|'@') <anything> | '`' '`' | '$' '$' | ('$' | '@') '\\' <escapedChar> | '@' '@')+:qs => QuasiText(join(qs))

exprHole ::= '$' ('{' <br> <seq>:s '}' => QuasiExprHole(s)
                 |'_' !(noIgnoreExpressionHole())
                 |<identifier>:n !(exprHoleKeywordCheck(n)) => QuasiExprHole(NounExpr(n)))
pattHole ::= '@' ('{' <br> <pattern>:s '}' => QuasiPatternHole(s)
                 |'_' !(noIgnorePatternHole())
                 |<identifier>:n !(quasiHoleKeywordCheck(n)) => QuasiPatternHole(FinalPattern(NounExpr(n), null)))

slotExpr ::= "&" <verb>:v => Slot(v)
verb ::= <identifier> | <string>

listAndMap ::= "[" (<assoc>:x ("," <assoc>)*:xs ","? ']' => MapExpr(cons(x, xs))
                   |(<seq>:s ("," <seq>)*:ss ","? ']')=> ListExpr(cons(s, ss))
                   | ']' => ListExpr(makeList()))
assoc ::= (<seq>:k "=>" <seq>:v => MapExprAssoc(k, v)
          |"=>" (<noun> | <slotExpr>):n => MapExprExport(n)
                | "def" <noun>:n ~":=" !(throwSemanticHere("Reserved syntax: forward export")))


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
block ::= "{" (<seq> |=> SeqExpr(makeList())):s <token '}'> => s

seqSep ::= (";"| <linesep>)+
seq ::= <expr>:e ((<seqSep> <expr>)+:es <seqSep>? => SeqExpr(cons(e, es))
                 |<seqSep>? => e)
parenArgs ::= "(" <args>:a <token ')'> => a
args ::= (<seq>:s ("," <seq>)*:ss => cons(s, ss)
         |=> makeList())

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
           | "&" <call> !(throwSemanticHere("reserved: unary prefix '&' applied to non-noun lValue")))

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
           |<keywordPattern>:p ":=" <assign>:a => Def(p, null, a)
           |<cond>:x (":=" <assign>:y => Assign(x, y)
                    |<assignOp>:o <assign>:y => AugAssign(o, x, y)
                    |<identifier>:v '=' (<parenArgs>:y => VerbAssign(v, x, y)
                                        |<assign>:y => VerbAssign(v, x, makeList(y)))
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
             (("(" <token ")"> => null) | <assign>)?:val => ej(val))

guard ::= (<noun> | <parenExpr>):e ("[" <args>:x <token ']'> => x)*:xs => Guard(e, xs)
optGuard ::= (":" <guard>)?
eqPattern ::= (<token '_'> <optGuard>:e => IgnorePattern(e)
              |<identifier>?:n <quasiString>:q => QuasiPattern(n, q)
              |<namePattern>
              |"==" <prim>:p => SamePattern(p)
              |"!=" <prim>:p => throwSemanticHere("reserved: not-same pattern")
              )

patterns ::= (<pattern>:p ("," <pattern>)*:ps => cons(p, ps)
             | => makeList())
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
mapPatts ::= <mapPattern>:m ("," <mapPattern>)*:ms => cons(m, ms)

listPatternInner ::= (<mapPatts>:ms <br> <token ']'> ("|" <listPattern>)?:t => MapPattern(ms, t)
                     |<patterns>:ps <br> <token ']'> ("+" <listPattern>)?:t => ListPattern(ps, t))
listPattern ::= (
                "via" <parenExpr>:e <listPattern>:p => ViaPattern(e, p)
                | <eqPattern>
                | "[" <listPatternInner>)
pattern ::= <listPattern>:p ("?" <order>:e => SuchThatPattern(p, e)
                            | => p)

basic ::= <docoDef> | <accumExpr> | <escapeExpr> | <forExpr> | <ifExpr> | <lambdaExpr> | <metaExpr> | <switchExpr> | <tryExpr> | <whileExpr> | <whenExpr>

docoDef ::= <doco>?:doc (<objectExpr>:o => Object(doc, o)
                       |<interfaceExpr>:i => Interface(doc, i))
doco ::= <token "/**"> (~('*' '/') <anything>)*:doc '*' '/' => strip(join(doc))
objectExpr ::= ((<token "def"> <objectName>:n) | <keywordPattern>:n) <objectTail>:t => makeList(n, t)
objectName ::= (<token '_'> <optGuard>:e => IgnorePattern(e)
               |<namePattern>)
objectTail ::= (<functionTail>
               |((<token "extends"> <br> <order>)?:e <oImplements>:oi <scriptPair>:s
                  => Script(e, oi, s)))
oImplements ::= (<token "implements"> <br> <order>:x ("," <order>)*:xs => cons(x, xs)
                | => makeList())
functionTail ::= <parenParamList>:ps <optResultGuard>:g <oImplements>:fi <block>:b => Function(ps, g, fi, b)
parenParamList ::= "(" (<pattern>:p ("," <pattern>)*:ps <token ")"> => cons(p,  ps)
                       | <token ")"> => makeList())
optResultGuard ::= (":" <guard>)?
scriptPair ::= "{" <method>*:methods <matcher>*:matchers <token "}"> => makeList(methods, matchers)
method ::= (<doco>?:doc ((<token "to"> => To) | <token "method"> => Method):t <verb>?:v <parenParamList>:ps <optResultGuard>:g <block>:b => t(doc, v, ps, g, b))
matcher ::= <token "match"> <pattern>:p <block>:b => Matcher(p, b)

interfaceExpr ::= (<token "interface"> <objectName>:n <iguards>?:g ((<multiExtends>:es <oImplements>:oi <iscript>:s => makeList(n, g, es, oi, s))
                       |<parenParamDescList>:ps <optGuard>:rg => makeList(n, g, makeList(), makeList(), InterfaceFunction(ps, rg))))
iguards ::= <token "guards"> <pattern>
multiExtends ::= ((<token "extends"> <br> <order>:x ("," <order>)*:xs => cons(x, xs))
                 | => makeList())
iscript ::= "{" (<messageDesc>:m <br> => m)*:ms <token "}"> => ms
messageDesc ::= (<doco>?:doc (<token "to"> | <token "method">):t <verb>?:v <parenParamDescList>:ps <optGuard>:g
                => MessageDesc(doc, t, v, ps, g))
paramDesc ::= (<justNoun> | <token '_'> => null):n <optGuard>:g => ParamDesc(n, g)
parenParamDescList ::= "(" <paramDesc>:p ("," <paramDesc>)*:ps <token ")"> => cons(p,  ps)

accumExpr ::= <token "accum"> <call>:c <accumulator>:a => Accum(c, a)
accumulator ::= (((<token "for"> <forPattern>:p <token "in"> <logical>:a <accumBody>:b <catcher>?:c => AccumFor(p, a, b, c)))
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

forExpr ::= <token "for"> <forPattern>:p <token "in"> <br> <assign>:a <block>:b <catcher>?:c => For(p, a, b, c)

forPattern ::= <pattern>:p (<br> "=>" <pattern>:px => makeList(p, px)
                           | => makeList(null, p))

ifExpr ::= <token "if"> <parenExpr>:p <br> <block>:b (<token "else"> (<ifExpr> | <block>) | => null):e => If(p, b, e)

lambdaExpr ::= <doco>?:doc <token "fn"> <patterns>:ps <block>:b => Lambda(doc, ps, b)

metaExpr ::= <token "meta"> "." (<token "getState"> => "State"
                                |<token "scope"> => "Scope"
                                |<token "context"> => "Context"):s "(" <token ")"> => Meta(s)
switchExpr ::= <token "switch"> <parenExpr>:e "{" (<matcher>:m <br> => m)*:ms <token "}"> => Switch(e, ms)

tryExpr ::= <token "try"> <block>:tb <catcher>*:cs (<token "finally"> <block>)?:fb => Try(tb, cs, fb)
catcher ::= <token "catch"> <pattern>:p <block>:b => Catch(p, b)

whileExpr ::= <token "while"> <parenExpr>:e <block>:b <catcher>?:c => While(e, b, c)

whenExpr ::= <token "when"> <parenArgs>:a <br> "->" <block>:b <catcher>*:cs (<token "finally"> <block>)?:fb => When(a, b, cs, fb)

topSeq ::= <topExpr>:x (<seqSep> <topExpr>)*:xs <seqSep>? => SeqExpr(cons(x, xs))
pragma ::= <token "pragma"> "." <verb>:v "(" <string>:s <token ")"> => Pragma(v, s)
topExpr ::= (<pragma> => NounExpr("null")) | <expr>
start ::= <updoc>? <br> <topSeq>?

"""

try:
    from eparser_generated import BaseEParser
except ImportError:
    BaseEParser= PortableOMeta.makeGrammar(egrammar,  {}, "BaseEParser")


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


    def action_keywordCheck(self, ident):
        """
        Ensure an identifier isn't a keyword or reserved word.
        """
        if ident in self.reserved:
            raise ParseError(ident + " is a reserved word")
        elif ident in self.basicKeywords:
            raise ParseError(ident + " is a keyword")
        else:
            return ident

    def action_valueHole(self):
        """
        Look up a value hole in the table and return its position.
        """
        try:
            return self.valueHoles.index(self.input.position - 1)
        except ValueError:
            raise ValueError("A literal $ is not meaningful in E source.")

    def action_patternHole(self):
        """
        Look up a pattern hole in the table and return its position.
        """
        try:
            return self.patternHoles.index(self.input.position - 1)
        except ValueError:
            raise ValueError("A literal @ is not meaningful in E source.")


    def action_quasiHoleKeywordCheck(self, n):
        if n in self.keywords:
            raise ValueError("Unexpected keyword %r in quasi hole" % (n,))
        else:
            return None

    def action_exprHoleKeywordCheck(self, n):
        if n in self.keywords:
            raise ValueError("Unexpected keyword %r in quasi hole" % (n,))
        else:
            return None

    def action_throwSemanticHere(self, arg):
        """
        Raise an error when invalid source is parsed.
        """
        raise ValueError(arg)


    def lookupActionName(self, name, _locals):
        """
        Look up names in parser actions.
        """
        if name == "null":
            return None

        if name == 'zero':
            return '0'
        m = getattr(self, "action_" + name, None)
        if m is None:
            n = getattr(nodes, name, None)
            if n is None:
               return _locals[name]
            else:
                return n
        return m

    def action_cons(self, first, rest):
        return [first] + rest

    def action_concat(self, *bits):
        return ''.join(map(str, bits))

    def action_float(self, x):
        return float(x)

    def action_makeFloat(self, ds, fs, e):
        if e:
            return float(ds+"."+fs+e)
        else:
            return float(ds+"."+fs
)
    def action_int(self, x, base=10):
        return int(x, base)

    def action_join(self, x):
        return ''.join(x)

    def action_makeList(self, *bits):
        return list(bits)

    def action_noIgnorePatternHole(self):
        raise RuntimeError()

    def action_noIgnoreExpressionHole(self):
        raise RuntimeError()

    def action_nounExprFromSource(self, n):
        return nodes.NounExpr.fromSource(n)

    def action_strip(self, x):
        return x.strip()

    def action_unichr(self, x):
        return unichr(x)

    def action_makeHex(self, hs):
        return int(''.join(hs), 16)

    def action_makeOctal(self, ds):
        return int('0'+''.join(ds), 8)

    def action_isDigit(self, x):
        return x in string.digits

    def action_isOctDigit(self, x):
        return x in string.octdigits

    def action_isHexDigit(self, x):
        return x in string.hexdigits

    def action_contains(self, container, value):
        return value in container

    def action_Object(self, doc, o):
        return nodes.Object(doc, *o)

    def action_Interface(self, doc, i):
        return nodes.Interface(doc, *i)

    def action_AccumFor(self, p, *args):
        return nodes.AccumFor(*(p + list(args)))

    def action_For(self, p, *args):
        return nodes.For(*(p + list(args)))

    def action_SeqExpr(self, xs):
        return nodes.SeqExpr(filter(None, xs))

    def action_Script(self, e, oi, s):
        return nodes.Script(e, oi, *s)

    #noIgnoreExpressionHole nounExprFromSource valueHole
