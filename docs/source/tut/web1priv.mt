def [=> makeHTTPEndpoint] | _ := import("lib/http/server")
def [=> strToInt] | _ := import("lib/atoi")

def [=> start] | _ := import("web1")

def makeWebServer():
    "Make an HTTP server listening on the port given by the last CLI arg."
    def portArg := currentProcess.getArguments().last()
    def via (strToInt) portNum := portArg
    return makeHTTPEndpoint(makeTCP4ServerEndpoint(portNum))

start(makeWebServer)
