def makeMapPump := import("tubes.mapPump")
def makeTube := import("tubes.tube")
def makeReadFount := import("tubes.readFount")
def makeWriteDrain := import("tubes.writeDrain")

def yell(s):
    return s.toUpperCase()

def yellingPump := makeMapPump(yell)
def yellingTube := makeTube(yellingPump)

makeReadFount(stdin).flowTo(yellingTube).flowTo(makeWriteDrain(stdout))
