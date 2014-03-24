def [readHole, pattern, value] := import("terml.readHole")

object uint8:
    to pack(data):
        return [data & 0xff]
    to unpack(bytes):
        return bytes[0]
    to size():
        return 1

object ubint16:
    to pack(data):
        return [data >> 8 & 0xff, data & 0xff]
    to unpack(bytes):
        return bytes[0] << 8 | bytes[1]
    to size():
        return 2

def makeStruct(layout):
    return object struct:
        to substitute(values):
            traceln(`Values $values, layout $layout`)
            def m := layout.diverge()
            for k => v in layout:
                if (readHole(v) =~ [==value, index]):
                    m[k] := values[index]
            traceln(`Substituted $values to get $m`)
            return makeStruct(m.snapshot())
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
        to size():
            var i := 0
            for v in layout:
                i += v.size()
            return i

object struct__quasiParser:
    to valueMaker(template):
        def members := template.split(" ")
        def layout := [].asMap().diverge()
        for member in members:
            def [k, v] := member.split(":")
            layout[k] := v            
        return makeStruct(layout)

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
