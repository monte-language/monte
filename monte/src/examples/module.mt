module magicNumber
export (makeFoo, makeBar, Baz)
def makeFoo(title):
    return object Foo:
        to doSomething():
            traceln(`Hi, I'm a Foo called $title. The magic number is $magicNumber`)

def makeBar():
    return object Bar:
        to doSomething():
            traceln("Bar is doing something")

object Baz:
    to doSomething():
        traceln("Beep!")
