def makeTerm :DeepFrozen := import("terml.makeTerm")
def makeTag :DeepFrozen := import("terml.makeTag")
def convertToTerm :DeepFrozen := import("terml.convertToTerm")
object termFactory as DeepFrozen:
    match [name, args]:
        makeTerm(makeTag(null, name, null), null,
                 [convertToTerm(a, null) for a in args], null)
