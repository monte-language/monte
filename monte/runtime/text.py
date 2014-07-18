from monte.runtime.base import MonteObject, throw, toString
from monte.runtime.data import String, Twine, Character, unicodeFromTwine
from monte.runtime.guards.base import deepFrozenGuard
from monte.runtime.tables import ConstList, FlexList

def findOneOf(elts, specimen, start):
    for i, c in enumerate(specimen[start:]):
        if c in elts:
            return i + start
    return -1

LITERAL, VALUE_HOLE, PATTERN_HOLE = object(), object(), object()

class Substituter(MonteObject):
    _m_fqn = "simple__quasiParser$Substituter"
    _m_auditorStamps = (deepFrozenGuard,)
    def __init__(self, template):
        self.segments = segs = []
        for seg in template:
            if isinstance(seg, Twine):
                segs.append((LITERAL, unicodeFromTwine(seg)))
            else:
                segs.append(seg)

    def substitute(self, values):
        if not isinstance(values, (ConstList, FlexList)):
            raise RuntimeError("%r is not a list" % (values,))
        return String(u"".join(self._sub(values.l)))

    def _sub(self, values):
        for typ, val in self.segments:
            if typ is LITERAL:
                yield val
            elif typ is VALUE_HOLE:
                yield toString(values[val])
            else:
                raise RuntimeError("Can't substitute with a pattern")

    def matchBind(self, values, specimen, ej):
        #XXX maybe put this on a different object?
        if not isinstance(specimen, Twine):
            raise RuntimeError("%r is not a string" % (specimen,))
        if not isinstance(values, (ConstList, FlexList)):
            raise RuntimeError("%r is not a list" % (values,))
        specimen = unicodeFromTwine(specimen)
        values = values.l
        i = 0
        bindings = []
        for n in range(len(self.segments)):
            typ, val = self.segments[n]
            if typ is LITERAL:
                j = i + len(val)
                if specimen[i:j] != val:
                    throw.eject(ej, "expected %r..., found %r" % (
                        val, specimen[i:j]))
            elif typ is VALUE_HOLE:
                s = values[val]
                if not isinstance(s, String):
                        raise RuntimeError("%r is not a string" % (s,))
                s = unicodeFromTwine(s)
                j = i + len(s)
                if specimen[i:j] != s:
                    throw.eject(ej, "expected %r... ($-hole %s), found %r" % (
                        s, val, specimen[i:j]))
            elif typ is PATTERN_HOLE:
                nextVal = None
                if n == len(self.segments) - 1:
                    bindings.append(String(specimen[i:]))
                    continue
                nextType, nextVal = self.segments[n + 1]
                if nextType is VALUE_HOLE:
                    nextVal = values[nextVal]
                    if not isinstance(nextVal, String):
                        raise RuntimeError("%r is not a string" % (nextVal,))
                    nextVal = unicodeFromTwine(nextVal)
                elif nextType is PATTERN_HOLE:
                    bindings.append(String(u""))
                    continue
                j = specimen.find(nextVal, i)
                if j == -1:
                    throw.eject(ej, "expected %r..., found %r" % (
                        unicodeFromTwine(nextVal),
                        specimen[i:]))
                bindings.append(String(specimen[i:j]))
            i = j
        return ConstList(bindings)

class SimpleQuasiParser(MonteObject):
    _m_fqn = "simple__quasiParser"
    _m_auditorStamps = (deepFrozenGuard,)
    def valueHole(self, n):
        return (VALUE_HOLE, n.n)

    def patternHole(self, n):
        return (PATTERN_HOLE, n.n)

    def valueMaker(self, template):
        return Substituter(template)

    def matchMaker(self, template):
        return Substituter(template)

simpleQuasiParser = SimpleQuasiParser()

def quasiMatcher(matchMaker, values):
    def matchit(specimen, ej):
        return matchMaker.matchBind(values, specimen, ej)
    return matchit


class TextWriter(MonteObject):
    def __init__(self, out, newline=u'\n', context=None):
        self.out = out
        self.context = context or set()
        self.newline = newline

    def indent(self, morePrefix):
        return TextWriter(self.out, self.newline + u' ' * 4, self.context)

    def quote(self, obj):
        if isinstance(obj, (String, Character)):
            self._m_print(obj.quote())
        else:
            self._m_print(obj)

    def raw_print(self, string):
        self.out.write(string.encode('utf-8'))

    def _m_print(self, obj):
        from monte.runtime.ref import _resolution
        obj = _resolution(obj)
        if id(obj) in self.context:
            self.raw_print(u'<**CYCLE**>')
            return
        self.context.add(id(obj))
        sub = TextWriter(self.out, self.newline, self.context)
        try:
            p = getattr(obj, '_printOn', None)
            if p is None:
                sub.raw_print(unicode(obj))
            else:
                p(sub)
        except Exception, e:
            self.raw_print(u'<**%s throws %r when printed**>' % (
                getattr(obj, '_m_fqn', type(obj)), e))
        try:
            self.context.remove(id(obj))
        except KeyError:
            pass

    def println(self, obj):
        self._m_print(obj)
        self.raw_print(self.newline)
