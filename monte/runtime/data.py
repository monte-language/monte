import struct, math
from sys import float_info
from monte.runtime.base import MonteObject, ejector
from monte.runtime.flow import MonteIterator

class MonteNull(MonteObject):
    """
    The null object.

    null has no methods.
    """
    _m_fqn = "null"
    #_m_auditorStamps = (deepFrozenGuard,)

    def __eq__(self, other):
        return self is other

    def _printOn(self, out):
        out.raw_print(u"null")

    def __hash__(self):
        return hash(None)

null = MonteNull()

class Bool(MonteObject):
    #_m_auditorStamps = (deepFrozenGuard,)
    def __init__(self, value):
        self._b = value

    def __hash__(self):
        return hash(self._b)

    def __nonzero__(self):
        return self._b

    def __eq__(self, other):
        if not isinstance(other, Bool):
            return false
        return bwrap(self._b == other._b)

    def _m_and(self, other):
        if not isinstance(other, Bool):
            raise RuntimeError("Bools can't be compared with non-bools")
        return bwrap(self._b and other._b)

    def _m_or(self, other):
        if not isinstance(other, Bool):
            raise RuntimeError("Bools can't be compared with non-bools")
        return bwrap(self._b or other._b)

    def _m_not(self):
        return bwrap(not self._b)

    def xor(self, other):
        if not isinstance(other, Bool):
            raise RuntimeError("Bools can't be compared with non-bools")
        return bwrap(self._b != other._b)

    def  op__cmp(self, other):
        if not isinstance(other, Bool):
            raise RuntimeError("%r is not a boolean" % (other,))
        return Integer(cmp(self._b, other._b))

    def _printOn(self, out):
        out.raw_print([u"false", u"true"][self._b])


false = Bool(False)
true = Bool(True)

def bwrap(b):
    return true if b else false

_CHAR_ESCAPES = {
    u'\B': u'\\b',
    u'\t': u'\\t',
    u'\n': u'\\n',
    u'\f': u'\\f',
    u'\r': u'\\r',
    u'"': u'\\"',
    u'\'': u'\\\'',
}


def escapedChar(c):
    if c in _CHAR_ESCAPES:
        return _CHAR_ESCAPES[c]
    i = ord(c)
    if i < 32 or i > 126:
        return u'\\u%04x' % i
    return c


def escapedByte(c):
    if c in _CHAR_ESCAPES:
        return _CHAR_ESCAPES[c]
    i = ord(c)
    if i > 255:
        raise RuntimeError("not a bytestring")
    if i < 32 or i > 126:
        return u'\\x%02x' % i
    return c


class Character(MonteObject):
    """
    A character.
    """
    _m_fqn = "__makeCharacter$char"
    #_m_auditorStamps = (deepFrozenGuard,)

    def __init__(self, value):
        self._c = value

    def __hash__(self):
        return hash(self._c)

    def __eq__(self, other):
        if not isinstance(other, Character):
            return false
        return bwrap(self._c == other._c)

    def add(self, other):
        if not isinstance(other, Integer):
            raise RuntimeError("%r is not an integer" % (other,))
        return Character(unichr(ord(self._c) + other.n))

    def subtract(self, other):
        if not isinstance(other, Integer):
            raise RuntimeError("%r is not an integer" % (other,))
        return Character(unichr(ord(self._c) - other.n))

    def next(self):
        if ord(self._c) == 0x10FFFF:
            return self
        return Character(unichr(ord(self._c) + 1))

    def previous(self):
        if self._c == '\x00':
            return self
        return Character(unichr(ord(self._c) - 1))

    def max(self, other):
        if not isinstance(other, Character):
            raise RuntimeError("%r is not a character" % (other,))
        return Character(max(self._c, other._c))

    def min(self, other):
        if not isinstance(other, Character):
            raise RuntimeError("%r is not a character" % (other,))
        return Character(min(self._c, other._c))

    def quote(self):
        return String(u"'%s'" % (escapedChar(self._c),))

    def _printOn(self, out):
        out.raw_print(self._c)


class Bytestring(MonteObject):
    def __init__(self, b):
        if not isinstance(b, str):
            raise RuntimeError("%r is not a byte string" % (b,))
        self.b = b

    def quote(self):
        return String(u''.join([u'b`'] + [escapedByte(c) for c in self.b]
                               + [u'`']))
    def _printOn(self, out):
        out._m_print(self.quote())

    def __eq__(self, other):
        if not isinstance(other, Bytestring):
            return false
        return bwrap(self.b == other.b)

    def _makeIterator(self):
        return MonteIterator(enumerate(Integer(ord(b)) for b in self.b))

    def op__cmp(self, other):
        if not isinstance(other, Bytestring):
            raise RuntimeError("%r is not a bytestring" % (other,))
        return Integer(cmp(self.b, other.b))

    def get(self, idx):
        if not isinstance(idx, Integer):
            raise RuntimeError("%r is not an integer" % (idx,))
        return Integer(ord(self.b[idx.n]))

    def slice(self, start, end=None):
        if not isinstance(start, Integer):
            raise RuntimeError("%r is not an integer" % (start,))
        start = start.n
        if end is not None and not isinstance(end, Integer):
            raise RuntimeError("%r is not an integer" % (end,))
        elif end is not None:
            end = end.n
        if start < 0:
            raise RuntimeError("Slice indices must be positive")
        if end is not None and end < 0:
            raise RuntimeError("Slice indices must be positive")
        return Bytestring(self.b[start:end])

    def size(self):
        return Integer(len(self.b))

    def add(self, other):
        if not isinstance(other, Bytestring):
            raise RuntimeError("%r is not a bytestring" % (other,))

        return Bytestring(self.b + other.b)

    def multiply(self, n):
        if not isinstance(n, Integer):
            raise RuntimeError("%r is not an integer" % (n,))
        return Bytestring(self.b * n.n)

    def startsWith(self, other):
        if not isinstance(other, Bytestring):
            raise RuntimeError("%r is not a bytestring" % (other,))

        return bwrap(self.b.startswith(other.b))

    def endsWith(self, other):
        if not isinstance(other, Bytestring):
            raise RuntimeError("%r is not a string" % (other,))

        return bwrap(self.b.endswith(other.b))

    def split(self, other):
        from monte.runtime.tables import ConstList
        if not isinstance(other, Bytestring):
            raise RuntimeError("%r is not a bytestring" % (other,))
        return ConstList(Bytestring(x) for x in self.b.split(other.b))

    def join(self, items):
        it = items._makeIterator()
        ej = ejector("iteration")
        segments = []
        try:
            while True:
                key, item = it.next(ej)
                segments.append(item)
        except ej._m_type:
            pass
        finally:
            ej.disable()
        return Bytestring(self.b.join(segments))

    # E calls this 'replaceAll'.
    def replace(self, old, new):
        if not isinstance(old, Bytestring):
            raise RuntimeError("%r is not a bytestring" % (old,))
        if not isinstance(new, Bytestring):
            raise RuntimeError("%r is not a bytestring" % (new,))
        return Bytestring(self.b.replace(old.b, new.b))

    def toUpperCase(self):
        return String(self.b.upper())

    def toLowerCase(self):
        return String(self.b.lower())


class Integer(MonteObject):
    _m_fqn = "__makeInt$int"
    #_m_auditorStamps = (deepFrozenGuard,)

    def __init__(self, val):
        self.n = int(val)

    def __hash__(self):
        return hash(self.n)

    def __eq__(self, other):
        if not isinstance(other, Integer):
            return false
        return bwrap(self.n == other.n)

    def __int__(self):
        return self.n

    # Type conversions.

    def asChar(self):
        return Character(unichr(self.n))

    def asFloat(self):
        return Float(float(self.n))

    def toString(self, radix):
        if not isinstance(radix, Integer):
            raise RuntimeError("%r is not a integer" % (radix,))
        radix = radix.n
        if radix == 16:
            return String(hex(self.n)[2:].decode('ascii'))
        elif radix == 10:
            return String(unicode(self.n))
        elif radix == 8:
            return String(oct(self.n)[1:].decode('ascii'))
        elif radix == 2:
            return String(bin(self.n)[2:].decode('ascii'))
        else:
            raise NotImplementedError("too lazy to implement radix '%s'" % (radix,))

    # Operators.

    def add(self, other):
        return numWrap(self.n + other.n)

    def subtract(self, other):
        return numWrap(self.n - other.n)

    def multiply(self, other):
        return numWrap(self.n * other.n)

    def approxDivide(self, other):
        return numWrap(self.n.__truediv__(other.n))

    def floorDivide(self, other):
        return numWrap(self.n.__floordiv__(other.n))

    def shiftLeft(self, other):
        return Integer(self.n << other.n)

    def shiftRight(self, other):
        return Integer(self.n >> other.n)

    def mod(self, other):
        return numWrap(self.n % other.n)

    def remainder(self, other):
        return numWrap(self.n % other.n)

    def _m_and(self, other):
        return Integer(self.n & other.n)

    def _m_or(self, other):
        return Integer(self.n | other.n)

    def xor(self, other):
        return Integer(self.n ^ other.n)

    def pow(self, other):
        return numWrap(self.n ** other.n)

    def _m_not(self):
        return Integer(~self.n)

    def negate(self):
        return Integer(-self.n)

    def butNot(self, other):
        return Integer(self.n & ~other.n)

    # Comparator.

    def op__cmp(self, other):
        if not isinstance(other, (Integer, Float)):
            raise RuntimeError("%r is not a number" % (other,))
        return Integer(cmp(self.n, other.n))

    # Comparison protocol.

    def aboveZero(self):
        return bwrap(0 < self.n)

    def atLeastZero(self):
        return bwrap(0 <= self.n)

    def atMostZero(self):
        return bwrap(0 >= self.n)

    def belowZero(self):
        return bwrap(0 > self.n)

    def isZero(self):
        return bwrap(0 == self.n)

    def isNaN(self):
        return false

    # Float compatibiity.

    def ceil(self):
        return self

    def floor(self):
        return self

    def round(self):
        return self

    def truncate(self):
        return self

    def abs(self):
        return Integer(abs(self.n))

    # Order.

    def next(self):
        return Integer(self.n + 1)

    def previous(self):
        return Integer(self.n - 1)

    # Misc.

    def bitLength(self):
        return Integer(self.n.bit_length())

    def max(self, other):
        if not isinstance(other, Integer):
            raise RuntimeError("%r is not an integer" % (other,))
        return numWrap(max(self.n, other.n))

    def min(self, other):
        if not isinstance(other, Integer):
            raise RuntimeError("%r is not an integer" % (other,))
        return numWrap(min(self.n, other.n))

    def _printOn(self, out):
        out.raw_print(unicode(self.n))


class Float(MonteObject):
    _m_fqn = "__makeFloat$float"
    #_m_auditorStamps = (deepFrozenGuard,)

    def __init__(self, val):
        self.n = float(val)

    def __hash__(self):
        return hash(self.n)

    def __eq__(self, other):
        if not isinstance(other, (Integer, Float)):
            return false
        return bwrap(self.n == other.n)

    def _printOn(self, out):
        out.raw_print(unicode(self.n))

    # XXX add trig functions, sqrt

    # Operators.

    def add(self, other):
        return numWrap(self.n + other.n)

    def subtract(self, other):
        return numWrap(self.n - other.n)

    def multiply(self, other):
        return numWrap(self.n * other.n)

    def approxDivide(self, other):
        return numWrap(self.n.__truediv__(other.n))

    def floorDivide(self, other):
        return numWrap(self.n.__floordiv__(other.n))

    def pow(self, other):
        return numWrap(self.n ** other.n)

    # Comparator.

    def op__cmp(self, other):
        if not isinstance(other, (Integer, Float)):
            raise RuntimeError("%r is not a number" % (other,))
        #cmp doesn't do NaNs, so
        if self.n < other.n:
            return Float(-1.0)
        elif self.n == other.n:
            return Float(0.0)
        elif self.n > other.n:
            return Float(1.0)
        else:
            return Float(float('nan'))

    # Comparison protocol.

    def aboveZero(self):
        return bwrap(0 < self.n)

    def atLeastZero(self):
        return bwrap(0 <= self.n)

    def atMostZero(self):
        return bwrap(0 >= self.n)

    def belowZero(self):
        return bwrap(0 > self.n)

    def isZero(self):
        return bwrap(0 == self.n)

    def isNaN(self):
        return math.isnan(self.n)

    def isInfinite(self):
        return math.isinf(self.n)

    # Floatish methods.

    def ceil(self):
        return Float(math.ceil(self.n))

    def floor(self):
        return Float(math.floor(self.n))

    def round(self):
        return Integer(round(self.n))

    def truncate(self):
        return Integer(int(self.n))

    def abs(self):
        return Float(abs(self.n))

    def negate(self):
        return Float(-self.n)

    # Order.

    def next(self):
        if math.isnan(self.n) or self.n == float('inf'):
            return self
        if self.n == float_info.max:
            return Float(float('inf'))
        if self.n == float('-inf'):
            return Float(-float_info.max)
        x = self.n
        if x == -0.0 or x == 0.0:
            x = 0.0
        n = struct.unpack('<q', struct.pack('<d', x))[0]
        return struct.unpack('<d', struct.pack('<q', n + 1))[0]

    def previous(self):
        if math.isnan(self.n) or self.n == float('-inf'):
            return self
        if self.n == -float_info.max:
            return Float(float('-inf'))
        if self.n == float('inf'):
            return Float(float_info.max)
        x = self.n
        if x == -0.0 or x == 0.0:
            x = 0.0
        n = struct.unpack('<q', struct.pack('<d', x))[0]
        return struct.unpack('<d', struct.pack('<q', n - 1))[0]

    # Misc.

    def max(self, other):
        if not isinstance(other, (Float, Integer)):
            raise RuntimeError("%r is not a number" % (other,))
        return numWrap(max(self.n, other.n))

    def min(self, other):
        if not isinstance(other, (Float, Integer)):
            raise RuntimeError("%r is not an integer" % (other,))
        return numWrap(min(self.n, other.n))


def numWrap(n):
    if isinstance(n, float):
        return Float(n)
    elif isinstance(n, int):
        return Integer(n)
    else:
        raise RuntimeError("welp: " + repr(n))


nan = Float(float('nan'))
infinity = Float(float('inf'))


def unicodeFromTwine(t):
    if isinstance(t, EmptyTwine):
        return u""
    if isinstance(t, String):
        return t.s
    raise RuntimeError("wip")


class TwineMaker(MonteObject):
    _m_fqn = "__makeString"

    def fromParts(self, parts):
        from monte.runtime.tables import ConstList, FlexList
        if not isinstance(parts, (ConstList, FlexList)):
            raise RuntimeError("%r is not a list" % (parts,))
        if len(parts.l) == 0:
            return theEmptyTwine
        elif len(parts.l) == 1:
            return parts.l[0]
        elif all(isinstance(p, String) for p in parts):
            return String(u''.join(p.s for p in parts))
        else:
            return CompositeTwine(parts)

    def fromString(self, s, span=null):
        if not isinstance(s, Twine):
            raise RuntimeError("%r is not a string" % (s,))
        if span is null:
            return s
        else:
            return LocatedTwine(unicodeFromTwine(s), span)

    def fromChars(self, chars):
        from monte.runtime.tables import ConstList, FlexList
        if not isinstance(chars, (ConstList, FlexList)):
            raise RuntimeError("%r is not a list" % (chars,))
        if not all(isinstance(c, Character) for c in chars.l):
            raise RuntimeError("%r is not a list of characters" % (chars,))
        return String(u''.join(c._c for c in chars.l))

theTwineMaker = TwineMaker()


class Twine(MonteObject):
    def add(self, other):
        from monte.runtime.tables import ConstList
        if not isinstance(other, Twine):
            raise RuntimeError("%r is not a string" % (other,))
        mine = self.getParts().l
        his = other.getParts().l
        if len(mine) > 1 and len(his) > 1:
            # Smush the last and first segments together, if they'll fit.
            mine = mine[:-1] + mine[-1].mergedParts(his[0])
            his = his[1:]
        return theTwineMaker.fromParts(ConstList(mine + his))

    def asFrom(self, origin, startLine, startCol):
        from monte.runtime.tables import ConstList
        parts = []
        s = self.bare()
        end = len(s)
        i = 0
        j = s.s.index(u'\n')
        while i < end:
            if j == -1:
                j = end - i
            endCol = startCol + j - i
            span = SourceSpan(origin, true, startLine, startCol,
                              startLine, endCol)
            parts.append(LocatedTwine(s.s[i:j + 1], span))
            startLine += 1
            startCol = 0
            i = j + 1
        return theTwineMaker.fromParts(ConstList(parts))

    def endsWith(self, other):
        return self.bare().endsWith(other)

    def getPartAt(self, pos):
        if pos < 0:
            raise RuntimeError("Index out of bounds")
        parts = self.getParts().l
        sofar = 0
        for (i, atom) in enumerate(parts):
            siz = atom.size()
            if pos < sofar + siz.n:
                return [i, pos - sofar]
            sofar += siz
        raise RuntimeError("%s bigger than %s" % (pos, sofar))

    def getSourceMap(self):
        from monte.runtime.tables import ConstList, ConstMap
        parts = self.getParts().l
        result = []
        offset = 0
        for part in parts:
            partSize = part.size().n
            span = part.getSpan()
            if span is not null:
                k = ConstList([Integer(offset), Integer(offset + partSize)])
                result.append((k, span))
            offset += partSize
        return ConstMap(dict(result), [x[0] for x in result])

    def infect(self, other, oneToOne=false):
        if not isinstance(other, Twine):
            raise RuntimeError("%r is not a string" % (other,))
        if oneToOne is true:
            if self.size() == other.size():
                return self.infectOneToOne(other)
            else:
                raise RuntimeError("%r and %r must be the same size" %
                                   (other, self))
        else:
            span = self.getSpan()
            if span is not null:
                span = span.notOneToOne()
            return theTwineMaker.fromString(other, span)

    def op__cmp(self, other):
        return self.bare().op__cmp(other.bare())

    def multiply(self, n):
        if not isinstance(n, Integer):
            raise RuntimeError("%r is not an integer" % (n,))
        result = theEmptyTwine
        for _ in range(n.n):
            result = result.add(self)
        return result

    def quote(self):
        result = String(u'"')
        p1 = 0
        for p2 in range(self.size().n):
            ch = self.get(Integer(p2))
            if ch._c != '\n':
                ech = escapedChar(ch._c)
                if len(ech) > 1:
                    result = result.add(self.slice(Integer(p1), Integer(p2)))
                    result = result.add(self.slice(Integer(p2), Integer(p2 + 1))
                                        .infect(String(ech)))
                    p1 = p2 + 1
        result = result.add(self.slice(Integer(p1), self.size()))
        return result.add(String(u'"'))

    def split(self, other):
        from monte.runtime.tables import ConstList
        if not isinstance(other, Twine):
            raise RuntimeError("%r is not a string" % (other,))
        sepLen = other.size().n
        if sepLen == Integer(0):
            raise RuntimeError("separator must not empty")
        result = []
        p1 = 0
        p2 = self.indexOf(other)
        while p2 != 1:
            result.append(self.slice(Integer(p1), Integer(p2)))
            p1 = p2 + sepLen
            p2 = self.indexOf(other, Integer(p1))
        result.append(self.slice(Integer(p1), self.size()))
        return ConstList(result)

    def startsWith(self, other):
        return self.bare().startsWith(other)

     # E calls this 'replaceAll'.
    def replace(self, old, new):
        if not isinstance(old, String):
            raise RuntimeError("%r is not a string" % (old,))
        if not isinstance(new, String):
            raise RuntimeError("%r is not a string" % (new,))
        result = theEmptyTwine
        oldLen = old.size().n
        if oldLen == 0:
            raise RuntimeError("can't replace the null string")
        p1 = 0
        p2 = self.indexOf(old)
        while p2 != -1:
            left = self.slice(Integer(p1), Integer(p2))
            chunk = self.slice(Integer(p2), Integer(p2 + oldLen))
            result = result.add(left).add(chunk.infect(new, false))
            p1 = p2 + oldLen
        result = result.add(self.slice(Integer(p1), self.size()))
        return result

    def toUpperCase(self):
        return self.infect(self.bare().s.upper(), true)

    def toLowerCase(self):
        return self.infect(self.bare().s.lower(), true)




class EmptyTwine(Twine):
    def _uncall(self):
        from monte.runtime.tables import ConstList
        return ConstList([theTwineMaker, "fromParts",
                          ConstList([ConstList([])])])

    def size(self):
        return Integer(0)

    def bare(self):
        return self

    def get(self, idx):
        raise RuntimeError("index out of bounds")

    def getParts(self):
        from monte.runtime.tables import ConstList
        return ConstList([])

    def getSpan(self):
        return null

    def infectOneToOne(self, other):
        return other

    def isBare(self):
        return true

    def slice(self, start, end=None):
        return self

    def _printOn(self, out):
        out.raw_print(u"")

theEmptyTwine = EmptyTwine()


class String(Twine):
    _m_fqn = "__makeStr$str"
    #_m_auditorStamps = (deepFrozenGuard,)

    def __init__(self, s):
        if not isinstance(s, unicode):
            raise RuntimeError("%r is not a unicode string" % (s,))
        self.s = s

    def __hash__(self):
        return hash(self.s)

    def __eq__(self, other):
        if not isinstance(other, (String)):
            return false
        return bwrap(self.s == other.s)

    def bare(self):
        return self

    def endsWith(self, other):
        if not isinstance(other, Twine):
            raise RuntimeError("%r is not a string" % (other,))
        suffix = unicodeFromTwine(other)
        return bwrap(self.s.endswith(suffix))

    def get(self, idx):
        if not isinstance(idx, Integer):
            raise RuntimeError("%r is not an integer" % (idx,))
        return Character(self.s[idx.n])

    def getParts(self):
        from monte.runtime.tables import ConstList
        return ConstList([self])

    def getSpan(self):
        return null

    def isBare(self):
        return true

    def op__cmp(self, other):
        if not isinstance(other, String):
            raise RuntimeError("%r is not a string" % (other,))

        return Integer(cmp(self.s, other.s))

    def size(self):
        return Integer(len(self.s))

    def slice(self, start, end=None):
        if not isinstance(start, Integer):
            raise RuntimeError("%r is not an integer" % (start,))
        start = start.n
        if end is not None and not isinstance(end, Integer):
            raise RuntimeError("%r is not an integer" % (end,))
        elif end is not None:
            end = end.n
        if start < 0:
            raise RuntimeError("Slice indices must be positive")
        if end is not None and end < 0:
            raise RuntimeError("Slice indices must be positive")
        return String(self.s[start:end])

    # def split(self, other):
    #     from monte.runtime.tables import ConstList
    #     if not isinstance(other, String):
    #         raise RuntimeError("%r is not a string" % (other,))
    #     return ConstList(String(x) for x in self.s.split(other.s))

    def startsWith(self, other):
        if not isinstance(other, String):
            raise RuntimeError("%r is not a string" % (other,))

        return bwrap(self.s.startswith(other.s))

    def _makeIterator(self):
        return MonteIterator(enumerate(Character(c) for c in self.s))

    def _printOn(self, out):
        out.raw_print(self.s)
