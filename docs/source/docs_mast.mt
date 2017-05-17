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


def serialize(tree :DeepFrozen) as DeepFrozen:
    def context := makeMASTContext()
    context(tree)
    return context.bytes()


def main(_argv, => stdio, => makeFileResource) as DeepFrozen:
    when (def text := makeTextReader(stdio.stdin()).read()) ->
        def suite := JSON.decode(text, throw)
        trace(`suite size: ${suite.size()}`)

        for case in (suite):
            def expr := ::"m``".fromStr(case["source"])
            def mast := serialize(expr.expand())
            def fname := `${case["section"]}_${case["lineno"]}.mast`
            trace(`$fname: ${mast.size()} bytes for ${case["source"]}`)
            makeFileResource(fname).setContents(mast)
