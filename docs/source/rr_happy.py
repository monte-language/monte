'''rr_happy -- generate haskell happy parser from railroad diagrams

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

    for name, choices in rules:
        if choices:
            firstSeq, rest = choices[0], choices[1:]
            yield '%s : %s' % (name, ' '.join(firstSeq))
            for seq in rest:
                yield '    | %s' % ' '.join(seq)


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
                      [("'%s'" % expr.text, None)])
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
