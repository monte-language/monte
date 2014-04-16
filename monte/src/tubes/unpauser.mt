def makeUnpauser(thunk) :any:
    var called :boolean := false
    return object pause:
        to unpause():
            if (!called):
                called := true
                thunk()
