object enumerate:
    to withStart(iterable, var start):
        def rv := [].diverge()
        for item in iterable:
            rv.push([start, item])
            start := start.next()
        return rv.snapshot()

    to run(iterable):
        return enumerate.withStart(iterable, 0)
