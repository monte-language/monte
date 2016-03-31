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


def makeMafiaBot() as DeepFrozen:
    def nick := "mafiaBot"
    def channels :List[Str] := ["#montebot"]
    var game := null
    var players := []

    return object mafiaBot:
        to getNick():
            return nick

        to loggedIn(client):
            for channel in channels:
                client.join(channel)
                client.say(channel, "Who wants to play mafia?")

        to privmsg(client, user, channel, message):
            traceln("mafiaBot got", message, "on", channel, "from", user)
            def who := user.getNick()
            def say := fn txt { client.say(channel, txt) }
            switch (message):
                match `I want to play.`:
                    if (game == null):
                        players with= (who)
                        say(`Who else besides $players?`)
                    else:
                        say("Sorry, $who, we already started.")
                match `mafiaBot: start`:
                    if (players.size() >= 2):
                        say(`Starting with $players...`)
                        game := makeMafia(players.snapshot().asSet())
                        say("TODO: implement game play.")
                    else:
                        say(`We need more players, $who!`)
                match _:
                    null


def main(argv,
         => makeTCP4ClientEndpoint,
         => Timer,
         => unsealException,
         => getAddrInfo) as DeepFrozen:
    def [hostname] := argv
    def irc := makeIRCService(makeTCP4ClientEndpoint, getAddrInfo, Timer,
                              hostname)
    irc.connect(makeMafiaBot())
