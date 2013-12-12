import weakref
from twisted.internet.defer import Deferred
from twisted.python.failure import Failure
from twisted.internet.task import coiterate
from twisted.python import log
from monte.objects import miranda_methods, E

_notARef = object()
_theViciousRef = object()
_pendingPromises = {}
_theQueue = []
_theCoiterator = None

def send(self, message, args, kwargs, resolver):
    _theQueue.append((_executeSend, (self, message, args, kwargs, resolver)))
    _maybeStartQueue()

def _executeSend(self, message, args, kwargs, resolver):
    state = _e_ref_state(self)
    if state == 'BROKEN':
        if message in ['whenBroken', '_whenMoreResolved']:
            sendOnly(args[0], '__call__', [self])
            return
    elif state == 'EVENTUAL':
        p = _asRef(self)
        p1, r1 = Ref.promise()
        p.messages.append((message, args, kwargs, r1))
        result = p1
    elif state == 'NEAR':
        if message == '_whenMoreResolved':
            sendOnly(args[0], '__call__', [self])
            return
        try:
            result = getattr(self, message)(*args, **kwargs)
        except Exception:
            result = Failure()
            log.err()
    if resolver:
        sendOnly(resolver, 'resolve', [result])

def sendOnly(self, message, args=None, kwargs=None):
    _theQueue.append((_executeSend, (self, message, (args or ()), (kwargs or {}), None)))
    _maybeStartQueue()

def _executeTurn():
    global _theCoiterator
    while _theQueue:
        f, args = _theQueue.pop(0)
        f(*args)
        yield None
    _theCoiterator = None

def _maybeStartQueue():
    global _theCoiterator
    if not _theCoiterator:
        _theCoiterator = coiterate(_executeTurn())

def wrap(v):
    if isinstance(v, Deferred):
        p, r = Ref.promise()
        v.addBoth(r.resolve)
        return p
    else:
        return v

class _Resolver(object):
    def __init__(self, p):
        self.promise = p

    def resolve(self, value):
        if self.promise is None:
            raise RuntimeError("Already resolved")
        self.promise.set_target(value)
        self.promise.commit()
        self.promise = None

    def smash(self, exc=None):
        self.resolve(Failure(exc))

def _toRef(o):
    if isinstance(o, Promise):
        return o
    else:
        return NearRef(o)

def _asRef(o):
    if id(o) not in _pendingPromises:
        return _notARef
    else:
        tp, p = _pendingPromises[id(o)]
        if tp is not o:
            # id reuse
            del _pendingPromises[id(o)]
            return _notARef
        else:
            return p


def isResolved(o):
    p = _asRef(o)
    if p is _notARef:
        return True
    elif p.switchable:
        return False
    p._shorten()
    target = _asRef(p.target)
    if target is _notARef:
        return True
    else:
        return isResolved(target)




def _whenResolvedReactor(callback, ref, resolver):
    done = [False]
    def whenResolvedRun(o):
        if done[0]:
            return None
        if isResolved(ref):
            try:
                outcome = callback(ref)
            except Exception:
                outcome = Failure()
            if resolver is not None:
                resolver.resolve(outcome)
            done[0] = True
        else:
            sendOnly(ref, '_whenMoreResolved', [whenResolvedRun])
    return whenResolvedRun




def _whenBrokenReactor(callback, ref, resolver):
    def whenBrokenRun(o):
        state = _e_ref_state(ref)
        if state == 'EVENTUAL':
            sendOnly(ref, '_whenMoreResolved', [whenBrokenRun])
            return
        if state == 'BROKEN':
            try:
                outcome = callback(ref)
            except Exception:
                outcome = Failure()
            if resolver is not None:
                resolver.resolve(outcome)
    return whenBrokenRun


def _e_ref_state(o):
    p = _asRef(o)
    if p is _notARef:
        return 'NEAR'
    else:
        if isinstance(p.target, Failure):
            return 'BROKEN'
        if p.switchable:
            return 'EVENTUAL'
        else:
            return 'NEAR'

def _get_target(o):
    p = _asRef(o)
    if p is _notARef:
        return o
    else:
        if p.switchable:
            return o
        else:
            return p.target

class Ref(object):
    @staticmethod
    def promise():
        buf = []
        sref = SwitchableRef(BufferingRef(buf))
        return (sref, LocalResolver(sref, buf))

    @staticmethod
    def broken(problem):
        return UnconnectedRef(problem)

    @staticmethod
    def optBroken(optProblem):
        if optProblem is None:
            return None
        else:
            return Ref.broken(optProblem)

    # elided: disconnected

    @staticmethod
    def isNear(ref):
        if isinstance(ref, Promise):
            return ref.state() == 'near'
        else:
            return True

    @staticmethod
    def isEventual(ref):
        if isinstance(ref, Promise):
            return ref.state() == 'eventual'
        else:
            return False

    @staticmethod
    def isBroken(ref):
        if isinstance(ref, Promise):
            return ref.state() == 'broken'
        else:
            return False

    @staticmethod
    def optProblem(ref):
        if isinstance(ref, Promise):
            return ref._problem
        else:
            return None

    @staticmethod
    def state(ref):
        if isinstance(ref, Promise):
            return ref._state
        else:
            return 'near'

    @staticmethod
    def resolution(ref):
        """
        Shortens refs, removing as much indirection as possible. If
        eventual or broken, returns eventual or broken ref. If near,
        returns a non-Ref.
        """
        if ref is None:
            return None
        if isinstance(ref, Promise):
            return ref.resolution()
        else:
            return ref

    @staticmethod
    def fulfillment(ref):
        ref = Ref.resolution(ref)
        optProb = Ref.optProblem(ref)
        if Ref.isResolved(ref):
            if optProb is None:
                return ref
            else:
                raise optProb
        else:
            raise RuntimeError("Not resolved: " + str(ref))

    @staticmethod
    def isResolved(ref):
        if isinstance(ref, Promise):
            return ref.isResolved()
        else:
            return True

    @staticmethod
    def isFar(ref):
        return Ref.isEventual(ref) and Ref.isResolved(ref)

    # TODO: isPassByProxy? isPBC?
    @staticmethod
    def whenResolved(o, callback):
        p, r = promise()
        sendOnly(o, '_whenMoreResolved',
                 [_whenResolvedReactor(callback, o, r)])
        return p

    @staticmethod
    def whenResolvedOnly(o, callback):
        p, r = promise()
        return sendOnly(o, '_whenMoreResolved',
                        [_whenResolvedReactor(callback, o, r)])

    @staticmethod
    def whenBroken(o, callback):
        p, r = promise()
        sendOnly(o, '_whenMoreResolved',
                 [_whenBrokenReactor(callback, o, r)])
        return p

    @staticmethod
    def whenBrokenOnly(o, callback):
        p, r = promise()
        return sendOnly(o, '_whenMoreResolved',
                        [_whenBrokenReactor(callback, o, r)])


class _Ref(object):

    def __init__(self):
        self.switchable = True
        self.target = _notARef
        self.messages = []
        self.tp = None

    def _get_current_object(self):
        self._shorten()
        t = self.target
        if t is _notARef:
            raise ValueError("Promise unresolved, synchronous operations not available")
        elif isinstance(t, Failure):
            t.raiseException()
        else:
            return t

    def set_target(self, target):
        if self.switchable:
            self.target = _get_target(target)
            if self is self.target:
                raise RuntimeError("Ref loop")
            else:
                while self.messages:
                    msg, args, kwargs, resolver = self.messages.pop(0)
                    send(self.target, msg, args, kwargs, resolver)
                self.messages = None
        else:
            raise RuntimeError("No longer switchable")


    def _shorten(self):
        subp = _asRef(self.target)
        if subp is not _notARef and _e_ref_state(subp) == 'NEAR':
            t = _get_target(subp.target)
            self.target = t

class NearRef(object):
    def __init__(self, val):
        self.target = val

    def optProblem(self):
        return None

    def resolution(self):
        return self.target

    def callAll(self, verb, args):
        return E.callAll(self.target, verb, args)

    def sendAll(self, verb, args):
        return E.sendAll(self.target, verb, args)

    def sendAllOnly(self, verb, args):
        return E.sendAllOnly(self.target, verb, args)

    def isResolved(self):
        return True

    def sendMsg(self, msg):
        from monte.objects.vat import theCurrentVat
        optProblem = theCurrentVat.qSendMsg(self.target, msg)
        if optProblem is not None:
            raise optProblem

    def commit(self):
        pass

    def _optSealedDispatch(self, brand):
        return Ref._optSealedDispatch(self.target, brand)

    def _conformTo(self, guard):
        return Ref.conformTo(self.target, guard)

    def _m___printOn(self, out):
        out.print_(self.target)

class UnconnectedRef(object):
    def __init__(self, problem):
        if problem is None:
            raise RuntimeError("Missing problem")
        self._problem = problem
        self._state = 'broken'

    def resolutionRef(self):
        return self

    def _doBreakage(self, verb, args):
        if len(args) == 1 and verb in ('__whenMoreResolved', '__whenBroken'):
            return sendOnly(args[0], 'run', self)
        else:
            return None

    def callAll(self, verb, args):
        self._doBreakage(verb, args)
        raise self._problem

    def sendAll(self, verb, args):
        self._doBreakage(verb, args)
        return self

    def sendAllOnly(self, verb, args):
        return self._doBreakage(verb, args)

    def isResolved(self):
        return True

    def setTarget(self, newTarget):
        raise RuntimeError("Not switchable")

    def commit(self):
        pass

    def _m___optSealedDispatch(self, brand):
        return miranda_methods.optSealedDispatch(self, brand)

    def _m___conformTo(self, guard):
        return miranda_methods.conformTo(self, guard)

    def _m___printOn(self, out):
        out.print_("<ref broken by ", self._problem, ">")


class _Buffer(object):
    #python is terrible
    def __init__(self, buf):
        self.buf = buf


class BufferingRef(object):
    def __init__(self, buf):
        self.buf = weakref.ref(_Buffer(buf))

    def optProblem(self):
        return None

    def resolutionRef(self):
        return self

    def state(self):
        return 'eventual'

    #XXX what calls this
    def callAll(self, verb, args):
        raise RuntimeError("Not synchronously callable (%s)" % (verb,))

    def sendAll(self, verb, args):
        optMsgs = self.buf()
        if optMsgs is None:
            return self
        else:
            p, r = Ref.promise()
            optMsgs.buf.append((r, verb, args))
            return (p, r)


    def sendAllOnly(self, verb, args):
        optMsgs = self.buf()
        if optMsgs is None:
            return self
        else:
            optMsgs.buf.append((None, verb, args))
            return None

    def isResolved(self):
        return False


    def setTarget(self, newTarget):
        raise RuntimeError("Not switchable")

    def commit(self):
        pass

    def deliverAll(self, buf, target, optSendingContext):
        msgs = self.buf.buf
        self.buf.buf = []
        targRef = _toRef(target)
        for msg in msgs:
            context = msg.getSendingContext()
            context.appendContext(optSendingContext)
            targRef.sendMsg(msg)
        return len(msgs)

    def _optSealedDispatch(self, brand):
        return miranda_methods._optSealedDispatch(self, brand)

    def _conformTo(self, guard):
        return miranda_methods.conformTo(self, guard)

    def _printOn(self, out):
        out.print_("<Promise>")


class SwitchableRef(object):
    def __init__(self, target):
        self.target = target
        self.isSwitchable = True

    def optProblem(self):
        if self.isSwitchable:
            return None
        else:
            self.resolutionRef()
            return self.target.optProblem()

    def resolutionRef(self):
        self.target = self.target.resolutionRef()
        if self.isSwitchable:
            return self
        else:
            return self.target

    def state(self):
        if self.isSwitchable:
            return "eventual"
        else:
            self.resolutionRef()
            return self.target.state()

    def callAll(self, verb, args):
        if self.isSwitchable:
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
            return False
        else:
            self.resolutionRef()
            return self.target.isResolved()

    def setTarget(self, newTarget):
        if self.isSwitchable:
           self.target = newTarget.resolutionRef()
           if self is self.target:
               raise RuntimeError("Ref loop")
        else:
            raise RuntimeError("No longer switchable")

    def commit(self):
        newTarget = self.target
        self.target = _theViciousRef
        self.switchable = False
        newTarget = _get_target(newTarget)
        if newTarget is _theViciousRef:
            raise RuntimeError("Ref loop")
        else:
            self.target = newTarget

    def _m___optSealedDispatch(self, brand):
        if self.isSwitchable:
            return miranda_methods.optSealedDispatch(self, brand)
        else:
            self.resolutionRef()
            return self.target._m___optSealedDispatch(self, brand)

    def _m___conformTo(self, guard):
        if self.isSwitchable:
            return miranda_methods.conformTo(self, guard)
        else:
            self.resolutionRef()
            return self.target._m___conformTo(guard)

    def _m___printOn(self, out):
        if self.isSwitchable:
            return out.print_("<Promise>")
        else:
            self.resolutionRef()
            self.target._printOn(out)



Promise = (NearRef, SwitchableRef, BufferingRef, UnconnectedRef)
