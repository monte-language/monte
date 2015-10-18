imports
exports (main)


def helloWeb(request) as DeepFrozen:
    "Build an HTML response including details from a request."
    def [=> smallBody] | _ := import.script("lib/http/resource")
    def [=> tag] | _ := import.script("lib/http/tag")

    escape badRequest:
        def [[verb, path], headers] exit badRequest := request
        def body := tag.body(
            tag.h1("Hello!"),
            tag.p("This is a Monte webserver."),

            tag.h2("Request Info"),
            tag.p(verb),
            tag.p(path),
            tag.p(`$headers`))
        return smallBody(`$body`)
    catch _:
        return null


def main(=> makeTCP4ServerEndpoint, => currentProcess) as DeepFrozen:
    # TODO: move to imports list
    def [=> strToInt] | _ := import.script("lib/atoi")
    def [=> makeHTTPEndpoint] | _ := import.script("lib/http/server")

    def via (strToInt) portNum := currentProcess.getArguments().last()
    def ep := makeHTTPEndpoint(makeTCP4ServerEndpoint(portNum))

    ep.listen(helloWeb)
