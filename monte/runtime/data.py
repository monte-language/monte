import struct, math
from sys import float_info
from monte.runtime.base import MonteObject
from monte.runtime.flow import MonteIterator

class MonteNull(MonteObject):
    """
    The null object.

    null has no methods.
    """
    _m_fqn = "null"
    def __eq__(self, other):
        return self is other

    def _printOn(self, out):
        out.raw_print(u"null")

    def __hash__(self):
        return hash(None)

null = MonteNull()

class Bool(MonteObject):

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
    '\b': '\\b',
    '\t': '\\t',
    '\n': '\\n',
    '\f': '\\f',
    '\r': '\\r',
    '"': '\\"',
    '\'': '\\\'',
}
def escapedChar(c):
    if c in _CHAR_ESCAPES:
        return _CHAR_ESCAPES[c]
    i = ord(c)
    if i < 32 or i > 126:
        return '\\u%04x' % i
    return c


class Character(MonteObject):
    """
    A character.
    """
    _m_fqn = "__makeCharacter$char"
    def __init__(self, value):
        self._c = value

    def __hash__(self):
        return hash(self._c)

    def __eq__(self, other):
        if not isinstance(other, Character):
            return False
        return self._c == other._c

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


class Integer(MonteObject):
    _m_fqn = "__makeInt$int"
    def __init__(self, val):
        self.n = int(val)

    def __hash__(self):
        return hash(self.n)

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
    def __init__(self, val):
        self.n = float(val)

    def __hash__(self):
        return hash(self.n)

    def _printOn(self, out):
        out.raw_print(unicode(self.n))

    # XXX add trig functions, sqrt

    # Operators.

    def add(self, other):
        return numWrap(self.n + other.f)

    def subtract(self, other):
        return numWrap(self.n - other.f)

    def multiply(self, other):
        return numWrap(self.n * other.f)

    def approxDivide(self, other):
        return numWrap(self.n.__truediv__(other.f))

    def floorDivide(self, other):
        return numWrap(self.n.__floordiv__(other.f))

    def pow(self, other):
        return numWrap(self.n ** other.f)

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


class String(MonteObject):
    _m_fqn = "__makeStr$str"
    def __init__(self, s):
        if not isinstance(s, unicode):
            raise RuntimeError("%r is not a unicode string" % (s,))
        self.s = s

    def _printOn(self, out):
        out.raw_print(self.s)

    def quote(self):
        return String(u''.join([u'"'] + [escapedChar(c) for c in self.s] + [u'"']))

    def __hash__(self):
        return hash(self.s)

    def _makeIterator(self):
        return MonteIterator(enumerate(Character(c) for c in self.s))

    def op__cmp(self, other):
        if not isinstance(other, String):
            raise RuntimeError("%r is not a string" % (other,))

        return Integer(cmp(self.s, other.s))

    def get(self, idx):
        if not isinstance(idx, Integer):
            raise RuntimeError("%r is not an integer" % (idx,))
        return Character(self.s[idx.n])

    def slice(self, start, end=None):
        if not isinstance(start, Integer):
            raise RuntimeError("%r is not an integer" % (start,))
        if end is not None and not isinstance(end, Integer):
            raise RuntimeError("%r is not an integer" % (end,))
        if start < 0:
            raise RuntimeError("Slice indices must be positive")
        if end is not None and end < 0:
            raise RuntimeError("Slice indices must be positive")
        return String(self.s[start:end])

    def size(self):
        return Integer(len(self.s))

    def add(self, other):
        if not isinstance(other, String):
            raise RuntimeError("%r is not a string" % (other,))

        return String(self.s + other.s)

    def multiply(self, n):
        if not isinstance(n, Integer):
            raise RuntimeError("%r is not an integer" % (n,))
        return String(self.s * n.n)

    def startsWith(self, other):
        if not isinstance(other, String):
            raise RuntimeError("%r is not a string" % (other,))

        return bwrap(self.s.startswith(other.s))

    def endsWith(self, other):
        if not isinstance(other, String):
            raise RuntimeError("%r is not a string" % (other,))

        return bwrap(self.s.endswith(other.s))

    def split(self, other):
        if not isinstance(other, String):
            raise RuntimeError("%r is not a string" % (other,))

    # E calls this 'rjoin'.
    def join(self, items):
        return String(self.s.join(items))

    # E calls this 'replaceAll'.
    def replace(self, old, new):
        if not isinstance(old, String):
            raise RuntimeError("%r is not a string" % (old,))
        if not isinstance(new, String):
            raise RuntimeError("%r is not a string" % (new,))
        return String(self.s.replace(old.s, new.s))

    def toUpperCase(self):
        return String(self.s.upper())

    def toLowerCase(self):
        return String(self.s.lower())

    # XXX Twine methods.


