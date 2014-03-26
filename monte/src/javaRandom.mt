def GEN := 0x5deece66d
def MASK48 := (1 << 48) - 1

def makeJavaRandom(seed):
    var state := GEN ^ seed & MASK48
    return object javaRandom:
        to next(width):
            if (width < 0):
                throw("Width too small")
            if (width > 48):
                throw("Width too wide")

            state *= GEN
            state += 0xb
            state &= MASK48

            return state >> (48 - width)

def r := makeJavaRandom(0)
