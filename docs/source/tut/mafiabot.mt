import "mafia" =~ [=> makeMafia :DeepFrozen]
import "irc/client" =~ [=> makeIRCClient :DeepFrozen,
                        => connectIRCClient :DeepFrozen]
exports (main)

def makeIRCService(makeTCP4ClientEndpoint, getAddrInfo, Timer,
                   hostname :Str) as DeepFrozen:
    def port := 6667  # TODO: named arg with default value

    return object IRC:
        to _printOn(out):
            out.print(`IRC($hostname)`)

        to connect(handler):
            def client := makeIRCClient(handler, Timer)

            def addrs := getAddrInfo(b`$hostname`, b``)
            return when (addrs) ->
                def choices := [
                    for addr in (addrs)
                    if (addr.getFamily() == "INET" &&
                        addr.getSocketType() == "stream") addr.getAddress()]
                traceln("choices:", choices)
                def [address] + _ := choices
                def ep := makeTCP4ClientEndpoint(address, port)
                connectIRCClient(client, ep)
                client


def makeModerator(channel :Str, nicknames: Set[Str], say) as DeepFrozen:
    def game := makeMafia(nicknames)
    object Player:
        to coerce(specimen, ej):
            if (nicknames.contains(specimen)):
                return specimen
            ej(`not a player in $channel`)

    def makePlayer(me :Player):
        return object player:
            to _printOn(out):
                out.print(`<mafia player $me in $channel>`)
            to voteFor(whom: Player):
                game.vote(me, whom)

                say(`$game`)

    def toPlayer := [for nick in (nicknames) nick => makePlayer(nick)]

    return object moderator:
        to _printOn(out):
            out.print(`<mafia moderator in $channel>`)
        to announce():
            say(`$game`)
        to getPlayer(name :Player):
            return toPlayer[name]
        to hasPlayer(specimen):
            return nicknames.contains(specimen)
        to getWinner():
            return game.getWinner()

# TODO: pickSecretChannelName for the mafia to gather in.
def makeMafiaBot() as DeepFrozen:
    def nick := "mafiaBot"
    def moderators := [].asMap().diverge()

    return object mafiaBot:
        to getNick():
            return nick

        to loggedIn(client):
            return null

        to privmsg(client, user, channel, message):
            traceln("mafiaBot got", message, "on", channel, "from", user)
            traceln(moderators)
            def who := user.getNick()

            if (channel == nick &&
                message =~ `join @dest` &&
                !moderators.contains(dest)):
                mafiaBot.join(client, who, dest)
            else if (channel != nick &&
                     message == "start"):
                mafiaBot.startGame(client, who, channel)
            else if (moderators.snapshot() =~ [(channel) => m] | _):
                if (message =~ `lynch @whom!` &&
                    m.hasPlayer(who) &&
                    m.hasPlayer(whom)):
                    m.getPlayer(who).voteFor(whom)
                    traceln("lynch", who, whom)
                if (m.getWinner() != null):
                    client.part(channel, "Good game!")
                    moderators.removeKey(channel)

        to join(client, who, channel):
            when(client.hasJoined(channel)) ->
                client.say(channel, `Thank you for inviting me, $who.`)
                client.say(channel, `Say "start" to begin.`)
            
        to startGame(client, who, channel):
            def say := fn txt { client.say(channel, txt) }
            escape badChannel:
                def users := client.getUsers(channel, badChannel)
                def players := [
                    for name => _ in (users)
                    if (name != nick)
                    # @chanop -> chanop
                    (if (name =~ `@@@op`) { op } else { name })].asSet()
                traceln("players:", players, users)

                def m := moderators[channel] := makeModerator(
                    channel, players, say)
                m.announce()

def main(argv,
         => makeTCP4ClientEndpoint,
         => Timer,
         => unsealException,
         => getAddrInfo) as DeepFrozen:
    def [hostname] := argv
    def irc := makeIRCService(makeTCP4ClientEndpoint, getAddrInfo, Timer,
                              hostname)
    irc.connect(makeMafiaBot())
