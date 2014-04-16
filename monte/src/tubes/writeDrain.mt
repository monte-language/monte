def makeWriteDrain(dest):
    return object writeDrain:
        to flowingFrom(fount):
            return null
        to receive(item):
            dest<-write(item)
            return 0.0
        to progress(amount):
            pass
        to flowStopped():
            pass
