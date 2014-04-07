def oneOrMore(p):
    return p + p.repeated()

def justFirst(x, y):
    return (x + y) % def first([x, _]) { return x }

def justSecond(x, y):
    return (x + y) % def second([_, x]) { return x }

def bracket(bra, x, ket):
    return justSecond(bra, justFirst(x, ket))

[
    "oneOrMore" => oneOrMore,
    "justFirst" => justFirst,
    "justSecond" => justSecond,
    "bracket" => bracket,
]
