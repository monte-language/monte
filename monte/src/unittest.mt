object unitTestAssertions:
    to equal(left, right):
        if (left != right):
            throw(`assertion failure: $left != $right`)

def runTests(suites):
    for s in suites:
        traceln(`testing suite $s`)
        def tests := s(unitTestAssertions)
        for t in tests:
            traceln(`$t`)
            t()


runTests

