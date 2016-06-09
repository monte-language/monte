import "lib/json" =~ [=> JSON :DeepFrozen]
import "lib/codec/utf8" =~ [=> UTF8 :DeepFrozen]
exports (main)

"docs_examples: run tests extracted from Monte docs

Usage:
 python extract_examples.py suite.json *.rst
 monte eval docs_examples.mt suite.json

See also extract_examples.py and ../Makefile.
"

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

        def tryEval(expr, msg, ej):
            return try { eval(expr, safeScope) } catch oops { ej([oops, msg]) }

        def fixAST := want.contains("m`").pick(fn ast { ast.canonical() },
                                               fn v { v })

        escape abort:
            def expected := fixAST(tryEval(want, "expected result??", abort))
            def actual := fixAST(tryEval(source, "actual result??", abort))

            def result := try { actual == expected } catch oops {
                abort([oops, `$actual =??= $expected`]) }

            if (result):
                wins += 1
                # traceln(`$section.rst:$lineno: ok $wins $source => $expected`)
            else:
                losses += 1
                traceln(`$section.rst:$lineno: FAIL: $source => $actual ; expected: $expected`)
        catch [oops, msg]:
            aborts += 1
            traceln(`$section.rst:$lineno: ABORT: $msg`)
            traceln.exception(oops)

    return ["pass" => wins, "fail" => losses, "abort" => aborts]


def main(argv, => makeFileResource) as DeepFrozen:
    def suite := loadJSON(makeFileResource(argv.last()))
    when (suite) ->
        traceln(suite.size())
        def result := runSuite(suite)
        traceln(result)
