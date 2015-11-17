
{-
guardOpt ::= Optional(Sequence(
 ':',
 Choice(
     0,
     Sequence('IDENTIFIER',
                 Optional(Sequence('[',
                                   OneOrMore(NonTerminal('expr'), ','),
                                   ']'))),
     Sequence('(', NonTerminal('expr'), ')'))))
-}
guardOpt = guardOpt_1
  <|> guardOpt_2
  where
    guardOpt_1 = 
    guardOpt_2 = (tok ":") guardOpt_2_2
    guardOpt_2_2 = guardOpt_2_2_1
      <|> guardOpt_2_2_2
    guardOpt_2_2_1 = (tok "IDENTIFIER") guardOpt_2_2_1_2
    guardOpt_2_2_1_2 = guardOpt_2_2_1_2_1
      <|> guardOpt_2_2_1_2_2
    guardOpt_2_2_1_2_1 = 
    guardOpt_2_2_1_2_2 = (tok "[") guardOpt_2_2_1_2_2_2 (tok "]")
    guardOpt_2_2_1_2_2_2 = expr
      <|> guardOpt_2_2_1_2_2_2 (tok ",") expr
    guardOpt_2_2_2 = (tok "(") expr (tok ")")

{-
interface ::= Sequence(
 "interface",
 NonTerminal('namePattern'),
 Optional(Sequence("guards", NonTerminal('pattern'))),
 Optional(Sequence("extends", OneOrMore(NonTerminal('order'), ','))),
 Comment("implements_@@"), Comment("msgs@@"))
-}
interface = (tok "interface") namePattern interface_3 interface_4
  where
    interface_3 = interface_3_1
      <|> interface_3_2
    interface_3_1 = 
    interface_3_2 = (tok "guards") pattern
    interface_4 = interface_4_1
      <|> interface_4_2
    interface_4_1 = 
    interface_4_2 = (tok "extends") interface_4_2_2
    interface_4_2_2 = order
      <|> interface_4_2_2 (tok ",") order

{-
FunctionExpr ::= Sequence('def', '(', ZeroOrMore(NonTerminal('pattern'), ','), ')',
  NonTerminal('block'))
-}
functionExpr = FunctionExpr <$> (tok "def") <*> (tok "(") <*> functionExpr_3 <*> (tok ")") <*> block
  where
    functionExpr_3 = functionExpr_3_1
      <|> functionExpr_3_2
    functionExpr_3_1 = 
    functionExpr_3_2 = pattern
      <|> functionExpr_3_2 (tok ",") pattern

{-
ObjectExpr ::= Sequence(
 "object",
 Choice(0, Sequence("bind", NonTerminal('name')),
        "_",
        NonTerminal('name')),
 NonTerminal('guardOpt'), Comment("objectExpr"))
-}
objectExpr = ObjectExpr <$> (tok "object") <*> objectExpr_2 <*> guardOpt
  where
    objectExpr_2 = objectExpr_2_1
      <|> (tok "_")
      <|> name
    objectExpr_2_1 = (tok "bind") name

{-
objectExpr ::= Sequence(
 Optional(Sequence('extends', NonTerminal('order'))),
 NonTerminal('auditors'),
 '{', ZeroOrMore(NonTerminal('objectScript'), ';'), '}')
-}
objectExpr = objectExpr_1 auditors (tok "{") objectExpr_4 (tok "}")
  where
    objectExpr_1 = objectExpr_1_1
      <|> objectExpr_1_2
    objectExpr_1_1 = 
    objectExpr_1_2 = (tok "extends") order
    objectExpr_4 = objectExpr_4_1
      <|> objectExpr_4_2
    objectExpr_4_1 = 
    objectExpr_4_2 = objectScript
      <|> objectExpr_4_2 (tok ";") objectScript

{-
objectScript ::= Sequence(
 Optional(NonTerminal('doco')),
 Choice(0, "pass", ZeroOrMore("@@meth")),
 Choice(0, "pass", ZeroOrMore(NonTerminal('matchers'))))
-}
objectScript = objectScript_1 objectScript_2 objectScript_3
  where
    objectScript_1 = objectScript_1_1
      <|> doco
    objectScript_1_1 = 
    objectScript_2 = (tok "pass")
      <|> objectScript_2_2
    objectScript_2_2 = objectScript_2_2_1
      <|> objectScript_2_2_2
    objectScript_2_2_1 = 
    objectScript_2_2_2 = (tok "@@meth")
      <|> objectScript_2_2_2 objectScript_2_2_2_2 (tok "@@meth")
    objectScript_2_2_2_2 = 
    objectScript_3 = (tok "pass")
      <|> objectScript_3_2
    objectScript_3_2 = objectScript_3_2_1
      <|> objectScript_3_2_2
    objectScript_3_2_1 = 
    objectScript_3_2_2 = matchers
      <|> objectScript_3_2_2 objectScript_3_2_2_2 matchers
    objectScript_3_2_2_2 = 

{-
matchers ::= OneOrMore(Sequence("match",
          NonTerminal('pattern'),
          NonTerminal('block')))
-}
matchers = matchers_1
  <|> matchers matchers_2 matchers_1
  where
    matchers_1 = (tok "match") pattern block
    matchers_2 = 

{-
doco ::= Terminal('.String')
-}

{-
InterfaceExpr ::= Sequence('@@@@@')
-}
interfaceExpr = InterfaceExpr <$> (tok "@@@@@")

{-
IfExpr ::= Sequence(
 "if", "(", NonTerminal('expr'), ")", NonTerminal('block'),
 Optional(Sequence("else", Choice(
     0, Sequence("if", Comment('blockExpr@@')),
     NonTerminal('block')))))
-}
ifExpr = IfExpr <$> (tok "if") <*> (tok "(") <*> expr <*> (tok ")") <*> block <*> ifExpr_6
  where
    ifExpr_6 = ifExpr_6_1
      <|> ifExpr_6_2
    ifExpr_6_1 = 
    ifExpr_6_2 = (tok "else") ifExpr_6_2_2
    ifExpr_6_2_2 = ifExpr_6_2_2_1
      <|> block
    ifExpr_6_2_2_1 = (tok "if")

{-
ForExpr ::= Sequence(
 "for",
 NonTerminal('pattern'),
 Optional(Sequence("=>", NonTerminal('pattern'))),
 "in", NonTerminal('comp'),
 NonTerminal('blockCatch'))
-}
forExpr = ForExpr <$> (tok "for") <*> pattern <*> forExpr_3 <*> (tok "in") <*> comp <*> blockCatch
  where
    forExpr_3 = forExpr_3_1
      <|> forExpr_3_2
    forExpr_3_1 = 
    forExpr_3_2 = (tok "=>") pattern

{-
blockCatch ::= Sequence(
 NonTerminal('block'),
 Optional(
     Sequence("catch", NonTerminal('pattern'),
              NonTerminal('block'))))
-}
blockCatch = block blockCatch_2
  where
    blockCatch_2 = blockCatch_2_1
      <|> blockCatch_2_2
    blockCatch_2_1 = 
    blockCatch_2_2 = (tok "catch") pattern block

{-
WhileExpr ::= Sequence(
 "while", "(", NonTerminal('expr'), ")", NonTerminal('blockCatch'))
-}
whileExpr = WhileExpr <$> (tok "while") <*> (tok "(") <*> expr <*> (tok ")") <*> blockCatch

{-
SwitchExpr ::= Sequence(
 "switch", "(", NonTerminal('expr'), ")",
 "{", NonTerminal('matchers'), "}")
-}
switchExpr = SwitchExpr <$> (tok "switch") <*> (tok "(") <*> expr <*> (tok ")") <*> (tok "{") <*> matchers <*> (tok "}")

{-
matchers ::= OneOrMore(Sequence("match",
          NonTerminal('pattern'),
          NonTerminal('block')))
-}
matchers = matchers_1
  <|> matchers matchers_2 matchers_1
  where
    matchers_1 = (tok "match") pattern block
    matchers_2 = 

{-
EscapeExpr ::= Sequence(
 "escape", NonTerminal('pattern'),
 NonTerminal('blockCatch'))
-}
escapeExpr = EscapeExpr <$> (tok "escape") <*> pattern <*> blockCatch

{-
TryExpr ::= Sequence(
 "try", NonTerminal('block'), NonTerminal('catchers'))
-}
tryExpr = TryExpr <$> (tok "try") <*> block <*> catchers

{-
catchers ::= Sequence(
 ZeroOrMore(Sequence("catch",
                     NonTerminal('pattern'),
                     NonTerminal('block'))),
 Optional(Sequence("finally", NonTerminal('block'))))
-}
catchers = catchers_1 catchers_2
  where
    catchers_1 = catchers_1_1
      <|> catchers_1_2
    catchers_1_1 = 
    catchers_1_2 = catchers_1_2_1
      <|> catchers_1_2 catchers_1_2_2 catchers_1_2_1
    catchers_1_2_1 = (tok "catch") pattern block
    catchers_1_2_2 = 
    catchers_2 = catchers_2_1
      <|> catchers_2_2
    catchers_2_1 = 
    catchers_2_2 = (tok "finally") block

{-
WhenExpr ::= Sequence(
 "when",
 "(", OneOrMore(NonTerminal('expr'), ','), ")",
 "->", NonTerminal('block'),
 NonTerminal('catchers'))
-}
whenExpr = WhenExpr <$> (tok "when") <*> (tok "(") <*> whenExpr_3 <*> (tok ")") <*> (tok "->") <*> block <*> catchers
  where
    whenExpr_3 = expr
      <|> whenExpr_3 (tok ",") expr

{-
LambdaExpr ::= Sequence(
 "fn",
 ZeroOrMore(NonTerminal('pattern'), ','),
 NonTerminal('block'))
-}
lambdaExpr = LambdaExpr <$> (tok "fn") <*> lambdaExpr_2 <*> block
  where
    lambdaExpr_2 = lambdaExpr_2_1
      <|> lambdaExpr_2_2
    lambdaExpr_2_1 = 
    lambdaExpr_2_2 = pattern
      <|> lambdaExpr_2_2 (tok ",") pattern

{-
MetaExpr ::= Sequence(
 "meta", ".",
 Choice(0,
        Sequence("context", "(", ")"),
        Sequence("getState", "(", ")")))
-}
metaExpr = MetaExpr <$> (tok "meta") <*> (tok ".") <*> metaExpr_3
  where
    metaExpr_3 = metaExpr_3_1
      <|> metaExpr_3_2
    metaExpr_3_1 = (tok "context") (tok "(") (tok ")")
    metaExpr_3_2 = (tok "getState") (tok "(") (tok ")")

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
block = (tok "{") block_2 (tok "}")
  where
    block_2 = block_2_1
      <|> (tok "pass")
    block_2_1 = block_2_1_1
      <|> block_2_1_2
    block_2_1_1 = 
    block_2_1_2 = block_2_1_2_1
      <|> block_2_1_2 (tok ";") block_2_1_2_1
    block_2_1_2_1 = blockExpr
      <|> expr

{-
blockExpr ::= Choice(
 0,
 NonTerminal('FunctionExpr'),
 NonTerminal('ObjectExpr'),
 NonTerminal('bind'),
 NonTerminal('DefExpr'),
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
blockExpr = functionExpr
  <|> objectExpr
  <|> bind
  <|> defExpr
  <|> interfaceExpr
  <|> ifExpr
  <|> forExpr
  <|> whileExpr
  <|> switchExpr
  <|> escapeExpr
  <|> tryExpr
  <|> whenExpr
  <|> lambdaExpr
  <|> metaExpr

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
expr = assign
  <|> expr_2
  where
    expr_2 = expr_2_1 expr_2_2
    expr_2_1 = (tok "continue")
      <|> (tok "break")
      <|> (tok "return")
    expr_2_2 = expr_2_2_1
      <|> (tok ";")
      <|> blockExpr
    expr_2_2_1 = (tok "(") (tok ")")

{-
bind ::= Sequence(
 "bind",
 NonTerminal('name'),
 NonTerminal('guardOpt'), Comment("objectExpr@@"))
-}
bind = (tok "bind") name guardOpt

{-
name ::= Choice(0, "IDENTIFIER", Sequence("::", ".String."))
-}
name = (tok "IDENTIFIER")
  <|> name_2
  where
    name_2 = (tok "::") (tok ".String.")

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
comprehension = comprehension_1
  <|> comprehension_2
  where
    comprehension_1 = pattern (tok "in") iter expr
    comprehension_2 = pattern (tok "=>") pattern (tok "in") iter expr (tok "=>") expr

{-
iter ::= Sequence(
 NonTerminal('order'),
 Optional(Sequence("if", NonTerminal('comp'))))
-}
iter = order iter_2
  where
    iter_2 = iter_2_1
      <|> iter_2_2
    iter_2_1 = 
    iter_2_2 = (tok "if") comp

{-
module ::= Sequence(
 Optional(Sequence("imports",
                   NonTerminal('imports'),
                   Optional(NonTerminal('exports')))),
 NonTerminal('block'))
-}
module = module_1 block
  where
    module_1 = module_1_1
      <|> module_1_2
    module_1_1 = 
    module_1_2 = (tok "imports") imports module_1_2_3
    module_1_2_3 = module_1_2_3_1
      <|> exports
    module_1_2_3_1 = 

{-
imports ::= ZeroOrMore(NonTerminal('namedPattern'))
-}
imports = imports_1
  <|> imports_2
  where
    imports_1 = 
    imports_2 = namedPattern
      <|> imports_2 imports_2_2 namedPattern
    imports_2_2 = 

{-
exports ::= Sequence("exports", "(", ZeroOrMore(NonTerminal('name')), ")")
-}
exports = (tok "exports") (tok "(") exports_3 (tok ")")
  where
    exports_3 = exports_3_1
      <|> exports_3_2
    exports_3_1 = 
    exports_3_2 = name
      <|> exports_3_2 exports_3_2_2 name
    exports_3_2_2 = 

{-
DefExpr ::= Sequence('def',
          NonTerminal('pattern'),
          Optional(Sequence("exit", NonTerminal('order'))),
          Sequence(":=", NonTerminal('assign')))
-}
defExpr = DefExpr <$> (tok "def") <*> pattern <*> defExpr_3 <*> defExpr_4
  where
    defExpr_3 = defExpr_3_1
      <|> defExpr_3_2
    defExpr_3_1 = 
    defExpr_3_2 = (tok "exit") order
    defExpr_4 = (tok ":=") assign

{-
ForwardExpr ::= Sequence('def',
          NonTerminal('pattern'),
          Optional(Sequence("exit", NonTerminal('order'))),
          Optional(Sequence(":=", NonTerminal('assign'))))
-}
forwardExpr = ForwardExpr <$> (tok "def") <*> pattern <*> forwardExpr_3 <*> forwardExpr_4
  where
    forwardExpr_3 = forwardExpr_3_1
      <|> forwardExpr_3_2
    forwardExpr_3_1 = 
    forwardExpr_3_2 = (tok "exit") order
    forwardExpr_4 = forwardExpr_4_1
      <|> forwardExpr_4_2
    forwardExpr_4_1 = 
    forwardExpr_4_2 = (tok ":=") assign

{-
call ::= Sequence(
 NonTerminal('calls'),
 Optional(Sequence(NonTerminal('curry'))))
-}
call = calls call_2
  where
    call_2 = call_2_1
      <|> call_2_2
    call_2_1 = 
    call_2_2 = curry

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
calls = prim
  <|> calls_2
  <|> getExpr
  where
    calls_2 = calls calls_2_2 calls_2_3
    calls_2_2 = calls_2_2_1
      <|> calls_2_2_2
    calls_2_2_1 = 
    calls_2_2_2 = calls_2_2_2_1 calls_2_2_2_2
    calls_2_2_2_1 = (tok ".")
      <|> (tok "<-")
    calls_2_2_2_2 = (tok "IDENTIFIER")
      <|> (tok ".String.")
    calls_2_3 = (tok "(") calls_2_3_2 (tok ")")
    calls_2_3_2 = calls_2_3_2_1
      <|> calls_2_3_2_2
    calls_2_3_2_1 = 
    calls_2_3_2_2 = expr
      <|> calls_2_3_2_2 (tok ",") expr

{-
getExpr ::= Sequence(
 NonTerminal('calls'),
 Sequence("[", ZeroOrMore(NonTerminal('expr'), ','), "]"))
-}
getExpr = calls getExpr_2
  where
    getExpr_2 = (tok "[") getExpr_2_2 (tok "]")
    getExpr_2_2 = getExpr_2_2_1
      <|> getExpr_2_2_2
    getExpr_2_2_1 = 
    getExpr_2_2_2 = expr
      <|> getExpr_2_2_2 (tok ",") expr

{-
curry ::= Sequence(
 Choice(0, '.', '<-'),
 Choice(0, "IDENTIFIER", ".String."))
-}
curry = curry_1 curry_2
  where
    curry_1 = (tok ".")
      <|> (tok "<-")
    curry_2 = (tok "IDENTIFIER")
      <|> (tok ".String.")

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
comp = order comp_2
  where
    comp_2 = comp_2_1
      <|> comp_2_2
    comp_2_1 = 
    comp_2_2 = comp_2_2_1 comp
    comp_2_2_1 = comp_2_2_1_1
      <|> comp_2_2_1_2
      <|> (tok "&!")
      <|> comp_2_2_1_4
    comp_2_2_1_1 = (tok "=~")
      <|> (tok "!~")
    comp_2_2_1_2 = (tok "==")
      <|> (tok "!=")
    comp_2_2_1_4 = (tok "^")
      <|> (tok "&")
      <|> (tok "|")

{-
logical ::= Sequence(
 NonTerminal('comp'),
 Optional(Sequence(Choice(0, '||', '&&'), NonTerminal('logical'))))
-}
logical = comp logical_2
  where
    logical_2 = logical_2_1
      <|> logical_2_2
    logical_2_1 = 
    logical_2_2 = logical_2_2_1 logical
    logical_2_2_1 = (tok "||")
      <|> (tok "&&")

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
order = prefix order_2
  where
    order_2 = order_2_1
      <|> order_2_2
    order_2_1 = 
    order_2_2 = order_2_2_1 order
    order_2_2_1 = (tok "**")
      <|> order_2_2_1_2
      <|> order_2_2_1_3
      <|> order_2_2_1_4
      <|> order_2_2_1_5
      <|> order_2_2_1_6
    order_2_2_1_2 = (tok "*")
      <|> (tok "/")
      <|> (tok "//")
      <|> (tok "%")
    order_2_2_1_3 = (tok "+")
      <|> (tok "-")
    order_2_2_1_4 = (tok "<<")
      <|> (tok ">>")
    order_2_2_1_5 = (tok "..")
      <|> (tok "..!")
    order_2_2_1_6 = (tok ">")
      <|> (tok "<")
      <|> (tok ">=")
      <|> (tok "<=")
      <|> (tok "<=>")

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
assign = patternBinding
  <|> assign_2
  <|> assign_3
  <|> logical
  where
    assign_2 = assign_2_1 pattern (tok ":=") assign
    assign_2_1 = (tok "var")
      <|> (tok "bind")
    assign_3 = lval (tok ":=") assign

{-
ForwardDeclaration ::= Sequence('def', NonTerminal('name'))
-}
forwardDeclaration = ForwardDeclaration <$> (tok "def") <*> name

{-
lval ::= Choice(
 0,
 NonTerminal('name'),
 NonTerminal('getExpr'))
-}
lval = name
  <|> getExpr

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
prim = literal
  <|> quasiliteral
  <|> noun
  <|> prim_4
  <|> prim_5
  <|> prim_6
  where
    prim_4 = (tok "(") expr (tok ")")
    prim_5 = (tok "{") prim_5_2 (tok "}")
    prim_5_2 = prim_5_2_1
      <|> prim_5_2_2
    prim_5_2_1 = 
    prim_5_2_2 = expr
      <|> prim_5_2_2 (tok ";") expr
    prim_6 = (tok "[") (tok "for") comprehension (tok "]")

{-
noun ::= Choice(0, "IDENTIFIER", Sequence("::", ".String."))
-}
noun = (tok "IDENTIFIER")
  <|> noun_2
  where
    noun_2 = (tok "::") (tok ".String.")

{-
prefix ::= Choice(
 0,
 NonTerminal('unary'),
 NonTerminal('SlotExpression'),
 NonTerminal('BindingExpression'),
 Sequence(NonTerminal('call'), NonTerminal('guardOpt')))
-}
prefix = unary
  <|> slotExpression
  <|> bindingExpression
  <|> prefix_4
  where
    prefix_4 = call guardOpt

{-
unary ::= Choice(
 0,
 Sequence('-', NonTerminal('prim')),
 Sequence(Choice(0, "~", "!"), NonTerminal('call')))
-}
unary = unary_1
  <|> unary_2
  where
    unary_1 = (tok "-") prim
    unary_2 = unary_2_1 call
    unary_2_1 = (tok "~")
      <|> (tok "!")

{-
SlotExpression ::= Sequence('&', NonTerminal('noun'))
-}
slotExpression = SlotExpression <$> (tok "&") <*> noun

{-
BindingExpression ::= Sequence('&&', NonTerminal('noun'))
-}
bindingExpression = BindingExpression <$> (tok "&&") <*> noun

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
pattern = namePattern
  <|> pattern_2
  <|> quasiLiteralPattern
  <|> viaPattern
  <|> ignorePattern
  <|> listPattern
  <|> mapPattern
  <|> suchThatPattern
  where
    pattern_2 = samePattern
      <|> notSamePattern

{-
namePattern ::= Choice(0,
        NonTerminal('FinalPattern'),
        NonTerminal('VarPattern'),
        NonTerminal('BindPattern'),
        NonTerminal('SlotPattern'),
        NonTerminal('BindingPattern'))
-}
namePattern = finalPattern
  <|> varPattern
  <|> bindPattern
  <|> slotPattern
  <|> bindingPattern

{-
FinalPattern ::= Sequence(Choice(0, "IDENTIFIER", ".String."),
         NonTerminal('guardOpt'))
-}
finalPattern = FinalPattern <$> finalPattern_1 <*> guardOpt
  where
    finalPattern_1 = (tok "IDENTIFIER")
      <|> (tok ".String.")

{-
VarPattern ::= Sequence("var", NonTerminal('name'),
         Optional(NonTerminal('guard')))
-}
varPattern = VarPattern <$> (tok "var") <*> name <*> varPattern_3
  where
    varPattern_3 = varPattern_3_1
      <|> guard
    varPattern_3_1 = 

{-
BindPattern ::= Sequence("bind", NonTerminal('name'),
    Optional(NonTerminal('guard')))
-}
bindPattern = BindPattern <$> (tok "bind") <*> name <*> bindPattern_3
  where
    bindPattern_3 = bindPattern_3_1
      <|> guard
    bindPattern_3_1 = 

{-
SlotPattern ::= Sequence("&", NonTerminal('name'),
    Optional(NonTerminal('guard')))
-}
slotPattern = SlotPattern <$> (tok "&") <*> name <*> slotPattern_3
  where
    slotPattern_3 = slotPattern_3_1
      <|> guard
    slotPattern_3_1 = 

{-
BindingPattern ::= Sequence("&&", NonTerminal('name'))
-}
bindingPattern = BindingPattern <$> (tok "&&") <*> name

{-
IgnorePattern ::= Sequence("_", Optional(NonTerminal('guard')))
-}
ignorePattern = IgnorePattern <$> (tok "_") <*> ignorePattern_2
  where
    ignorePattern_2 = ignorePattern_2_1
      <|> guard
    ignorePattern_2_1 = 

{-
ListPattern ::= Sequence("[",
         ZeroOrMore(NonTerminal('pattern'), ','),
         ']',
         Optional(Sequence("+", NonTerminal('pattern'))))
-}
listPattern = ListPattern <$> (tok "[") <*> listPattern_2 <*> (tok "]") <*> listPattern_4
  where
    listPattern_2 = listPattern_2_1
      <|> listPattern_2_2
    listPattern_2_1 = 
    listPattern_2_2 = pattern
      <|> listPattern_2_2 (tok ",") pattern
    listPattern_4 = listPattern_4_1
      <|> listPattern_4_2
    listPattern_4_1 = 
    listPattern_4_2 = (tok "+") pattern

{-
MapPattern ::= Sequence("[",
         OneOrMore(NonTerminal('mapPatternItem'), ','),
         ']',
         Optional(Sequence("|", NonTerminal('pattern'))))
-}
mapPattern = MapPattern <$> (tok "[") <*> mapPattern_2 <*> (tok "]") <*> mapPattern_4
  where
    mapPattern_2 = mapPatternItem
      <|> mapPattern_2 (tok ",") mapPatternItem
    mapPattern_4 = mapPattern_4_1
      <|> mapPattern_4_2
    mapPattern_4_1 = 
    mapPattern_4_2 = (tok "|") pattern

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
mapPatternItem = mapPatternItem_1 mapPatternItem_2
  where
    mapPatternItem_1 = mapPatternItem_1_1
      <|> mapPatternItem_1_2
    mapPatternItem_1_1 = (tok "=>") namePattern
    mapPatternItem_1_2 = mapPatternItem_1_2_1 (tok "=>") pattern
    mapPatternItem_1_2_1 = mapPatternItem_1_2_1_1
      <|> mapPatternItem_1_2_1_2
    mapPatternItem_1_2_1_1 = (tok ".String.")
      <|> (tok ".int.")
      <|> (tok ".float64.")
      <|> (tok ".char.")
    mapPatternItem_1_2_1_2 = (tok "(") expr (tok ")")
    mapPatternItem_2 = mapPatternItem_2_1
      <|> mapPatternItem_2_2
    mapPatternItem_2_1 = 
    mapPatternItem_2_2 = (tok ":=") order

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
mapItem = mapItem_1
  <|> mapItem_2
  where
    mapItem_1 = (tok "=>") mapItem_1_2
    mapItem_1_2 = mapItem_1_2_1
      <|> mapItem_1_2_2
      <|> name
    mapItem_1_2_1 = (tok "&") name
    mapItem_1_2_2 = (tok "&&") name
    mapItem_2 = expr (tok "=>") expr

{-
SamePattern ::= Sequence("==", NonTerminal('prim'))
-}
samePattern = SamePattern <$> (tok "==") <*> prim

{-
NotSamePattern ::= Sequence("!=", NonTerminal('prim'))
-}
notSamePattern = NotSamePattern <$> (tok "!=") <*> prim

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
quasiliteralPattern = QuasiliteralPattern <$> quasiliteralPattern_1 <*> (tok "`") <*> quasiliteralPattern_3 <*> (tok "`")
  where
    quasiliteralPattern_1 = quasiliteralPattern_1_1
      <|> (tok "IDENTIFIER")
    quasiliteralPattern_1_1 = 
    quasiliteralPattern_3 = quasiliteralPattern_3_1
      <|> quasiliteralPattern_3_2
    quasiliteralPattern_3_1 = 
    quasiliteralPattern_3_2 = quasiliteralPattern_3_2_1
      <|> quasiliteralPattern_3_2 quasiliteralPattern_3_2_2 quasiliteralPattern_3_2_1
    quasiliteralPattern_3_2_1 = quasiliteralPattern_3_2_1_1
    quasiliteralPattern_3_2_1_1 = (tok "@IDENT")
      <|> quasiliteralPattern_3_2_1_1_2
    quasiliteralPattern_3_2_1_1_2 = (tok "@{") pattern (tok "}")
    quasiliteralPattern_3_2_2 = 

{-
ViaPattern ::= Sequence("via", "(", NonTerminal('expr'), ')',
         NonTerminal('pattern'))
-}
viaPattern = ViaPattern <$> (tok "via") <*> (tok "(") <*> expr <*> (tok ")") <*> pattern

{-
SuchThatPattern ::= Sequence(NonTerminal('pattern'), "?", "(", NonTerminal('expr'), ")")
-}
suchThatPattern = SuchThatPattern <$> pattern <*> (tok "?") <*> (tok "(") <*> expr <*> (tok ")")

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
quasiliteral = quasiliteral_1 (tok "`") quasiliteral_3 (tok "`")
  where
    quasiliteral_1 = quasiliteral_1_1
      <|> (tok "IDENTIFIER")
    quasiliteral_1_1 = 
    quasiliteral_3 = quasiliteral_3_1
      <|> quasiliteral_3_2
    quasiliteral_3_1 = 
    quasiliteral_3_2 = quasiliteral_3_2_1
      <|> quasiliteral_3_2 quasiliteral_3_2_2 quasiliteral_3_2_1
    quasiliteral_3_2_1 = quasiliteral_3_2_1_1
    quasiliteral_3_2_1_1 = (tok "$IDENT")
      <|> quasiliteral_3_2_1_1_2
    quasiliteral_3_2_1_1_2 = (tok "${") expr (tok "}")
    quasiliteral_3_2_2 = 

{-
IntExpr ::= Sequence(".int.")
-}
intExpr = IntExpr <$> (tok ".int.")

{-
DoubleExpr ::= Sequence(".float64.")
-}
doubleExpr = DoubleExpr <$> (tok ".float64.")

{-
CharExpr ::= Sequence(".char.")
-}
charExpr = CharExpr <$> (tok ".char.")

{-
StrExpr ::= Sequence(".String.")
-}
strExpr = StrExpr <$> (tok ".String.")

{-
literal ::= Choice(0,
       NonTerminal('IntExpr'),
       NonTerminal('DoubleExpr'),
       NonTerminal('CharExpr'),
       NonTerminal('StringExpr'))
-}
literal = intExpr
  <|> doubleExpr
  <|> charExpr
  <|> stringExpr
/usr/local/src/monte/docs/source/symbols.rst:309: ERROR: Unexpected indentation.
/usr/local/src/monte/docs/source/symbols.rst:317: ERROR: Unknown target name: "guards".
/usr/local/src/monte/docs/source/symbols.rst:317: ERROR: Unknown target name: "extends".
/usr/local/src/monte/docs/source/symbols.rst:317: ERROR: Unknown target name: "implements".
/usr/local/src/monte/docs/source/symbols.rst:317: ERROR: Unknown target name: "guards".
/usr/local/src/monte/docs/source/symbols.rst:317: ERROR: Unknown target name: "extends".
/usr/local/src/monte/docs/source/symbols.rst:317: ERROR: Unknown target name: "implements".
/usr/local/src/monte/docs/source/custom-guards.rst:31: WARNING: unknown document: container
None:None: WARNING: undefined label: auditors (if the link has no caption the label must precede a section header)
/usr/local/src/monte/docs/source/intro.rst:54: WARNING: undefined label: auditors (if the link has no caption the label must precede a section header)
