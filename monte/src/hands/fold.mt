object fold implements DeepFrozen:
    # A small collection of useful generalized catamorphisms over iterables.

    to run(operation, accumulator, iterable):
        return fold.foldl(operation, accumulator, iterable)

    to foldl(operation, var accumulator, iterable):
        for item in iterable:
            accumulator := operation(accumulator, item)
        return accumulator

    to foldr(operation, var accumulator, iterable):
        # There's no reversal operation on lists, so we have to do this the
        # hard way.
        var index := iterable.size()
        while (index > 0):
            index -= 1
            accumulator := operation(iterable[index], accumulator)
        return accumulator
