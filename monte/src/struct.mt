def [readHole, pattern, value] := import("terml.readHole")

object uint8:
    to pack(datum):
        return [datum & 0xff]
    to read(bytes):
        return bytes[0]
    to size():
        return 1

object ubint16:
    to pack(datum):
        return [datum >> 8 & 0xff, datum & 0xff]
    to read(bytes):
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
        to build(data):
            var l := []
            for key => packer in layout:
                def datum := data[key]
                l += packer.pack(datum)
            return l
        to parse(bytes):
            var m := [].asMap()
            var offset := 0
            for key => reader in layout:
                def slice := bytes.slice(offset, offset + reader.size())
                m |= [key => reader.read(slice)]
                offset += reader.size()
            return m

object struct__quasiParser:
    to valueMaker(template):
        def members := template.split(" ")
        def layout := [].asMap().diverge()
        for member in members:
            def [k, v] := member.split(":")
            layout[k] := v            
        return makeStruct(layout)

var s := makeStruct(["x" => uint8, "y" => ubint16])
def data := ["x" => 42, "y" => 1000]
def bytes := [24, 87, 255]
traceln(`${s.build(data)}`)
traceln(`${s.parse(bytes)}`)

s := struct`x:$uint8 y:$ubint16`
traceln(`${s.build(data)}`)
traceln(`${s.parse(bytes)}`)
