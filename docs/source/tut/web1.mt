import "lib/http/server" =~ [=> makeHTTPEndpoint :DeepFrozen]
exports (main)


def helloWeb(request) as DeepFrozen:
    "Build an HTML response including details from a request."

    def body := b`<p>Hello!</p>`
    return [200, ["Content-Type" => "text/html"], body]


def main(argv, => makeTCP4ServerEndpoint) as DeepFrozen:
    def portNum := _makeInt(argv.last())
    def ep := makeHTTPEndpoint(makeTCP4ServerEndpoint(portNum))
    traceln(`serving on port $portNum`)
    ep.listen(helloWeb)
