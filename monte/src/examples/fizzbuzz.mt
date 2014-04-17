def __makeOrderedSpace := import("regions")

def fizzBuzz(top):
    for t in 0..top:
        if ((t % 3 == 0) || (t % 5 == 0)):
            if (t % 15 == 0):
                traceln(`$t  FizzBuzz`)
            else if (t % 3 == 0):
                traceln(`$t  Fizz`)
            else:
                traceln(`$t  Buzz`)

fizzBuzz(42)
