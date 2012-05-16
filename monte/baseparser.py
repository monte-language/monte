# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

import string
from pymeta.grammar import OMetaGrammar, PortableOMeta, OMeta, ActionNoun, ActionCall, ActionLiteral

baseGrammar = r"""
spaces ::= (' '|'\t'|'\f'|('#' (~<eol> <anything>)*))*

number ::= <spaces> <barenumber>
barenumber ::= '-'?:sign ('0' (('x'|'X') <hexdigit>*:hs => makeHex(sign, hs)
                    |<floatPart sign '0'>
                    |<octaldigit>*:ds => makeOctal(sign, ds))
               |<decdigits>:ds <floatPart sign ds>
               |<decdigits>:ds => signedInt(sign, join(ds)))


exponent ::= ('e' | 'E'):e ('+' | '-' | => ""):s <decdigits>:ds => concat(e, s, join(ds))


floatPart :sign :ds ::= ('.' <decdigits>:fs <exponent>?:e => makeFloat(sign, ds, fs, e)
                               | <exponent>:e => float(sign, concat(ds, e)))

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

eol ::= <spaces> ('\r' '\n'|'\r' | '\n')

uriBody ::= (<letterOrDigit> |';'|'/'|'?'|':'|'@'|'&'|'='|'+'|'$'|','|'-'|'.'|'!'|'~'|'*'|'\''|'('|')'|'%'|'\\'|'|'|'#')+:x => join(x)

"""

CommonBaseParser = PortableOMeta.makeGrammar(baseGrammar,  {}, "CommonBaseParser")

class CommonParser(CommonBaseParser):

    def action_concat(self, *bits):
        return ''.join(map(str, bits))

    def action_float(self, sign, x):
        return float((sign or '')+x)

    def action_makeFloat(self, sign, ds, fs, e):
        if e:
            return float((sign or '') + ds+"."+fs+e)
        else:
            return float((sign or '') + ds+"."+fs)
    
    def action_signedInt(self, sign, x, base=10):
        return int((sign or '')+x, base)

    def action_int(self, x, base=10):
        return int(x, base)

    def action_join(self, x):
        return ''.join(x)

    def action_makeHex(self, sign, hs):
        return int((sign or '') + ''.join(hs), 16)

    def action_makeOctal(self, sign, ds):
        return int((sign or '') + '0'+''.join(ds), 8)

    def action_isDigit(self, x):
        return x in string.digits

    def action_isOctDigit(self, x):
        return x in string.octdigits

    def action_isHexDigit(self, x):
        return x in string.hexdigits
    
    def action_unichr(self, x):
        return unichr(x)

    def action_contains(self, container, value):
        return value in container

    def action_cons(self, first, rest):
        return [first] + rest

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
            return _locals[name]
        else:
            return m
