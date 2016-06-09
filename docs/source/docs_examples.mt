import "lib/json" =~ [=> JSON :DeepFrozen]
import "lib/codec/utf8" =~ [=> UTF8 :DeepFrozen]
exports (main)

def loadJSON(fr) as DeepFrozen:
    def bs := fr <- getContents()
    return when (bs) ->
        def via (UTF8.decode) json := bs
        def via (JSON.decode) obj := json
        obj

def runSuite(suite) as DeepFrozen:
    def [var wins, var losses, var aborts] := [0, 0, 0]
    for case in (suite):
        def [=>section, =>lineno, =>source, =>want] | _ := case

        def doOrAbort(thunk, getMsg, ej):
            try:
                return thunk()
            catch oops:
                traceln(`$section.rst:$lineno: ABORT: ${getMsg()}`)
                traceln.exception(oops)
                aborts += 1
                ej(oops)

        def tryEval(expr, msg, ej):
            return doOrAbort(fn { eval(expr, safeScope) },
                             fn { `$msg $expr` }, ej)

        escape abort:
            def fixAST(v):
                def isAST := want.contains("m`")
                return if (isAST) { v.canonical() } else { v }
            def expected := fixAST(tryEval(want, "expected result??", abort))
            def actual := fixAST(tryEval(source, "actual result??", abort))

            def result := doOrAbort(
                fn { actual == expected },
                fn { `$actual =??= $expected` }, abort)

            if (result):
                wins += 1
                # traceln(`$section.rst:$lineno: ok $wins $source => $expected`)
            else:
                losses += 1
                traceln(`$section.rst:$lineno: FAIL: $source => $actual != $expected`)
    return ["pass" => wins, "fail" => losses, "abort" => aborts]


def main(argv, => makeFileResource) as DeepFrozen:
    def suite := loadJSON(makeFileResource(argv.last()))
    when (suite) ->
        traceln(suite.size())
        def result := runSuite(suite)
        traceln(result)
