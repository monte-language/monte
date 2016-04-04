import "lib/http/server" =~ [=> makeHTTPEndpoint :DeepFrozen]
import "formData" =~ [=> fieldMap :DeepFrozen]
exports (main)

object calculator as DeepFrozen:
    to run (request):
        return switch (request.getVerb()):
            match =="GET":
                calculator.get(request)
            match =="POST":
                calculator.post(request)

    to get(request):
        def body := b`
        <form method="POST">
          <label>Arbitraty code to execute:<input name="code" /></label>
        </form>
        `
        return [200, ["Content-Type" => "text/html"], body]

    to post(request):
        def code := fieldMap(request.getBody())["code"]
        def emptyEnvironment := [].asMap()
        def result := eval(code, emptyEnvironment)
        return [200, ["Content-Type" => "text/plain"], b`${`$result`}`]

def main(argv, => makeTCP4ServerEndpoint) as DeepFrozen:
    def portNum := _makeInt(argv.last())
    def ep := makeHTTPEndpoint(makeTCP4ServerEndpoint(portNum))
    traceln(`serving $calculator on port $portNum`)
    ep.listen(calculator)
