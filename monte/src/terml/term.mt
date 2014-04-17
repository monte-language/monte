interface TermType:
    pass

object Term:
    to coerce(specimen, ej):
        if (specimen =~ t :TermType):
            return t
        else:
            throw.eject(ej, "is not a term")
