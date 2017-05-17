import "lib/monte/mast" =~ [=> makeMASTContext :DeepFrozen]
import "lib/json" =~ [=> JSON :DeepFrozen]
import "lib/streams" =~ [=> flow :DeepFrozen, => makeSink :DeepFrozen]
import "lib/codec/utf8" =~ [=> UTF8 :DeepFrozen]

exports (main)

def makeTextReader(source) as DeepFrozen:
    def [chunkVow, collector] := makeSink.asList()
    flow(source, collector)

    return object textReader:
        to read():
            return when (def chunks := chunkVow) ->
                UTF8.decode(b``.join(chunks), throw)


def withMAST(case :DeepFrozen) :Map[Str, DeepFrozen] as DeepFrozen:
    def serialize(tree :DeepFrozen) as DeepFrozen:
        def context := makeMASTContext()
        context(tree)
        return context.bytes()

    def hexDigit :DeepFrozen := "0123456789ABCDEF"

    def hex(bs :Bytes) :Str as DeepFrozen:
        def hi := fn b { b >> 4 }
        def lo := fn b { b & 0x0f }
        return "".join([for b in (bs) "" + hexDigit[hi(b)] + hexDigit[lo(b)]])

    def expr := ::"m``".fromStr(case["source"])
    def mast := serialize(expr.expand())

    def fname := `${case["section"]}_${case["lineno"]}.mast`
    trace(`$fname: ${mast.size()} bytes for ${case["source"]}`)

    return case.with("MAST", hex(mast))


def main(argv, => stdio, => makeFileResource) as DeepFrozen:
    def [_eval, _script, outfn] := argv
    when (def text := makeTextReader(stdio.stdin()).read()) ->
        def suite := JSON.decode(text, throw)
        trace(`suite size: ${suite.size()}`)

        def suiteWithMast := [for case in (suite) withMAST(case)]
        def out := UTF8.encode(JSON.encode(suiteWithMast, throw), throw)
        makeFileResource(outfn).setContents(out)
    catch oops:
        traceln.exception(oops)
