def makeUnpauser := import("tubes.unpauser")

def makeReadFount(source):
    # Read from an asynchronous source, possibly outside the runtime, and feed
    # its output to a drain.
    var drain := null
    var pending := null
    var pauses := 0

    return object readFount:
        to _getNext():
            if (pending == null):
                def data := source<-read()
                when (data) ->
                    pending := data
                    readFount._checkFlow()

        to _checkFlow():
            if (pauses == 0 & pending != null & drain != null):
                drain.receive(pending)
                pending := null
                readFount._getNext()

        to flowTo(newDrain):
            drain := newDrain
            if (drain == null):
                return null

            def nextFount := drain.flowingFrom(readFount)
            readFount._getNext()
            return nextFount

        to pauseFlow():
            pauses += 1
            def unpause():
                pauses -= 1
                readFount._checkFlow()
            return makeUnpauser(unpause)

        to stopFlow():
            if (drain != null):
                drain.flowStopped()
            drain := null
