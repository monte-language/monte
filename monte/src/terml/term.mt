#XXX terrible

def makeTerm := import("terml.makeTerm")
def TermType := makeTerm(null, null, null, null)._getAllegedType()

object Term:
    to coerce(specimen, ej):
        if (specimen._getAllegedType() != TermType):
            throw.eject(ej, "is not a term")
