import "lib/tubes" =~ [=> makeUTF8EncodePump :DeepFrozen,
                       => makePumpTube :DeepFrozen]
exports (main)


def makeFormatter(drain) as DeepFrozen:
    def h := [null, "=", "-", "~"]

    def rep(s :Str, qty :Int) :Str as DeepFrozen:
        if (qty < 1):
            return ""
        return "".join([for _ in (1..qty) s])

    def dedent(paragraph :Str, =>indent := 0) :Str as DeepFrozen:
        "Remove leading spaces from every line of a paragraph."

        def pfx := rep("   ", indent)
        def pieces := [for line in (paragraph.split("\n"))
                       pfx + line.trim()]
        return "\n".join(pieces)


    return object formatter:
        to heading(level :(1..!h.size()), text):
            drain.receive(`$\n$text$\n${rep(h[level], text.size())}$\n$\n`)

        to paras(text :Str, =>indent := 0):
            drain.receive(dedent(text, "indent"=>indent).trim() + "\n\n")

        to item(text :Str):
            drain.receive(`      - $text$\n`)
        to endList():
            drain.receive("\n")

        to dt(term :Str):
            drain.receive(term + "\n")

        to dd(text :Str):
            drain.receive(dedent(text, "indent"=>1) + "\n")

        to module(name :Str):
            # cheat a little and use the Python domain for Monte.
            drain.receive(`.. py:module:: $name$\n$\n`)

        to data(name :Str, docstring :Str):
            drain.receive(`.. py:data:: $name$\n$\n`)
            if (docstring != null):
                drain.receive(dedent(docstring, "indent" => 1) + "\n\n")

        to method_(sig :Str, docstring :NullOk[Str]):
            drain.receive(`   .. py:method:: $sig$\n$\n`)
            if (docstring != null):
                drain.receive(dedent(docstring, "indent" => 2) + "\n\n")

        to todo(text :Str):
            drain.receive(".. todo::\n")
            drain.receive(dedent(text, "indent" => 1) + "\n\n")

object Not as DeepFrozen:
    to get(subGuard):
        return object notSubGuard:
            to coerce(specimen, ej):
                escape not:
                    subGuard.coerce(specimen, not)
                    ej("not")
                return specimen


def makeDocstringWalker(doc) as DeepFrozen:
    return object walker:
        to explainScope(name :Str, scope :Map,
                        sections :Map[Str, List[Str]],
                        related :Map[Str, List]):
            doc.module(name)

            def done := [].diverge()  # would rather flatMap, but oh well...

            def walkNames(names):
                for name in (names):
                    trace("documenting: ", name)
                    def &&obj := scope[`&&$name`]
                    done.push(`&&$name`)
                    if (obj == scope):
                        continue
                    walker.explainObject(name, obj)
                    if (related =~ [(name) => others] | _):
                        for obj in (others):
                            walker.explainObject(`$obj`, obj)

            for section => names in (sections):
                doc.heading(2, section)
                walkNames(names)

            if (scope.getKeys().asSet() - done.asSet() =~ missed : Not[Empty]):
                doc.heading(2, "Oops! Not in any section")
                walkNames([for `&&@name` in (missed) name])

        to explainObject(name :Str, obj):
            def docOf(x) :Str:
                def d := try { x.getDocstring() } catch _ { "*cannot get docstring*" }
                return switch (d):
                    match ==null:
                        "*no docstring*"
                    match txt:
                        txt

            def novelDoc(iface):
                return switch (`$iface`):
                    match =="<computed interface>":
                        ""
                    match label:
                        " :" + label

            def iface := obj._getAllegedInterface()
            # TODO: novelDoc(iface)
            doc.data(name, docOf(iface))

            def methods := try { iface.getMethods() } catch _ { return; }
            for verb => meth in ([for m in (methods)
                                  m.getVerb() => m].sortKeys()):
                def arity := meth.getArity()

                doc.method_(`$verb/$arity`, docOf(meth))
            doc.endList()


def safeScopeBySection :DeepFrozen := [
    "Primitive values" => ["true", "false", "null", "NaN", "Infinity"],
    "Data Constructors" => ["_makeInt", "_makeDouble",
                            "_makeString", "_makeBytes",
                            "_makeList", "_makeMap",
                            "_makeOrderedSpace", "_makeTopSet", "_makeOrderedRegion",
                            "_makeSourceSpan",
                            "_makeFinalSlot", "_makeVarSlot", "makeLazySlot"],
    "Basic guards" => ["Any", "Void", "Empty",
                       "Bool", "Str", "Char", "Double", "Int", "Bytes",
                       "List", "Map", "Set", "Pair"],
    "Guard utilities" => ["NullOk", "Same", "SubrangeGuard", "_auditedBy"],
    "Tracing" => ["trace", "traceln"],
    "Brands" => ["makeBrandPair"],
    "Quasiparsers" => ["simple__quasiParser", "b__quasiParser", "m__quasiParser"],
    "Flow control" => ["M", "throw", "_loop", "_iterForever"],
    "Evaluation" => ["eval", "typhonEval", "safeScope"],
    "Reference/object operations" => ["Ref", "promiseAllFulfilled",
                                      "DeepFrozen", "Selfless", "Transparent", "Near",
                                      "Binding"],
    "Abstract Syntax" => ["astBuilder"],
    "Utilities for syntax expansions" => ["_accumulateList", "_accumulateMap",
                                          "_bind",
                                          "_booleanFlow", "_comparer", "_equalizer",
                                          "_makeVerbFacet",
                                          "_mapEmpty", "_mapExtract",
                                          "_matchSame", "_quasiMatcher",
                                          "_slotToBinding",
                                          "_splitList", "_suchThat",
                                          "_switchFailed",
                                          "_validateFor"],
    "Interface constructors" => ["_makeMessageDesc", "_makeParamDesc", "_makeProtocolDesc"]
]

def related :DeepFrozen := [
    # "Int" => [1]
].asMap()

def unsafeScopeBySection :DeepFrozen := [
    "Time" => ["Timer"],
    "I/O" => [
        "makeStdErr",
        "makeStdIn",
        "makeStdOut",
        "makeFileResource"],
    "Networking" => [
        "makeTCP4ClientEndpoint",
        "makeTCP4ServerEndpoint",
        "getAddrInfo"],
    "Runtime" => [
        "currentRuntime",
        "unsealException"],
    "Processes and Vats" => [
        "currentProcess",
        "currentVat",
        "makeProcess"]
]

def doSafeScope(rst, d) as DeepFrozen:
    rst.heading(1, "safeScope")

    rst.paras("Bindings in the safe scope are available to modules by
    default. They are all `DeepFrozen`.")

    rst.todo("Fix the `module.name` notation
    resulting from abuse of sphinx python support.")

    d.explainScope("safeScope", safeScope, safeScopeBySection, related)

def doEntryCaps(rst, d, caps) as DeepFrozen:
    rst.heading(1, "Entrypoint Arguments")

    rst.todo("Fix the `module.name` notation
    resulting from abuse of sphinx python support.")

    d.explainScope("__entrypoint_io__", caps, unsafeScopeBySection,
                   [].asMap())
    

def main(argv,
         =>Timer,
         =>currentProcess,
         =>currentRuntime,
         =>currentVat,
         =>getAddrInfo,
         =>makeFileResource,
         =>makeProcess,
         =>makeStdErr,
         =>makeStdIn,
         =>makeStdOut,
         =>makeTCP4ClientEndpoint,
         =>makeTCP4ServerEndpoint,
         =>unsealException) as DeepFrozen:
    def stdout := makePumpTube(makeUTF8EncodePump())
    stdout<-flowTo(makeStdOut())

    def rst := makeFormatter(stdout)
    def d := makeDocstringWalker(rst)

    doSafeScope(rst, d)

    def io := [
        =>&&Timer,
        =>&&currentProcess,
        =>&&currentRuntime,
        =>&&currentVat,
        =>&&getAddrInfo,
        =>&&makeFileResource,
        =>&&makeProcess,
        =>&&makeStdErr,
        =>&&makeStdIn,
        =>&&makeStdOut,
        =>&&makeTCP4ClientEndpoint,
        =>&&makeTCP4ServerEndpoint,
        =>&&unsealException]

    doEntryCaps(rst, d, io)
