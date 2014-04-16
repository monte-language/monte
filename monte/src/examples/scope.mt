def scoop():
    var a := 1
    def foo():
        var b := 2
        traceln(`a is $a and b is $b`)

    # traceln(`I cannot access $b here`)

    return foo

scoop()()
