def enumerate := import("hands.enumerate")

def _findRules(instructions):
    def map := [].asMap().diverge()
    for [index, instruction] in enumerate(instructions):
        if (instruction =~ [=='U', label]):
            map[label] := index
    return map.snapshot()

def makeCAMP(instructions):
    # Create a machine for parsers.
    # The machine understands the following codes:
    # * A: match Anything
    # * X item: match eXactly item
    # * J offset: Jump to offset
    # * H offset: save cHoice point
    # * L rule: caLl rule
    # * U name: enter rUle
    # * R: Return from rule
    # * M offset: coMmit choice point
    # * F: Fail
    # * E: End

    var input := null
    var failing :boolean := false
    var position := 0
    var pc := 0
    var end := null
    def stack := [].diverge()

    def rules := _findRules(instructions)

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
                match [=='L', rule]:
                    stack.push([pc + 1])
                    pc := rules[rule]
                match [=='U', _]:
                    # XXX push rule name onto rule trail
                    pc += 1
                match =='R':
                    if (stack.size() > 0):
                        switch (stack.pop()):
                            match [newCounter]:
                                pc := newCounter
                            match [newCounter, _, _]:
                                pc := newCounter
                    else:
                        throw(`Return to empty stack at PC $pc`)
                match [=='M', offset]:
                    pc += offset
                    stack.pop()
                match =='F':
                    pc += 1
                    failing := true
                match =='E':
                    # We have succeeded unconditionally!
                    pc := instructions.size()
                    failing := false
                match _:
                    traceln(`Stumped: $instruction`)

        to run(data) :boolean:
            input := data
            position := 0
            pc := 0
            failing := false
            end := input.size()

            while (pc < instructions.size()):
                if (failing):
                    if (!machine.backtrack()):
                        return false
                else:
                    machine.process(instructions[pc])
            return !failing & position == data.size()

def testAnything(assert):
    def anythingSuccess():
        assert.equal(makeCAMP(['A'])("x"), true)
    def anythingFailure():
        assert.equal(makeCAMP(['A'])(""), false)
    return [
        anythingSuccess,
        anythingFailure,
    ]

def testExactly(assert):
    def singleChar():
        assert.equal(makeCAMP([['X', 'x']])("x"), true)
    def wrongChar():
        assert.equal(makeCAMP([['X', 'x']])("y"), false)
    def multipleChars():
        def insts := [
            ['X', 'x'],
            ['X', 'y'],
            ['X', 'z'],
        ]
        assert.equal(makeCAMP(insts)("xyz"), true)
    def trailing():
        assert.equal(makeCAMP([['X', 'x']])("xy"), false)
    def shortEmptyString():
        assert.equal(makeCAMP([['X', 'x']])(""), false)
    def short():
        def insts := [
            ['X', 'x'],
            ['X', 'y'],
        ]
        assert.equal(makeCAMP(insts)("x"), false)
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
        assert.equal(makeCAMP(insts)("x"), true)
        assert.equal(makeCAMP(insts)("y"), true)
        assert.equal(makeCAMP(insts)("z"), false)
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
        assert.equal(makeCAMP(insts)("x"), true)
        assert.equal(makeCAMP(insts)("y"), true)
        assert.equal(makeCAMP(insts)("z"), true)
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
        assert.equal(makeCAMP(insts)("x"), true)
        assert.equal(makeCAMP(insts)("y"), true)
        assert.equal(makeCAMP(insts)("z"), true)
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
        assert.equal(makeCAMP(insts)(""), true)
        assert.equal(makeCAMP(insts)("x"), false)
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
