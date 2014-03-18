def _any(l) :boolean:
    var rv :boolean := false
    for x in l:
        rv |= x
    return rv

def _all(l) :boolean:
    var rv :boolean := true
    for x in l:
        rv &= x
    return rv

[_any, _all]
