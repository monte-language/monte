def [readHole, pattern, value] := import("terml.readHole")

interface Struct:
    pass

object uint8 implements Struct:
    to pack(data :int):
        return [data & 0xff]
    to unpack(bytes) :int:
        return bytes[0]
    to size() :int:
        return 1

def testUint8(assert):
    def pack():
        assert.equal(uint8.pack(42), [42])
    def unpack():
        assert.equal(uint8.unpack([42]), 42)
    return [
        pack,
        unpack,
    ]

object ubint16 implements Struct:
    to pack(data :int):
        return [data >> 8 & 0xff, data & 0xff]
    to unpack(bytes) :int:
        return bytes[0] << 8 | bytes[1]
    to size() :int:
        return 2

def testUbint16(assert):
    def pack():
        assert.equal(ubint16.pack(42), [0, 42])
    def unpack():
        assert.equal(ubint16.unpack([0, 42]), 42)
    return [
        pack,
        unpack,
    ]

object ubint32 implements Struct:
    to pack(data :int):
        return [
            data >> 24 & 0xff,
            data >> 16 & 0xff,
            data >> 8 & 0xff,
            data & 0xff,
        ]
    to unpack(bytes) :int:
        return bytes[0] << 24 |
        bytes[1] << 16 |
        bytes[2] << 8 |
        bytes[3]
    to size() :int:
        return 4

def testUbint32(assert):
    def pack():
        assert.equal(ubint32.pack(0xdeadbeef), [0xde, 0xad, 0xbe, 0xef])
    def unpack():
        assert.equal(ubint32.unpack([0xde, 0xad, 0xbe, 0xef]), 0xdeadbeef)
    return [
        pack,
        unpack,
    ]

object ubint64 implements Struct:
    to pack(data :int):
        return [
            data >> 56 & 0xff,
            data >> 48 & 0xff,
            data >> 40 & 0xff,
            data >> 32 & 0xff,
            data >> 24 & 0xff,
            data >> 16 & 0xff,
            data >> 8 & 0xff,
            data & 0xff,
        ]
    to unpack(bytes) :int:
        return bytes[0] << 56 |
        bytes[1] << 48 |
        bytes[2] << 40 |
        bytes[3] << 32 |
        bytes[4] << 24 |
        bytes[5] << 16 |
        bytes[6] << 8 |
        bytes[7]
    to size() :int:
        return 8

def makeStruct(layout) :Struct:
    return object struct implements Struct:
        to substitute(values):
            traceln(`Values $values, layout $layout`)
            def m := layout.diverge()
            for k => v in layout:
                if (readHole(v) =~ [==value, index]):
                    m[k] := values[index]
            traceln(`Substituted $values to get $m`)
            return makeStruct(m.snapshot())
        to matchBind(values, bytes, ej):
            var m := [].asMap()
            var offset := 0
            var target := null
            for k => var reader in layout:
                if (readHole(reader) =~ [==value, index]):
                    reader := values[index]
                if (readHole(k) =~ [==pattern, target]):
                    def slice := bytes.slice(offset, offset + reader.size())
                    m |= [target => reader.unpack(slice)]
                offset += reader.size()
            return m.sortKeys()
        to pack(data):
            var l := []
            for key => packer in layout:
                def datum := data[key]
                l += packer.pack(datum)
            return l
        to unpack(bytes):
            var m := [].asMap()
            var offset := 0
            for key => reader in layout:
                def slice := bytes.slice(offset, offset + reader.size())
                m |= [key => reader.unpack(slice)]
                offset += reader.size()
            return m
        to size() :int:
            var i := 0
            for v in layout:
                i += v.size()
            return i

object struct__quasiParser:
    to valueMaker(template) :Struct:
        def members := template.split(" ")
        def layout := [].asMap().diverge()
        for member in members:
            def [k, v] := member.split(":")
            layout[k] := v            
        return makeStruct(layout)
    to matchMaker(template) :Struct:
        return struct__quasiParser.valueMaker(template)

var s := makeStruct(["x" => uint8, "y" => ubint16])
var data := ["x" => 42, "y" => 1000]
var bytes := [24, 87, 255]
traceln(`${s.pack(data)}`)
traceln(`${s.unpack(bytes)}`)

s := struct`x:$uint8 y:$ubint16`
traceln(`${s.pack(data)}`)
traceln(`${s.unpack(bytes)}`)

var p := struct`x:$s y:$ubint16`
data := ["x" => data, "y" => 42]
bytes += [255, 255]
traceln(`${p.pack(data)}`)
traceln(`${p.unpack(bytes)}`)

if ([42, 255, 0] =~ struct`@r:$uint8 @q:$ubint16`):
    traceln(`r $r q $q`)

def unittest := import("unittest")

unittest([
    testUint8,
    testUbint16,
    testUbint32,
])

[
    "struct" => struct__quasiParser,
    "uint8" => uint8,
    "ubint16" => ubint16,
    "ubint32" => ubint32,
    "ubint64" => ubint64,
]
