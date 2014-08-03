import struct
from StringIO import StringIO
from encodings.utf_8 import IncrementalDecoder

from terml.nodes import Tag, Term

shiftTable = ''.join(chr((x + 32) % 256) for x in range(256))
unshiftTable = ''.join(chr((x - 32) % 256) for x in range(256))


def asciiShift(bs):
    return bs.translate(shiftTable)


def asciiUnshift(bs):
    return bs.translate(unshiftTable)

kernelNodeInfo = [
    ('null', 0),
    ('true', 0),
    ('false', 0),
    ('.String.', None),
    ('.float64.', None),
    ('.char.', None),
    ('.int.', None),
    ('.tuple.', None),
    ('.bag.', None),
    ('.attr.', 2),
    ('LiteralExpr', 1),
    ('NounExpr', 1),
    ('BindingExpr', 1),
    ('SeqExpr', 1),
    ('MethodCallExpr', 3),
    ('Def', 3),
    ('Escape', 4),
    ('Object', 4),
    ('Script', 3),
    ('Method', 5),
    ('Matcher', 2),
    ('Assign', 2),
    ('Finally', 2),
    ('KernelTry', 3),
    ('HideExpr', 1),
    ('If', 3),
    ('Meta', 1),
    ('FinalPattern', 2),
    ('IgnorePattern', 1),
    ('VarPattern', 2),
    ('ListPattern', 2),
    ('ViaPattern', 2),
    ('BindingPattern', 1),
    ('Character', 1),
    ('Module', 3)
]

nodeLookup = dict((v[0], k) for k, v in enumerate(kernelNodeInfo))
arities = dict(kernelNodeInfo)
tags = dict((i, Tag(k)) for (i, (k, a)) in enumerate(kernelNodeInfo))

def zze(val):
  if val < 0:
    return ((val * 2) ^ -1) | 1
  else:
    return val * 2


def zzd(val):
    if val & 1:
        return (val / 2) ^ -1
    return val / 2


def dumpVarint(value):
    if value == 0:
        target = "\x00"
    else:
        target = []
    while value > 0:
        chunk = value & 0x7f
        value >>= 7
        if value > 0:
            target.append(chr(chunk | 0x80))
        else:
            target.append(chr(chunk))
    return asciiShift(''.join(target))


def loadVarint(data, i):
    val = 0
    pos = 0
    while i < len(data):
        byte = (ord(data[i]) - 32) % 256
        val |= (byte & 0x7f) << pos
        pos += 7
        i += 1
        if not (byte & 0x80):
            return val, i
    raise ValueError("Input truncated")


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
        val, i = loadVarint(data, i)
        literalVal = zzd(val)
    elif tag.name == '.String.':
        siz, i = loadVarint(data, i)
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
            arity, i = loadVarint(data, i)
    if arity is None:
        dataStack.append(Term(tag, literalVal, (), None))
    else:
        opStack.append(createTerm(tag, arity))
        opStack.extend([loadTerm] * arity)
    return i


def dump(ast):
    out = StringIO()
    dumpTerm(ast, out)
    return out.getvalue()


def dumpTerm(term, out):
    o = term.data
    name = term.tag.name
    out.write(asciiShift(chr(nodeLookup[name])))
    if name == '.int.':
        out.write(dumpVarint(zze(o)))
    elif name == '.tuple.':
        out.write(dumpVarint(len(term.args)))
        for t in term.args:
            dumpTerm(t, out)
    elif name == '.String.':
        bs = o.encode('utf-8')
        out.write(dumpVarint(len(bs)))
        out.write(bs)
    elif name == '.float64.':
        out.write(asciiShift(struct.pack('!d', o)))
    elif name == '.char.':
        out.write(o.encode('utf-8'))
    else:
        assert name in arities
        assert len(term.args) == arities[name], "Bad arity of term: %r" % term
        for t in term.args:
            dumpTerm(t, out)
