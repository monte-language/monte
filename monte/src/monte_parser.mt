module unittest, makeMonteLexer, astBuilder
export (parseModule, parseExpression, parsePattern)
def spanCover(left, right):
    if (left == null || right == null):
        return null
    return left.combine(right)

# # XXX dupe from term parser module
# def makeQuasiTokenChain(makeLexer, template):
#     var i := -1
#     var current := makeLexer("", qBuilder)
#     var lex := current
#     def [VALUE_HOLE, PATTERN_HOLE] := makeLexer.holes()
#     var j := 0
#     return object chainer:
#         to _makeIterator():
#             return chainer

#         to valueHole():
#            return VALUE_HOLE

#         to patternHole():
#            return PATTERN_HOLE

#         to next(ej):
#             if (i >= template.size()):
#                 throw.eject(ej, null)
#             j += 1
#             if (current == null):
#                 if (template[i] == VALUE_HOLE || template[i] == PATTERN_HOLE):
#                     def hol := template[i]
#                     i += 1
#                     return [j, hol]
#                 else:
#                     current := lex.lexerForNextChunk(template[i])._makeIterator()
#                     lex := current
#             escape e:
#                 def t := current.next(e)[1]
#                 return [j, t]
#             catch z:
#                 i += 1
#                 current := null
#                 return chainer.next(ej)

def parseMonte(lex, builder, mode, err):
    def [VALUE_HOLE, PATTERN_HOLE] := [lex.valueHole(), lex.patternHole()]
    def _toks := [].diverge()
    while (true):
         _toks.push(lex.next(__break)[1])
    catch p:
        if (p != null):
            throw.eject(err, p)
    def tokens := _toks.snapshot()
    traceln(`tokens: $tokens ${tokens.size()}`)
    var dollarHoleValueIndex := -1
    var atHoleValueIndex := -1
    var position := -1

    def spanHere():
        if (position + 1 >= tokens.size()):
            return null
        return tokens[position.max(0)].getSpan()

    def spanFrom(start):
        return spanCover(start, spanHere())

    def advance(ej):
        position += 1
        if (position >= tokens.size()):
            throw.eject(ej, ["hit EOF", tokens.last().getSpan()])
        return tokens[position]

    def advanceTag(ej):
        def t := advance(ej)
        def isHole := t == VALUE_HOLE || t == PATTERN_HOLE
        if (isHole):
            return t
        else:
            return t.getTag().getName()

    def acceptTag(tagname, fail):
        def t := advance(fail)
        def specname := t.getTag().getName()
        if (specname != tagname):
            position -= 1
            throw.eject(fail, [`expected $tagname, got $specname`, spanHere()])
        return t

    def acceptEOLs():
        while (true):
            if ((position + 1) >= tokens.size()):
                return
            def t := tokens[position + 1]
            def isHole := t == VALUE_HOLE || t == PATTERN_HOLE
            if (isHole || !["EOL", "#"].contains(t.getTag().getName())):
                return
            position += 1

    def peek():
        if (position + 1 >= tokens.size()):
            return null
        return tokens[position + 1]

    def opt(rule, ej):
        escape e:
            return rule(e)
        catch _:
            return null

    def peekTag():
        if (position + 1 >= tokens.size()):
            return null
        return tokens[position + 1].getTag().getName()

    def matchEOLsThenTag(indent, tagname):
        def origPosition := position
        if (indent):
            acceptEOLs()
        if (position + 1 >= tokens.size()):
            position := origPosition
            return false
        if (tokens[position + 1].getTag().getName() == tagname):
            position += 1
            return true
        else:
            position := origPosition
            return false

    def acceptList(rule):
        acceptEOLs()
        def items := [].diverge()
        escape e:
            items.push(rule(e))
            while (true):
                acceptTag(",", __break)
                acceptEOLs()
                items.push(rule(__break))
        return items.snapshot()

    def acceptListOrMap(ruleList, ruleMap):
        var isMap := false
        def items := [].diverge()
        def startpos := position
        acceptEOLs()
        escape em:
            items.push(ruleMap(em))
            isMap := true
        catch _:
            escape e:
                position := startpos
                items.push(ruleList(e))
                isMap := false
            catch _:
                return [[], false]
        while (true):
            acceptTag(",", __break)
            acceptEOLs()
            if (isMap):
                items.push(ruleMap(__break))
            else:
                items.push(ruleList(__break))
        return [items.snapshot(), isMap]

    def expr
    def order
    def blockExpr
    def prim
    def pattern
    def assign
    def quasiliteral(id, isPattern, ej):
        def spanStart := if (id == null) {spanHere()} else {id.getSpan()}
        def name := if (id == null) {null} else {id.getData()}
        def parts := [].diverge()
        while (true):
            def t := advance(ej)
            def tname := t.getTag().getName()
            if (tname == "QUASI_OPEN" && t.getData() != ""):
                parts.push(builder.QuasiText(t.getData(), t.getSpan()))
            else if (tname == "QUASI_CLOSE"):
                parts.push(builder.QuasiText(t.getData(), t.getSpan()))
                break
            else if (tname == "DOLLAR_IDENT"):
                parts.push(builder.QuasiExprHole(
                               builder.NounExpr(t.getData(), t.getSpan()),
                               t.getSpan()))
            else if (tname == "${"):
                def subexpr := expr(ej)
                parts.push(builder.QuasiExprHole(subexpr, subexpr.getSpan()))
            else if (tname == "AT_IDENT"):
                parts.push(builder.QuasiPatternHole(
                               builder.FinalPattern(
                                   builder.NounExpr(t.getData(), t.getSpan()),
                                   null, t.getSpan()),
                               t.getSpan()))
            else if (tname == "@{"):
                def subpatt := pattern(ej)
                parts.push(builder.QuasiPatternHole(subpatt, subpatt.getSpan()))
        if (isPattern):
            return builder.QuasiParserPattern(name, parts, spanFrom(spanStart))
        else:
            return builder.QuasiParserExpr(name, parts, spanFrom(spanStart))

    def guard(ej):
       def spanStart := spanHere()
       if (peekTag() == "IDENTIFIER"):
            def t := advance(ej)
            def n := builder.NounExpr(t.getData(), t.getSpan())
            if (peekTag() == "["):
                advance(ej)
                def g := acceptList(expr)
                acceptTag("]", ej)
                return builder.GetExpr(n, g, spanFrom(spanStart))
            else:
                return n
       acceptTag("(", ej)
       def e := expr(ej)
       acceptTag(")", ej)
       return e

    def noun(ej):
        if (peekTag() == "IDENTIFIER"):
            def t := advance(ej)
            return builder.NounExpr(t.getData(), t.getSpan())
        else:
            def spanStart := spanHere()
            acceptTag("::", ej)
            def t := acceptTag(".String.", ej)
            return builder.NounExpr(t.getData(), spanFrom(spanStart))

    def maybeGuard():
        def origPosition := position
        if (peekTag() == ":"):
            advance(null)
            escape e:
                return guard(e)
            catch _:
                # might be suite-starting colon
                position := origPosition
                return null

    def namePattern(ej, tryQuasi):
        def spanStart := spanHere()
        def nex := peekTag()
        if (nex == "IDENTIFIER"):
            def t := advance(ej)
            def nex2 := peekTag()
            if (nex2 == "QUASI_OPEN" || nex2 == "QUASI_CLOSE"):
                if (tryQuasi):
                    return quasiliteral(t, true, ej)
                else:
                    throw.eject(ej, [nex2, spanHere()])
            else:
                def g := maybeGuard()
                return builder.FinalPattern(builder.NounExpr(t.getData(), t.getSpan()), g, spanFrom(spanStart))
        else if (nex == "::"):
            advance(ej)
            def spanStart := spanHere()
            def t := acceptTag(".String.", ej)
            def g := maybeGuard()
            return builder.FinalPattern(builder.NounExpr(t.getData(), t.getSpan()), g, spanFrom(spanStart))
        else if (nex == "var"):
            advance(ej)
            def n := noun(ej)
            def g := maybeGuard()
            return builder.VarPattern(n, g, spanFrom(spanStart))
        else if (nex == "&"):
            advance(ej)
            def n := noun(ej)
            def g := maybeGuard()
            return builder.SlotPattern(n, g, spanFrom(spanStart))
        else if (nex == "&&"):
            advance(ej)
            return builder.BindingPattern(noun(ej), spanFrom(spanStart))
        else if (nex == "bind"):
            advance(ej)
            return builder.BindPattern(noun(ej), spanFrom(spanStart))
        throw.eject(ej, [`Unrecognized name pattern $nex`, spanHere()])

    def mapPatternItemInner(ej):
        def spanStart := spanHere()
        if (peekTag() == "=>"):
            advance(ej)
            def p := namePattern(ej, false)
            return builder.MapPatternImport(p, spanFrom(spanStart))
        def k := if (peekTag() == "(") {
            advance(ej)
            def e := expr(ej)
            acceptEOLs()
            acceptTag(")", ej)
            e
        } else {
            if ([".String.", ".int.", ".float64.", ".char."].contains(peekTag())) {
                def t := advance(ej)
                builder.LiteralExpr(t, t.getSpan())
            } else {
                throw.eject(ej, ["Map pattern keys must be literals or expressions in parens", spanHere()])
            }
        }
        acceptTag("=>", ej)
        return builder.MapPatternAssoc(k, pattern(ej), spanFrom(spanStart))

    def mapPatternItem(ej):
        def spanStart := spanHere()
        def p := mapPatternItemInner(ej)
        if (peekTag() == ":="):
            advance(ej)
            return builder.MapPatternDefault(p, order(ej), spanFrom(spanStart))
        else:
            return builder.MapPatternRequired(p, spanFrom(spanStart))

    def _pattern(ej):
        escape e:
            return namePattern(e, true)
        # ... if namePattern fails, keep going
        def spanStart := spanHere()
        def nex := peekTag()
        if (nex == "QUASI_OPEN" || nex == "QUASI_CLOSE"):
            return quasiliteral(null, true, ej)
        else if (nex == "=="):
            def spanStart := spanHere()
            advance(ej)
            return builder.SamePattern(prim(ej), true, spanFrom(spanStart))
        else if (nex == "!="):
            def spanStart := spanHere()
            advance(ej)
            return builder.SamePattern(prim(ej), false, spanFrom(spanStart))
        else if (nex == "_"):
            advance(ej)
            def spanStart := spanHere()
            def g := if (peekTag() == ":" && tokens[position + 2].getTag().getName() != "EOL") {
                advance(ej); guard(ej)
            } else {
                null
            }
            return builder.IgnorePattern(g, spanFrom(spanStart))
        else if (nex == "via"):
            advance(ej)
            def spanStart := spanHere()
            acceptTag("(", ej)
            def e := expr(ej)
            acceptTag(")", ej)
            return builder.ViaPattern(e, pattern(ej), spanFrom(spanStart))
        else if (nex == "["):
            def spanStart := spanHere()
            advance(ej)
            def [items, isMap] := acceptListOrMap(pattern, mapPatternItem)
            acceptEOLs()
            acceptTag("]", ej)
            if (isMap):
                def tail := if (peekTag() == "|") {advance(ej); _pattern(ej)}
                return builder.MapPattern(items, tail, spanFrom(spanStart))
            else:
                def tail := if (peekTag() == "+") {advance(ej); _pattern(ej)}
                return builder.ListPattern(items, tail, spanFrom(spanStart))
        throw.eject(ej, [`Invalid pattern $nex`, spanHere()])

    bind pattern(ej):
        def spanStart := spanHere()
        def p := _pattern(ej)
        if (peekTag() == "?"):
            advance(ej)
            acceptTag("(", ej)
            def e := expr(ej)
            acceptTag(")", ej)
            return builder.SuchThatPattern(p, e, spanFrom(spanStart))
        else:
            return p
    "XXX buggy expander eats this line"

    def mapItem(ej):
        def spanStart := spanHere()
        if (peekTag() == "=>"):
            advance(ej)
            return builder.MapExprExport(prim(ej), spanFrom(spanStart))
        def k := expr(ej)
        acceptTag("=>", ej)
        def v := expr(ej)
        return builder.MapExprAssoc(k, v, spanFrom(spanStart))

    def seqSep(ej):
        if (![";", "#", "EOL"].contains(peekTag())):
            ej(null)
        advance(ej)
        while (true):
            if (![";", "#", "EOL"].contains(peekTag())):
                break
            advance(ej)

    def seq(indent, ej):
        def ex := if (indent) {blockExpr} else {expr}
        def start := spanHere()
        def exprs := [ex(ej)].diverge()
        while (true):
            seqSep(__break)
            exprs.push(ex(__break))
        opt(seqSep, ej)
        if (exprs.size() == 1):
            return exprs[0]
        return builder.SeqExpr(exprs.snapshot(), spanFrom(start))

    def block(indent, ej):
        if (indent):
            acceptTag(":", ej)
            acceptEOLs()
            acceptTag("INDENT", ej)
        else:
            acceptTag("{", ej)
        acceptEOLs()
        def contents := if (peekTag() == "pass") {
            advance(ej)
            acceptEOLs()
            builder.SeqExpr([], null)
        } else {
            escape e {
                seq(indent, ej)
            } catch _ {
                builder.SeqExpr([], null)
            }
        }
        if (indent):
            acceptTag("DEDENT", ej)
        else:
            acceptTag("}", ej)
        return contents

    def suite(rule, indent, ej):
        if (indent):
            acceptTag(":", ej)
            acceptEOLs()
            acceptTag("INDENT", ej)
        else:
            acceptTag("{", ej)
        acceptEOLs()
        def content := rule(indent, ej)
        acceptEOLs()
        if (indent):
            acceptTag("DEDENT", ej)
        else:
            acceptTag("}", ej)
        return content

    def repeat(rule, indent, ej):
        def contents := [].diverge()
        while (true):
            contents.push(rule(indent, __break))
        return contents.snapshot()

    def forExprHead(needParens, ej):
        def p1 := pattern(ej)
        def p2 := if (peekTag() == "=>") {advance(ej); pattern(ej)
                  } else {null}
        if (needParens):
            acceptEOLs()
        acceptTag("in", ej)
        if (needParens):
            acceptEOLs()
            acceptTag("(", ej)
            acceptEOLs()
        def it := order(ej)
        if (needParens):
            acceptEOLs()
            acceptTag(")", ej)
            acceptEOLs()
        return if (p2 == null) {[null, p1, it]} else {[p1, p2, it]}

    def matchers(indent, ej):
        def spanStart := spanHere()
        acceptTag("match", ej)
        def pp := pattern(ej)
        def bl := block(indent, ej)
        acceptEOLs()
        return builder.Matcher(pp, bl, spanFrom(spanStart))

    def catcher(indent, ej):
        def spanStart := spanHere()
        return builder.Catcher(pattern(ej), block(indent, ej), spanFrom(spanStart))

    def methBody(indent, ej):
        acceptEOLs()
        def doco := if (peekTag() == ".String.") {
            advance(ej)
        } else {
            null
        }
        acceptEOLs()
        def contents := escape e {
            seq(indent, ej)
        } catch _ {
            builder.SeqExpr([], null)
        }
        return [doco, contents]

    def meth(indent, ej):
        acceptEOLs()
        def spanStart := spanHere()
        def mknode := if (peekTag() == "to") {
            advance(ej)
            builder."To"
        } else {
            acceptTag("method", ej)
            builder."Method"
        }
        def verb := if (peekTag() == ".String.") {
            advance(ej)
        } else {
            def t := acceptTag("IDENTIFIER", ej)
            __makeString.fromString(t.getData(), t.getSpan())
        }
        acceptTag("(", ej)
        def patts := acceptList(pattern)
        acceptTag(")", ej)
        def resultguard := if (peekTag() == ":") {
            advance(ej)
            if (peekTag() == "EOL") {
                # Oops, end of indenty block.
                position -= 1
                null
            } else {
                guard(ej)
            }
        } else {
            null
        }
        def [doco, body] := suite(methBody, indent, ej)
        return mknode(doco, verb, patts, resultguard, body, spanFrom(spanStart))

    def objectScript(indent, ej):
        def doco := if (peekTag() == ".String.") {
            advance(ej)
        } else {
            null
        }
        def meths := [].diverge()
        while (true):
            acceptEOLs()
            if (peekTag() == "pass"):
                advance(ej)
                continue
            meths.push(meth(indent, __break))
        def matchs := [].diverge()
        while (true):
            if (peekTag() == "pass"):
                advance(ej)
                continue
            matchs.push(matchers(indent, __break))
        return [doco, meths.snapshot(), matchs.snapshot()]

    def oAuditors(ej):
        return [
            if (peekTag() == "as") {
                advance(ej)
                order(ej)
            } else {
                null
            },
            if (peekTag() == "implements") {
                advance(ej)
                acceptList(order)
            } else {
                []
            }]

    def blockLookahead(ej):
        def origPosition := position
        try:
            acceptTag(":", ej)
            acceptEOLs()
            acceptTag("INDENT", ej)
        finally:
            position := origPosition

    def objectExpr(name, indent, tryAgain, ej, spanStart):
        def oExtends := if (peekTag() == "extends") {
            advance(ej)
            order(ej)
        } else {
            null
        }
        def [oAs, oImplements] := oAuditors(ej)
        if (indent):
            blockLookahead(tryAgain)
        def [doco, methods, matchers] := suite(objectScript, indent, ej)
        def span := spanFrom(spanStart)
        return builder.ObjectExpr(doco, name, oAs, oImplements,
            builder.Script(oExtends, methods, matchers, span), span)

    def objectFunction(name, indent, tryAgain, ej, spanStart):
        acceptTag("(", ej)
        def patts := acceptList(pattern)
        acceptTag(")", ej)
        def resultguard := if (peekTag() == ":") {
            advance(ej)
            if (peekTag() == "EOL") {
                # Oops, end of indenty block.
                position -= 1
                null
            } else {
                guard(ej)
            }
        } else {
            null
        }
        def [oAs, oImplements] := oAuditors(ej)
        if (indent):
            blockLookahead(tryAgain)
        def [doco, body] := suite(methBody, indent, ej)
        def span := spanFrom(spanStart)
        return builder.ObjectExpr(doco, name, oAs, oImplements,
            builder.FunctionScript(patts, resultguard, body, span), span)

    def paramDesc(ej):
        def spanStart := spanHere()
        def name := if (peekTag() == "_") {
            advance(ej)
            null
        } else if (peekTag() == "IDENTIFIER") {
            def t := advance(ej)
            __makeString.fromString(t.getData(), t.getSpan())
        } else {
            acceptTag("::", ej)
            acceptTag(".String.", ej)
        }
        def g := if (peekTag() == ":") {
            advance(ej)
            guard(ej)
        } else {
            null
        }
        return builder.ParamDesc(name, g, spanFrom(spanStart))

    def messageDescInner(indent, tryAgain, ej):
        acceptTag("(", ej)
        def params := acceptList(paramDesc)
        acceptTag(")", ej)
        def resultguard := if (peekTag() == ":") {
            advance(ej)
            if (peekTag() == "EOL") {
                # Oops, end of indenty block.
                position -= 1
                null
            } else {
                guard(ej)
            }
        } else {
            null
        }
        def doco := if ([":", "{"].contains(peekTag())) {
            if (indent) {
                blockLookahead(tryAgain)
            }
            suite(fn i, j {acceptEOLs(); acceptTag(".String.", j)}, indent, ej)
        } else {
            null
        }
        return [doco, params, resultguard]

    def messageDesc(indent, ej):
        def spanStart := spanHere()
        acceptTag("to", ej)
        def verb := if (peekTag() == ".String.") {
            advance(ej)
        } else {
            def t := acceptTag("IDENTIFIER", ej)
            __makeString.fromString(t.getData(), t.getSpan())
        }
        def [doco, params, resultguard] := messageDescInner(indent, ej, ej)
        return builder.MessageDesc(doco, verb, params, resultguard, spanFrom(spanStart))

    def interfaceBody(indent, ej):
        def doco := if (peekTag() == ".String.") {
            advance(ej)
        } else {
            null
        }
        def msgs := [].diverge()
        while (true):
            acceptEOLs()
            if (peekTag() == "pass"):
                advance(ej)
                continue
            msgs.push(messageDesc(indent, __break))
        return [doco, msgs.snapshot()]

    def basic(indent, tryAgain, ej):
        def origPosition := position
        def tag := peekTag()
        if (tag == "if"):
            def spanStart := spanHere()
            advance(ej)
            acceptTag("(", ej)
            def test := expr(ej)
            acceptTag(")", ej)
            if (indent):
                blockLookahead(tryAgain)
            def consq := block(indent, ej)
            def maybeElseStart := position
            if (indent):
                acceptEOLs()
            def alt := if (matchEOLsThenTag(indent, "else")) {
                if (peekTag() == "if") {
                    basic(indent, ej, ej)
                } else {
                    block(indent, ej)
                }} else {
                    position := maybeElseStart
                    null
                }
            return builder.IfExpr(test, consq, alt, spanFrom(spanStart))
        if (tag == "escape"):
            def spanStart := spanHere()
            advance(ej)
            def p1 := pattern(ej)
            if (indent):
                blockLookahead(tryAgain)
            def e1 := block(indent, ej)
            if (matchEOLsThenTag(indent, "catch")):
                def p2 := pattern(ej)
                def e2 := block(indent, ej)
                return builder.EscapeExpr(p1, e1, p2, e2, spanFrom(spanStart))
            return builder.EscapeExpr(p1, e1, null, null, spanFrom(spanStart))
        if (tag == "for"):
            def spanStart := spanHere()
            advance(ej)
            def [k, v, it] := forExprHead(false, ej)
            if (indent):
                blockLookahead(tryAgain)
            def body := block(indent, ej)
            def [catchPattern, catchBody] := if (matchEOLsThenTag(indent, "catch")) {
                [pattern(ej), block(indent, ej)]
            } else {
                [null, null]
            }
            return builder.ForExpr(it, k, v, body, catchPattern, catchBody, spanFrom(spanStart))
        if (tag == "fn"):
            def spanStart := spanHere()
            advance(ej)
            def patt := acceptList(pattern)
            def body := block(false, ej)
            return builder.FunctionExpr(patt, body, spanFrom(spanStart))
        if (tag == "switch"):
            def spanStart := spanHere()
            advance(ej)
            acceptTag("(", ej)
            def spec := expr(ej)
            acceptTag(")", ej)
            if (indent):
                blockLookahead(tryAgain)
            return builder.SwitchExpr(
                spec,
                suite(fn i, j {repeat(matchers, i, j)}, indent, ej),
                spanFrom(spanStart))
        if (tag == "try"):
            def spanStart := spanHere()
            advance(ej)
            if (indent):
                blockLookahead(tryAgain)
            def tryblock := block(indent, ej)
            def catchers := [].diverge()
            while (matchEOLsThenTag(indent, "catch")):
                catchers.push(catcher(indent, ej))
            def origPosition := position
            def finallyblock := if (matchEOLsThenTag(indent, "finally")) {
                block(indent, ej)
            } else {
                null
            }
            return builder.TryExpr(tryblock, catchers.snapshot(),
                                   finallyblock, spanFrom(spanStart))
        if (tag == "while"):
            def spanStart := spanHere()
            advance(ej)
            acceptTag("(", ej)
            def test := expr(ej)
            acceptTag(")", ej)
            if (indent):
                blockLookahead(tryAgain)
            def whileblock := block(indent, ej)
            def catchblock := if (matchEOLsThenTag(indent, "catch")) {
               catcher(indent, ej)
            } else {
                null
            }
            return builder.WhileExpr(test, whileblock, catchblock, spanFrom(spanStart))
        if (tag == "when"):
            def spanStart := spanHere()
            advance(ej)
            acceptTag("(", ej)
            def exprs := acceptList(expr)
            acceptTag(")", ej)
            acceptTag("->", ej)
            if (indent):
                acceptEOLs()
                acceptTag("INDENT", tryAgain)
            else:
                acceptTag("{", ej)
            def whenblock := escape e {
                seq(indent, ej)
            } catch _ {
                builder.SeqExpr([], null)
            }
            if (indent):
                acceptTag("DEDENT", ej)
            else:
                acceptTag("}", ej)
            def catchers := [].diverge()
            while (matchEOLsThenTag(indent, "catch")):
               catchers.push(catcher(indent, ej))
            def finallyblock := if (matchEOLsThenTag(indent, "finally")) {
                block(indent, ej)
            } else {
                null
            }
            return builder.WhenExpr(exprs, whenblock, catchers.snapshot(),
                                    finallyblock, spanFrom(spanStart))
        if (tag == "bind"):
            def spanStart := spanHere()
            advance(ej)
            def name := builder.BindPattern(noun(ej), spanFrom(spanStart))
            if (peekTag() == "("):
                return objectFunction(name, indent, tryAgain, ej, spanStart)
            else if (peekTag() == ":="):
                position := origPosition
                return assign(ej)
            else:
                return objectExpr(name, indent, tryAgain, ej, spanStart)

        if (tag == "object"):
            def spanStart := spanHere()
            advance(ej)
            def name := if (peekTag() == "bind") {
                advance(ej)
                builder.BindPattern(noun(ej), spanFrom(spanStart))
            } else if (peekTag() == "_") {
                advance(ej)
                builder.IgnorePattern(null, spanHere())
            } else {
                builder.FinalPattern(noun(ej), null, spanFrom(spanStart))
            }
            return objectExpr(name, indent, tryAgain, ej, spanStart)

        if (tag == "def"):
            def spanStart := spanHere()
            advance(ej)
            var isBind := false
            if (!["IDENTIFIER", "::", "bind"].contains(peekTag())):
                position := origPosition
                return assign(ej)
            def name := if (peekTag() == "bind") {
                advance(ej)
                isBind := true
                builder.BindPattern(noun(ej), spanFrom(spanStart))
            } else {
                builder.FinalPattern(noun(ej), null, spanFrom(spanStart))
            }
            if (peekTag() == "("):
                return objectFunction(name, indent, tryAgain, ej, spanStart)
            else if (["exit", ":="].contains(peekTag())):
                position := origPosition
                return assign(ej)
            else if (isBind):
                throw.eject(ej, ["expected :=", spanHere()])
            else:
                return builder.ForwardExpr(name, spanFrom(spanStart))

        if (tag == "interface"):
            def spanStart := spanHere()
            advance(ej)
            def name := namePattern(ej, false)
            def guards_ := if (peekTag() == "guards") {
                advance(ej)
                pattern(ej)
            } else {
                null
            }
            def extends_ := if (peekTag() == "extends") {
                advance(ej)
                acceptList(order)
            } else {
                []
            }
            def implements_ := if (peekTag() == "implements") {
                advance(ej)
                acceptList(order)
            } else {
                []
            }
            if (peekTag() == "("):
                def [doco, params, resultguard] := messageDescInner(indent, tryAgain, ej)
                return builder.FunctionInterfaceExpr(doco, name, guards_, extends_, implements_,
                     builder.MessageDesc(doco, "run", params, resultguard, spanFrom(spanStart)),
                     spanFrom(spanStart))
            if (indent):
                blockLookahead(tryAgain)
            def [doco, msgs] := suite(interfaceBody, indent, ej)
            return builder.InterfaceExpr(doco, name, guards_, extends_, implements_, msgs,
                spanFrom(spanStart))
        if (peekTag() == "meta"):
            def spanStart := spanHere()
            acceptTag("meta", ej)
            acceptTag(".", ej)
            def verb := acceptTag("IDENTIFIER", ej)
            if (verb.getData() == "context"):
                acceptTag("(", ej)
                acceptTag(")", ej)
                return builder.MetaContextExpr(spanFrom(spanStart))
            if (verb.getData() == "getState"):
                acceptTag("(", ej)
                acceptTag(")", ej)
                return builder.MetaStateExpr(spanFrom(spanStart))
            throw.eject(ej, [`Meta verbs are "context" or "getState"`, spanHere()])

        if (indent && peekTag() == "pass"):
            advance(ej)
            return builder.SeqExpr([], advance(ej).getSpan())
        throw.eject(tryAgain, [`don't recognize $tag`, spanHere()])

    bind blockExpr(ej):
        def origPosition := position
        escape e:
            return basic(true, e, ej)
        position := origPosition
        return expr(ej)
    "XXX buggy expander eats this line"

    bind prim(ej):
        def tag := peekTag()
        if ([".String.", ".int.", ".float64.", ".char."].contains(tag)):
            def t := advance(ej)
            return builder.LiteralExpr(t.getData(), t.getSpan())
        if (tag == "IDENTIFIER"):
            def t := advance(ej)
            def nex := peekTag()
            if (nex == "QUASI_OPEN" || nex == "QUASI_CLOSE"):
                return quasiliteral(t, false, ej)
            else:
                return builder.NounExpr(t.getData(), t.getSpan())
        if (tag == "::"):
            def spanStart := spanHere()
            advance(ej)
            def t := acceptTag(".String.", ej)
            return builder.NounExpr(t.getData(), t.getSpan())
        if (tag == "QUASI_OPEN" || tag == "QUASI_CLOSE"):
            return quasiliteral(null, false, ej)
        # paren expr
        if (tag == "("):
            advance(ej)
            acceptEOLs()
            def e := seq(false, ej)
            acceptEOLs()
            acceptTag(")", ej)
            return e
        # hideexpr
        if (tag == "{"):
            def spanStart := spanHere()
            advance(ej)
            acceptEOLs()
            if (peekTag() == "}"):
                advance(ej)
                return builder.HideExpr(builder.SeqExpr([], null), spanFrom(spanStart))
            def e := seq(false, ej)
            acceptEOLs()
            acceptTag("}", ej)
            return builder.HideExpr(e, spanFrom(spanStart))
        # list/map
        if (tag == "["):
            def spanStart := spanHere()
            advance(ej)
            acceptEOLs()
            if (peekTag() == "for"):
                advance(ej)
                def [k, v, it] := forExprHead(true, ej)
                def filt := if (peekTag() == "if") {
                    advance(ej)
                    acceptTag("(", ej)
                    acceptEOLs()
                    def e := expr(ej)
                    acceptEOLs()
                    acceptTag(")", ej)
                    e
                } else {
                    null
                }
                acceptEOLs()
                def body := expr(ej)
                if (peekTag() == "=>"):
                    advance(ej)
                    acceptEOLs()
                    def vbody := expr(ej)
                    acceptTag("]", ej)
                    return builder.MapComprehensionExpr(it, filt, k, v, body, vbody,
                        spanFrom(spanStart))
                acceptTag("]", ej)
                return builder.ListComprehensionExpr(it, filt, k, v, body,
                    spanFrom(spanStart))
            def [items, isMap] := acceptListOrMap(expr, mapItem)
            acceptEOLs()
            acceptTag("]", ej)
            if (isMap):
                return builder.MapExpr(items, spanFrom(spanStart))
            else:
                return builder.ListExpr(items, spanFrom(spanStart))
        return basic(false, ej, ej)
    "XXX buggy expander eats this line"
    def call(ej):
        def spanStart := spanHere()
        def base := prim(ej)
        def trailers := [].diverge()

        def callish(methodish, curryish):
            def verb := if (peekTag() == ".String.") {
                advance(ej).getData()
            } else {
                def t := acceptTag("IDENTIFIER", ej)
                __makeString.fromString(t.getData(), t.getSpan())
            }
            if (peekTag() == "("):
                advance(ej)
                def arglist := acceptList(expr)
                acceptEOLs()
                acceptTag(")", ej)
                trailers.push([methodish, [verb, arglist, spanFrom(spanStart)]])
                return false
            else:
                trailers.push(["CurryExpr", [verb, curryish, spanFrom(spanStart)]])
                return true

        def funcallish(name):
            acceptTag("(", ej)
            def arglist := acceptList(expr)
            acceptEOLs()
            acceptTag(")", ej)
            trailers.push([name, [arglist, spanFrom(spanStart)]])

        while (true):
            if (peekTag() == "."):
                advance(ej)
                if (callish("MethodCallExpr", false)):
                    break
            else if (peekTag() == "("):
                funcallish("FunCallExpr")
            else if (peekTag() == "<-"):
                advance(ej)
                if (peekTag() == "("):
                    funcallish("FunSendExpr")
                else:
                    if(callish("SendExpr", true)):
                        break
            else if (peekTag() == "["):
                advance(ej)
                def arglist := acceptList(expr)
                acceptEOLs()
                acceptTag("]", ej)
                trailers.push(["GetExpr", [arglist, spanFrom(spanStart)]])
            else:
                break
        var result := base
        for tr in trailers:
            result := M.call(builder, tr[0], [result] + tr[1])
        return result

    def prefix(ej):
        def spanStart := spanHere()
        def op := peekTag()
        if (op == "-"):
            advance(ej)
            return builder.PrefixExpr("-", prim(ej), spanFrom(spanStart))
        if (["~", "!"].contains(op)):
            advance(ej)
            return builder.PrefixExpr(op, call(ej), spanFrom(spanStart))
        if (op == "&"):
            advance(ej)
            return builder.SlotExpr(noun(ej), spanFrom(spanStart))
        if (op == "&&"):
            advance(ej)
            return builder.BindingExpr(noun(ej), spanFrom(spanStart))
        def base := call(ej)
        if (peekTag() == ":"):
            advance(ej)
            if (peekTag() == "EOL"):
                # oops, a token too far
                position -= 1
                return base
            return builder.CoerceExpr(base, guard(ej), spanFrom(spanHere))
        return base
    def operators  := [
        "**" => 1,
        "*" => 2,
        "/" => 2,
        "//" => 2,
        "%" => 2,
        "+" => 3,
        "-" => 3,
        "<<" => 4,
        ">>" => 4,
        ".." => 5,
        "..!" => 5,
        ">" => 6,
        "<" => 6,
        ">=" => 6,
        "<=" => 6,
        "<=>" => 6,
        "=~" => 7,
        "!~" => 7,
        "==" => 7,
        "!=" => 7,
        "&!" => 7,
        "^" => 7,
        "&" => 8,
        "|" => 8,
        "&&" => 9,
        "||" => 10]

    def leftAssociative := ["+", "-", ">>", "<<", "/", "*", "//", "%"]
    def selfAssociative := ["|", "&"]
    def convertInfix(maxPrec, ej):
        def lhs := prefix(ej)
        def output := [lhs].diverge()
        def opstack := [].diverge()
        def emitTop():
            def [_, opName] := opstack.pop()
            def rhs := output.pop()
            def lhs := output.pop()
            def tehSpan := spanCover(lhs.getSpan(), rhs.getSpan())
            if (opName == "=="):
                output.push(builder.SameExpr(lhs, rhs, true, tehSpan))
            else if (opName == "!="):
                output.push(builder.SameExpr(lhs, rhs, false, tehSpan))
            else if (opName == "&&"):
                output.push(builder.AndExpr(lhs, rhs, tehSpan))
            else if (opName == "||"):
                output.push(builder.OrExpr(lhs, rhs, tehSpan))
            else if (["..", "..!"].contains(opName)):
                output.push(builder.RangeExpr(lhs, opName, rhs, tehSpan))
            else if (opName == "=~"):
                output.push(builder.MatchBindExpr(lhs, rhs, tehSpan))
            else if ([">", "<", ">=", "<=", "<=>"].contains(opName)):
                output.push(builder.CompareExpr(lhs, opName, rhs, tehSpan))
            else:
                output.push(builder.BinaryExpr(lhs, opName, rhs, tehSpan))

        while (true):
            def op := peekTag()
            def nextPrec := operators.fetch(op, __break)
            if (nextPrec > maxPrec):
                break
            advance(ej)
            acceptEOLs()
            # XXX buggy expander can't handle compound booleans
            if (opstack.size() > 0):
                def selfy := selfAssociative.contains(op) && (opstack.last()[1] == op)
                def lefty := leftAssociative.contains(op) && opstack.last()[0] <= nextPrec
                def b2 := lefty || selfy
                if (opstack.last()[0] < nextPrec || b2):
                    emitTop()
            opstack.push([operators[op], op])
            if (["=~", "!~"].contains(op)):
                output.push(pattern(ej))
            else:
                output.push(prefix(ej))
        while (opstack.size() > 0):
            emitTop()
        if (output.size() != 1):
            throw(["Internal parser error", spanHere()])
        return output[0]

    bind order(ej):
        return convertInfix(6, ej)
    "XXX buggy expander eats this line"

    def infix(ej):
        return convertInfix(10, ej)

    def _assign(ej):
        def spanStart := spanHere()
        def defStart := position
        if (peekTag() == "def"):
            advance(ej)
            def patt := pattern(ej)
            def ex := if (peekTag() == "exit") {
                advance(ej)
                order(ej)
            } else {
                null
            }
            # careful, this might be a trap
            if (peekTag() == ":="):
                advance(ej)
                return builder.DefExpr(patt, ex, assign(ej), spanFrom(spanStart))
            else:
                # bail out!
                position := defStart
                return basic(false, ej, ej)
        if (["var", "bind"].contains(peekTag())):
            def patt := pattern(ej)
            if (peekTag() == ":="):
                advance(ej)
                return builder.DefExpr(patt, null, assign(ej), spanFrom(spanStart))
            else:
                # curses, foiled again
                position := defStart
                return basic(false, ej, ej)
        def lval := infix(ej)
        if (peekTag() == ":="):
            advance(ej)
            def lt := lval.asTerm().getTag().getName()
            if (["NounExpr", "GetExpr"].contains(lt)):
                return builder.AssignExpr(lval, assign(ej), spanFrom(spanStart))
            throw.eject(ej, [`Invalid assignment target`, lt.getSpan()])
        if (peekTag() =~ `@op=`):
            advance(ej)
            def lt := lval.asTerm().getTag().getName()
            if (["NounExpr", "GetExpr"].contains(lt)):
                return builder.AugAssignExpr(op, lval, assign(ej), spanFrom(spanStart))
            throw.eject(ej, [`Invalid assignment target`, lt.getSpan()])
        if (peekTag() == "VERB_ASSIGN"):
            def verb := advance(ej).getData()
            def lt := lval.asTerm().getTag().getName()
            if (["NounExpr", "GetExpr"].contains(lt)):
                acceptTag("(", ej)
                acceptEOLs()
                def node := builder.VerbAssignExpr(verb, lval, acceptList(expr),
                     spanFrom(spanStart))
                acceptEOLs()
                acceptTag(")", ej)
                return node
            throw.eject(ej, [`Invalid assignment target`, lt.getSpan()])
        return lval
    bind assign := _assign

    def _expr(ej):
        if (["continue", "break", "return"].contains(peekTag())):
            def spanStart := spanHere()
            def ex := advanceTag(ej)
            if (peekTag() == "(" && tokens[position + 2].getTag().getName() == ")"):
                position += 2
                return builder.ExitExpr(ex, null, spanFrom(spanStart))
            if (["EOL", "#", ";", "DEDENT", null].contains(peekTag())):
                return builder.ExitExpr(ex, null, spanFrom(spanStart))
            def val := blockExpr(ej)
            return builder.ExitExpr(ex, val, spanFrom(spanStart))
        return assign(ej)

    bind expr := _expr

    def module_(ej):
        def start := spanHere()
        def modKw := acceptTag("module", ej)
        def imports := acceptList(pattern)
        acceptEOLs()
        def exports := if (peekTag() == "export") {
            advance(ej)
            acceptTag("(", ej)
            def exports := acceptList(noun)
            acceptTag(")", ej)
            acceptEOLs()
            exports
        }
        def body := seq(true, ej)
        return builder."Module"(imports, exports, body, spanFrom(start))

    def start(ej):
        acceptEOLs()
        if (peekTag() == "module"):
            return module_(ej)
        else:
            return seq(true, ej)
    if (mode == "module"):
        def val := start(err)
        acceptEOLs()
        if (position < (tokens.size() - 1)):
            throw.eject(err, `Trailing garbage: ${tokens.slice(position, tokens.size())}`)
        return val
    else if (mode == "expression"):
        return blockExpr(err)
    else if (mode == "pattern"):
        return pattern(err)
    return "broke"

def parseExpression(lex, builder, err):
    return parseMonte(lex, builder, "expression", err)

def parseModule(lex, builder, err):
    return parseMonte(lex, builder, "module", err)

def parsePattern(lex, builder, err):
    return parseMonte(lex, builder, "pattern", err)

# object quasiMonteParser:
#     to valueHole(n):
#         return VALUE_HOLE
#     to patternHole(n):
#         return PATTERN_HOLE

#     to valueMaker(template):
#         def chain := makeQuasiTokenChain(makeMonteLexer, template)
#         def q := makeMonteParser(chain, astBuilder)
#         return object qast extends q:
#            to substitute(values):
#                return q.transform(holeFiller)

#     to matchMaker(template):
#         def chain := makeQuasiTokenChain(makeMonteLexer, template)
#         def q := makeMonteParser(chain, astBuilder)
#         return object qast extends q:
#             to matchBind(values, specimen, ej):
#                 escape ej:
#                     def holeMatcher := makeHoleMatcher(ej)
#                     q.transform(holeMatcher)
#                     return holeMatcher.getBindings()
#                 catch blee:
#                     ej(`$q doesn't match $specimen: $blee`)

# Tests.

def expr(s):
 return parseExpression(makeMonteLexer(s + "\n"), astBuilder, throw).asTerm()

def pattern(s):
 return parsePattern(makeMonteLexer(s), astBuilder, throw).asTerm()

def test_Literal(assert):
    assert.equal(expr("\"foo bar\""), term`LiteralExpr("foo bar")`)
    assert.equal(expr("'z'"), term`LiteralExpr('z')`)
    assert.equal(expr("7"), term`LiteralExpr(7)`)
    assert.equal(expr("(7)"), term`LiteralExpr(7)`)
    assert.equal(expr("0.5"), term`LiteralExpr(0.5)`)

def test_Noun(assert):
    assert.equal(expr("foo"), term`NounExpr("foo")`)
    assert.equal(expr("::\"object\""), term`NounExpr("object")`)

def test_QuasiliteralExpr(assert):
    assert.equal(expr("`foo`"), term`QuasiParserExpr(null, [QuasiText("foo")])`)
    assert.equal(expr("bob`foo`"), term`QuasiParserExpr("bob", [QuasiText("foo")])`)
    assert.equal(expr("bob`foo`` $x baz`"), term`QuasiParserExpr("bob", [QuasiText("foo`` "), QuasiExprHole(NounExpr("x")), QuasiText(" baz")])`)
    assert.equal(expr("`($x)`"), term`QuasiParserExpr(null, [QuasiText("("), QuasiExprHole(NounExpr("x")), QuasiText(")")])`)

def test_Hide(assert):
    assert.equal(expr("{}"), term`HideExpr(SeqExpr([]))`)
    assert.equal(expr("{1}"), term`HideExpr(LiteralExpr(1))`)

def test_List(assert):
    assert.equal(expr("[]"), term`ListExpr([])`)
    assert.equal(expr("[a, b]"), term`ListExpr([NounExpr("a"), NounExpr("b")])`)

def test_Map(assert):
    assert.equal(expr("[k => v, => a]"),
         term`MapExpr([MapExprAssoc(NounExpr("k"), NounExpr("v")),
                       MapExprExport(NounExpr("a"))])`)
    assert.equal(expr("[=> b, k => v]"),
         term`MapExpr([MapExprExport(NounExpr("b")),
                       MapExprAssoc(NounExpr("k"), NounExpr("v"))])`)

def test_ListComprehensionExpr(assert):
    assert.equal(expr("[for k => v in (a) if (b) c]"), term`ListComprehensionExpr(NounExpr("a"), NounExpr("b"), FinalPattern(NounExpr("k"), null), FinalPattern(NounExpr("v"), null), NounExpr("c"))`)
    assert.equal(expr("[for v in (a) c]"), term`ListComprehensionExpr(NounExpr("a"), null, null, FinalPattern(NounExpr("v"), null), NounExpr("c"))`)

def test_MapComprehensionExpr(assert):
    assert.equal(expr("[for k => v in (a) if (b) k1 => v1]"), term`MapComprehensionExpr(NounExpr("a"), NounExpr("b"), FinalPattern(NounExpr("k"), null), FinalPattern(NounExpr("v"), null), NounExpr("k1"), NounExpr("v1"))`)
    assert.equal(expr("[for v in (a) k1 => v1]"), term`MapComprehensionExpr(NounExpr("a"), null, null, FinalPattern(NounExpr("v"), null), NounExpr("k1"), NounExpr("v1"))`)

def test_IfExpr(assert):
    assert.equal(expr("if (1) {2} else if (3) {4} else {5}"),
        term`IfExpr(LiteralExpr(1), LiteralExpr(2), IfExpr(LiteralExpr(3), LiteralExpr(4), LiteralExpr(5)))`)
    assert.equal(expr("if (1) {2} else {3}"), term`IfExpr(LiteralExpr(1), LiteralExpr(2), LiteralExpr(3))`)
    assert.equal(expr("if (1) {2}"), term`IfExpr(LiteralExpr(1), LiteralExpr(2), null)`)
    assert.equal(expr("if (1):\n  2\nelse if (3):\n  4\nelse:\n  5"),
        term`IfExpr(LiteralExpr(1), LiteralExpr(2), IfExpr(LiteralExpr(3), LiteralExpr(4), LiteralExpr(5)))`)
    assert.equal(expr("if (1):\n  2\nelse:\n  3"), term`IfExpr(LiteralExpr(1), LiteralExpr(2), LiteralExpr(3))`)
    assert.equal(expr("if (1):\n  2"), term`IfExpr(LiteralExpr(1), LiteralExpr(2), null)`)


def test_EscapeExpr(assert):
    assert.equal(expr("escape e {1} catch p {2}"),
        term`EscapeExpr(FinalPattern(NounExpr("e"), null), LiteralExpr(1), FinalPattern(NounExpr("p"), null), LiteralExpr(2))`)
    assert.equal(expr("escape e {1}"),
        term`EscapeExpr(FinalPattern(NounExpr("e"), null), LiteralExpr(1), null, null)`)
    assert.equal(expr("escape e:\n  1\ncatch p:\n  2"),
        term`EscapeExpr(FinalPattern(NounExpr("e"), null), LiteralExpr(1), FinalPattern(NounExpr("p"), null), LiteralExpr(2))`)
    assert.equal(expr("escape e:\n  1"),
        term`EscapeExpr(FinalPattern(NounExpr("e"), null), LiteralExpr(1), null, null)`)

def test_ForExpr(assert):
    assert.equal(expr("for v in foo {1}"), term`ForExpr(NounExpr("foo"), null, FinalPattern(NounExpr("v"), null), LiteralExpr(1), null, null)`)
    assert.equal(expr("for k => v in foo {1}"), term`ForExpr(NounExpr("foo"), FinalPattern(NounExpr("k"), null), FinalPattern(NounExpr("v"), null), LiteralExpr(1), null, null)`)
    assert.equal(expr("for k => v in foo {1} catch p {2}"), term`ForExpr(NounExpr("foo"), FinalPattern(NounExpr("k"), null), FinalPattern(NounExpr("v"), null), LiteralExpr(1), FinalPattern(NounExpr("p"), null), LiteralExpr(2))`)
    assert.equal(expr("for v in foo:\n  1"), term`ForExpr(NounExpr("foo"), null, FinalPattern(NounExpr("v"), null), LiteralExpr(1), null, null)`)
    assert.equal(expr("for k => v in foo:\n  1"), term`ForExpr(NounExpr("foo"), FinalPattern(NounExpr("k"), null), FinalPattern(NounExpr("v"), null), LiteralExpr(1), null, null)`)
    assert.equal(expr("for k => v in foo:\n  1\ncatch p:\n  2"), term`ForExpr(NounExpr("foo"), FinalPattern(NounExpr("k"), null), FinalPattern(NounExpr("v"), null), LiteralExpr(1), FinalPattern(NounExpr("p"), null), LiteralExpr(2))`)


def test_FunctionExpr(assert):
    assert.equal(expr("fn {1}"), term`FunctionExpr([], LiteralExpr(1))`)
    assert.equal(expr("fn a, b {1}"), term`FunctionExpr([FinalPattern(NounExpr("a"), null), FinalPattern(NounExpr("b"), null)], LiteralExpr(1))`)

def test_SwitchExpr(assert):
    assert.equal(expr("switch (1) {match p {2} match q {3}}"), term`SwitchExpr(LiteralExpr(1), [Matcher(FinalPattern(NounExpr("p"), null), LiteralExpr(2)), Matcher(FinalPattern(NounExpr("q"), null), LiteralExpr(3))])`)
    assert.equal(expr("switch (1):\n  match p:\n    2\n  match q:\n    3"), term`SwitchExpr(LiteralExpr(1), [Matcher(FinalPattern(NounExpr("p"), null), LiteralExpr(2)), Matcher(FinalPattern(NounExpr("q"), null), LiteralExpr(3))])`)

def test_TryExpr(assert):
    assert.equal(expr("try {1} catch p {2} catch q {3} finally {4}"),
        term`TryExpr(LiteralExpr(1), [Catcher(FinalPattern(NounExpr("p"), null), LiteralExpr(2)), Catcher(FinalPattern(NounExpr("q"), null), LiteralExpr(3))], LiteralExpr(4))`)
    assert.equal(expr("try {1} finally {2}"),
        term`TryExpr(LiteralExpr(1), [], LiteralExpr(2))`)
    assert.equal(expr("try {1} catch p {2}"),
        term`TryExpr(LiteralExpr(1), [Catcher(FinalPattern(NounExpr("p"), null), LiteralExpr(2))], null)`)
    assert.equal(expr("try:\n  1\ncatch p:\n  2\ncatch q:\n  3\nfinally:\n  4"),
        term`TryExpr(LiteralExpr(1), [Catcher(FinalPattern(NounExpr("p"), null), LiteralExpr(2)), Catcher(FinalPattern(NounExpr("q"), null), LiteralExpr(3))], LiteralExpr(4))`)
    assert.equal(expr("try:\n  1\nfinally:\n  2"),
        term`TryExpr(LiteralExpr(1), [], LiteralExpr(2))`)
    assert.equal(expr("try:\n  1\ncatch p:\n  2"),
        term`TryExpr(LiteralExpr(1), [Catcher(FinalPattern(NounExpr("p"), null), LiteralExpr(2))], null)`)

def test_WhileExpr(assert):
    assert.equal(expr("while (1):\n  2"), term`WhileExpr(LiteralExpr(1), LiteralExpr(2), null)`)
    assert.equal(expr("while (1):\n  2\ncatch p:\n  3"), term`WhileExpr(LiteralExpr(1), LiteralExpr(2), Catcher(FinalPattern(NounExpr("p"), null), LiteralExpr(3)))`)

def test_WhenExpr(assert):
    assert.equal(expr("when (1) -> {2}"), term`WhenExpr([LiteralExpr(1)], LiteralExpr(2), [], null)`)
    assert.equal(expr("when (1, 2) -> {3}"), term`WhenExpr([LiteralExpr(1), LiteralExpr(2)], LiteralExpr(3), [], null)`)
    assert.equal(expr("when (1) -> {2} catch p {3}"), term`WhenExpr([LiteralExpr(1)], LiteralExpr(2), [Catcher(FinalPattern(NounExpr("p"), null), LiteralExpr(3))], null)`)
    assert.equal(expr("when (1) -> {2} finally {3}"), term`WhenExpr([LiteralExpr(1)], LiteralExpr(2), [], LiteralExpr(3))`)
    assert.equal(expr("when (1) -> {2} catch p {3} finally {4}"), term`WhenExpr([LiteralExpr(1)], LiteralExpr(2), [Catcher(FinalPattern(NounExpr("p"), null), LiteralExpr(3))], LiteralExpr(4))`)
    assert.equal(expr("when (1) ->\n  2"), term`WhenExpr([LiteralExpr(1)], LiteralExpr(2), [], null)`)
    assert.equal(expr("when (1, 2) ->\n  3"), term`WhenExpr([LiteralExpr(1), LiteralExpr(2)], LiteralExpr(3), [], null)`)
    assert.equal(expr("when (1) ->\n  2\ncatch p:\n  3"), term`WhenExpr([LiteralExpr(1)], LiteralExpr(2), [Catcher(FinalPattern(NounExpr("p"), null), LiteralExpr(3))], null)`)
    assert.equal(expr("when (1) ->\n  2\nfinally:\n  3"), term`WhenExpr([LiteralExpr(1)], LiteralExpr(2), [], LiteralExpr(3))`)
    assert.equal(expr("when (1) ->\n  2\ncatch p:\n  3\nfinally:\n  4"), term`WhenExpr([LiteralExpr(1)], LiteralExpr(2), [Catcher(FinalPattern(NounExpr("p"), null), LiteralExpr(3))], LiteralExpr(4))`)

def test_ObjectExpr(assert):
    assert.equal(expr("object foo {}"), term`ObjectExpr(null, FinalPattern(NounExpr("foo"), null), null, [], Script(null, [], []))`)
    assert.equal(expr("object _ {}"), term`ObjectExpr(null, IgnorePattern(null), null, [], Script(null, [], []))`)
    assert.equal(expr("object ::\"object\" {}"), term`ObjectExpr(null, FinalPattern(NounExpr("object"), null), null, [], Script(null, [], []))`)
    assert.equal(expr("bind foo {}"), term`ObjectExpr(null, BindPattern(NounExpr("foo")), null, [], Script(null, [], []))`)
    assert.equal(expr("object bind foo {}"), term`ObjectExpr(null, BindPattern(NounExpr("foo")), null, [], Script(null, [], []))`)
    assert.equal(expr("object foo { to doA(x, y) :z {0} method blee() {1} to \"object\"() {2} match p {3} match q {4}}"),
        term`ObjectExpr(null, FinalPattern(NounExpr("foo"), null), null, [], Script(null, [To(null, "doA", [FinalPattern(NounExpr("x"), null), FinalPattern(NounExpr("y"), null)], NounExpr("z"), LiteralExpr(0)), Method(null, "blee", [], null, LiteralExpr(1)), To(null, "object", [], null, LiteralExpr(2))], [Matcher(FinalPattern(NounExpr("p"), null), LiteralExpr(3)), Matcher(FinalPattern(NounExpr("q"), null), LiteralExpr(4))]))`)
    assert.equal(expr("object foo {\"hello\" to blee() {\"yes\"\n1}}"), term`ObjectExpr("hello", FinalPattern(NounExpr("foo"), null), null, [], Script(null, [To("yes", "blee", [], null, LiteralExpr(1))], []))`)
    assert.equal(expr("object foo as A implements B, C {}"), term`ObjectExpr(null, FinalPattern(NounExpr("foo"), null), NounExpr("A"), [NounExpr("B"), NounExpr("C")], Script(null, [], []))`)
    assert.equal(expr("object foo extends baz {}"), term`ObjectExpr(null, FinalPattern(NounExpr("foo"), null), null, [], Script(NounExpr("baz"), [], []))`)

    assert.equal(expr("object foo:\n  pass"), term`ObjectExpr(null, FinalPattern(NounExpr("foo"), null), null, [], Script(null, [], []))`)
    assert.equal(expr("object _:\n  pass"), term`ObjectExpr(null, IgnorePattern(null), null, [], Script(null, [], []))`)
    assert.equal(expr("object ::\"object\":\n  pass"), term`ObjectExpr(null, FinalPattern(NounExpr("object"), null), null, [], Script(null, [], []))`)
    assert.equal(expr("bind foo:\n  pass"), term`ObjectExpr(null, BindPattern(NounExpr("foo")), null, [], Script(null, [], []))`)
    assert.equal(expr("object bind foo:\n  pass"), term`ObjectExpr(null, BindPattern(NounExpr("foo")), null, [], Script(null, [], []))`)
    assert.equal(expr("object foo:\n  to doA(x, y) :z:\n    0\n  method blee():\n    1\n  to \"object\"():\n    2\n  match p:\n    3\n  match q:\n    4"),
        term`ObjectExpr(null, FinalPattern(NounExpr("foo"), null), null, [], Script(null, [To(null, "doA", [FinalPattern(NounExpr("x"), null), FinalPattern(NounExpr("y"), null)], NounExpr("z"), LiteralExpr(0)), Method(null, "blee", [], null, LiteralExpr(1)), To(null, "object", [], null, LiteralExpr(2))], [Matcher(FinalPattern(NounExpr("p"), null), LiteralExpr(3)), Matcher(FinalPattern(NounExpr("q"), null), LiteralExpr(4))]))`)
    assert.equal(expr("object foo:\n  \"hello\"\n  to blee():\n    \"yes\"\n    1"), term`ObjectExpr("hello", FinalPattern(NounExpr("foo"), null), null, [], Script(null, [To("yes", "blee", [], null, LiteralExpr(1))], []))`)
    assert.equal(expr("object foo as A implements B, C:\n  pass"), term`ObjectExpr(null, FinalPattern(NounExpr("foo"), null), NounExpr("A"), [NounExpr("B"), NounExpr("C")], Script(null, [], []))`)
    assert.equal(expr("object foo extends baz:\n  pass"), term`ObjectExpr(null, FinalPattern(NounExpr("foo"), null), null, [], Script(NounExpr("baz"), [], []))`)

def test_Function(assert):
    assert.equal(expr("def foo() {1}"), term`ObjectExpr(null, FinalPattern(NounExpr("foo"), null), null, [], FunctionScript([], null, LiteralExpr(1)))`)
    assert.equal(expr("def foo(a, b) :c {1}"), term`ObjectExpr(null, FinalPattern(NounExpr("foo"), null), null, [], FunctionScript([FinalPattern(NounExpr("a"), null), FinalPattern(NounExpr("b"), null)], NounExpr("c"), LiteralExpr(1)))`)
    assert.equal(expr("def foo():\n  1"), term`ObjectExpr(null, FinalPattern(NounExpr("foo"), null), null, [], FunctionScript([], null, LiteralExpr(1)))`)
    assert.equal(expr("def foo(a, b) :c:\n  1"), term`ObjectExpr(null, FinalPattern(NounExpr("foo"), null), null, [], FunctionScript([FinalPattern(NounExpr("a"), null), FinalPattern(NounExpr("b"), null)], NounExpr("c"), LiteralExpr(1)))`)

def test_Interface(assert):
    assert.equal(expr("interface foo {\"yes\"}"), term`InterfaceExpr("yes", FinalPattern(NounExpr("foo"), null), null, [], [], [])`)
    assert.equal(expr("interface foo extends baz, blee {\"yes\"}"), term`InterfaceExpr("yes", FinalPattern(NounExpr("foo"), null), null, [NounExpr("baz"), NounExpr("blee")], [], [])`)
    assert.equal(expr("interface foo implements bar {\"yes\"}"), term`InterfaceExpr("yes", FinalPattern(NounExpr("foo"), null), null, [], [NounExpr("bar")], [])`)
    assert.equal(expr("interface foo extends baz implements boz, bar {}"), term`InterfaceExpr(null, FinalPattern(NounExpr("foo"), null), null, [NounExpr("baz")], [NounExpr("boz"), NounExpr("bar")], [])`)
    assert.equal(expr("interface foo guards FooStamp extends boz, biz implements bar {}"), term`InterfaceExpr(null, FinalPattern(NounExpr("foo"), null), FinalPattern(NounExpr("FooStamp"), null), [NounExpr("boz"), NounExpr("biz")], [NounExpr("bar")], [])`)
    assert.equal(expr("interface foo {\"yes\"\nto run(a :int, b :float64) :any}"), term`InterfaceExpr("yes", FinalPattern(NounExpr("foo"), null), null, [], [], [MessageDesc(null, "run", [ParamDesc("a", NounExpr("int")), ParamDesc("b", NounExpr("float64"))], NounExpr("any"))])`)
    assert.equal(expr("interface foo {\"yes\"\nto run(a :int, b :float64) :any {\"msg docstring\"}}"), term`InterfaceExpr("yes", FinalPattern(NounExpr("foo"), null), null, [], [], [MessageDesc("msg docstring", "run", [ParamDesc("a", NounExpr("int")), ParamDesc("b", NounExpr("float64"))], NounExpr("any"))])`)
    assert.equal(expr("interface foo(a :int, b :float64) :any {\"msg docstring\"}"), term`FunctionInterfaceExpr("msg docstring", FinalPattern(NounExpr("foo"), null), null, [], [], MessageDesc("msg docstring", "run", [ParamDesc("a", NounExpr("int")), ParamDesc("b", NounExpr("float64"))], NounExpr("any")))`)
    assert.equal(expr("interface foo(a :int, b :float64) :any"), term`FunctionInterfaceExpr(null, FinalPattern(NounExpr("foo"), null), null, [], [], MessageDesc(null, "run", [ParamDesc("a", NounExpr("int")), ParamDesc("b", NounExpr("float64"))], NounExpr("any")))`)

    assert.equal(expr("interface foo:\n  \"yes\""), term`InterfaceExpr("yes", FinalPattern(NounExpr("foo"), null), null, [], [], [])`)
    assert.equal(expr("interface foo extends baz, blee:\n  \"yes\""), term`InterfaceExpr("yes", FinalPattern(NounExpr("foo"), null), null, [NounExpr("baz"), NounExpr("blee")], [], [])`)
    assert.equal(expr("interface foo implements bar:\n  \"yes\""), term`InterfaceExpr("yes", FinalPattern(NounExpr("foo"), null), null, [], [NounExpr("bar")], [])`)
    assert.equal(expr("interface foo extends baz implements boz, bar:\n  pass"), term`InterfaceExpr(null, FinalPattern(NounExpr("foo"), null), null, [NounExpr("baz")], [NounExpr("boz"), NounExpr("bar")], [])`)
    assert.equal(expr("interface foo guards FooStamp extends boz, biz implements bar:\n  pass"), term`InterfaceExpr(null, FinalPattern(NounExpr("foo"), null), FinalPattern(NounExpr("FooStamp"), null), [NounExpr("boz"), NounExpr("biz")], [NounExpr("bar")], [])`)
    assert.equal(expr("interface foo:\n  \"yes\"\n  to run(a :int, b :float64) :any"), term`InterfaceExpr("yes", FinalPattern(NounExpr("foo"), null), null, [], [], [MessageDesc(null, "run", [ParamDesc("a", NounExpr("int")), ParamDesc("b", NounExpr("float64"))], NounExpr("any"))])`)
    assert.equal(expr("interface foo:\n  \"yes\"\n  to run(a :int, b :float64) :any:\n    \"msg docstring\""), term`InterfaceExpr("yes", FinalPattern(NounExpr("foo"), null), null, [], [], [MessageDesc("msg docstring", "run", [ParamDesc("a", NounExpr("int")), ParamDesc("b", NounExpr("float64"))], NounExpr("any"))])`)
    assert.equal(expr("interface foo(a :int, b :float64) :any:\n  \"msg docstring\""), term`FunctionInterfaceExpr("msg docstring", FinalPattern(NounExpr("foo"), null), null, [], [], MessageDesc("msg docstring", "run", [ParamDesc("a", NounExpr("int")), ParamDesc("b", NounExpr("float64"))], NounExpr("any")))`)

def test_Call(assert):
    assert.equal(expr("a.b(c, d)"), term`MethodCallExpr(NounExpr("a"), "b", [NounExpr("c"), NounExpr("d")])`)
    assert.equal(expr("a.b()"), term`MethodCallExpr(NounExpr("a"), "b", [])`)
    assert.equal(expr("a.b"), term`CurryExpr(NounExpr("a"), "b", false)`)
    assert.equal(expr("a.b().c()"), term`MethodCallExpr(MethodCallExpr(NounExpr("a"), "b", []), "c", [])`)
    assert.equal(expr("a.\"if\"()"), term`MethodCallExpr(NounExpr("a"), "if", [])`)
    assert.equal(expr("a(b, c)"), term`FunCallExpr(NounExpr("a"), [NounExpr("b"), NounExpr("c")])`)

def test_Send(assert):
    assert.equal(expr("a <- b(c, d)"), term`SendExpr(NounExpr("a"), "b", [NounExpr("c"), NounExpr("d")])`)
    assert.equal(expr("a <- b()"), term`SendExpr(NounExpr("a"), "b", [])`)
    assert.equal(expr("a <- b"), term`CurryExpr(NounExpr("a"), "b", true)`)
    assert.equal(expr("a <- b() <- c()"), term`SendExpr(SendExpr(NounExpr("a"), "b", []), "c", [])`)
    assert.equal(expr("a <- \"if\"()"), term`SendExpr(NounExpr("a"), "if", [])`)
    assert.equal(expr("a <- (b, c)"), term`FunSendExpr(NounExpr("a"), [NounExpr("b"), NounExpr("c")])`)

def test_Get(assert):
    assert.equal(expr("a[b, c]"), term`GetExpr(NounExpr("a"), [NounExpr("b"), NounExpr("c")])`)
    assert.equal(expr("a[]"), term`GetExpr(NounExpr("a"), [])`)
    assert.equal(expr("a.b()[c].d()"), term`MethodCallExpr(GetExpr(MethodCallExpr(NounExpr("a"), "b", []), [NounExpr("c")]), "d", [])`)

def test_Meta(assert):
    assert.equal(expr("meta.context()"), term`MetaContextExpr()`)
    assert.equal(expr("meta.getState()"), term`MetaStateExpr()`)

def test_Def(assert):
    assert.equal(expr("def a := b"), term`DefExpr(FinalPattern(NounExpr("a"), null), null, NounExpr("b"))`)
    assert.equal(expr("def a exit b := c"), term`DefExpr(FinalPattern(NounExpr("a"), null), NounExpr("b"), NounExpr("c"))`)
    assert.equal(expr("var a := b"), term`DefExpr(VarPattern(NounExpr("a"), null), null, NounExpr("b"))`)
    assert.equal(expr("bind a := b"), term`DefExpr(BindPattern(NounExpr("a")), null, NounExpr("b"))`)

def test_Assign(assert):
    assert.equal(expr("a := b"), term`AssignExpr(NounExpr("a"), NounExpr("b"))`)
    assert.equal(expr("a[b] := c"), term`AssignExpr(GetExpr(NounExpr("a"), [NounExpr("b")]), NounExpr("c"))`)
    assert.equal(expr("a foo= (b)"), term`VerbAssignExpr("foo", NounExpr("a"), [NounExpr("b")])`)
    assert.equal(expr("a += b"), term`AugAssignExpr("+", NounExpr("a"), NounExpr("b"))`)

def test_Prefix(assert):
    assert.equal(expr("-3"), term`PrefixExpr("-", LiteralExpr(3))`)
    assert.equal(expr("!foo.baz()"), term`PrefixExpr("!", MethodCallExpr(NounExpr("foo"), "baz", []))`)
    assert.equal(expr("~foo.baz()"), term`PrefixExpr("~", MethodCallExpr(NounExpr("foo"), "baz", []))`)
    assert.equal(expr("&&foo"), term`BindingExpr(NounExpr("foo"))`)
    assert.equal(expr("&foo"), term`SlotExpr(NounExpr("foo"))`)

def test_Coerce(assert):
    assert.equal(expr("foo :baz"), term`CoerceExpr(NounExpr("foo"), NounExpr("baz"))`)

def test_Infix(assert):
    assert.equal(expr("x ** -y"), term`BinaryExpr(NounExpr("x"), "**", PrefixExpr("-", NounExpr("y")))`)
    assert.equal(expr("x * y"), term`BinaryExpr(NounExpr("x"), "*", NounExpr("y"))`)
    assert.equal(expr("x / y"), term`BinaryExpr(NounExpr("x"), "/", NounExpr("y"))`)
    assert.equal(expr("x // y"), term`BinaryExpr(NounExpr("x"), "//", NounExpr("y"))`)
    assert.equal(expr("x % y"), term`BinaryExpr(NounExpr("x"), "%", NounExpr("y"))`)
    assert.equal(expr("x + y"), term`BinaryExpr(NounExpr("x"), "+", NounExpr("y"))`)
    assert.equal(expr("(x + y) + z"), term`BinaryExpr(BinaryExpr(NounExpr("x"), "+", NounExpr("y")), "+", NounExpr("z"))`)
    assert.equal(expr("x - y"), term`BinaryExpr(NounExpr("x"), "-", NounExpr("y"))`)
    assert.equal(expr("x - y + z"), term`BinaryExpr(BinaryExpr(NounExpr("x"), "-", NounExpr("y")), "+", NounExpr("z"))`)
    assert.equal(expr("x..y"), term`RangeExpr(NounExpr("x"), "..", NounExpr("y"))`)
    assert.equal(expr("x..!y"), term`RangeExpr(NounExpr("x"), "..!", NounExpr("y"))`)
    assert.equal(expr("x < y"), term`CompareExpr(NounExpr("x"), "<", NounExpr("y"))`)
    assert.equal(expr("x <= y"), term`CompareExpr(NounExpr("x"), "<=", NounExpr("y"))`)
    assert.equal(expr("x <=> y"), term`CompareExpr(NounExpr("x"), "<=>", NounExpr("y"))`)
    assert.equal(expr("x >= y"), term`CompareExpr(NounExpr("x"), ">=", NounExpr("y"))`)
    assert.equal(expr("x > y"), term`CompareExpr(NounExpr("x"), ">", NounExpr("y"))`)
    assert.equal(expr("x << y"), term`BinaryExpr(NounExpr("x"), "<<", NounExpr("y"))`)
    assert.equal(expr("x >> y"), term`BinaryExpr(NounExpr("x"), ">>", NounExpr("y"))`)
    assert.equal(expr("x << y >> z"), term`BinaryExpr(BinaryExpr(NounExpr("x"), "<<", NounExpr("y")), ">>", NounExpr("z"))`)
    assert.equal(expr("x == y"), term`SameExpr(NounExpr("x"), NounExpr("y"), true)`)
    assert.equal(expr("x != y"), term`SameExpr(NounExpr("x"), NounExpr("y"), false)`)
    assert.equal(expr("x &! y"), term`BinaryExpr(NounExpr("x"), "&!", NounExpr("y"))`)
    assert.equal(expr("x ^ y"), term`BinaryExpr(NounExpr("x"), "^", NounExpr("y"))`)
    assert.equal(expr("x & y"), term`BinaryExpr(NounExpr("x"), "&", NounExpr("y"))`)
    assert.equal(expr("x & y & z"), term`BinaryExpr(BinaryExpr(NounExpr("x"), "&", NounExpr("y")), "&", NounExpr("z"))`)
    assert.equal(expr("x | y"), term`BinaryExpr(NounExpr("x"), "|", NounExpr("y"))`)
    assert.equal(expr("x | y | z"), term`BinaryExpr(BinaryExpr(NounExpr("x"), "|", NounExpr("y")), "|", NounExpr("z"))`)
    assert.equal(expr("x && y"), term`AndExpr(NounExpr("x"), NounExpr("y"))`)
    assert.equal(expr("x && y && z"), term`AndExpr(NounExpr("x"), AndExpr(NounExpr("y"), NounExpr("z")))`)
    assert.equal(expr("x || y"), term`OrExpr(NounExpr("x"), NounExpr("y"))`)
    assert.equal(expr("x || y || z"), term`OrExpr(NounExpr("x"), OrExpr(NounExpr("y"), NounExpr("z")))`)
    assert.equal(expr("x =~ y"), term`MatchBindExpr(NounExpr("x"), FinalPattern(NounExpr("y"), null))`)
    assert.equal(expr("x && y || z"),  expr("(x && y) || z"))
    assert.equal(expr("x || y && z"),  expr("x || (y && z)"))
    assert.equal(expr("x =~ a || y == b && z != c"),
                     expr("(x =~ a) || ((y == b) && (z != c))"))
    assert.equal(expr("x | y > z"),  expr("x | (y > z)"))
    assert.equal(expr("x < y | y > z"),  expr("(x < y) | (y > z)"))
    assert.equal(expr("x & y > z"),  expr("x & (y > z)"))
    assert.equal(expr("x < y & y > z"),  expr("(x < y) & (y > z)"))
    assert.equal(expr("x..y <=> a..!b"),  expr("(x..y) <=> (a..!b)"))
    assert.equal(expr("a << b..y >> z"),  expr("(a << b) .. (y >> z)"))
    assert.equal(expr("x.y() :List[Int] > a..!b"),
                 expr("(x.y() :List[Int]) > a..!b"))
    assert.equal(expr("a + b >> z"),  expr("(a + b) >> z"))
    assert.equal(expr("a >> b + z"),  expr("a >> (b + z)"))
    assert.equal(expr("a + b * c"), expr("a + (b * c)"))
    assert.equal(expr("a - b + c * d"), expr("(a - b) + (c * d)"))
    assert.equal(expr("a / b + c - d"), expr("((a / b) + c) - d"))
    assert.equal(expr("a / b * !c ** ~d"), expr("(a / b) * ((!c) ** (~d))"))

def test_Exits(assert):
    assert.equal(expr("return x + y"), term`ExitExpr("return", BinaryExpr(NounExpr("x"), "+", NounExpr("y")))`)
    assert.equal(expr("continue x + y"), term`ExitExpr("continue", BinaryExpr(NounExpr("x"), "+", NounExpr("y")))`)
    assert.equal(expr("break x + y"), term`ExitExpr("break", BinaryExpr(NounExpr("x"), "+", NounExpr("y")))`)
    assert.equal(expr("return(x + y)"), term`ExitExpr("return", BinaryExpr(NounExpr("x"), "+", NounExpr("y")))`)
    assert.equal(expr("continue(x + y)"), term`ExitExpr("continue", BinaryExpr(NounExpr("x"), "+", NounExpr("y")))`)
    assert.equal(expr("break(x + y)"), term`ExitExpr("break", BinaryExpr(NounExpr("x"), "+", NounExpr("y")))`)
    assert.equal(expr("return()"), term`ExitExpr("return", null)`)
    assert.equal(expr("continue()"), term`ExitExpr("continue", null)`)
    assert.equal(expr("break()"), term`ExitExpr("break", null)`)
    assert.equal(expr("return"), term`ExitExpr("return", null)`)
    assert.equal(expr("continue"), term`ExitExpr("continue", null)`)
    assert.equal(expr("break"), term`ExitExpr("break", null)`)

def test_IgnorePattern(assert):
    assert.equal(pattern("_"), term`IgnorePattern(null)`)
    assert.equal(pattern("_ :Int"), term`IgnorePattern(NounExpr("Int"))`)
    assert.equal(pattern("_ :(1)"), term`IgnorePattern(LiteralExpr(1))`)

def test_FinalPattern(assert):
    assert.equal(pattern("foo"), term`FinalPattern(NounExpr("foo"), null)`)
    assert.equal(pattern("foo :Int"), term`FinalPattern(NounExpr("foo"), NounExpr("Int"))`)
    assert.equal(pattern("foo :(1)"), term`FinalPattern(NounExpr("foo"), LiteralExpr(1))`)
    assert.equal(pattern("::\"foo baz\""), term`FinalPattern(NounExpr("foo baz"), null)`)
    assert.equal(pattern("::\"foo baz\" :Int"), term`FinalPattern(NounExpr("foo baz"), NounExpr("Int"))`)
    assert.equal(pattern("::\"foo baz\" :(1)"), term`FinalPattern(NounExpr("foo baz"), LiteralExpr(1))`)

def test_SlotPattern(assert):
    assert.equal(pattern("&foo"), term`SlotPattern(NounExpr("foo"), null)`)
    assert.equal(pattern("&foo :Int"), term`SlotPattern(NounExpr("foo"), NounExpr("Int"))`)
    assert.equal(pattern("&foo :(1)"), term`SlotPattern(NounExpr("foo"), LiteralExpr(1))`)
    assert.equal(pattern("&::\"foo baz\""), term`SlotPattern(NounExpr("foo baz"), null)`)
    assert.equal(pattern("&::\"foo baz\" :Int"), term`SlotPattern(NounExpr("foo baz"), NounExpr("Int"))`)
    assert.equal(pattern("&::\"foo baz\" :(1)"), term`SlotPattern(NounExpr("foo baz"), LiteralExpr(1))`)

def test_VarPattern(assert):
    assert.equal(pattern("var foo"), term`VarPattern(NounExpr("foo"), null)`)
    assert.equal(pattern("var foo :Int"), term`VarPattern(NounExpr("foo"), NounExpr("Int"))`)
    assert.equal(pattern("var foo :(1)"), term`VarPattern(NounExpr("foo"), LiteralExpr(1))`)
    assert.equal(pattern("var ::\"foo baz\""), term`VarPattern(NounExpr("foo baz"), null)`)
    assert.equal(pattern("var ::\"foo baz\" :Int"), term`VarPattern(NounExpr("foo baz"), NounExpr("Int"))`)
    assert.equal(pattern("var ::\"foo baz\" :(1)"), term`VarPattern(NounExpr("foo baz"), LiteralExpr(1))`)

def test_BindPattern(assert):
    assert.equal(pattern("bind foo"), term`BindPattern(NounExpr("foo"))`)
    assert.equal(pattern("bind ::\"foo baz\""), term`BindPattern(NounExpr("foo baz"))`)

def test_BindingPattern(assert):
    assert.equal(pattern("&&foo"), term`BindingPattern(NounExpr("foo"))`)
    assert.equal(pattern("&&::\"foo baz\""), term`BindingPattern(NounExpr("foo baz"))`)

def test_SamePattern(assert):
    assert.equal(pattern("==1"), term`SamePattern(LiteralExpr(1), true)`)
    assert.equal(pattern("==(x)"), term`SamePattern(NounExpr("x"), true)`)

def test_NotSamePattern(assert):
    assert.equal(pattern("!=1"), term`SamePattern(LiteralExpr(1), false)`)
    assert.equal(pattern("!=(x)"), term`SamePattern(NounExpr("x"), false)`)

def test_ViaPattern(assert):
    assert.equal(pattern("via (b) a"), term`ViaPattern(NounExpr("b"), FinalPattern(NounExpr("a"), null))`)

def test_ListPattern(assert):
    assert.equal(pattern("[]"), term`ListPattern([], null)`)
    assert.equal(pattern("[a, b]"), term`ListPattern([FinalPattern(NounExpr("a"), null), FinalPattern(NounExpr("b"), null)], null)`)
    assert.equal(pattern("[a, b] + c"), term`ListPattern([FinalPattern(NounExpr("a"), null), FinalPattern(NounExpr("b"), null)], FinalPattern(NounExpr("c"), null))`)

def test_MapPattern(assert):
     assert.equal(pattern("[\"k\" => v, (a) => b, => c]"), term`MapPattern([MapPatternRequired(MapPatternAssoc(LiteralExpr("k"), FinalPattern(NounExpr("v"), null))), MapPatternRequired(MapPatternAssoc(NounExpr("a"), FinalPattern(NounExpr("b"), null))), MapPatternRequired(MapPatternImport(FinalPattern(NounExpr("c"), null)))], null)`)
     assert.equal(pattern("[\"a\" => b := 1] | c"), term`MapPattern([MapPatternDefault(MapPatternAssoc(LiteralExpr("a"), FinalPattern(NounExpr("b"), null)), LiteralExpr(1))], FinalPattern(NounExpr("c"), null))`)
     assert.equal(pattern("[\"k\" => &v, => &&b, => ::\"if\"]"), term`MapPattern([MapPatternRequired(MapPatternAssoc(LiteralExpr("k"), SlotPattern(NounExpr("v"), null))), MapPatternRequired(MapPatternImport(BindingPattern(NounExpr("b")))), MapPatternRequired(MapPatternImport(FinalPattern(NounExpr("if"), null)))], null)`)

def test_QuasiliteralPattern(assert):
    assert.equal(pattern("`foo`"), term`QuasiParserPattern(null, [QuasiText("foo")])`)
    assert.equal(pattern("bob`foo`"), term`QuasiParserPattern("bob", [QuasiText("foo")])`)
    assert.equal(pattern("bob`foo`` $x baz`"), term`QuasiParserPattern("bob", [QuasiText("foo`` "), QuasiExprHole(NounExpr("x")), QuasiText(" baz")])`)
    assert.equal(pattern("`($x)`"), term`QuasiParserPattern(null, [QuasiText("("), QuasiExprHole(NounExpr("x")), QuasiText(")")])`)
    assert.equal(pattern("`foo @{w}@x $y${z} baz`"), term`QuasiParserPattern(null, [QuasiText("foo "), QuasiPatternHole(FinalPattern(NounExpr("w"), null)), QuasiPatternHole(FinalPattern(NounExpr("x"), null)), QuasiText(" "), QuasiExprHole(NounExpr("y")), QuasiExprHole(NounExpr("z")), QuasiText(" baz")])`)

def test_SuchThatPattern(assert):
    assert.equal(pattern("x :y ? (1)"), term`SuchThatPattern(FinalPattern(NounExpr("x"), NounExpr("y")), LiteralExpr(1))`)


# def test_holes(assert):
#     assert.equal(quasiMonteParser.valueMaker(["foo(", quasiMonteParser.valueHole(0), ")"]), term`ValueHoleExpr(0)`)
#     assert.equal(expr("@{2}"), term`PatternHoleExpr(2)`)
#     assert.equal(pattern("${2}"), term`ValueHoleExpr(0)`)
#     assert.equal(pattern("@{2}"), term`PatternHoleExpr(0)`)
unittest([test_Literal, test_Noun, test_QuasiliteralExpr, test_Hide, test_Call, test_Send, test_Get, test_Meta, test_List, test_Map, test_ListComprehensionExpr, test_MapComprehensionExpr, test_IfExpr, test_EscapeExpr, test_ForExpr, test_FunctionExpr, test_SwitchExpr, test_TryExpr, test_WhileExpr, test_WhenExpr, test_ObjectExpr, test_Function, test_Interface, test_Def, test_Assign, test_Prefix, test_Coerce, test_Infix, test_Exits, test_IgnorePattern, test_FinalPattern, test_VarPattern, test_BindPattern, test_SamePattern, test_NotSamePattern, test_SlotPattern, test_BindingPattern, test_ViaPattern, test_ListPattern, test_MapPattern, test_QuasiliteralPattern, test_SuchThatPattern])
