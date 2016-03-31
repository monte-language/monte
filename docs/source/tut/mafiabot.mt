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


object mafiaBot as DeepFrozen:
    to getNick():
        return "mafiaBot"

    to loggedIn(client):
        client.join("#montebot")
        
    to privmsg(client, user, channel, message):
        traceln("mafiaBot got", message, "on", channel, "from", user)


def main(argv,
         => makeTCP4ClientEndpoint,
         => Timer,
         => unsealException,
         => getAddrInfo) as DeepFrozen:
    def [hostname] := argv
    def net := makeNet(makeTCP4ClientEndpoint, getAddrInfo)
    when (def ep := net.connect(b`$hostname`, 6667)) ->
        def client := makeIRCClient(mafiaBot, Timer)
        connectIRCClient(client, ep)
    catch oops:
        traceln("oops!", unsealException(oops))
