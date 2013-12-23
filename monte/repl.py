from twisted.internet import reactor
from twisted.conch.stdio import runWithProtocol
from twisted.conch.manhole import Manhole
from twisted.python import log

class MonteInterpreter(object):
    def __init__(self, handler):
        self.handler = handler

    def push(self, line):
        self.write("input: %r\n" % line)

    def resetBuffer(self):
        pass

    def write(self, data, async=False):
        self.handler.addOutput(data, async)

class MonteRepl(Manhole):
    def connectionMade(self):
        Manhole.connectionMade(self)
        self.interpreter = MonteInterpreter(self)

    def connectionLost(self, reason):
        reactor.stop()


def startRepl():
    log.startLogging(open('child.log', 'w'))
    runWithProtocol(MonteRepl)




















