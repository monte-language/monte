def __makeOrderedSpace := import("regions")
def atoi := import("hands.atoi")

def makeLexer(s :str):
    var position := 0

    return object lexer:
        to nextChar():
            if (position >= s.size()):
                return null
            else:
                def rv := s[position]
                position += 1
                return rv

        to backup():
            position -= 1

        to nextToken():
            switch (lexer.nextChar()):
                match ==null:
                    return null
                match ==' ':
                    return lexer.nextToken()
                match =='(':
                    return '('
                match ==')':
                    return ')'
                match ==',':
                    return ','
                match x :('0'..'9'):
                    var digits := [x]
                    var next := lexer.nextChar()
                    while (next =~ _ :('0'..'9')):
                        digits with= next
                        next := lexer.nextChar()
                    lexer.backup()
                    return ["int", atoi(digits)]
                match x :('a'..'z'):
                    var chars := [x]
                    var next := lexer.nextChar()
                    while (next =~ _ :('a'..'z')):
                        chars with= next
                        next := lexer.nextChar()
                    lexer.backup()
                    return ["functor", "".join(chars)]
                match x:
                    throw(`Not a valid character: $x`)
