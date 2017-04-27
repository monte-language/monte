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

    def decl(sort :Str, name :Str, docstring :NullOk[Str]):
        drain.receive(`.. py:$sort:: $name$\n$\n`)
        if (docstring != null):
            drain.receive(dedent(docstring, "indent" => 1) + "\n\n")

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
            decl("module", name, null)

        to data(name :Str, docstring :Str):
            decl("data", name, docstring)

        to class(name :Str, docstring :Str):
            decl("class", name, docstring)

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
    def docOf(x) :Str:
        def d := try { x.getDocstring() } catch _ { "*cannot get docstring*" }
        return switch (d):
            match ==null:
                "*no docstring*"
            match txt:
                txt

    # TODO: novelDoc(iface)
    def novelDoc(iface):
        return switch (`$iface`):
            match =="<computed interface>":
                ""
            match label:
                " :" + label

    def explainMethods(methods):
        for verb => meth in ([for m in (methods)
                              m.getVerb() => m].sortKeys()):
            def arity := meth.getArity()

            doc.method_(`$verb/$arity`, docOf(meth))
        doc.endList()

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
                    escape notInterface:
                        walker.explainInterface(name, obj, notInterface)
                    catch _:
                        walker.explainObject(name, obj, done)
                    if (related =~ [(name) => others] | _):
                        for obj in (others):
                            walker.explainObject(`$obj`, obj)

            for section => names in (sections):
                doc.heading(2, section)
                walkNames(names)

            if (scope.getKeys().asSet() - done.asSet() =~ missed : Not[Empty]):
                doc.heading(2, "Oops! Not in any section")
                walkNames([for `&&@name` in (missed) name])

        to explainInterface(name :Str, iface, ej):
            # XXX _respondsTo isn't reliable even for basic data guards
            def kludge := [List => [], Map => [].asMap(), Bool => true]
            def iface2 := if (kludge =~ [(iface) => ex] | _) { ex._getAllegedInterface()} else { iface }
            def methods := try { iface2.getMethods() } catch _ { ej() }
            doc.class(name, docOf(iface._getAllegedInterface()))
            explainMethods(methods)

        to explainObject(name :Str, obj, seen):
            def iface := obj._getAllegedInterface()
            if (seen.contains(`&&$iface`)):
                doc.data(name, ` :$iface`)
            else:
                doc.data(name, docOf(iface))

                def methods := try { iface.getMethods() } catch _ { return; }
                explainMethods(methods)


def safeScopeBySection :DeepFrozen := [
    "Basic guards" => ["Bool", "Str", "Char", "Double", "Int", "Bytes",
                       "List", "Map", "Set", "Pair",
                       "FinalSlot", "VarSlot"],
    "Guard utilities" => ["Any", "Void", "Empty",
                          "NullOk", "Same", "Vow", "SubrangeGuard", "_auditedBy"],
    "Primitive values" => ["true", "false", "null", "NaN", "Infinity"],
    "Data Constructors" => ["_makeInt", "_makeDouble",
                            "_makeStr", "_makeString", "_makeBytes",
                            "_makeList", "_makeMap",
                            "_makeOrderedSpace", "_makeTopSet", "_makeOrderedRegion",
                            "_makeSourceSpan",
                            "_makeFinalSlot", "_makeVarSlot", "makeLazySlot"],
    "Tracing" => ["trace", "traceln"],
    "Brands" => ["makeBrandPair"],
    "Quasiparsers" => ["``", "b``", "m``", "mpatt``"],
    "Flow control" => ["M", "throw", "_loop", "_iterForever"],
    "Evaluation" => ["eval", "astEval", "safeScope"],
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
        "stdio",
        "makeStdErr",
        "makeStdIn",
        "makeStdOut",
        "makeFileResource"],
    "Networking" => [
        "makeTCP4ClientEndpoint",
        "makeTCP4ServerEndpoint",
        "makeTCP6ClientEndpoint",
        "makeTCP6ServerEndpoint",
        "getAddrInfo"],
    "Runtime" => [
        "currentRuntime",
        "unsealException"],
    "Processes and Vats" => [
        "currentProcess",
        "makeProcess"]
]

def doSafeScope(rst, d) as DeepFrozen:
    rst.heading(1, "safeScope")

    rst.paras("Bindings in the safe scope are available to modules by
    default. They are all `DeepFrozen`.")

    rst.todo("Fix the `module.name` notation
    resulting from abuse of sphinx python support.")

    rst.todo("When ``Bool`` is fixed to reveal its interface,
    re-run mtDocStrings to document and, or, xor, not, butNot, pick, op__cmp.")

    d.explainScope("safeScope", safeScope, safeScopeBySection, related)

def doEntryCaps(rst, d, caps) as DeepFrozen:
    rst.heading(1, "Entrypoint Arguments")

    rst.todo("Fix the `module.name` notation
    resulting from abuse of sphinx python support.")

    d.explainScope("__entrypoint_io__", caps, unsafeScopeBySection,
                   [].asMap())
    

def main(_argv,
         # from typhon/scopes/unsafe.py
         =>Timer,
         # excluded by loader.mt
         #=>bench,
         =>currentProcess,
         =>currentRuntime,
         =>getAddrInfo,
         =>makeFileResource,
         =>makeProcess,
         =>makeStdErr,
         =>makeStdIn,
         =>makeStdOut,
         =>makeTCP4ClientEndpoint,
         =>makeTCP4ServerEndpoint,
         =>makeTCP6ClientEndpoint,
         =>makeTCP6ServerEndpoint,
         =>stdio,
         =>unsealException) as DeepFrozen:
    def stdout := makePumpTube(makeUTF8EncodePump())
    stdout<-flowTo(makeStdOut())

    def rst := makeFormatter(stdout)
    def d := makeDocstringWalker(rst)

    doSafeScope(rst, d)

    def io := [
        =>&&Timer,
        #=>&&bench,
        =>&&currentProcess,
        =>&&currentRuntime,
        =>&&getAddrInfo,
        =>&&makeFileResource,
        =>&&makeProcess,
        =>&&makeStdErr,
        =>&&makeStdIn,
        =>&&makeStdOut,
        =>&&makeTCP4ClientEndpoint,
        =>&&makeTCP4ServerEndpoint,
        =>&&makeTCP6ClientEndpoint,
        =>&&makeTCP6ServerEndpoint,
        =>&&stdio,
        =>&&unsealException]

    doEntryCaps(rst, d, io)
