def zip(xs, ys):
    var index := 0
    def l := [].diverge()
    var x := var y := null
    while (xs.size() > index || ys.size() > index):
        if (xs.size() > index):
            x := xs[index]
        else:
            x := null
        if (ys.size() > index):
            y := ys[index]
        else:
            y := null

        l.push([x, y])
        index += 1
    return l.snapshot()

object uint8:
    to pack(datum):
        return [datum & 0xff]
    to size():
        return 1

object ubint16:
    to pack(datum):
        return [datum >> 8 & 0xff, datum & 0xff]
    to size():
        return 2

def makeStruct(layout):
    return object struct:
        to build(data):
            var l := []
            for key in layout.getKeys():
                def packer := layout[key]
                def datum := data[key]
                l += packer.pack(datum)
            return l.snapshot()
        to parse(bytes):
            pass

object struct__quasiParser:
    to valueMaker(template):
        def members := template.split(" ")
        def layout := [].asMap().diverge()
        for member in members:
            def [k, v] := member.split(":")
            layout[k] := v            
        return makeStruct(layout)

def s := makeStruct(["x" => uint8, "y" => ubint16])
def data := ["x" => 42, "y" => 1000]
traceln(`${s.build(data)}`)
