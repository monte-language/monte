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
            while (drain != null & pauses == 0 & index >= data.size()):
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
    return object tube:
        to deliver(item):
            pump.received(item)


def f := makeListFount([1, 2, 3, 4, 5])
def d := makeListDrain()
f.flowTo(d)
traceln(`${d.getContents()}`)
