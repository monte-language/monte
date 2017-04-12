import "http/server" =~ [=> makeHTTPEndpoint :DeepFrozen]
exports (main)

def helloWeb(request) as DeepFrozen:
    "Build a simple HTML response."

    return [200, ["Content-Type" => "text/html"], b`<p>Hello!</p>`]

def main(argv, => makeTCP4ServerEndpoint) :Int as DeepFrozen:
    "Obtain a port and create an HTTP server on that port."

    def portNum :Int := _makeInt(argv.last())
    def ep := makeHTTPEndpoint(makeTCP4ServerEndpoint(portNum))
    traceln(`serving on port $portNum`)
    ep.listen(helloWeb)
    return 0
