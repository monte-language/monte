def makeTube(pump):
    var upstream := var downstream := null
    var pause := null
    var stash := []
    return object tube:
        to flowingFrom(fount):
            upstream := fount
            return tube
        to receive(item):
            def pumped := pump.received(item)
            if (downstream == null && pause == null):
                pause := upstream.pauseFlow()
                stash += pumped
                return null
            else:
                for pumpedItem in pumped:
                    downstream.receive(pumpedItem)
        to progress(amount):
            if (downstream != null):
                downstream.progress(amount)
        to flowStopped():
            if (downstream != null):
                downstream.flowStopped()
        to flowTo(drain):
            if (drain == null):
                return null
            downstream := drain
            def nextFount := drain.flowingFrom(tube)
            if (stash.size() != 0):
                for item in stash:
                    downstream.receive(item)
                stash := []
            if (pause != null):
                pause.unpause()
                pause := null
            return nextFount
        to pauseFlow():
            return upstream.pauseFlow()
        to stopFlow():
            downstream.flowStopped()
            downstream := null
            return upstream.stopFlow()
