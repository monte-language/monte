'''syntax_diagrams.py -- generate railroad diagrams for Monte syntax
'''

from railroad_diagrams import (
    Diagram,
    NonTerminal,
    Sequence, Choice,
    Skip, Optional, ZeroOrMore, OneOrMore)


diagrams = []

def add(name, diagram):
    diagrams.append((name, diagram))


add('module', Diagram(Sequence(
    Optional(Sequence("module"
                      , NonTerminal('imports')
                      , Optional(NonTerminal('exports'))))
    , NonTerminal('block'))));

add('imports', Diagram(ZeroOrMore(NonTerminal('pattern'))));
add('exports', Diagram(Sequence(
    'export', "(", ZeroOrMore(NonTerminal('noun')), ")")));
add('block', Diagram(Sequence(
    "{",
    ZeroOrMore(
        Choice(
            0,
            NonTerminal('blockExpr'),
            NonTerminal('expr')),
        ";"),
    "}"
)));

add('blockExpr', Diagram(Choice(
    0
    , NonTerminal('if')
    , NonTerminal('escape')
    , NonTerminal('for')
    , NonTerminal('fn')
    , NonTerminal('switch')
    , NonTerminal('try')
    , NonTerminal('while')
    , NonTerminal('when')
    , NonTerminal('bind')
    , NonTerminal('object')
    , NonTerminal('def')
    , NonTerminal('interface')
    , NonTerminal('meta')
    , NonTerminal('pass')
)));

add('if', Diagram(
  Sequence("if", "(", NonTerminal('expr'), ")", NonTerminal('block')
           , Optional(Sequence("else", Choice(0
              , Sequence("if", NonTerminal('blockExpr@@'))
              , NonTerminal('block')))))
));

add('escape', Diagram(
  Sequence("escape", NonTerminal('pattern'), NonTerminal('block'),
           Optional(Sequence("catch", NonTerminal('pattern'),
                                      NonTerminal('block'))))
));

add('for', Diagram(
  Sequence("for",
           NonTerminal('pattern'),
           Optional(Sequence("=>", NonTerminal('pattern'))),
           "in", NonTerminal('comp'),
           NonTerminal('block'),
           Optional(Sequence("catch", NonTerminal('pattern'), NonTerminal('block'))))
));

add('fn', Diagram(
  Sequence("fn", ZeroOrMore(NonTerminal('pattern'), ','), NonTerminal('block'))
));

add('switch', Diagram(
  Sequence("switch", "(", NonTerminal('expr'), ")",
           "{",
           OneOrMore(Sequence("match", NonTerminal('pattern'),
                              NonTerminal('block'))), "}")
));

add('try', Diagram(
  Sequence("try", NonTerminal('block'),
           ZeroOrMore(Sequence("catch",
                               NonTerminal('pattern'), NonTerminal('block'))),
           Optional(Sequence("finally", NonTerminal('block'))))
));

add('while', Diagram(
  Sequence("while", "(", NonTerminal('expr'), ")", NonTerminal('block'),
           Optional(Sequence("catch", NonTerminal('pattern'), NonTerminal('block'))))
));

add('when', Diagram(
  Sequence("when",
           "(", OneOrMore(NonTerminal('expr'), ','), ")",
           ZeroOrMore(Sequence("catch",
                               NonTerminal('pattern'), NonTerminal('block'))),
           Optional(Sequence("finally", NonTerminal('block'))))
));

add('bind', Diagram(
  Sequence("bind",
           NonTerminal("noun"),
           Optional(Sequence(":", NonTerminal('guard'))), "objectExpr@@")
));

add('object', Diagram(
  Sequence("object", Choice(0, Sequence("bind", NonTerminal('noun')),
                     "_",
                     NonTerminal("noun")),
           Optional(Sequence(":", NonTerminal('guard'))), "objectExpr@@")
));

add('def', Diagram(
  Sequence("def", Choice(0,
     Sequence(Choice(0,
         Sequence("bind", NonTerminal("noun"),
                  Optional(Sequence(":", NonTerminal('guard')))),
         NonTerminal("noun")),
         Choice(0, "objectFunction@@", NonTerminal('assign'))),
         NonTerminal('assign')))
));

add('interface', Diagram(
  Sequence("interface",
           NonTerminal('namePattern'),
           Optional(Sequence("guards", NonTerminal('pattern'))),
           Optional(Sequence("extends", OneOrMore(NonTerminal('order'), ','))),
           "implements_@@", "msgs@@")
));

add('meta', Diagram(
  Sequence("meta", ".", Choice(0,
           Sequence("context", "(", ")"),
           Sequence("getState", "(", ")")
           ))
));

add('pass', Diagram('pass'));

add('guard', Diagram(Choice(
    0, Sequence('IDENTIFIER',
                Optional(Sequence('[',
                                  OneOrMore(NonTerminal('expr'), ','),
                                  ']'))),
    Sequence('(', NonTerminal('expr'), ')')
)));


add('expr',
Diagram(Choice(0,
  Sequence(
      Choice(0, "continue", "break", "return")
    , Choice(0,
             Sequence("(", ")"),
             ";",
             NonTerminal('blockExpr'))),
  NonTerminal('assign'))));

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
    "@op=...XXX",
    "VERB_ASSIGN XXX"
)
));

add('lval', Diagram(Choice(
    0
    , NonTerminal('noun')
    , NonTerminal('getExpr')
)));

add('infix', Diagram(Sequence(
 NonTerminal('comp'),
 Optional(Sequence(Choice(0, '||', '&&'), NonTerminal('infix'))))));

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
    ), NonTerminal('comp')))));

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
    ), NonTerminal('order')))));

add('prefix', Diagram(Choice(
    0
    , Sequence('-', NonTerminal('prim'))
    , Sequence(Choice(0, "~", "!"), NonTerminal('call'))
    , Sequence('&', NonTerminal('noun'))
    , Sequence('&&', NonTerminal('noun'))
    , Sequence(NonTerminal('call'),
               Optional(Sequence(":", NonTerminal('guard'))))
)));

add('call', Diagram(Sequence(
    NonTerminal('calls'),
    Optional(Sequence(NonTerminal('curry')))
)));

add('calls', Diagram(
    Choice(
        0
        , NonTerminal('prim')
        , Sequence(
            NonTerminal('calls'),
            Optional(
                Sequence(Choice(0, ".", "<-"),
                         Choice(0, ".String.", "IDENTIFIER"))),
            Sequence("(", ZeroOrMore(NonTerminal('expr'), ','), ")"))
        , NonTerminal('getExpr'))
));

add('getExpr', Diagram(Sequence(
    NonTerminal('calls'),
    Sequence("[", ZeroOrMore(NonTerminal('expr'), ','), "]")
)));

add('curry', Diagram(Sequence(
    Choice(0, '.', '<-'),
    Choice(0, ".String.", "IDENTIFIER")
)));

add('prim', Diagram(Choice(
    0
    ,".String.", ".int.", ".float64.", ".char."
    , NonTerminal('quasiliteral')
    , "IDENTIFIER"
    , Sequence("::", ".String.")
    , Sequence("(", NonTerminal('expr'), ")")
    , Sequence("{", ZeroOrMore(NonTerminal('expr'), ';'), "}")
    , Sequence("[", Choice(
        0
        , Skip()
        , OneOrMore(NonTerminal('expr'), ',')
        , OneOrMore(Sequence(NonTerminal('expr'),
                             "=>", NonTerminal('expr')),
                    ',')
        , Sequence("for", NonTerminal('comprehension')))
               , "]")
)));

add('comprehension', Diagram(Choice(
    0
    , Sequence(NonTerminal('pattern'),
               "in", NonTerminal('iter'),
               NonTerminal('expr'))
    , Sequence(NonTerminal('pattern'), "=>", NonTerminal('pattern'),
               "in", NonTerminal('iter'),
               NonTerminal('expr'), "=>", NonTerminal('expr'))
)));

add('iter', Diagram(Sequence(
    NonTerminal('order'),
    Optional(Sequence("if", NonTerminal('comp')))
)));

add('pattern',
    Diagram(Sequence(
        Choice(0,
               NonTerminal('namePattern')
               , NonTerminal('quasiLiteral')
               , Sequence(Choice(0, "==", "!="), NonTerminal('prim'))
               , Sequence("_", ":", NonTerminal('guard'))
               , Sequence("via", "(", NonTerminal('expr'), ')',
                          NonTerminal('pattern'))
               , Sequence("[",
                          OneOrMore(NonTerminal('mapPatternItem'), ','), ']'))
        , Optional(Sequence("?", "(", NonTerminal('expr'), ")")))))

add('namePattern', Diagram(
    Choice(0,
           Sequence(
               Choice(0,
                      Sequence("::", ".String."),
                      "IDENTIFIER"),
               Optional(Sequence(':', NonTerminal('guard')))),
           Sequence("var", NonTerminal('noun'),
                    Optional(Sequence(":", NonTerminal('guard')))),
           Sequence("&", NonTerminal('noun'),
                    Optional(Sequence(":", NonTerminal('guard')))),
           Sequence("&&", NonTerminal('noun')),
           Sequence("bind", NonTerminal('noun'),
                    Optional(Sequence(":", NonTerminal('guard')))),
       )))

add('noun', Diagram(Choice(
    0, 'IDENTIFIER',
    Sequence('::', '.String.'))));

add('quasiliteral', Diagram(Sequence(
    Optional("IDENTIFIER"), 
    '`',
    ZeroOrMore(
        Choice(0, '...',
               '$IDENT',
               Sequence('${', NonTerminal('expr'), '}'),
               '@IDENT',
               Sequence('@{', NonTerminal('expr'), '}')
               
           ))
    , '`')));

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


def figFile(name, d,
            static='_static/'):
    fn = 'rr_%s.svg' % name
    with open(static + fn, 'wb') as out:
        d.writeSvg(out.write)
    return fn


def toReST(rst, ds):
    for name, diagram in ds:
        fn = figFile(name, diagram)
        rst.write('''
%(name)s
--------

.. figure: %(fn)s

'''
                  % dict(name=name, fn=fn))

def toHTML(out, ds):
    from railroad_diagrams import STYLE
    from railroad_diagrams import e as esc
    out.write(
        "<!doctype html><title>Test</title><style>%s</style>" % STYLE)
    for name, diag in ds:
        out.write('<h1>{0}</h1>\n'.format(esc(name)))
        diag.writeSvg(out.write)


if __name__ == '__main__':
    from sys import stdout
    #toHTML(stdout, diagrams)
    toReST(stdout, diagrams)

