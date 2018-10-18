import "lib/json" =~ [=> JSON]
import "lib/codec/utf8" =~ [=> UTF8]
exports (main)

def usage :Bytes := UTF8.encode("docs_examples: run tests extracted from Monte docs

Usage:
 monte eval docs_examples.mt <suitefile> <timeout>

e.g.
 monte eval docs_examples.mt suite.json 10

See extract_examples.py to generate <suitefile>.

See also extract_examples.py and ../Makefile.
", null)

def runSuite(suite, timeout) as DeepFrozen:
    def CaseID := Pair[Str, Int]  # section, lineno
    def Status := NullOk[Bool]
    def aborted := fn s :Status { s == null }
    def passed := fn s :Status { s != null && s }
    def failed := fn s :Status { s != null && !s}
    def var status :Map[CaseID, Status] := [].asMap()
    def getResults():
        def pick := fn crit { [for cid => s in (status) ? (crit(s)) cid] }
        return ["pass" => pick(passed),
                "fail" => pick(failed),
                "abort" => pick(aborted),
                "pending" => [for [=>section, =>lineno] | _ in (suite)
                              ? (!status.contains([section, lineno]))
                              [section, lineno]]]
    def [var wins :Int, var losses :Int, var aborts :Int] := [0, 0, 0]
    def var done :Bool := false
    def [resultsP, resultsR] := Ref.promise()
    when (timeout) ->
        done := true
        resultsR.resolve(getResults())
    def areWeThereYet():
        if (!done && wins + losses + aborts >= suite.size()):
            done := true
            resultsR.resolve(getResults())

    for case in (suite):
        def [=>section, =>lineno, =>source, =>want] | _ := case
        def caseId := [section, lineno]

        def tryEval(expr, msg, ej):
            return try { eval(expr, safeScope) } catch oops { ej([oops, msg]) }

        def fixAST := want.contains("m`").pick(fn ast { ast.canonical() },
                                               fn v { v })

        escape abort:
            def expected :Near := tryEval(want, "expected result??", abort)
            def actual := tryEval(source, "actual result??", abort)

            when (actual) ->
                if (fixAST(actual) == fixAST(expected)):
                    status with= (caseId, true)
                    wins += 1
                    # traceln(`$section.rst:$lineno: ok $wins $source => $expected`)
                else:
                    traceln(`$section.rst:$lineno: FAIL: $source => $actual ; expected: $expected`)
                    status with= (caseId, false)
                    losses += 1
                areWeThereYet()
        catch [oops, msg]:
            traceln(`$section.rst:$lineno: ABORT: $msg`)
            traceln.exception(oops)
            status with= (caseId, null)
            aborts += 1
            areWeThereYet()

    return resultsP


def main(argv, => stdio, => makeFileResource, => Timer) as DeepFrozen:
    escape ux:
        def [via (_makeDouble) timeout, suiteFile] + _ exit ux := argv.reverse()

        when (def bytes := makeFileResource(suiteFile) <- getContents()) ->
            escape fmtErr:
                def via (UTF8.decode) chars exit fmtErr := bytes
                def via (JSON.decode) suite exit fmtErr := chars

                traceln(`Testing ${suite.size()} cases with $timeout sec timeout.`)
                when (def result := runSuite(suite, Timer.fromNow(timeout))) ->
                    traceln([for status => caseIds in (result)
                             status => caseIds.size()])
                    traceln(`Timed out: ${result["pending"]}`)
                    0
            catch err:
                traceln(`cannot parse JSON from $suiteFile`)
                traceln.exception(err)
                1
        catch ioErr:
            traceln(`failed to getContents of $suiteFile`)
            traceln.exception(ioErr)
    catch _:
        def stderr := stdio.stderr()
        when (stderr<-(usage)) ->
            stderr<-complete()
            1
