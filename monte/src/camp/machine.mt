def enumerate := import("hands.enumerate")

def _findRules(instructions):
    def map := [].asMap().diverge()
    for [index, instruction] in enumerate(instructions):
        if (instruction =~ [=="rule", label]):
            map[label] := index
    return map.snapshot()

def makeCAMP(instructions):
    # Create a machine for parsers.
    # The machine understands the following codes:
    # * any: match Anything
    # * ex item: match eXactly item
    # * jmp offset: Jump to offset
    # * cho offset: save cHoice point
    # * call rule: Call a rule by name
    # * rule name: Declare named rule
    # * ret: Return from rule
    # * com offset: coMmit choice point
    # * fail: Fail
    # * end: End

    # The input stream. Currently should be some sort of finite sequence.
    var input := null

    # Whether the machine is currently in a failing state.
    var failing :boolean := false

    # Current position in the input.
    var position := 0

    # Current position in the code.
    var pc := 0

    # The last captured value.
    var lastCapture := null

    # The call/backtracking stack.
    def stack := [].diverge()

    # Locations of all of the rules, so that we can quickly index to them when
    # performing calls. This will eventually become part of the parser
    # compiler.
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
                match =="any":
                    if (position < input.size()):
                        lastCapture := input[position]
                        position += 1
                    else:
                        failing := true
                    pc += 1
                match [=="ex", obj]:
                    if (position < input.size() && input[position] == obj):
                        lastCapture := input[position]
                        position += 1
                    else:
                        failing := true
                    pc += 1
                match [=="jmp", offset]:
                    pc += offset
                match [=="cho", offset]:
                    stack.push([pc + offset, position, null])
                    pc += 1
                match [=="call", rule]:
                    stack.push([pc + 1])
                    pc := rules[rule]
                match [=="rule", _]:
                    # XXX push rule name onto rule trail
                    pc += 1
                match =="ret":
                    if (stack.size() > 0):
                        switch (stack.pop()):
                            match [newCounter]:
                                pc := newCounter
                            match [newCounter, _, _]:
                                pc := newCounter
                    else:
                        throw(`Return to empty stack at PC $pc`)
                match [=="com", offset]:
                    pc += offset
                    stack.pop()
                match =="fail":
                    pc += 1
                    failing := true
                match =="end":
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

            while (pc < instructions.size()):
                if (failing):
                    if (!machine.backtrack()):
                        return false
                else:
                    machine.process(instructions[pc])
            return !failing & position == data.size()

def testAnything(assert):
    def anythingSuccess():
        assert.equal(makeCAMP(["any"])("x"), true)
    def anythingFailure():
        assert.equal(makeCAMP(["any"])(""), false)
    return [
        anythingSuccess,
        anythingFailure,
    ]

def testExactly(assert):
    def singleChar():
        assert.equal(makeCAMP([["ex", 'x']])("x"), true)
    def wrongChar():
        assert.equal(makeCAMP([["ex", 'x']])("y"), false)
    def multipleChars():
        def insts := [
            ["ex", 'x'],
            ["ex", 'y'],
            ["ex", 'z'],
        ]
        assert.equal(makeCAMP(insts)("xyz"), true)
    def trailing():
        assert.equal(makeCAMP([["ex", 'x']])("xy"), false)
    def shortEmptyString():
        assert.equal(makeCAMP([["ex", 'x']])(""), false)
    def short():
        def insts := [
            ["ex", 'x'],
            ["ex", 'y'],
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
            ["cho", 3],
            ["ex", 'x'],
            ["com", 2],
            ["ex", 'y'],
        ]
        assert.equal(makeCAMP(insts)("x"), true)
        assert.equal(makeCAMP(insts)("y"), true)
        assert.equal(makeCAMP(insts)("z"), false)
    def LeftXYZ():
        # ('x' | 'y') | 'z'
        def insts := [
            ["cho", 6],
            ["cho", 3],
            ["ex", 'x'],
            ["com", 2],
            ["ex", 'y'],
            ["com", 2],
            ["ex", 'z'],
        ]
        assert.equal(makeCAMP(insts)("x"), true)
        assert.equal(makeCAMP(insts)("y"), true)
        assert.equal(makeCAMP(insts)("z"), true)
    def RightXYZ():
        # 'x' | ('y' | 'z')
        def insts := [
            ["cho", 3],
            ["ex", 'x'],
            ["com", 5],
            ["cho", 3],
            ["ex", 'y'],
            ["com", 2],
            ["ex", 'z'],
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
            ["cho", 4],
            "any",
            ["com", 1],
            "fail",
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
