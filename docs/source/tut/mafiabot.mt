import "mafia" =~ [=> makeMafia :DeepFrozen]
import "irc/client" =~ [=> makeIRCClient :DeepFrozen,
                        => connectIRCClient :DeepFrozen]
import "lib/entropy/entropy" =~ [=> makeEntropy :DeepFrozen]
import "lib/entropy/pcg" =~ [=> makePCG :DeepFrozen]
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
                def [address] + _ := choices
                def ep := makeTCP4ClientEndpoint(address, port)
                connectIRCClient(client, ep)
                client

def makeChannelVow(client, name) as DeepFrozen:
    "Return a vow because say() won't work until we have joined."
    def [wait, done] := Ref.promise()
    var waitingFor :NullOk[Set[Str]]:= null

    object chan:
        to _printOn(out):
            out.print(`<channel $name>`)
        to getName():
            return name
        to hasJoined():
            return client.hasJoined(name)
        to say(message) :Void:
            client.say(name, message)
        to getUsers(notReady):
            return client.getUsers(name, notReady)
        to waitFor(them :Set[Str]):
            waitingFor := them
            return wait
        to notify():
            if (waitingFor != null):
                escape oops:
                    def present := chan.getUsers(oops).getKeys().asSet()
                    traceln("notify present:", present, waitingFor,
                            waitingFor - present)
                    if ((waitingFor - present).size() == 0):
                        waitingFor := null
                        done.resolve(present)
        to tell(whom, what, notInChannel):
            if (chan.getUsers(notInChannel).contains(whom)):
                client.say(whom, what)
            else:
                notInChannel(`cannot tell $whom: not in $name`)
        to part(message):
            client.part(name, message)
    return when(chan.hasJoined()) ->
        chan


def makeModerator(playerNames :Set[Str], rng,
                  chan :Near, mafiaChan) as DeepFrozen:
    def [=> game, => mafiosos] := makeMafia(playerNames, rng)
    var night0 := true

    def makePlayer(me :Str):
        return object player:
            to _printOn(out):
                out.print(`<player $me>`)
            to voteFor(nominee :Str):
                try:
                    game.vote(me, nominee)
                catch _:
                    # nominee is not (any longer) a player
                    return
                chan.say(game.advance())

    def toPlayer := [for nick in (playerNames) nick => makePlayer(nick)]

    return object moderator:
        to _printOn(out):
            out.print(`<moderator in $chan>`)

        to begin():
            # Night 0
            chan.say(`$game`)
            when (mafiaChan) ->
                escape notHere:
                    for maf in (mafiosos):
                        chan.tell(
                            maf, `You're a mafioso in $chan.`, notHere)
                        chan.tell(
                            maf, `Join $mafiaChan to meet the others.`, notHere)
                traceln("waiting for", mafiosos, "in", mafiaChan)
                when (mafiaChan.waitFor(mafiosos)) ->
                    traceln("done waiting for", mafiosos)
                    night0 := false
                    # Morning of day 1...
                    chan.say(game.advance())

        to said(who :Str, message :Str) :Bool:
            "Return true to contine, false if game over."
            mafiaChan.notify()
            traceln("notifying", mafiaChan)
            if (night0):
                return true
            if (message =~ `lynch @whom!`):
                escape notPlaying:
                    def p := moderator.getPlayer(who, notPlaying)
                    p.voteFor(whom)
                    traceln("lynch", who, whom)

                    if (game.getWinner() =~ winner ? (winner != null)):
                        moderator.end()

            return game.getWinner() == null

        to getPlayer(name, notPlaying):
            return toPlayer.fetch(name, notPlaying)

        to end():
            chan.say(`$game`)
            chan.part("Good game!")
            mafiaChan.part("bye bye")


def makeMafiaBot(rng) as DeepFrozen:
    def nick := "mafiaBot"
    def chanMod := [].asMap().diverge()
    def keys := [].asMap().diverge()

    return object mafiaBot:
        to getNick():
            return nick

        to loggedIn(client):
            return null

        to privmsg(client, user, channel, message):
            # traceln("mafiaBot got", message, "on", channel, "from", user,
            #         "channels", chanMod.getKeys())
            def who := user.getNick()

            if (message =~ `join @dest` &&
                channel == nick &&
                !keys.contains(dest)):
                mafiaBot.join(client, who, dest)
            else if (message == "start" &&
                     !keys.contains(channel)):
                when(def chan := makeChannelVow(client, channel)) ->
                    mafiaBot.startGame(client, chan, channel)
            else if (chanMod.snapshot() =~ [(channel) => m] | _):
                if (!m.said(who, message)):
                    def chKey := keys[channel]
                    chanMod.removeKey(channel)
                    chanMod.removeKey(chKey)
                    keys.removeKey(channel)
                    keys.removeKey(chKey)
                    traceln("removed", channel, chKey)

        to join(client, who :Str, channel :Str):
            when(client.hasJoined(channel)) ->
                client.say(channel, `Thank you for inviting me, $who.`)
                client.say(channel, `Say "start" to begin.`)

        to startGame(client, chan :Near, channel :Str):
            def secret := `$channel-${rng.nextInt(2 ** 32)}`
            def secretChan := makeChannelVow(client, secret)
            escape notReady:
                def users := chan.getUsers(notReady)
                def playerNames := [
                    for name => _ in (users)
                    if (name != nick)
                    # @chanop -> chanop
                    (if (name =~ `@@@op`) { op } else { name })]
                traceln("players:", playerNames, users)

                def m := makeModerator(playerNames.asSet(), rng,
                                       chan, secretChan)
                chanMod[channel] := chanMod[secret] := m
                keys[channel] := secret
                keys[secret] := channel
                m.begin()

def main(argv,
         => makeTCP4ClientEndpoint,
         => Timer,
         => currentRuntime,
         => getAddrInfo) as DeepFrozen:
    def [_, seed] := currentRuntime.getCrypt().makeSecureEntropy().getEntropy()
    def rng := makeEntropy(makePCG(seed, 0))
    def [hostname] := argv
    def irc := makeIRCService(makeTCP4ClientEndpoint, getAddrInfo, Timer,
                              hostname)
    irc.connect(makeMafiaBot(rng))
