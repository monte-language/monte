import "lib/http/server" =~ [=> makeHTTPEndpoint :DeepFrozen]
import "lib/http/resource" =~ [=> smallBody :DeepFrozen]
import "lib/http/tag" =~ [=> tag :DeepFrozen]
exports (main)


def helloWeb(request) as DeepFrozen:
    "Build an HTML response including details from a request."

    def body := tag.body(
        tag.h1("Hello!"),
        tag.p("This is a Monte webserver."),

        tag.h2("Request Info"),
        tag.p(request.getVerb()),
        tag.p(request.getPath()),
        tag.p(`${request.getHeaders()}`))
    return smallBody(`$body`)


def main(argv, => makeTCP4ServerEndpoint) as DeepFrozen:
    def portNum := 5050  # _makeInt(argv.last())
    def ep := makeHTTPEndpoint(makeTCP4ServerEndpoint(portNum))
    traceln(portNum)
    ep.listen(helloWeb)
