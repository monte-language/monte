object failure:
    pass

object success:
    pass

def makeCAMP(instructions, input):
    var failing :boolean := false
    var position := 0
    var pc := 0
    def end := input.size()
    def stack := [].diverge()

    return object machine:

        to backtrack() :boolean:
            if (stack.size() > 0):
                switch (stack.pop()):
                    match [p, i, c]:
                        pc := p
                        position := i
                        failing := false
                    match _:
                        pass
                return true
            else:
                return false

        to process(instruction) :void:
            switch (instruction):
                match =='A':
                    if (position >= input.size()):
                        failing := true
                    position += 1
                    pc += 1
                match [=='X', obj]:
                    if (position < input.size() && input[position] == obj):
                        position += 1
                    else:
                        failing := true
                    pc += 1
                match [=='J', offset]:
                    pc += offset
                match [=='H', offset]:
                    stack.push([pc + offset, position, null])
                    pc += 1
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
                    pc += 1
                    failing := true
                match _:
                    traceln(`Stumped: $instruction`)

        to run() :boolean:
            while (pc < instructions.size()):
                if (failing):
                    if (!machine.backtrack()):
                        return false
                else:
                    machine.process(instructions[pc])
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

def testOrderedChoice(assert):
    def XY():
        # 'x' | 'y'
        def insts := [
            ['H', 3],
            ['X', 'x'],
            ['M', 2],
            ['X', 'y'],
        ]
        assert.equal(makeCAMP(insts, "x").run(), true)
        assert.equal(makeCAMP(insts, "y").run(), true)
        assert.equal(makeCAMP(insts, "z").run(), false)
    def LeftXYZ():
        # ('x' | 'y') | 'z'
        def insts := [
            ['H', 6],
            ['H', 3],
            ['X', 'x'],
            ['M', 2],
            ['X', 'y'],
            ['M', 2],
            ['X', 'z'],
        ]
        assert.equal(makeCAMP(insts, "x").run(), true)
        assert.equal(makeCAMP(insts, "y").run(), true)
        assert.equal(makeCAMP(insts, "z").run(), true)
    def RightXYZ():
        # 'x' | ('y' | 'z')
        def insts := [
            ['H', 3],
            ['X', 'x'],
            ['M', 5],
            ['H', 3],
            ['X', 'y'],
            ['M', 2],
            ['X', 'z'],
        ]
        assert.equal(makeCAMP(insts, "x").run(), true)
        assert.equal(makeCAMP(insts, "y").run(), true)
        assert.equal(makeCAMP(insts, "z").run(), true)
    return [
        XY,
        LeftXYZ,
        RightXYZ,
    ]

def testNot(assert):
    def EOF():
        # eof => ~anything
        def insts := [
            ['H', 4],
            'A',
            ['M', 1],
            'F',
        ]
        assert.equal(makeCAMP(insts, "").run(), true)
        assert.equal(makeCAMP(insts, "x").run(), false)
    return [
        EOF,
    ]


def unittest := import("unittest")
unittest([
    testAnything,
    testExactly,
    testOrderedChoice,
    testNot,
])

makeCAMP
