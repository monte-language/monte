def makeTerm := import("terml.makeTerm")
def makeTag := import("terml.makeTag")
def convertToTerm := import("terml.convertToTerm")
object termFactory:
    match [name, args]:
        makeTerm(makeTag(null, name, null), null,
                 [convertToTerm(a) for a in args], null)
