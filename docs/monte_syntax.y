
{-
guard ::= Sequence(
 ':',
 Choice(
     0, Sequence('IDENTIFIER',
                 Optional(Sequence('[',
                                   OneOrMore(NonTerminal('expr'), ','),
                                   ']'))),
     Sequence('(', NonTerminal('expr'), ')')))
-}
guard : ':' guard_2
guard_2 : guard_2_1
    | guard_2_2
guard_2_1 : 'IDENTIFIER' guard_2_1_2
guard_2_1_2 : guard_2_1_2_1
    | guard_2_1_2_2
guard_2_1_2_1 : 
guard_2_1_2_2 : '[' guard_2_1_2_2_2 ']'
guard_2_1_2_2_2 : expr
    | guard_2_1_2_2_2 ',' expr
guard_2_2 : '(' expr ')'

{-
interface ::= Sequence(
 "interface",
 NonTerminal('namePattern'),
 Optional(Sequence("guards", NonTerminal('pattern'))),
 Optional(Sequence("extends", OneOrMore(NonTerminal('order'), ','))),
 Comment("implements_@@"), Comment("msgs@@"))
-}
interface : 'interface' namePattern interface_3 interface_4
interface_3 : interface_3_1
    | interface_3_2
interface_3_1 : 
interface_3_2 : 'guards' pattern
interface_4 : interface_4_1
    | interface_4_2
interface_4_1 : 
interface_4_2 : 'extends' interface_4_2_2
interface_4_2_2 : order
    | interface_4_2_2 ',' order

{-
FunctionExpr ::= Sequence('def', '(', ZeroOrMore(NonTerminal('pattern'), ','), ')',
  NonTerminal('block'))
-}
FunctionExpr : 'def' '(' FunctionExpr_3 ')' block
FunctionExpr_3 : FunctionExpr_3_1
    | FunctionExpr_3_2
FunctionExpr_3_1 : 
FunctionExpr_3_2 : pattern
    | FunctionExpr_3_2 ',' pattern

{-
ObjectExpr ::= Sequence(
 "object",
 Choice(0, Sequence("bind", NonTerminal('name')),
        "_",
        NonTerminal('name')),
 Optional(NonTerminal('guard')), Comment("objectExpr"))
-}
ObjectExpr : 'object' ObjectExpr_2 ObjectExpr_3
ObjectExpr_2 : ObjectExpr_2_1
    | '_'
    | name
ObjectExpr_2_1 : 'bind' name
ObjectExpr_3 : ObjectExpr_3_1
    | guard
ObjectExpr_3_1 : 

{-
objectExpr ::= Sequence(
 Optional(Sequence('extends', NonTerminal('order'))),
 NonTerminal('auditors'),
 '{', ZeroOrMore(NonTerminal('objectScript'), ';'), '}')
-}
objectExpr : objectExpr_1 auditors '{' objectExpr_4 '}'
objectExpr_1 : objectExpr_1_1
    | objectExpr_1_2
objectExpr_1_1 : 
objectExpr_1_2 : 'extends' order
objectExpr_4 : objectExpr_4_1
    | objectExpr_4_2
objectExpr_4_1 : 
objectExpr_4_2 : objectScript
    | objectExpr_4_2 ';' objectScript

{-
objectScript ::= Sequence(
 Optional(NonTerminal('doco')),
 Choice(0, "pass", ZeroOrMore("@@meth")),
 Choice(0, "pass", ZeroOrMore(NonTerminal('matchers'))))
-}
objectScript : objectScript_1 objectScript_2 objectScript_3
objectScript_1 : objectScript_1_1
    | doco
objectScript_1_1 : 
objectScript_2 : 'pass'
    | objectScript_2_2
objectScript_2_2 : objectScript_2_2_1
    | objectScript_2_2_2
objectScript_2_2_1 : 
objectScript_2_2_2 : '@@meth'
    | objectScript_2_2_2 objectScript_2_2_2_2 '@@meth'
objectScript_2_2_2_2 : 
objectScript_3 : 'pass'
    | objectScript_3_2
objectScript_3_2 : objectScript_3_2_1
    | objectScript_3_2_2
objectScript_3_2_1 : 
objectScript_3_2_2 : matchers
    | objectScript_3_2_2 objectScript_3_2_2_2 matchers
objectScript_3_2_2_2 : 

{-
matchers ::= OneOrMore(Sequence("match",
          NonTerminal('pattern'),
          NonTerminal('block')))
-}
matchers : matchers_1
    | matchers matchers_2 matchers_1
matchers_1 : 'match' pattern block
matchers_2 : 

{-
doco ::= Terminal('.String')
-}

{-
InterfaceExpr ::= Sequence('@@@@@')
-}
InterfaceExpr : '@@@@@'

{-
IfExpr ::= Sequence(
 "if", "(", NonTerminal('expr'), ")", NonTerminal('block'),
 Optional(Sequence("else", Choice(
     0, Sequence("if", Comment('blockExpr@@')),
     NonTerminal('block')))))
-}
IfExpr : 'if' '(' expr ')' block IfExpr_6
IfExpr_6 : IfExpr_6_1
    | IfExpr_6_2
IfExpr_6_1 : 
IfExpr_6_2 : 'else' IfExpr_6_2_2
IfExpr_6_2_2 : IfExpr_6_2_2_1
    | block
IfExpr_6_2_2_1 : 'if'

{-
ForExpr ::= Sequence(
 "for",
 NonTerminal('pattern'),
 Optional(Sequence("=>", NonTerminal('pattern'))),
 "in", NonTerminal('comp'),
 NonTerminal('blockCatch'))
-}
ForExpr : 'for' pattern ForExpr_3 'in' comp blockCatch
ForExpr_3 : ForExpr_3_1
    | ForExpr_3_2
ForExpr_3_1 : 
ForExpr_3_2 : '=>' pattern

{-
blockCatch ::= Sequence(
 NonTerminal('block'),
 Optional(
     Sequence("catch", NonTerminal('pattern'),
              NonTerminal('block'))))
-}
blockCatch : block blockCatch_2
blockCatch_2 : blockCatch_2_1
    | blockCatch_2_2
blockCatch_2_1 : 
blockCatch_2_2 : 'catch' pattern block

{-
WhileExpr ::= Sequence(
 "while", "(", NonTerminal('expr'), ")", NonTerminal('blockCatch'))
-}
WhileExpr : 'while' '(' expr ')' blockCatch

{-
SwitchExpr ::= Sequence(
 "switch", "(", NonTerminal('expr'), ")",
 "{", NonTerminal('matchers'), "}")
-}
SwitchExpr : 'switch' '(' expr ')' '{' matchers '}'

{-
matchers ::= OneOrMore(Sequence("match",
          NonTerminal('pattern'),
          NonTerminal('block')))
-}
matchers : matchers_1
    | matchers matchers_2 matchers_1
matchers_1 : 'match' pattern block
matchers_2 : 

{-
EscapeExpr ::= Sequence(
 "escape", NonTerminal('pattern'),
 NonTerminal('blockCatch'))
-}
EscapeExpr : 'escape' pattern blockCatch

{-
TryExpr ::= Sequence(
 "try", NonTerminal('block'), NonTerminal('catchers'))
-}
TryExpr : 'try' block catchers

{-
catchers ::= Sequence(
 ZeroOrMore(Sequence("catch",
                     NonTerminal('pattern'),
                     NonTerminal('block'))),
 Optional(Sequence("finally", NonTerminal('block'))))
-}
catchers : catchers_1 catchers_2
catchers_1 : catchers_1_1
    | catchers_1_2
catchers_1_1 : 
catchers_1_2 : catchers_1_2_1
    | catchers_1_2 catchers_1_2_2 catchers_1_2_1
catchers_1_2_1 : 'catch' pattern block
catchers_1_2_2 : 
catchers_2 : catchers_2_1
    | catchers_2_2
catchers_2_1 : 
catchers_2_2 : 'finally' block

{-
WhenExpr ::= Sequence(
 "when",
 "(", OneOrMore(NonTerminal('expr'), ','), ")",
 "->", NonTerminal('block'),
 NonTerminal('catchers'))
-}
WhenExpr : 'when' '(' WhenExpr_3 ')' '->' block catchers
WhenExpr_3 : expr
    | WhenExpr_3 ',' expr

{-
LambdaExpr ::= Sequence(
 "fn",
 ZeroOrMore(NonTerminal('pattern'), ','),
 NonTerminal('block'))
-}
LambdaExpr : 'fn' LambdaExpr_2 block
LambdaExpr_2 : LambdaExpr_2_1
    | LambdaExpr_2_2
LambdaExpr_2_1 : 
LambdaExpr_2_2 : pattern
    | LambdaExpr_2_2 ',' pattern

{-
MetaExpr ::= Sequence(
 "meta", ".",
 Choice(0,
        Sequence("context", "(", ")"),
        Sequence("getState", "(", ")")))
-}
MetaExpr : 'meta' '.' MetaExpr_3
MetaExpr_3 : MetaExpr_3_1
    | MetaExpr_3_2
MetaExpr_3_1 : 'context' '(' ')'
MetaExpr_3_2 : 'getState' '(' ')'

{-
block ::= Sequence(
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
 "}")
-}
block : '{' block_2 '}'
block_2 : block_2_1
    | 'pass'
block_2_1 : block_2_1_1
    | block_2_1_2
block_2_1_1 : 
block_2_1_2 : block_2_1_2_1
    | block_2_1_2 ';' block_2_1_2_1
block_2_1_2_1 : blockExpr
    | expr

{-
blockExpr ::= Choice(
 0,
 NonTerminal('FunctionExpr'),
 NonTerminal('ObjectExpr'),
 NonTerminal('bind'),
 NonTerminal('def'),
 NonTerminal('InterfaceExpr'),
 NonTerminal('IfExpr'),
 NonTerminal('ForExpr'),
 NonTerminal('WhileExpr'),
 NonTerminal('SwitchExpr'),
 NonTerminal('EscapeExpr'),
 NonTerminal('TryExpr'),
 NonTerminal('WhenExpr'),
 NonTerminal('LambdaExpr'),
 NonTerminal('MetaExpr'))
-}
blockExpr : FunctionExpr
    | ObjectExpr
    | bind
    | def
    | InterfaceExpr
    | IfExpr
    | ForExpr
    | WhileExpr
    | SwitchExpr
    | EscapeExpr
    | TryExpr
    | WhenExpr
    | LambdaExpr
    | MetaExpr

{-
expr ::= Choice(
 0,
 NonTerminal('assign'),
 Sequence(
     Choice(0, "continue", "break", "return"),
     Choice(0,
            Sequence("(", ")"),
            ";",
            NonTerminal('blockExpr'))))
-}
expr : assign
    | expr_2
expr_2 : expr_2_1 expr_2_2
expr_2_1 : 'continue'
    | 'break'
    | 'return'
expr_2_2 : expr_2_2_1
    | ';'
    | blockExpr
expr_2_2_1 : '(' ')'

{-
bind ::= Sequence(
 "bind",
 NonTerminal('name'),
 Optional(NonTerminal('guard')), Comment("objectExpr@@"))
-}
bind : 'bind' name bind_3
bind_3 : bind_3_1
    | guard
bind_3_1 : 

{-
name ::= Choice(0, "IDENTIFIER", Sequence("::", ".String."))
-}
name : 'IDENTIFIER'
    | name_2
name_2 : '::' '.String.'

{-
def ::= Sequence(
 "def",
 Choice(
     0,
     Sequence(
         Choice(
             0,
             Sequence("bind", NonTerminal("name"),
                      Optional(NonTerminal('guard'))),
             NonTerminal("name")),
         Choice(0, Comment("objectFunction@@"), NonTerminal('assign'))),
     NonTerminal('assign')))
-}
def : 'def' def_2
def_2 : def_2_1
    | assign
def_2_1 : def_2_1_1 def_2_1_2
def_2_1_1 : def_2_1_1_1
    | name
def_2_1_1_1 : 'bind' name def_2_1_1_1_3
def_2_1_1_1_3 : def_2_1_1_1_3_1
    | guard
def_2_1_1_1_3_1 : 
def_2_1_2 : assign

{-
comprehension ::= Choice(
 0,
 Sequence(NonTerminal('pattern'),
          "in", NonTerminal('iter'),
          NonTerminal('expr')),
 Sequence(NonTerminal('pattern'), "=>", NonTerminal('pattern'),
          "in", NonTerminal('iter'),
          NonTerminal('expr'), "=>", NonTerminal('expr')))
-}
comprehension : comprehension_1
    | comprehension_2
comprehension_1 : pattern 'in' iter expr
comprehension_2 : pattern '=>' pattern 'in' iter expr '=>' expr

{-
iter ::= Sequence(
 NonTerminal('order'),
 Optional(Sequence("if", NonTerminal('comp'))))
-}
iter : order iter_2
iter_2 : iter_2_1
    | iter_2_2
iter_2_1 : 
iter_2_2 : 'if' comp

{-
module ::= Sequence(
 Optional(Sequence("imports",
                   NonTerminal('imports'),
                   Optional(NonTerminal('exports')))),
 NonTerminal('block'))
-}
module : module_1 block
module_1 : module_1_1
    | module_1_2
module_1_1 : 
module_1_2 : 'imports' imports module_1_2_3
module_1_2_3 : module_1_2_3_1
    | exports
module_1_2_3_1 : 

{-
imports ::= ZeroOrMore(NonTerminal('namedPattern'))
-}
imports : imports_1
    | imports_2
imports_1 : 
imports_2 : namedPattern
    | imports_2 imports_2_2 namedPattern
imports_2_2 : 

{-
exports ::= Sequence("exports", "(", ZeroOrMore(NonTerminal('name')), ")")
-}
exports : 'exports' '(' exports_3 ')'
exports_3 : exports_3_1
    | exports_3_2
exports_3_1 : 
exports_3_2 : name
    | exports_3_2 exports_3_2_2 name
exports_3_2_2 : 

{-
PatternBinding ::= Sequence('def',
          NonTerminal('pattern'),
          Optional(Sequence("exit", NonTerminal('order'))),
          Optional(Sequence(":=", NonTerminal('assign'))))
-}
PatternBinding : 'def' pattern PatternBinding_3 PatternBinding_4
PatternBinding_3 : PatternBinding_3_1
    | PatternBinding_3_2
PatternBinding_3_1 : 
PatternBinding_3_2 : 'exit' order
PatternBinding_4 : PatternBinding_4_1
    | PatternBinding_4_2
PatternBinding_4_1 : 
PatternBinding_4_2 : ':=' assign

{-
call ::= Sequence(
 NonTerminal('calls'),
 Optional(Sequence(NonTerminal('curry'))))
-}
call : calls call_2
call_2 : call_2_1
    | call_2_2
call_2_1 : 
call_2_2 : curry

{-
calls ::= Choice(
    0, NonTerminal('prim'),
    Sequence(
        NonTerminal('calls'),
        Optional(
            Sequence(Choice(0, ".", "<-"),
                     Choice(0, "IDENTIFIER", ".String."))),
        Sequence("(", ZeroOrMore(NonTerminal('expr'), ','), ")")),
    NonTerminal('getExpr'))
-}
calls : prim
    | calls_2
    | getExpr
calls_2 : calls calls_2_2 calls_2_3
calls_2_2 : calls_2_2_1
    | calls_2_2_2
calls_2_2_1 : 
calls_2_2_2 : calls_2_2_2_1 calls_2_2_2_2
calls_2_2_2_1 : '.'
    | '<-'
calls_2_2_2_2 : 'IDENTIFIER'
    | '.String.'
calls_2_3 : '(' calls_2_3_2 ')'
calls_2_3_2 : calls_2_3_2_1
    | calls_2_3_2_2
calls_2_3_2_1 : 
calls_2_3_2_2 : expr
    | calls_2_3_2_2 ',' expr

{-
getExpr ::= Sequence(
 NonTerminal('calls'),
 Sequence("[", ZeroOrMore(NonTerminal('expr'), ','), "]"))
-}
getExpr : calls getExpr_2
getExpr_2 : '[' getExpr_2_2 ']'
getExpr_2_2 : getExpr_2_2_1
    | getExpr_2_2_2
getExpr_2_2_1 : 
getExpr_2_2_2 : expr
    | getExpr_2_2_2 ',' expr

{-
curry ::= Sequence(
 Choice(0, '.', '<-'),
 Choice(0, "IDENTIFIER", ".String."))
-}
curry : curry_1 curry_2
curry_1 : '.'
    | '<-'
curry_2 : 'IDENTIFIER'
    | '.String.'

{-
comp ::= Sequence(
 NonTerminal('order'),
 Optional(Sequence(Choice(
     0,
     Choice(0, "=~", "!~"),
     Choice(0, "==", "!="),
     "&!",
     Choice(0, "^", "&", "|")
 ), NonTerminal('comp'))))
-}
comp : order comp_2
comp_2 : comp_2_1
    | comp_2_2
comp_2_1 : 
comp_2_2 : comp_2_2_1 comp
comp_2_2_1 : comp_2_2_1_1
    | comp_2_2_1_2
    | '&!'
    | comp_2_2_1_4
comp_2_2_1_1 : '=~'
    | '!~'
comp_2_2_1_2 : '=='
    | '!='
comp_2_2_1_4 : '^'
    | '&'
    | '|'

{-
logical ::= Sequence(
 NonTerminal('comp'),
 Optional(Sequence(Choice(0, '||', '&&'), NonTerminal('logical'))))
-}
logical : comp logical_2
logical_2 : logical_2_1
    | logical_2_2
logical_2_1 : 
logical_2_2 : logical_2_2_1 logical
logical_2_2_1 : '||'
    | '&&'

{-
order ::= Sequence(
 NonTerminal('prefix'),
 Optional(Sequence(Choice(
     0,
     "**",
     Choice(0, "*", "/", "//", "%"),
     Choice(0, "+", "-"),
     Choice(0, "<<", ">>"),
     Choice(0, "..", "..!"),
     Choice(0, ">", "<", ">=", "<=", "<=>")
 ), NonTerminal('order'))))
-}
order : prefix order_2
order_2 : order_2_1
    | order_2_2
order_2_1 : 
order_2_2 : order_2_2_1 order
order_2_2_1 : '**'
    | order_2_2_1_2
    | order_2_2_1_3
    | order_2_2_1_4
    | order_2_2_1_5
    | order_2_2_1_6
order_2_2_1_2 : '*'
    | '/'
    | '//'
    | '%'
order_2_2_1_3 : '+'
    | '-'
order_2_2_1_4 : '<<'
    | '>>'
order_2_2_1_5 : '..'
    | '..!'
order_2_2_1_6 : '>'
    | '<'
    | '>='
    | '<='
    | '<=>'

{-
assign ::= Choice(
 0,
 NonTerminal('PatternBinding'),
 Sequence(Choice(0, 'var', 'bind'),
          NonTerminal('pattern'),
          # XXX the next two seem to be optional in the code.
          ":=", NonTerminal('assign')),
 Sequence(NonTerminal('lval'), ":=", NonTerminal('assign')),
 Comment("@op=...XXX"),
 Comment("VERB_ASSIGN XXX"),
 NonTerminal('logical'))
-}
assign : PatternBinding
    | assign_2
    | assign_3
    | logical
assign_2 : assign_2_1 pattern ':=' assign
assign_2_1 : 'var'
    | 'bind'
assign_3 : lval ':=' assign

{-
ForwardDeclaration ::= Sequence('def', NonTerminal('name'))
-}
ForwardDeclaration : 'def' name

{-
lval ::= Choice(
 0,
 NonTerminal('name'),
 NonTerminal('getExpr'))
-}
lval : name
    | getExpr

{-
prim ::= Choice(
 0,
 NonTerminal('Literal'),
 NonTerminal('quasiliteral'),
 NonTerminal('noun'),
 Sequence("(", NonTerminal('expr'), ")"),
 Sequence("{", ZeroOrMore(NonTerminal('expr'), ';'), "}"),
 Sequence("[",
          "for", NonTerminal('comprehension'),
          "]"))
-}
prim : Literal
    | quasiliteral
    | noun
    | prim_4
    | prim_5
    | prim_6
prim_4 : '(' expr ')'
prim_5 : '{' prim_5_2 '}'
prim_5_2 : prim_5_2_1
    | prim_5_2_2
prim_5_2_1 : 
prim_5_2_2 : expr
    | prim_5_2_2 ';' expr
prim_6 : '[' 'for' comprehension ']'

{-
noun ::= Choice(0, "IDENTIFIER", Sequence("::", ".String."))
-}
noun : 'IDENTIFIER'
    | noun_2
noun_2 : '::' '.String.'

{-
prefix ::= Choice(
 0,
 NonTerminal('unary'),
 NonTerminal('SlotExpression'),
 NonTerminal('BindingExpression'),
 Sequence(NonTerminal('call'), Optional(NonTerminal('guard'))))
-}
prefix : unary
    | SlotExpression
    | BindingExpression
    | prefix_4
prefix_4 : call prefix_4_2
prefix_4_2 : prefix_4_2_1
    | guard
prefix_4_2_1 : 

{-
unary ::= Choice(
 0,
 Sequence('-', NonTerminal('prim')),
 Sequence(Choice(0, "~", "!"), NonTerminal('call')))
-}
unary : unary_1
    | unary_2
unary_1 : '-' prim
unary_2 : unary_2_1 call
unary_2_1 : '~'
    | '!'

{-
SlotExpression ::= Sequence('&', NonTerminal('noun'))
-}
SlotExpression : '&' noun

{-
BindingExpression ::= Sequence('&&', NonTerminal('noun'))
-}
BindingExpression : '&&' noun

{-
pattern ::= Choice(0,
       NonTerminal('namePattern'),
       Choice(0,
         NonTerminal('SamePattern'),
         NonTerminal('NotSamePattern')),
       NonTerminal('QuasiLiteralPattern'),
       NonTerminal('ViaPattern'),
       NonTerminal('IgnorePattern'),
       NonTerminal('ListPattern'),
       NonTerminal('MapPattern'),
       NonTerminal('SuchThatPattern'))
-}
pattern : namePattern
    | pattern_2
    | QuasiLiteralPattern
    | ViaPattern
    | IgnorePattern
    | ListPattern
    | MapPattern
    | SuchThatPattern
pattern_2 : SamePattern
    | NotSamePattern

{-
namePattern ::= Choice(0,
        NonTerminal('FinalPattern'),
        NonTerminal('VarPattern'),
        NonTerminal('BindPattern'),
        NonTerminal('SlotPattern'),
        NonTerminal('BindingPattern'))
-}
namePattern : FinalPattern
    | VarPattern
    | BindPattern
    | SlotPattern
    | BindingPattern

{-
FinalPattern ::= Sequence(Choice(0, "IDENTIFIER", ".String."),
                 Optional(NonTerminal('guard')))
-}
FinalPattern : FinalPattern_1 FinalPattern_2
FinalPattern_1 : 'IDENTIFIER'
    | '.String.'
FinalPattern_2 : FinalPattern_2_1
    | guard
FinalPattern_2_1 : 

{-
VarPattern ::= Sequence("var", NonTerminal('name'),
         Optional(NonTerminal('guard')))
-}
VarPattern : 'var' name VarPattern_3
VarPattern_3 : VarPattern_3_1
    | guard
VarPattern_3_1 : 

{-
BindPattern ::= Sequence("bind", NonTerminal('name'),
    Optional(NonTerminal('guard')))
-}
BindPattern : 'bind' name BindPattern_3
BindPattern_3 : BindPattern_3_1
    | guard
BindPattern_3_1 : 

{-
SlotPattern ::= Sequence("&", NonTerminal('name'),
    Optional(NonTerminal('guard')))
-}
SlotPattern : '&' name SlotPattern_3
SlotPattern_3 : SlotPattern_3_1
    | guard
SlotPattern_3_1 : 

{-
BindingPattern ::= Sequence("&&", NonTerminal('name'))
-}
BindingPattern : '&&' name

{-
IgnorePattern ::= Sequence("_", Optional(NonTerminal('guard')))
-}
IgnorePattern : '_' IgnorePattern_2
IgnorePattern_2 : IgnorePattern_2_1
    | guard
IgnorePattern_2_1 : 

{-
ListPattern ::= Sequence("[",
         ZeroOrMore(NonTerminal('pattern'), ','),
         ']',
         Optional(Sequence("+", NonTerminal('pattern'))))
-}
ListPattern : '[' ListPattern_2 ']' ListPattern_4
ListPattern_2 : ListPattern_2_1
    | ListPattern_2_2
ListPattern_2_1 : 
ListPattern_2_2 : pattern
    | ListPattern_2_2 ',' pattern
ListPattern_4 : ListPattern_4_1
    | ListPattern_4_2
ListPattern_4_1 : 
ListPattern_4_2 : '+' pattern

{-
MapPattern ::= Sequence("[",
         OneOrMore(NonTerminal('mapPatternItem'), ','),
         ']',
         Optional(Sequence("|", NonTerminal('pattern'))))
-}
MapPattern : '[' MapPattern_2 ']' MapPattern_4
MapPattern_2 : mapPatternItem
    | MapPattern_2 ',' mapPatternItem
MapPattern_4 : MapPattern_4_1
    | MapPattern_4_2
MapPattern_4_1 : 
MapPattern_4_2 : '|' pattern

{-
mapPatternItem ::= Sequence(
     Choice(0,
            Sequence("=>", NonTerminal('namePattern')),
            Sequence(
              Choice(0,
                Choice(0, ".String.", ".int.", ".float64.", ".char."),
                Sequence("(", NonTerminal('expr'), ")")),
              "=>", NonTerminal('pattern'))),
     Optional(Sequence(":=", NonTerminal('order'))))
-}
mapPatternItem : mapPatternItem_1 mapPatternItem_2
mapPatternItem_1 : mapPatternItem_1_1
    | mapPatternItem_1_2
mapPatternItem_1_1 : '=>' namePattern
mapPatternItem_1_2 : mapPatternItem_1_2_1 '=>' pattern
mapPatternItem_1_2_1 : mapPatternItem_1_2_1_1
    | mapPatternItem_1_2_1_2
mapPatternItem_1_2_1_1 : '.String.'
    | '.int.'
    | '.float64.'
    | '.char.'
mapPatternItem_1_2_1_2 : '(' expr ')'
mapPatternItem_2 : mapPatternItem_2_1
    | mapPatternItem_2_2
mapPatternItem_2_1 : 
mapPatternItem_2_2 : ':=' order

{-
mapItem ::= Choice(
     0,
     Sequence("=>", Choice(
         0,
         Sequence("&", NonTerminal('name')),
         Sequence("&&", NonTerminal('name')),
         NonTerminal('name'))),
     Sequence(NonTerminal('expr'), "=>", NonTerminal('expr')))
-}
mapItem : mapItem_1
    | mapItem_2
mapItem_1 : '=>' mapItem_1_2
mapItem_1_2 : mapItem_1_2_1
    | mapItem_1_2_2
    | name
mapItem_1_2_1 : '&' name
mapItem_1_2_2 : '&&' name
mapItem_2 : expr '=>' expr

{-
SamePattern ::= Sequence("==", NonTerminal('prim'))
-}
SamePattern : '==' prim

{-
NotSamePattern ::= Sequence("!=", NonTerminal('prim'))
-}
NotSamePattern : '!=' prim

{-
QuasiliteralPattern ::= Sequence(
 Optional(Terminal("IDENTIFIER")),
 '`',
 ZeroOrMore(
     Choice(0, Comment('...text...'),
            Choice(
                0,
                Terminal('@IDENT'),
                Sequence('@{', NonTerminal('pattern'), '}')))),
 '`')
-}
QuasiliteralPattern : QuasiliteralPattern_1 '`' QuasiliteralPattern_3 '`'
QuasiliteralPattern_1 : QuasiliteralPattern_1_1
    | 'IDENTIFIER'
QuasiliteralPattern_1_1 : 
QuasiliteralPattern_3 : QuasiliteralPattern_3_1
    | QuasiliteralPattern_3_2
QuasiliteralPattern_3_1 : 
QuasiliteralPattern_3_2 : QuasiliteralPattern_3_2_1
    | QuasiliteralPattern_3_2 QuasiliteralPattern_3_2_2 QuasiliteralPattern_3_2_1
QuasiliteralPattern_3_2_1 : QuasiliteralPattern_3_2_1_1
QuasiliteralPattern_3_2_1_1 : '@IDENT'
    | QuasiliteralPattern_3_2_1_1_2
QuasiliteralPattern_3_2_1_1_2 : '@{' pattern '}'
QuasiliteralPattern_3_2_2 : 

{-
ViaPattern ::= Sequence("via", "(", NonTerminal('expr'), ')',
         NonTerminal('pattern'))
-}
ViaPattern : 'via' '(' expr ')' pattern

{-
SuchThatPattern ::= Sequence(NonTerminal('pattern'), "?", "(", NonTerminal('expr'), ")")
-}
SuchThatPattern : pattern '?' '(' expr ')'

{-
quasiliteral ::= Sequence(
 Optional(Terminal("IDENTIFIER")),
 '`',
 ZeroOrMore(
     Choice(0, Comment('...text...'),
            Choice(
                0,
                Terminal('$IDENT'),
                Sequence('${', NonTerminal('expr'), '}')))),
 '`')
-}
quasiliteral : quasiliteral_1 '`' quasiliteral_3 '`'
quasiliteral_1 : quasiliteral_1_1
    | 'IDENTIFIER'
quasiliteral_1_1 : 
quasiliteral_3 : quasiliteral_3_1
    | quasiliteral_3_2
quasiliteral_3_1 : 
quasiliteral_3_2 : quasiliteral_3_2_1
    | quasiliteral_3_2 quasiliteral_3_2_2 quasiliteral_3_2_1
quasiliteral_3_2_1 : quasiliteral_3_2_1_1
quasiliteral_3_2_1_1 : '$IDENT'
    | quasiliteral_3_2_1_1_2
quasiliteral_3_2_1_1_2 : '${' expr '}'
quasiliteral_3_2_2 : 

{-
Literal ::= Choice(0,
  ".int.", ".float64.", ".char.", ".String.",
  Sequence("[", ZeroOrMore(NonTerminal('expr'), ','), "]"),
  Sequence("[", ZeroOrMore(Sequence(NonTerminal('expr'),
                                    "=>", NonTerminal('expr')), ','), "]"))
-}
Literal : '.int.'
    | '.float64.'
    | '.char.'
    | '.String.'
    | Literal_5
    | Literal_6
Literal_5 : '[' Literal_5_2 ']'
Literal_5_2 : Literal_5_2_1
    | Literal_5_2_2
Literal_5_2_1 : 
Literal_5_2_2 : expr
    | Literal_5_2_2 ',' expr
Literal_6 : '[' Literal_6_2 ']'
Literal_6_2 : Literal_6_2_1
    | Literal_6_2_2
Literal_6_2_1 : 
Literal_6_2_2 : Literal_6_2_2_1
    | Literal_6_2_2 ',' Literal_6_2_2_1
Literal_6_2_2_1 : expr '=>' expr
/usr/local/src/monte/docs/source/custom-guards.rst:31: WARNING: unknown document: container
None:None: WARNING: undefined label: auditors (if the link has no caption the label must precede a section header)
/usr/local/src/monte/docs/source/intro.rst:54: WARNING: undefined label: auditors (if the link has no caption the label must precede a section header)
