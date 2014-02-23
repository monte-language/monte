
def getIterator(coll):
    from monte.runtime.compiler_helpers import wrap
    if isinstance(coll, dict):
        return coll.iteritems()
    elif isinstance(coll, (tuple, list)):
        return ((wrap(i), v) for (i, v) in enumerate(coll))
    else:
        gi = getattr(coll, "getIterator", None)
        if gi is not None:
            return gi()
        else:
            return ((wrap(i), v) for (i, v) in enumerate(coll))


def monteLooper(coll, obj):
    it = getIterator(coll)
    for key, item in it:
        obj.run(key, item)
