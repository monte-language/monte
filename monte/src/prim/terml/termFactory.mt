module makeTerm :DeepFrozen, makeTag :DeepFrozen, convertToTerm :DeepFrozen
export (termFactory)
object termFactory as DeepFrozen:
    match [name, args]:
        makeTerm(makeTag(null, name, null), null,
                 [convertToTerm(a, null) for a in args], null)
