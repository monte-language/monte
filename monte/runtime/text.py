from monte.runtime.base import MonteObject, throw, toString
from monte.runtime.data import String, Character
from monte.runtime.guards.base import deepFrozenGuard
from monte.runtime.tables import ConstList, FlexList

def findOneOf(elts, specimen, start):
    for i, c in enumerate(specimen[start:]):
        if c in elts:
            return i + start
    return -1

class Substituter(MonteObject):
    _m_fqn = "simple__quasiParser$Substituter"
    _m_auditorStamps = (deepFrozenGuard,)
    def __init__(self, template):
        if not isinstance(template, String):
            raise RuntimeError("%r is not a string" % (template,))
        self.template = template.s
        self.segments = segs = []
        last = 0
        i = 0
        while i < len(self.template):
            i = findOneOf('$@', self.template, last)
            if i == -1:
                # No more QL values or patterns; just go ahead and package up
                # the last segment if it exists.
                if last < len(self.template):
                    segs.append(('literal', self.template[last:]))
                break
            if self.template[i + 1] == self.template[i]:
                segs.append(('literal', self.template[last:i]))
                last = i
            elif self.template[i + 1] != '{':
                i -= 1
            else:
                if last != i and last < len(self.template) - 1:
                    segs.append(('literal', self.template[last:i]))
                    last = i
                if self.template[i] == '@':
                    typ = 'pattern'
                else:
                    typ = 'value'
                i += 2
                sub = i
                while True:
                    i += 1
                    c = self.template[i]
                    if c == '}':
                        break
                    elif not c.isdigit():
                        raise RuntimeError("Missing '}'", self.template)
                segs.append((typ, int(self.template[sub:i])))
                last = i + 1

    def substitute(self, values):
        if not isinstance(values, (ConstList, FlexList)):
            raise RuntimeError("%r is not a list" % (values,))
        return String(u"".join(self._sub(values.l)))

    def _sub(self, values):
        for typ, val in self.segments:
            if typ == 'literal':
                yield val
            elif typ == 'value':
                yield toString(values[val])
            else:
                raise RuntimeError("Can't substitute with a pattern")

    def matchBind(self, values, specimen, ej):
        #XXX maybe put this on a different object?
        if not isinstance(specimen, String):
            raise RuntimeError("%r is not a string" % (specimen,))
        if not isinstance(values, (ConstList, FlexList)):
            raise RuntimeError("%r is not a list" % (values,))
        specimen = specimen.s
        values = values.l
        i = 0
        bindings = []
        for n in range(len(self.segments)):
            typ, val = self.segments[n]
            if typ == 'literal':
                j = i + len(val)
                if specimen[i:j] != val:
                    throw.eject(ej, "expected %r..., found %r" % (
                        val, specimen[i:j]))
            elif typ == 'value':
                s = values[val]
                if not isinstance(s, String):
                        raise RuntimeError("%r is not a string" % (s,))
                s = s.s
                j = i + len(s)
                if specimen[i:j] != s:
                    throw.eject(ej, "expected %r... ($-hole %s), found %r" % (
                        s, val, specimen[i:j]))
            elif typ == 'pattern':
                nextVal = None
                if n == len(self.segments) - 1:
                    bindings.append(String(specimen[i:]))
                    continue
                nextType, nextVal = self.segments[n + 1]
                if nextType == 'value':
                    nextVal = values[nextVal]
                    if not isinstance(nextVal, String):
                        raise RuntimeError("%r is not a string" % (nextVal,))
                    nextVal = nextVal.s
                elif nextType == 'pattern':
                    bindings.append(String(u""))
                    continue
                j = specimen.find(nextVal)
                if j == -1:
                    throw.eject(ej, "expected %r..., found %r" % (nextVal.s, specimen[i:]))
                bindings.append(String(specimen[i:j]))
            i = j
        return ConstList(bindings)

class SimpleQuasiParser(MonteObject):
    _m_fqn = "simple__quasiParser"
    _m_auditorStamps = (deepFrozenGuard,)
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
