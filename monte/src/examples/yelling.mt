def makeMapPump := import("tubes.mapPump")
def makeTube := import("tubes.tube")
def makeReadFount := import("tubes.readFount")
def makeWriteDrain := import("tubes.writeDrain")

def yell(bytes):
    return "".join([c.asChar() for c in bytes]).toUpperCase()

def main():
    def yellingPump := makeMapPump(yell)
    def yellingTube := makeTube(yellingPump)

    makeReadFount(stdin).flowTo(yellingTube).flowTo(makeWriteDrain(stdout))
