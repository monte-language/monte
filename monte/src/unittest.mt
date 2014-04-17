object _failure:
    pass

object unitTestAssertions:
    to equal(left, right):
        if (left != right):
            throw([_failure, `Not equal: $left != $right`])
    to ejects(f):
        var reason := null
        def fail(msg):
            reason := msg
        escape ej:
            f(ej, fail)
        if (reason != null):
            throw([_failure, "Failed to eject: " + reason])

def runTests(suites):
    for s in suites:
        traceln(`Testing suite: $s`)
        def tests := s(unitTestAssertions)
        for t in tests:
            trace(`Testing case: $t`)
            try:
                t()
                traceln(` PASSED`)
            catch [==_failure, f]:
                traceln(` FAILURE: $f`)
            catch e:
                traceln(` ERROR: $e`)
