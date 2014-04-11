object fail:
    pass

object failure:
    pass

def makeCAMP(instructions, input):
    var position := 0
    var pc := 0
    def end := input.size()
    def stack := [].diverge()

    return object machine:

        to _checkEnd() :boolean:
            if (position >= end):
                pc := fail
                return true
            return false

        to backtrack() :void:
            if (stack.size() > 0):
                switch (stack.pop()):
                    match [p, i, c]:
                        pc := p
                        position := i
                    match _:
                        return
            else:
                throw(failure)

        to advance(instruction) :void:
            switch (instruction):
                match =='A':
                    if (!machine._checkEnd()):
                        position += 1
                match [=='X', obj]:
                    if (!machine._checkEnd()):
                        if (input[position] == obj):
                            position += 1
                        else:
                            pc := fail
                match [=='J', offset]:
                    pc += offset
                match [=='H', offset]:
                    stack.push([pc + offset, position, null])
                match [=='L', offset]:
                    pc += offset
                    stack.push([pc])
                match =='R':
                    switch (stack.pop()):
                        match [newCounter]:
                            pc := newCounter
                        match [newCounter, _, _]:
                            pc := newCounter
                match [=='M', offset]:
                    pc += offset
                    stack.pop()
                match =='F':
                    pc := fail
                match _:
                    traceln(`Stumped: $instruction`)

        to run():
            for instruction in instructions:
                if (pc == fail):
                    try:
                        machine.backtrack()
                    catch failure:
                        return false
                machine.advance(instruction)
            return pc != fail

def testAnything(assert):
    def anythingSuccess():
        assert.equal(makeCAMP(['A'], "x").run(), true)
    def anythingFailure():
        assert.equal(makeCAMP(['A'], "").run(), false)
    return [
        anythingSuccess,
        anythingFailure,
    ]

def testExactly(assert):
    def singleChar():
        assert.equal(makeCAMP([['X', 'x']], "x").run(), true)
    def wrongChar():
        assert.equal(makeCAMP([['X', 'x']], "y").run(), false)
    def multipleChars():
        def insts := [
            ['X', 'x'],
            ['X', 'y'],
            ['X', 'z'],
        ]
        assert.equal(makeCAMP(insts, "xyz").run(), true)
    def trailing():
        assert.equal(makeCAMP([['X', 'x']], "xy").run(), true)
    def shortEmptyString():
        assert.equal(makeCAMP([['X', 'x']], "").run(), false)
    def short():
        def insts := [
            ['X', 'x'],
            ['X', 'y'],
        ]
        assert.equal(makeCAMP(insts, "x").run(), false)
    return [
        singleChar,
        wrongChar,
        multipleChars,
        trailing,
        shortEmptyString,
        short,
    ]

def unittest := import("unittest")
unittest([
    testAnything,
    testExactly,
])
