import sys
from ecru.api import incrementalEval, e_privilegedScope, eval as eEval
from ecru.api import iterate as ecruIterate
from twisted.words.protocols.irc import IRCClient
from twisted.internet import reactor
from twisted.python import log
from twisted.internet.defer import Deferred
from twisted.internet.protocol import ReconnectingClientFactory
from twisted.internet.task import coiterate

CHANNEL = "#tmlabs"
NICK = "ecrubot"

class EcruIRCClient(IRCClient):
    """
    IRC REPL for Ecru.
    """

    def signedOn(self):
        """
        Join a channel.
        """
        self.setNick(NICK)
        self.join(CHANNEL)


    def privmsg(self, user, channel, message):
        if channel == user:
            return
        fromNick = user.split('!', 1)[0]
        if message.startswith(self.nickname + ":"):
            msg = message.split(self.nickname + ":",1)[1].strip()
        elif message.startswith("?"):
            msg = message.split("?",1)[1].strip()
        else:
            return
        self.factory.evaluate(self, fromNick, channel, msg).addCallback(
            lambda r: self.msg(channel, r))


class EcruBotFactory(ReconnectingClientFactory):
    """
    Factory for Ecru IRC bot.
    """
    protocol = EcruIRCClient

    def __init__(self):
        self.scopes = {}
        self.coiterator = None
        self.defaultScope, _ = eEval("safeScope", e_privilegedScope, False)
        self.whenResolved, _ = eEval("Ref.whenResolved", e_privilegedScope,
                                     False)
        self.whenBroken, _ = eEval("Ref.whenBroken", e_privilegedScope, False)

    def _whenQuiescent(self, _):
        self.coiterator = None

    def evaluate(self, protocol, user, channel, msg):
        """
        Evaluate an expression in a scope particular to the given user.
        """
        scope = self.scopes.get(user, None)
        if scope is None:
            apm, userScope = eEval("def print; def addPrintMethods(p) "
                                   "{ bind print := p }", self.defaultScope,
                                   False)
            def ircPrint(result):
                print "printmsg", channel, result, user
                protocol.msg(channel, "%s -- %s" % (result, user))
            apm.run(ircPrint)
            scope = self.scopes[user] = userScope
        p = incrementalEval(msg, scope)
        if self.coiterator is None:
            self.coiterator = coiterate(iter(ecruIterate, False))
            self.coiterator.addCallback(self._whenQuiescent)
        d = Deferred()
        self.whenResolved.run(p, d.callback)
        self.whenBroken.run(p, d.errback)
        def _whenEvaluated(res):
            value, newScope = res
            self.scopes[user] = newScope
            return value
        d.addCallback(_whenEvaluated)
        return d



if __name__ == '__main__':
    log.startLogging(sys.stdout)
    f = EcruBotFactory()
    reactor.connectTCP("irc.freenode.net", 6667, f)
    reactor.run()

