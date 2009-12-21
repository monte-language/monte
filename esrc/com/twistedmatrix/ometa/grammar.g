
number ::= <spaces> ('-' <barenumber>:x => negative(x)
                    |<barenumber>:x => x)
barenumber ::= ('0' ((('x'|'X') <hexdigit>*:hs => makeHex(hs))
                    |<octaldigit>+:ds => makeOctal(ds)))
               |<digit>+:ds => makeInt(ds)

octaldigit ::= :x ?(isOctDigit(x)) => x
hexdigit ::= :x ?(isHexDigit(x)) => x

escapedChar ::= '\\' ('n' => newline()
                     |'r' => '\r'
                     |'t' => '\t'
                     |'b' => '\b'
                     |'f' => '\f'
                     |'"' => '"'
                     |'\'' => '\''
                     |'\\' => '\\')

character ::= <token "'"> (<escapedChar> | <anything>):c <token "'"> => c

bareString ::= <token "\""> (<escapedChar> | ~('"') <anything>)*:c <token "\""> => makeString(c)
string ::= <bareString>:s => apply("tokenBR", makeList(makeLiteral(s)))

name ::= <letter>:x <letterOrDigit>*:xs => makeString(x, xs)

application ::= (<token "<"> <spaces> <name>:name
                  (<applicationArgs>:args
                     => apply(name, args)
                  |<token ">">
                     => apply(name, makeList())))

applicationArgs ::= (<spaces> <action>)+:args <token ">"> => applicationArgs(args)

expr1 ::= (<application>
          |<ruleValue>
          |<semanticPredicate>
          |<semanticAction>
          |<string>
          |(<number> | <character>):lit => exactly(lit)
          |<token "("> <expr>:e <token ")"> => e
          |<token "["> <expr>:e <token "]"> => listpattern(e))

expr2 ::= (<token "~"> (<token "~"> <expr2>:e => lookahead(e)
                       |<expr2>:e => not(e))
          |<expr1>)

expr3 ::= ((<expr2>:e ('*' => many(e)
                      |'+' => many1(e)
                      |'?' => optional(e)
                      | => e)):r
           (':' <name>:n => bindValue(r, n)
           | => r)
          |<token ":"> <name>:n
           => bindValue(apply("anything", makeList()), n))

expr4 ::= <expr3>*:es => sequence(es)

expr ::= <expr4>:e (<token "|"> <expr4>)*:es => or(e, es)

ruleValue ::= <token "=>"> <action>:a => compileAction(a)

semanticPredicate ::= <token "?("> <action>:a <token ")"> => pred(a)
semanticAction ::= <token "!("> <action>:a <token ")"> => compileAction(a)

rulePart :requiredName ::= (<spaces> <name>:n ?(eq(n, requiredName))
                            <expr4>:args
                            (<token "::="> <expr>:e
                               => sequence(makeList(args, e))
                            |  => args))
rule ::= (<spaces> ~~(<name>:n) <rulePart n>:r
          (<rulePart n>+:rs => makeList(n, or(r, rs))
          |                     => makeList(n, r)))



action ::= <spaces> (<actionCall> | <actionNoun> | <actionLiteral>)
actionCall ::= <name>:verb <token "("> <actionArgs>?:args <token ")"> => makeActionCall(verb, args)
actionArgs ::= <action>:a (<token ","> <action>)*:b => cons(a, b)
actionNoun ::= <name>:n => makeActionNoun(n)
actionLiteral ::=  (<number> | <character> | <bareString>):lit => makeActionLiteral(lit)


grammar ::= <rule>*:rs <spaces> => makeGrammar(makeMapFromPairs(rs))

