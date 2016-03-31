import "mafia" =~ [=> makeMafia :DeepFrozen]
import "irc/client" =~ [=> makeIRCClient :DeepFrozen,
                        => connectIRCClient :DeepFrozen]
exports (main)

def makeNet(makeTCP4ClientEndpoint, getAddrInfo) as DeepFrozen:
    return object Net:
        to connect(host :Bytes, port :Int):
            def addrs := getAddrInfo(host, b``)
            return when (addrs) ->
                def choices := [
                    for addr in (addrs)
                    if (addr.getFamily() == "INET" &&
                        addr.getSocketType() == "stream") addr.getAddress()]
                traceln("choices:", choices)
                def [address] + _ := choices
                makeTCP4ClientEndpoint(address, port)


def makeMafiaBot() as DeepFrozen:
    def nick := "mafiaBot"
    def channels :List[Str] := ["#montebot"]
    var game := null
    var players := [].asSet()

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
                        game := makeMafia(players)
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
    def net := makeNet(makeTCP4ClientEndpoint, getAddrInfo)
    when (def ep := net.connect(b`$hostname`, 6667)) ->
        def client := makeIRCClient(makeMafiaBot(), Timer)
        connectIRCClient(client, ep)
    catch oops:
        traceln("oops!", unsealException(oops))
