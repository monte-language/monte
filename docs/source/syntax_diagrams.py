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

add('module', Diagram(Sequence(
    Optional(Sequence("module",
                      NonTerminal('imports'),
                      Optional(NonTerminal('exports')))),
    NonTerminal('block'))))

add('imports', Diagram(ZeroOrMore(NonTerminal('pattern'))))
add('exports', Diagram(Sequence(
    'export', "(", ZeroOrMore(NonTerminal('noun')), ")")))
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

add('switch', Diagram(Sequence(
    "switch", "(", NonTerminal('expr'), ")",
    "{",
    OneOrMore(Sequence("match", NonTerminal('pattern'),
                       NonTerminal('block'))), "}")))

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

maybeGuard = lambda: Optional(Sequence(":", NonTerminal('guard')))

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

add('guard', Diagram(Choice(
    0, Sequence('IDENTIFIER',
                Optional(Sequence('[',
                                  OneOrMore(NonTerminal('expr'), ','),
                                  ']'))),
    Sequence('(', NonTerminal('expr'), ')'))))

add('expr', Diagram(Choice(
    0,
    Sequence(
        Choice(0, "continue", "break", "return"),
        Choice(0,
               Sequence("(", ")"),
               ";",
               NonTerminal('blockExpr'))),
    NonTerminal('assign'))))

add('assign', Diagram(Choice(
    0,
    Sequence('def',
             NonTerminal('pattern'),
             Optional(Sequence("exit", NonTerminal('order'))),
             Optional(Sequence(":=", NonTerminal('assign')))),
    Sequence(Choice(0, 'var', 'bind'),
             NonTerminal('pattern'),
             # XXX the next two seem to be optional in the code.
             ":=", NonTerminal('assign')),
    Sequence(NonTerminal('lval'), ":=", NonTerminal('assign')),
    Comment("@op=...XXX"),
    Comment("VERB_ASSIGN XXX"))))

add('lval', Diagram(Choice(
    0,
    NonTerminal('noun'),
    NonTerminal('getExpr'))))

add('infix', Diagram(Sequence(
    NonTerminal('comp'),
    Optional(Sequence(Choice(0, '||', '&&'), NonTerminal('infix'))))))

add('comp', Diagram(
    NonTerminal('order'),
    Optional(Sequence(Choice(
        0,
        "=~",
        "!~",
        "==",
        "!=",
        "&!",
        "^",
        "&",
        "|"
    ), NonTerminal('comp')))))

add('order', Diagram(
    NonTerminal('prefix'),
    Optional(Sequence(Choice(
        0,
        "**",
        "*",
        "/",
        "//",
        "%",
        "+",
        "-",
        "<<",
        ">>",
        "..",
        "..!",
        ">",
        "<",
        ">=",
        "<=",
        "<=>"
    ), NonTerminal('order')))))

add('prefix', Diagram(Choice(
    0,
    Sequence('-', NonTerminal('prim')),
    Sequence(Choice(0, "~", "!"), NonTerminal('call')),
    Sequence('&', NonTerminal('noun')),
    Sequence('&&', NonTerminal('noun')),
    Sequence(NonTerminal('call'), maybeGuard()))))

add('call', Diagram(Sequence(
    NonTerminal('calls'),
    Optional(Sequence(NonTerminal('curry'))))))


verb = lambda: Choice(0, "IDENTIFIER", ".String.")
add('calls', Diagram(
    Choice(
        0, NonTerminal('prim'),
        Sequence(
            NonTerminal('calls'),
            Optional(
                Sequence(Choice(0, ".", "<-"), verb())),
            Sequence("(", ZeroOrMore(NonTerminal('expr'), ','), ")")),
        NonTerminal('getExpr'))))

add('getExpr', Diagram(Sequence(
    NonTerminal('calls'),
    Sequence("[", ZeroOrMore(NonTerminal('expr'), ','), "]"))))

add('curry', Diagram(Sequence(
    Choice(0, '.', '<-'), verb())))

idString = lambda: Choice(0, "IDENTIFIER", Sequence("::", ".String."))
add('prim', Diagram(Choice(
    0,
    ".String.", ".int.", ".float64.", ".char.",
    NonTerminal('quasiliteral'),
    idString(),
    Sequence("(", NonTerminal('expr'), ")"),
    Sequence("{", ZeroOrMore(NonTerminal('expr'), ';'), "}"),
    Sequence("[",
             Choice(
                 0,
                 Skip(),
                 OneOrMore(NonTerminal('expr'), ','),
                 OneOrMore(Sequence(NonTerminal('expr'),
                                    "=>", NonTerminal('expr')),
                           ','),
                 Sequence("for", NonTerminal('comprehension'))),
             "]"))))

add('comprehension', Diagram(Choice(
    0,
    Sequence(NonTerminal('pattern'),
             "in", NonTerminal('iter'),
             NonTerminal('expr')),
    Sequence(NonTerminal('pattern'), "=>", NonTerminal('pattern'),
             "in", NonTerminal('iter'),
             NonTerminal('expr'), "=>", NonTerminal('expr')))))

add('iter', Diagram(Sequence(
    NonTerminal('order'),
    Optional(Sequence("if", NonTerminal('comp'))))))

add('pattern',
    Diagram(Sequence(
        Choice(0,
               NonTerminal('namePattern'),
               NonTerminal('quasiLiteral'),
               Sequence(Choice(0, "==", "!="), NonTerminal('prim')),
               Sequence("_", maybeGuard()),
               Sequence("via", "(", NonTerminal('expr'), ')',
                        NonTerminal('pattern')),
               Sequence("[",
                        ZeroOrMore(NonTerminal('pattern'), ','),
                        ']',
                        Optional(Sequence("+", NonTerminal('pattern')))),
               Sequence("[",
                        OneOrMore(NonTerminal('mapPatternItem'), ','),
                        ']',
                        Optional(Sequence("|", NonTerminal('pattern'))))),
        Optional(Sequence("?", "(", NonTerminal('expr'), ")")))))

add('namePattern', Diagram(
    Choice(0,
           Sequence(idString(), maybeGuard()),
           Sequence("var", NonTerminal('noun'), maybeGuard()),
           Sequence("&", NonTerminal('noun'), maybeGuard()),
           Sequence("bind", NonTerminal('noun'), maybeGuard()),
           Sequence("&&", NonTerminal('noun')))))

add('noun', Diagram(idString()))

add('quasiliteral', Diagram(Sequence(
    Optional(Terminal("IDENTIFIER")),
    '`',
    ZeroOrMore(
        Choice(0, Comment('...text...'),
               Choice(
                   0,
                   Terminal('$IDENT'),
                   Sequence('${', NonTerminal('expr'), '}')),
               Choice(
                   0,
                   Terminal('@IDENT'),
                   Sequence('@{', NonTerminal('pattern'), '}')))),
    '`')))

add('mapPatternItem',
    Diagram(Sequence(
        Choice(0,
               Sequence("=>", NonTerminal('namePattern')),
               Sequence(Choice(0,
                               Sequence("(", NonTerminal('expr'), ")"),
                               ".String.", ".int.", ".float64.", ".char."),
                        "=>", NonTerminal('pattern'))),
        Optional(Sequence(":=", NonTerminal('order'))))))

add('mapItem',
    Diagram(Choice(
        0,
        Sequence("=>", Choice(
            0,
            Sequence("&", NonTerminal('noun')),
            Sequence("&&", NonTerminal('noun')),
            NonTerminal('noun'))),
        Sequence(NonTerminal('expr'), "=>", NonTerminal('expr')))))


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
%(name)s
%(underline)s

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
