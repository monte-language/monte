def makeScanPump(f, a):
    var accum := a
    return object scanPump:
        to started():
            pass
        to received(item):
            accum := f(accum, item)
            return [accum]
        to progressed(amount):
            pass
        to stopped():
            pass
