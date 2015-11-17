'''rr_happy -- generate haskell parser from railroad diagrams

TODO:
  1. lexical stuff
  2. grammar actions

'''

from sys import stderr  # poor-man's logging
from pprint import pformat

import railroad_diagrams as rrd


def gen_rule(name, body, expr):
    rules = expand(body, hint=name)

    yield ''
    yield '{-'
    yield name + ' ::= ' + expr
    yield '-}'

    def unCtor(name):
        # IntExpr -> intExpr
        return name[0].lower() + name[1:]

    def doRule(name, choices, indent='', ctor=None):
        if choices:
            firstSeq, rest = map(unCtor, choices[0]), choices[1:]

            if ctor:
                yield indent + '%s = %s <$> %s' % (
                    name, ctor, ' <*> '.join(firstSeq))
            else:
                yield indent + '%s = %s' % (name, ' '.join(firstSeq))
            for seq in rest:
                yield indent + '  <|> %s' % ' '.join(map(unCtor, seq))

    if rules:
        (_, choices), more = rules[0], rules[1:]

        for chunk in doRule(unCtor(name), choices,
                            ctor=name if name[0].isupper() else None):
            yield chunk
        if more:
            yield '  where'
            for name, choices in more:
                for chunk in doRule(unCtor(name), choices, indent='    '):
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
        # @@TODO: non-literal terminals
        return logged('terminal ' + hint + ' =>',
                      [('(tok "%s")' % expr.text, None)])
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
        thisRule = (hint, [[name
                            for rules in expanded
                            for (name, _) in [rules[0]]]])
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
