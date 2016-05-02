'''rr_grammar -- make grammar from railroad diagram info

..

Monte Grammar
=============

.. note:: Lexical details such as indented blocks are
          not captured in this grammar.

.. todo:: finish grammar productions marked @@.
          Meanwhile, see `monte_parser.mt`__ for details.

__ https://github.com/monte-language/typhon/blob/master/mast/lib/monte/monte_parser.mt

.. productionlist::
'''

from collections import deque
import json

import railroad_diagrams as rrd


def main(argrd, argwr):
    infp, outfp = argrd(1), argwr(2)

    syntax = json.load(infp)

    top = __doc__.split('..\n', 1)[1]
    outfp.write(top)

    for item in syntax:
        if not item:
            continue
        lhs = eval(item['expr'], rrd.__dict__)
        for chunk in to_prod(item['name'], lhs):
            outfp.write(chunk)


def to_prod(name, expr):
    yield '   {name}: '.format(name=name)
    if isinstance(expr, rrd.Choice):
        sep = ''
        for rhs in expr.items:
            yield sep
            for chunk in expand(rhs):
                yield chunk
            sep = '\n   : | '
    else:
        for chunk in expand(expr):
            yield chunk
    yield '\n'


def expand(expr):
    if isinstance(expr, rrd.Comment):
        # TODO: OneOf, NoneOf
        yield '/* {text} */ '.format(text=expr.text)
    elif isinstance(expr, rrd.Skip):
        yield '/* empty */'  # ??
    elif isinstance(expr, rrd.Terminal):
        yield ("""'"'""" if expr.text == '"'
               else expr.text if expr.text.isupper()
               else expr.text if expr.text.startswith('.')
               else '"{text}" '.format(text=expr.text))
    elif isinstance(expr, rrd.NonTerminal):
        yield '`{text}` '.format(text=expr.text)
    elif isinstance(expr, rrd.Choice):
        if (isinstance(expr, rrd.Maybe) or
            isinstance(expr, rrd.Optional)):
            yield '['
            for chunk in expand(expr.items[0]):
                yield chunk
            yield '] '
        elif isinstance(expr, rrd.Many):
            yield '('
            for chunk in expand(expr.items[0]):
                yield chunk
            yield ')+'
        else:
            sep = '('
            for child in expr.items:
                yield sep
                for chunk in expand(child):
                    yield chunk
                sep = ' | '
            yield ')'
    elif isinstance(expr, rrd.OneOrMore):
        yield '('
        for chunk in expand(expr.item):
            yield chunk
        yield ' '
        if not isinstance(expr.rep, rrd.Skip):
            for chunk in expand(expr.rep):
                yield chunk
        yield ')+ '

    elif isinstance(expr, rrd.Sequence):
        for child in expr.items:
            yield ' '
            for chunk in expand(child):
                yield chunk
    else:
        import pdb; pdb.set_trace()


GRAY, BLACK = 0, 1


def topological(graph):
    # ack: https://gist.github.com/kachayev/5910538
    order, enter, state = deque(), set(graph), {}

    def dfs(node):
        state[node] = GRAY
        for k in graph.get(node, ()):
            sk = state.get(k, None)
            if sk == GRAY:
                raise ValueError("cycle: %s" % k)
            if sk == BLACK:
                continue
            enter.discard(k)
            dfs(k)
        order.appendleft(node)
        state[node] = BLACK

    while enter:
        dfs(enter.pop())
    return order


def descendants(expr):
    roots = ['expr', 'pattern']

    def recur(items):
        return [descendant
                for child in items
                for descendant in descendants(child)]

    if (isinstance(expr, rrd.Comment) or
        isinstance(expr, rrd.Skip) or
        isinstance(expr, rrd.Terminal)):
        return []
    elif isinstance(expr, rrd.NonTerminal):
        return [] if expr.text in roots else [expr.text]
    elif (isinstance(expr, rrd.Choice) or
          isinstance(expr, rrd.Sequence)):
        return recur(expr.items)
    elif isinstance(expr, rrd.OneOrMore):
        return recur([expr.item, expr.rep])
    else:
        raise ValueError(expr)

if __name__ == '__main__':
    def _script():
        from sys import argv

        main(argrd=lambda n: open(argv[n]),
             argwr=lambda n: open(argv[n], "w"))

    _script()
