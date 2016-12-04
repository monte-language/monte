import "lib/http/server" =~ [=> makeHTTPEndpoint :DeepFrozen]
import "lib/http/tag" =~ [=> tag :DeepFrozen]
import "formData" =~ [=> fieldMap :DeepFrozen]
exports (main)

object calculator as DeepFrozen:
    to run(request):
        return switch (request.getVerb()):
            match =="GET":
                calculator.get(request)
            match =="POST":
                calculator.post(request)

    to get(request):
        def body := b`
        <form method="POST">
          <label>Arbitrary code to execute:<input name="code" /></label>
        </form>
        `
        return [200, ["Content-Type" => "text/html"], body]

    to post(request):
        def code := fieldMap(request.getBody())["code"]
        def result := eval(code, safeScope)
        # NB: The `tag` object does automatic HTML escaping. No extra effort
        # is required to prevent XSS. ~ C.
        def html := tag.pre(M.toString(result))
        return [200, ["Content-Type" => "text/plain"], b`$html`]

def main(argv, => makeTCP4ServerEndpoint) :Int as DeepFrozen:
    def portNum := _makeInt(argv.last())
    def ep := makeHTTPEndpoint(makeTCP4ServerEndpoint(portNum))
    traceln(`serving $calculator on port $portNum`)
    ep.listen(calculator)
    return 0
