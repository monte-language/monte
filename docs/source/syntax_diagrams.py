'''syntax_diagrams.py -- generate railroad diagrams for Monte syntax

based on typhon/mast/lib/monte/monte_parser.mt
'''

from railroad_diagrams import (
    Diagram,
    Terminal, NonTerminal, Comment,
    Sequence, Choice,
    Skip, Optional, ZeroOrMore, OneOrMore)


diagrams = []


def add(name, diagram):
    diagrams.append((name, diagram))

add('block', Diagram(Sequence(
    "{",
    Choice(
        0,
        ZeroOrMore(
            Choice(
                0,
                NonTerminal('blockExpr'),
                NonTerminal('expr')),
            ";"),
        "pass"),
    "}")))

add('blockExpr', Diagram(Choice(
    0,
    NonTerminal('if'),
    NonTerminal('escape'),
    NonTerminal('for'),
    NonTerminal('fn'),
    NonTerminal('switch'),
    NonTerminal('try'),
    NonTerminal('while'),
    NonTerminal('when'),
    NonTerminal('bind'),
    NonTerminal('object'),
    NonTerminal('def'),
    NonTerminal('interface'),
    NonTerminal('meta'))))

add('if', Diagram(Sequence(
    "if", "(", NonTerminal('expr'), ")", NonTerminal('block'),
    Optional(Sequence("else", Choice(
        0, Sequence("if", Comment('blockExpr@@')),
        NonTerminal('block')))))))

add('escape', Diagram(Sequence(
    "escape", NonTerminal('pattern'),
    NonTerminal('blockCatch'))))

add('blockCatch', Diagram(Sequence(
    NonTerminal('block'),
    Optional(
        Sequence("catch", NonTerminal('pattern'),
                 NonTerminal('block'))))))

add('for', Diagram(Sequence(
    "for",
    NonTerminal('pattern'),
    Optional(Sequence("=>", NonTerminal('pattern'))),
    "in", NonTerminal('comp'),
    NonTerminal('blockCatch'))))

add('fn', Diagram(Sequence(
    "fn",
    ZeroOrMore(NonTerminal('pattern'), ','),
    NonTerminal('block'))))

matchers = lambda: OneOrMore(Sequence("match",
                                      NonTerminal('pattern'),
                                      NonTerminal('block')))
add('switch', Diagram(Sequence(
    "switch", "(", NonTerminal('expr'), ")",
    "{", matchers(), "}")))

add('try', Diagram(Sequence(
    "try", NonTerminal('block'), NonTerminal('catchers'))))

add('catchers', Diagram(Sequence(
    ZeroOrMore(Sequence("catch",
                        NonTerminal('pattern'),
                        NonTerminal('block'))),
    Optional(Sequence("finally", NonTerminal('block'))))))


add('while', Diagram(Sequence(
    "while", "(", NonTerminal('expr'), ")", NonTerminal('blockCatch'))))

add('when', Diagram(Sequence(
    "when",
    "(", OneOrMore(NonTerminal('expr'), ','), ")",
    "->", NonTerminal('block'),
    NonTerminal('catchers'))))

maybeGuard = lambda: Optional(NonTerminal('guard'))

add('bind', Diagram(Sequence(
    "bind",
    NonTerminal("noun"),
    maybeGuard(), Comment("objectExpr@@"))))

add('object', Diagram(Sequence(
    "object",
    Choice(0, Sequence("bind", NonTerminal('noun')),
           "_",
           NonTerminal("noun")),
    maybeGuard(), Comment("objectExpr@@"))))

add('objectExpr', Diagram(Sequence(
    Optional(Sequence('extends', NonTerminal('order'))),
    NonTerminal('auditors'),
    '{', ZeroOrMore(NonTerminal('objectScript'), ';'), '}')))

add('objectScript', Diagram(Sequence(
    Optional(NonTerminal('doco')),
    Choice(0, "pass", ZeroOrMore("@@meth")),
    Choice(0, "pass", ZeroOrMore("@@matchers")))))

add('doco', Diagram(Terminal('.String')))

add('def', Diagram(Sequence(
    "def",
    Choice(
        0,
        Sequence(
            Choice(
                0,
                Sequence("bind", NonTerminal("noun"), maybeGuard()),
                NonTerminal("noun")),
            Choice(0, Comment("objectFunction@@"), NonTerminal('assign'))),
        NonTerminal('assign')))))

add('interface', Diagram(Sequence(
    "interface",
    NonTerminal('namePattern'),
    Optional(Sequence("guards", NonTerminal('pattern'))),
    Optional(Sequence("extends", OneOrMore(NonTerminal('order'), ','))),
    Comment("implements_@@"), Comment("msgs@@"))))

add('meta', Diagram(Sequence(
    "meta", ".",
    Choice(0,
           Sequence("context", "(", ")"),
           Sequence("getState", "(", ")")))))

add('guard', Diagram(Sequence(
    ':',
    Choice(
        0, Sequence('IDENTIFIER',
                    Optional(Sequence('[',
                                      OneOrMore(NonTerminal('expr'), ','),
                                      ']'))),
        Sequence('(', NonTerminal('expr'), ')')))))




STYLE = """
<style>
svg.railroad-diagram {
    background-color: hsl(30,20%,95%);
}
svg.railroad-diagram path {
    stroke-width: 3;
    stroke: black;
    fill: rgba(0,0,0,0);
}
svg.railroad-diagram text {
    font: bold 14px monospace;
    text-anchor: middle;
}
svg.railroad-diagram text.label {
    text-anchor: start;
}
svg.railroad-diagram text.comment {
    font: italic 12px monospace;
}
svg.railroad-diagram g.non-terminal text {
    font-style: italic;
    font-weight: normal;
}
svg.railroad-diagram rect {
    stroke-width: 3;
    stroke: black;
    fill: hsl(120,100%,90%);
}
</style>
"""


def toReST(rst, ds):
    from StringIO import StringIO
    rst.write('''
Syntax Reference
================

''')

    # Write CSS inline 'cause RTFD can't deal. ~ C.
    rst.write(".. raw:: html\n\n")
    for line in STYLE.split('\n'):
        if line:
            rst.write("    %s\n" % line)

    for name, diagram in ds:
        rst.write('''
.. index::
   single: syntax; %(name)s

**%(name)s**

.. raw:: html

'''
                  % dict(name=name,
                         underline='-' * len(name)))
        buf = StringIO()
        diagram.writeSvg(buf.write)
        for line in buf.getvalue().split('\n'):
            rst.write('   ' + line + '\n')


def toHTML(out, ds):
    from railroad_diagrams import e as esc
    out.write(
        "<!doctype html><title>Test</title><style>%s</style>" % STYLE)
    for name, diag in ds:
        out.write('<h1>{0}</h1>\n'.format(esc(name)))
        diag.writeSvg(out.write)


if __name__ == '__main__':
    from sys import stdout, argv
    if '--html' in argv:
        toHTML(stdout, diagrams)
    else:
        toReST(stdout, diagrams)
