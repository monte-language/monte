import "lib/codec/percent" =~ [=> PercentEncoding :DeepFrozen]
import "lib/codec/utf8" =~  [=> UTF8 :DeepFrozen]
import "lib/codec" =~ [=> composeCodec :DeepFrozen]
import "unittest" =~ [=> unittest]

exports (fieldMap)

def UTF8Percent :DeepFrozen := composeCodec(PercentEncoding, UTF8)

def fieldMap(body) as DeepFrozen:
    def parts :=[for field in (body.split(b`&`))
                 field.split(b`=`, 1)]
    def decode := UTF8Percent.decode
    return [for [via (decode) n, via (decode) v] in (parts)
            n => v]

def t1(assert):
    assert.equal(fieldMap(b`code=1+1`), ["code" => "1+1"])
    assert.equal(fieldMap(b`code=1%20+%201`), ["code" => "1 + 1"])

unittest([t1])
