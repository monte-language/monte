def makeInputStream(data, offset, loc):
    def size := data.size()
    return object inputStream:
        to head(fail):
            if (offset >= size):
                throw.eject(fail, loc)
            return [data[offset], loc]

        to tail():
            def [line, col] := loc
            if (offset < size && data[offset] == '\n'):
                return makeInputStream(data, offset + 1, [line + 1, 0])
            else:
                return makeInputStream(data, offset + 1, [line, col + 1])


def makeOMeta(inputString):
    var input := makeInputStream(inputString, 0, [1, 0])
    return object OMeta:
        to rule_anything(fail):
          def h := input.head(fail)
          input := input.tail()
          return h
