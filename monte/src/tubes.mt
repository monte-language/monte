def makeUnpauser(thunk):
    var called := false
    return object pause:
        to unpause():
            if (!called):
                called := true
                thunk()


def makeListFount(data):
    var drain := null
    var index := 0
    var pauses := 0
    return object listFount:
        to sendNext():
            while (drain != null & pauses == 0 & index < data.size()):
                drain.receive(data[index])
                index += 1
        to flowTo(newDrain):
            if (newDrain == null):
                return null
            if (index >= data.size()):
                return null
            drain := newDrain
            def nextFount := drain.flowingFrom(listFount)
            listFount.sendNext()
            return nextFount
        to pauseFlow():
            pauses += 1
            def unpause():
                pauses -= 1
                listFount.sendNext()
            return makeUnpauser(unpause)
        to stopFlow():
            if (drain != null):
                drain.flowStopped()
            drain := null


def makeListDrain():
    def collector := [].diverge()
    return object listDrain:
        to getContents():
            return collector.snapshot()
        to flowingFrom(fount):
            return null
        to receive(item):
            collector.push(item)
            return 0.0
        to progress(amount):
            pass
        to flowStopped():
            pass


def makePump():
    return object pump:
        to started():
            pass
        to received(item):
            return item
        to progressed(amount):
            pass
        to stopped():
            pass


def makeTube(pump):
    var upstream := var downstream := null
    var pause := null
    var stash := null
    return object tube:
        to flowingFrom(fount):
            upstream := fount
            return tube
        to receive(item):
            def pumped := pump.received(item)
            if (downstream == null):
                pause := upstream.pauseFlow()
                stash := pumped
                return null
            else:
                return downstream.receive(pumped)
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
            if (stash != null):
                downstream.receive(stash)
                stash := null
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


def makeMapPump := import("tubes.mapPump")

var f := makeListFount([1, 2, 3, 4, 5])
var p := makeMapPump(def _(x) { return x + 1 })
var t := makeTube(p)
var d := makeListDrain()
f.flowTo(t).flowTo(d)
traceln(`${d.getContents()}`)
