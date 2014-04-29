import struct
from StringIO import StringIO
from encodings.utf_8 import IncrementalDecoder

from terml.nodes import Tag, Term

def asciiShift(bs):
    return ''.join(chr((ord(b) + 32) % 256) for b in bs)

def asciiUnshift(bs):
    return ''.join(chr((ord(b) - 32) % 256) for b in bs)

LONG_SHIFT = 15
LONG_BASE = 1 << LONG_SHIFT
LONG_MASK = LONG_BASE - 1

kernelNodeInfo = [
    ('null', 0),
    ('.String.', None),
    ('.float64.', None),
    ('.char.', None),
    # different tags for short ints...
    ('.int.', None),
    # ... and long ints
    ('.int.', None),
    # this one for small tuples...
    ('.tuple.', None),
    # ... this one for large
    ('.tuple.', None),
    ('LiteralExpr', 1),
    ('NounExpr', 1),
    ('BindingExpr', 1),
    ('SeqExpr', 1),
    ('MethodCallExpr', 3),
    ('Def', 3),
    ('Escape', 3),
    ('Catch', 2),
    ('Object', 4),
    ('Script', 3),
    ('Method', 5),
    ('Matcher', 2),
    ('Assign', 2),
    ('Finally', 2),
    ('KernelTry', 2),
    ('HideExpr', 1),
    ('If', 3),
    ('Meta', 1),
    ('FinalPattern', 2),
    ('IgnorePattern', 1),
    ('VarPattern', 2),
    ('ListPattern', 2),
    ('ViaPattern', 2),
    ('BindingPattern', 1),
    ('Character', 1)
]

SHORT_INT, LONG_INT  = (4, 5) # indices of the two '.int.'s above
BIG_TUPLE, SMALL_TUPLE  = (6, 7) # indices of the two '.int.'s above

nodeLookup = dict((v[0], k) for k, v in enumerate(kernelNodeInfo))
arities = dict(kernelNodeInfo)
tags = dict((i, Tag(k)) for (i, (k, a)) in enumerate(kernelNodeInfo))


def load(data):
    dataStack = []
    opStack = []
    i = loadTerm(data, 0, dataStack, opStack)
    while opStack:
        i = opStack.pop()(data, i, dataStack, opStack)
    assert i == len(data)
    assert len(dataStack) == 1, repr(dataStack)
    return dataStack[0]


def createTerm(tag, arity):
    def finish(data, i, dataStack, opStack):
        if arity == 0:
            args = ()
        else:
            args = dataStack[-arity:]
            del dataStack[-arity:]
        dataStack.append(Term(tag, None, args, None))
        return i
    return finish


def loadTerm(data, i, dataStack, opStack):
    kind = ord(asciiUnshift(data[i]))
    tag = tags[kind]
    i += 1
    arity = arities[tag.name]
    literalVal = None
    if tag.name == '.int.':
        if kind == SHORT_INT:
            literalVal = readInt32(data, i)
            i += 4
        else:
            literalVal = 0
            siz = readInt32(data, i)
            i += 4
            chunks = []
            for j in range(siz):
                chunk = struct.unpack('!h', asciiUnshift(data[i:i + 2]))[0]
                chunks.append(chunk)
                i += 2
                literalVal |= (chunk << LONG_SHIFT * j)
    elif tag.name == '.String.':
        siz = readInt32(data, i)
        i += 4
        literalVal = data[i:i + siz].decode('utf-8')
        i += siz
    elif tag.name == '.float64.':
        literalVal = struct.unpack('!d', asciiUnshift(data[i:i + 8]))[0]
        i += 8
    elif tag.name == '.char.':
        de = IncrementalDecoder()
        literalVal = de.decode(data[i])
        i += 1
        while literalVal == u'':
            literalVal = de.decode(data[i])
            i += 1
    elif tag.name == '.tuple.':
        if kind == BIG_TUPLE:
            arity = readInt32(data, i)
            i += 4
        else:
            arity = ord(asciiUnshift(data[i]))
            i += 1
    if arity is None:
        dataStack.append(Term(tag, literalVal, (), None))
    else:
        opStack.append(createTerm(tag, arity))
        opStack.extend([loadTerm] * arity)
    return i


def readInt32(data, i):
    return struct.unpack('!i', asciiUnshift(data[i:i + 4]))[0]


def dump(ast):
    out = StringIO()
    dumpTerm(ast, out)
    return out.getvalue()


def dumpTerm(term, out):
    o = term.data
    name = term.tag.name
    if name == '.int.':
        if abs(o) < 2**31:
            out.write(asciiShift(chr(SHORT_INT)))
            writeInt32(o, out)
        else:
            out.write(asciiShift(chr(LONG_INT)))
            chunks = []
            done = False
            while True:
                if abs(o) > LONG_BASE:
                    c = o & LONG_MASK
                else:
                    c = o
                chunks.append(struct.pack('!h', c))
                o >>= LONG_SHIFT
                if o == 0:
                    break
                if o == -1:
                    if done:
                        break
                    done = True
            writeInt32(len(chunks), out)
            out.write(asciiShift(''.join(chunks)))
        return
    elif name == '.tuple.':
        if len(term.args) > 255:
            out.write(asciiShift(chr(BIG_TUPLE)))
            out.write(asciiShift(struct.pack('!i', len(t.args))))
        else:
            out.write(asciiShift(chr(SMALL_TUPLE)))
            out.write(asciiShift(chr(len(term.args))))
        for t in term.args:
            dumpTerm(t, out)
        return
    out.write(asciiShift(chr(nodeLookup[name])))
    if name == '.String.':
        bs = o.encode('utf-8')
        writeInt32(len(bs), out)
        out.write(bs)
    elif name == '.float64.':
        out.write(asciiShift(struct.pack('!d', o)))
    elif name == '.char.':
        out.write(o.encode('utf-8'))
    else:
        for t in term.args:
            dumpTerm(t, out)


def writeInt32(i, out):
    out.write(asciiShift(struct.pack('!i', i)))
