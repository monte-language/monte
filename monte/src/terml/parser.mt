module makeTag, makeTerm, makeLexer, convertToTerm
export (parse)

def parse(lexer) as DeepFrozen:
    def stack := [[].diverge()].diverge()
    var token := lexer.nextToken()

    var expectingParen :boolean := false

    while (token != null):
        traceln(`Stack: $stack Token: $token`)
        # Handle argless functors.
        if (expectingParen && token != '('):
            expectingParen := false
            def tag := stack.pop()[0]
            def term := makeTerm(tag, null, null, null)
            stack[stack.size() - 1].push(term)
            continue

        switch (token):
            match [=="functor", name]:
                stack.push([makeTag(null, name, null)].diverge())
                expectingParen := true
            match [=="int", i]:
                # XXX should pass ejector here and handle things
                def term := convertToTerm(i, null)
                stack[stack.size() - 1].push(term)
            match ==',':
                pass
            match =='(':
                expectingParen := false
            match ==')':
                def [tag] + args := stack.pop()
                traceln(`Will make term with $tag and $args`)
                def term := makeTerm(tag, null, args, null)
                stack[stack.size() - 1].push(term)
        token := lexer.nextToken()

    return stack[0][0]

traceln(parse(makeLexer("term(42, nested(stuff), terms)")))
