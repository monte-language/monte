import weakref

from monte.runtime.base import MonteObject
from monte.runtime.data import String, bwrap, null, true, false
from monte.runtime.tables import ConstList

BROKEN, EVENTUAL, NEAR = String("BROKEN"), String("EVENTUAL"), String("NEAR")
_notARef = object()
_theViciousRef = object()

def _makePromise(vat):
    buf = _Buffer([], vat)
    sref = SwitchableRef(BufferingRef(buf))
    return ConstList((sref, LocalResolver(sref._m_controller, buf)))

class RefOps(MonteObject):
    """
    Public functions for ref manipulation. Exposed in safescope as 'Ref'.
    """

    def __init__(self, vat):
        self.vat = vat

    def promise(self):
        return _makePromise(self.vat)

    def broken(self, problem):
        return UnconnectedRef(problem)

    def optBroken(self, optProblem):
        if optProblem is null:
            return null
        else:
            return self.broken(optProblem)

    def isNear(self, ref):
        if isinstance(ref, Promise):
            return bwrap(ref._m_controller.state() is NEAR)
        else:
            return true

    def isEventual(self, ref):
        if isinstance(ref, Promise):
            return bwrap(ref._m_controller.state() is EVENTUAL)
        else:
            return false

    def isBroken(self, ref):
        if isinstance(ref, Promise):
            return bwrap(ref._m_controller.state() is BROKEN)
        else:
            return false

    def optProblem(self, ref):
        if isinstance(ref, Promise):
            return ref._m_controller.problem
        return null

    def state(self, ref):
        if isinstance(ref, Promise):
            return ref._m_controller.state()
        else:
            return NEAR

    def resolution(self, ref):
        if isinstance(ref, Promise):
            return ref._m_controller.resolution()
        else:
            return ref

    def fulfillment(self, ref):
        ref = self.resolution(ref)
        p = self.optProblem(ref)
        if self.isResolved(ref):
            if p is null:
                return ref
            else:
                raise p
        else:
            raise RuntimeError("Not resolved: %r" % (ref,))

    def isResolved(ref):
        if isinstance(ref, Promise):
            return ref._m_controller.isResolved()
        else:
            return true

    def isFar(self, ref):
        return self.isEventual(ref)._m_and(self.isResolved(ref))

    def whenResolved(self, o, callback):
        p, r = self.promise()
        prob = self.vat.sendOnly(
            o, String('_whenMoreResolved'),
            ConstList([_whenResolvedReactor(callback, o, r)]))
        if prob is not None:
            return self.broken(prob)
        return p

    def whenResolvedOnly(self, o, callback):
        p, r = self.promise()
        return self.vat.sendOnly(
            o, String('_whenMoreResolved'),
            ConstList([_whenResolvedReactor(callback, o, r)]))

    def whenBroken(self, o, callback):
        p, r = self.promise()
        prob = self.vat.sendOnly(
            o, String('_whenMoreResolved'),
            ConstList([_whenBrokenReactor(callback, o, r)]))
        if prob is not None:
            return self.broken(prob)
        return p

    def whenBrokenOnly(self, o, callback):
        p, r = self.promise()
        return self.vat.sendOnly(
            o, String('_whenMoreResolved'),
            ConstList([_whenBrokenReactor(callback, o, r)]))


    #isSettled
    #isSelfless
    #isSelfish

def _whenBrokenReactor(callback, ref, resolver, vat):
    def whenBroken(_):
        if not isinstance(ref, Promise):
            return

        if ref._m_controller.state() == EVENTUAL:
            vat.sendOnly(ref, '_whenMoreResolved', ConstList([whenBroken]))
        elif ref._m_controller.state() == BROKEN:
            try:
                outcome = callback(ref)
            except Exception, e:
                outcome = e
            if resolver is not null:
                resolver.resolve(outcome)
        return null
    return whenBroken


def _whenResolvedReactor(callback, ref, resolver, vat):
    done = [False]
    def whenResolved(_):
        if done[0]:
            return null
        if ref._m_controller.isResolved():
            try:
                outcome = callback(ref)
            except Exception, e:
                outcome = e
            if resolver is not null:
                resolver.resolve(outcome)
            done[0] = True
        else:
            vat.sendOnly(ref, '_whenMoreResolved', ConstList([whenResolved]))
    return whenResolved


class LocalResolver(MonteObject):
    def __init__(self, ref, buf):
        self.ref = ref
        self.buf = buf
        self.vat = buf.vat

    def resolve(self, target, strict=true):
        if self.ref is None:
            if strict is true:
                raise RuntimeError("Already resolved")
            return false
        else:
            self.ref.setTarget(_toRef(target, self.vat))
            self.ref.commit()
            if self.buf is not None:
                self.buf.deliverAll(target)
            self.ref = None
            self.buf = None
            return true

    def resolveRace(self, target):
        return self.resolve(target, false)

    def smash(self, problem):
        return self.resolve(UnconnectedRef(problem, self.vat), false)

    def isDone(self):
        return bwrap(self.ref is None)

    def _printOn(self, out):
        if self.ref is None:
            out.raw_print(u'<Closed Resolver>')
        else:
            out.raw_print(u'<Resolver>')


class RefControllerBase(MonteObject):
    def __init__(self, ref):
        self.ref = ref

    def resolution(self):
        result = self.resolutionRef()
        if self.ref is result:
            return result
        else:
            return result._m_controller.resolution()

    def state(self):
        if self.problem() is not None:
            return BROKEN
        target = self.resolutionRef()
        if self.ref is target:
            return EVENTUAL
        else:
            return target._m_controller.state()

    #optShorten??

    def sendMsg(self, msg):
        if msg.resolver is None:
            self.sendAllOnly(msg.verb, msg.args)
        else:
            msg.resolver.resolve(self.sendAll(msg.verb, msg.args))


class SwitchableRefController(RefControllerBase):
    def __init__(self, ref, target):
        self.ref = ref
        self.target = target
        self.isSwitchable = True

    def optProblem(self):
        if self.isSwitchable:
            return null
        else:
            self.resolutionRef()
            return self.target.optProblem()

    def resolutionRef(self):
        self.target = self.target.resolutionRef()
        if self.isSwitchable:
            return self.ref
        else:
            return self.target.ref

    def state(self):
        if self.isSwitchable:
            return "eventual"
        else:
            self.resolutionRef()
            return self.target.state()

    def callAll(self, verb, args):
        if self.isSwitchable:
            if verb == "_printOn":
                return self._printOn(*args)
            else:
                raise RuntimeError("not synchronously callable (%s)" % (verb,))
        else:
            self.resolutionRef()
            return self.target.callAll(verb, args)

    def sendMsg(self, msg):
        self.resolutionRef()
        self.target.sendMsg(msg)

    def sendAll(self, verb, args):
        self.resolutionRef()
        return self.target.sendAll(verb, args)

    def sendAllOnly(self, verb, args):
        self.resolutionRef()
        return self.target.sendAllOnly(verb, args)

    def isResolved(self):
        if self.isSwitchable:
            return false
        else:
            self.resolutionRef()
            return self.target.isResolved()

    def setTarget(self, newTarget):
        if self.isSwitchable:
           self.target = newTarget._m_controller.resolutionRef()._m_controller
           if self is self.target:
               raise RuntimeError("Ref loop")
        else:
            raise RuntimeError("No longer switchable")

    def commit(self):
        if not self.isSwitchable:
            return
        newTarget = self.target.resolutionRef()._m_controller
        self.target = _theViciousRef
        self.switchable = False
        newTarget = newTarget.resolutionRef()._m_controller
        if newTarget is _theViciousRef:
            raise RuntimeError("Ref loop")
        else:
            self.target = newTarget

    def _printOn(self, out):
        if self.isSwitchable:
            return out.raw_print(u"<Promise>")
        else:
            self.resolutionRef()
            self.target._printOn(out)


class _Buffer(object):
    def __init__(self, buf, vat):
        self.buf = buf
        self.vat = vat

    def deliverAll(self, target):
        #XXX record sending-context information for causality tracing
        msgs = self.buf
        del self.buf[:]
        targRef = _toRef(target, self.vat)
        for msg in msgs:
            targRef.sendMsg(msg)
        return len(msgs)


class BufferingRefController(object):
    def __init__(self, ref, buf, vat):
        self.ref = ref
        self.buf = weakref.ref(buf)
        self.vat = vat

    def optProblem(self):
        return null

    def resolutionRef(self):
        return self.ref

    def state(self):
        return EVENTUAL

    def callAll(self, verb, args):
        if verb == "_printOn":
            return self._printOn(*args)
        else:
            raise RuntimeError("not synchronously callable (%s)" % (verb,))

    def sendAll(self, verb, args):
        optMsgs = self.buf()
        if optMsgs is None:
            return self
        else:
            p, r = _makePromise(self.vat)
            optMsgs.buf.append((r, verb, args))
            return ConstList((p, r))

    def sendAllOnly(self, verb, args):
        optMsgs = self.buf()
        if optMsgs is not None:
            optMsgs.buf.append((null, verb, args))
        return null

    def isResolved(self):
        return false

    def commit(self):
        pass

    def _printOn(self, out):
        out.raw_print(u"<Promise>")


class NearRefController(RefControllerBase):
    def __init__(self, ref, target, vat):
        self.ref = ref
        self.target = target
        self.vat = vat

    def optProblem(self):
        return null

    def resolution(self):
        return self.ref

    def callAll(self, verb, args):
        return getattr(self.target, verb)(*args)

    def sendAll(self, verb, args):
        return self.vat.sendAll(self.target, verb, args)

    def sendAllOnly(self, verb, args):
        return self.vat.sendAllOnly(self.target, verb, args)

    def isResolved(self):
        return true

    def sendMsg(self, msg):
        self.vat.qSendMsg(self.target, msg)

    def commit(self):
        pass


class UnconnectedRefController(RefControllerBase):
    def __init__(self, ref, problem, vat):
        self.ref = ref
        self.problem = problem
        self.vat = vat

    def state(self):
        return BROKEN

    def resolutionRef(self):
        return self.ref

    def doBreakage(self, verb, args):
        if len(args) == 1 and verb in ('__whenMoreResolved', '__whenBroken'):
            return self.vat.sendAllOnly(args[0], "run", self.ref)

    def callAll(self, verb, args):
        if verb == "_printOn":
            return self._printOn(*args)
        else:
            self.doBreakage(verb, args)
            raise self.problem

    def sendAll(self, verb, args):
        self._doBreakage(verb, args)
        return self

    def sendAllOnly(self, verb, args):
        return self._doBreakage(verb, args)

    def isResolved(self):
        return true

    def commit(self):
        pass

    def _printOn(self, out):
        out.raw_print(u'<ref broken by %r>' % (self.problem))


class Promise(MonteObject):
    def __getattr__(self, verb):
        return lambda *args: self._m_controller.callAll(verb, args)


class SwitchableRef(Promise):
    def __init__(self, target):
        self._m_controller = SwitchableRefController(self, target)


class BufferingRef(Promise):
    def __init__(self, buf):
        self._m_controller = BufferingRefController(self, buf)


class NearRef(Promise):
    def __init__(self, target, vat):
        self._m_controller = NearRefController(self, target, vat)


class UnconnectedRef(Promise):
    def __init__(self, problem, vat):
        self._m_controller = UnconnectedRefController(self, problem, vat)


def _toRef(self, o, vat):
    if isinstance(o, Promise):
        return o
    return NearRef(o, vat)
