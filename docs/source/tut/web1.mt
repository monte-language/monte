# Import a name from the "lib/http/server" module.
import "lib/http/server" =~ [=> makeHTTPEndpoint :DeepFrozen]
# Export the entrypoint.
exports (main)

def helloWeb(request) as DeepFrozen:
    "Build a simple HTML response."

    return [200, ["Content-Type" => "text/html"], b`<p>Hello!</p>`]

def main(argv, => makeTCP4ServerEndpoint) :Int as DeepFrozen:
    "Obtain a port and create an HTTP server on that port."

    # m`argv.last()` is the final command-line argument. The _makeInt()
    # function converts strings into integers.
    def portNum :Int := _makeInt(argv.last())
    def ep := makeHTTPEndpoint(makeTCP4ServerEndpoint(portNum))
    traceln(`serving on port $portNum`)
    ep.listen(helloWeb)
    return 0
