object unitTestAssertions:
    to equal(left, right):
        if (left != right):
            throw(`Assertion failure: $left != $right`)

def runTests(suites):
    for s in suites:
        traceln(`Testing suite: $s`)
        def tests := s(unitTestAssertions)
        for t in tests:
            trace(`Testing case: $t`)
            try:
                t()
                traceln(` PASSED`)
            catch e:
                traceln(` ERROR: $e`)
