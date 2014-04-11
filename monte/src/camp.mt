object failure:
    pass

def makeCAMP(instructions, input):
    var failing :boolean := false
    var position := 0
    var pc := 0
    def end := input.size()
    def stack := [].diverge()

    return object machine:

        to _checkEnd() :boolean:
            if (position >= end):
                failing := true
                return false
            return true

        to backtrack() :boolean:
            if (stack.size() > 0):
                switch (stack.pop()):
                    match [p, i, c]:
                        pc := p
                        position := i
                        failing := false
                    match _:
                        return true
            else:
                return false

        to process(instruction) :void:
            switch (instruction):
                match =='A':
                    if (machine._checkEnd()):
                        position += 1
                match [=='X', obj]:
                    if (machine._checkEnd()):
                        if (input[position] == obj):
                            position += 1
                        else:
                            failing := true
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
                    failing := true
                match _:
                    traceln(`Stumped: $instruction`)

        to run() :boolean:
            for instruction in instructions:
                if (failing):
                    if (!machine.backtrack()):
                        return false
                machine.process(instruction)
            return !failing

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
