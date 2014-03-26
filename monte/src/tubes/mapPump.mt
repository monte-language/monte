def makeMapPump(f):
    return object mapPump:
        to started():
            pass
        to received(item):
            return f(item)
        to progressed(amount):
            pass
        to stopped():
            pass
