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
    var position :int := 0

    # Current position in the code.
    var pc :int := 0

    # The last captured value.
    var lastCapture := null

    # The stack of reduction bindings. This stack gets saved and restored
    # during backtracking.
    var bindingStack :List[Map] := []

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
                    match [p, i, b]:
                        pc := p
                        position := i
                        bindingStack := b
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
                    stack.push([pc + offset, position, bindingStack])
                    pc += 1
                match [=="call", rule]:
                    stack.push([pc + 1])
                    pc := rules[rule]
                match =="push":
                    bindingStack with= [].asMap()
                    pc += 1
                match =="pop":
                    bindingStack := bindingStack.slice(0, bindingStack.size() - 1)
                    pc += 1
                match [=="rule", _]:
                    # XXX push rule name onto rule trail
                    pc += 1
                match [=="res", value]:
                    lastCapture := value
                    pc += 1
                match [=="bind", name]:
                    # Bind the last result to the given name.
                    var m := bindingStack.last()
                    # If the name's already been bound, bind it to the newer
                    # value.
                    m := [name => lastCapture] | m
                    bindingStack := bindingStack.slice(0, bindingStack.size() - 1).with(m)
                    pc += 1
                match [=="red", f]:
                    # Reduction. Apply the function to the bindings, producing
                    # a result.
                    lastCapture := f(bindingStack.last())
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

        to run(data):
            input := data
            position := 0
            pc := 0
            failing := false

            while (pc < instructions.size()):
                if (failing):
                    if (!machine.backtrack()):
                        return [false, null]
                else:
                    machine.process(instructions[pc])
            def succeeded := !failing & position == data.size()
            if (succeeded):
                return [true, lastCapture]
            else:
                # XXX This should probably return the rule trail?
                return [false, null]

def testAnything(assert):
    def anythingSuccess():
        assert.equal(makeCAMP(["any"])("x"), [true, 'x'])
    def anythingFailure():
        assert.equal(makeCAMP(["any"])(""), [false, null])
    return [
        anythingSuccess,
        anythingFailure,
    ]

def testExactly(assert):
    def singleChar():
        assert.equal(makeCAMP([["ex", 'x']])("x"), [true, 'x'])
    def wrongChar():
        assert.equal(makeCAMP([["ex", 'x']])("y"), [false, null])
    def multipleChars():
        def insts := [
            ["ex", 'x'],
            ["ex", 'y'],
            ["ex", 'z'],
        ]
        assert.equal(makeCAMP(insts)("xyz"), [true, 'z'])
    def trailing():
        assert.equal(makeCAMP([["ex", 'x']])("xy"), [false, null])
    def shortEmptyString():
        assert.equal(makeCAMP([["ex", 'x']])(""), [false, null])
    def short():
        def insts := [
            ["ex", 'x'],
            ["ex", 'y'],
        ]
        assert.equal(makeCAMP(insts)("x"), [false, null])
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
        assert.equal(makeCAMP(insts)("x"), [true, 'x'])
        assert.equal(makeCAMP(insts)("y"), [true, 'y'])
        assert.equal(makeCAMP(insts)("z"), [false, null])
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
        assert.equal(makeCAMP(insts)("x"), [true, 'x'])
        assert.equal(makeCAMP(insts)("y"), [true, 'y'])
        assert.equal(makeCAMP(insts)("z"), [true, 'z'])
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
        assert.equal(makeCAMP(insts)("x"), [true, 'x'])
        assert.equal(makeCAMP(insts)("y"), [true, 'y'])
        assert.equal(makeCAMP(insts)("z"), [true, 'z'])
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
        assert.equal(makeCAMP(insts)(""), [true, null])
        assert.equal(makeCAMP(insts)("x"), [false, null])
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
