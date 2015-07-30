def [=> smallBody] | _ := import("lib/http/resource")
def [=> tag] | _ := import("lib/http/tag")


def helloWeb(request):
    "Build an HTML response including details from a request."
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


def start(makeServer):
    makeServer().listen(helloWeb)


[=> start]
