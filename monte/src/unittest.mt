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

    to raises(f):
        var reason := null
        def fail(msg):
            reason := msg
        try:
            f(fail)
        catch e:
            pass
        if (reason != null):
            throw([_failure, "Failed to raise: " + reason])

def runTests(suites):
    for s in suites:
        traceln(`testing suite $s`)
        def tests := s(unitTestAssertions)
        for t in tests:
            traceln(`$t`)
            t()


runTests

