'''rr_happy -- generate haskell parser from railroad diagrams

TODO:
  1. lexical stuff
  2. grammar actions

'''

from sys import stderr  # poor-man's logging
from pprint import pformat

import railroad_diagrams as rrd

converted = ['prim',
             'LiteralExpr', 'NounExpr', 'HideExpr',
             'MapExpr', 'MapComprehensionExpr',
             'ListExpr', 'ListComprehensionExpr']


def gen_rule(name, body, expr):
    if name not in converted:
        return

    yield ''
    yield '{-'
    yield name + ' ::= ' + expr
    yield '-}'

    def unCtor(name):
        # IntExpr -> intExpr
        return name[0].lower() + name[1:]

    def fmtRule(items, lhs=None, ctor=None):
        pfx, sep = ((ctor + ' <$>', ' <*> ') if ctor
                    else ('', ' '))
        rhs = sep.join(items)
        rhs = rhs.replace('*> <*>', '*>').replace('<*> <*', '<*')
        return (lhs + ' = ' if lhs else '  <|> ') + rhs

    def doRules(name, choices, indent='', ctor=None):
        if choices:
            firstSeq, rest = map(unCtor, choices[0]), choices[1:]

            yield indent + fmtRule(firstSeq, lhs=name, ctor=ctor)
            for seq in rest:
                yield indent + fmtRule(map(unCtor, seq), lhs='', ctor=ctor)

    rules = expand(body, hint=name)

    if rules:
        (_, choices), more = rules[0], rules[1:]

        for chunk in doRules(unCtor(name), choices,
                             ctor=(name
                                   if name[0].isupper()
                                   and name != 'LiteralExpr'
                                   else None)):
            yield chunk
        if more:
            yield '  where'
            for name, choices in more:
                for chunk in doRules(unCtor(name), choices, indent='    '):
                    yield chunk


def logged(label, val, logging=False):
    if logging:
        print >>stderr, '::', label, pformat(val)
    return val


def expand(expr, hint=''):
    '''Expand expression, if necessary, to further choice-of-sequences rules.
    '''

    def mkName():
        ix[0] += 1
        return '%s_%s' % (hint, ix[0])
    ix = [0]
    recur = lambda items: logged('recur',
                                 [expand(item, mkName())
                                  for item in items
                                  if not isinstance(item, rrd.Comment)])
    more = lambda first, rest: logged('more', (
        [first] +
        [(name, rule)
         for rules in rest
         for (name, rule) in rules if rule is not None]))

    logged("expr class of " + hint, expr.__class__.__name__)

    if isinstance(expr, rrd.Terminal):
        tag = expr.text
        p = ('parse{tag}'.format(tag=tag[1:-1]) if '.' in tag
             else '(tok "{tag}")'.format(tag=tag))

        return logged('terminal ' + hint + ' =>',
                      [(p, None)])

    elif isinstance(expr, rrd.NonTerminal):
        return logged('nonterminal ' + hint + ' =>', [(expr.text, None)])

    elif isinstance(expr, rrd.Skip):
        thisRule = (hint, [[]])  # One choice; no items in sequence
        return logged('Skip', [thisRule])

    elif isinstance(expr, rrd.Choice):
        expanded = recur(expr.items)
        thisRule = (hint, [[name]
                           for rules in expanded
                           for (name, _) in [rules[0]]])
        return more(thisRule, expanded)

    elif isinstance(expr, rrd.Sequence):
        expanded = recur(expr.items)
        choices = [[name
                    for rules in expanded
                    for (name, _) in [rules[0]]]]
        if isinstance(expr, rrd.Sigil):
            rhs = choices[0]
            rhs = [rhs[0] + ' *>'] + rhs[1:]
            choices = [rhs]
        elif isinstance(expr, rrd.Brackets):
            rhs = choices[0]
            rhs = ([rhs[0] + ' *>']
                   + rhs[1:-1] +
                   ['<* ' + rhs[-1]])
            choices = [rhs]

        thisRule = (hint, choices)

        return more(thisRule, expanded)

    elif isinstance(expr, rrd.OneOrMore):
        expanded = recur([expr.item])
        (item, _) = expanded[0][0]

        sep = []
        if expr.rep:
            expSep = recur([expr.rep])
            (s, _) = expSep[0][0]
            sep = [s]
            expanded = expanded + expSep

        # left recursion per 2.2. Parsing sequences in Using Happy
        # https://www.haskell.org/happy/doc/html/sec-sequences.html
        thisRule = (hint, [[item],
                           [hint] + sep + [item]])

        return more(thisRule, expanded)
    else:
        raise NotImplementedError(expr)


'''

Monte Syntax Builder
--------------------

stuff from `monte_parser.mt`:

AndExpr(lhs, rhs
AssignExpr(lval, assign(ej)
AugAssignExpr(op, lval, assign(ej)
BinaryExpr(lhs, opName, rhs
BindingExpr(noun(ej)
BindingExpr(noun(ej)
BindingPattern(n
BindPattern(n, g
BindPattern(n, null
Catcher(cp, cb
CatchExpr(n, cp, cb
CoerceExpr(base, guard(ej)
CompareExpr(lhs, opName, rhs
DefExpr(patt, ex, assign(ej)
DefExpr(patt, null, assign(ej)
EscapeExpr(p1, e1, null, null
EscapeExpr(p1, e1, p2, e2
ExitExpr(ex, null
ExitExpr(ex, val
FinallyExpr(n, finallyblock
FinalPattern(
FinalPattern(noun(ej), null
ForExpr(it, k, v, body, catchPattern, catchBody
ForwardExpr(name
FunctionExpr(patt, body
FunctionInterfaceExpr(doco, name, guards_, extends_, implements_,
FunctionScript(patts, namedPatts, resultguard, body, span), span)
GetExpr(n, g
HideExpr(e
IfExpr(test, consq, alt
IgnorePattern(g
IgnorePattern(null
InterfaceExpr(doco, name, guards_, extends_, implements_, msgs,
ListComprehensionExpr(it, filt, k, v, body,
ListExpr(items
ListPattern(items, tail
LiteralExpr(sub.getName(), null)
LiteralExpr("&" + sub.getNoun().getName(), null)
LiteralExpr("&&" + sub.getNoun().getName(), null)
LiteralExpr(t[1], t[2])
MapComprehensionExpr(it, filt, k, v, body, vbody,
MapExprAssoc, ej)
MapExpr(items
MapPatternImport, ej)
MapPattern(items, tail
MatchBindExpr(lhs, rhs
Matcher(pp, bl
MessageDesc(doco, "run", params, resultguard
MessageDesc(doco, verb, params, resultguard
MetaContextExpr(
MetaStateExpr(
"Method"
MismatchExpr(lhs, rhs
"Module"(importsList, exportsList, body,
NamedArg, ej)
NamedParamImport, ej)
NamedParam(null, p, null
NounExpr(t[1]
NounExpr(t[1], t[2])
ObjectExpr(doco, name, oAs, oImplements,
OrExpr(lhs, rhs
ParamDesc(name, g
PatternHoleExpr(advance(ej)[1]
PrefixExpr(op, call(ej)
PrefixExpr("-", prim(ej)
QuasiExprHole(
QuasiExprHole(subexpr
QuasiParserExpr(name, parts.snapshot()
QuasiParserPattern(name, parts.snapshot()
QuasiPatternHole(patt, t[2]))
QuasiPatternHole(subpatt
QuasiText(t[1], t[2]))
RangeExpr(lhs, opName, rhs
SameExpr(lhs, rhs, false
SameExpr(lhs, rhs, true
SamePattern(prim(ej), false
SamePattern(prim(ej), true
Script(oExtends, methods, matchers
SeqExpr([], advance(ej)[2])
SeqExpr(exprs.snapshot()
SeqExpr([], null)
SeqExpr([], null)
SlotExpr(noun(ej)
SlotExpr(noun(ej)
SlotPattern(n, g
SuchThatPattern(p, e
SwitchExpr(
"To"
ValueHoleExpr(advance(ej)[1]
ValueHoleExpr(advance(ej)[1]
ValueHolePattern(advance(ej)[1]
VarPattern(n, g
VerbAssignExpr(verb, lval, acceptList(expr),
ViaPattern(e, pattern(ej)
WhenExpr(exprs, whenblock, catchers.snapshot(),
WhileExpr(test, whileblock, catchblock
'''
