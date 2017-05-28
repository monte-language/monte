import "lib/streams" =~ [=> flow :DeepFrozen]
exports (main)

def main(_, => makeTCP4ServerEndpoint) :Vow[Int] as DeepFrozen:
    def endpoint := makeTCP4ServerEndpoint(7)
    endpoint.listenStream(flow)
    return when (Ref.promise()[0]) -> { 0 }
