object fold:
    # A small collection of useful generalized catamorphisms over iterables.

    to foldl(operation, var accumulator, iterable):
        for item in iterable:
            accumulator := operation(accumulator, item)
        return accumulator

    to run(operation, accumulator, iterable):
        return fold.foldl(operation, accumulator, iterable)
