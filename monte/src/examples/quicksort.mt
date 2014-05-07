# Ever seen a Haskell neophyte talk about how elegant Haskell's quicksort is?
def quicksort(l):
    # I'd like this to be `return switch` but the parser can't deal with it.
    switch (l):
        match []:
            return []
        match [head] + tail:
            def before := quicksort([i for i in tail if i < head])
            def after := quicksort([i for i in tail if i >= head])
            return before + [head] + after

traceln(quicksort([1, 0, -1, 2, 42, 7, 0, 1]))
