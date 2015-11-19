
{-
DefExpr ::= Sequence(Sigil('def', NonTerminal('pattern')),
         Optional(Sigil("exit", NonTerminal('order'))),
         Sigil(":=", NonTerminal('assign')))
-}
defExpr = DefExpr <$> defExpr_1 <*> defExpr_2 <*> defExpr_3
  where
    defExpr_1 = ((symbol "def") *> pattern)
    defExpr_2 = defExpr_2_1
      <|> defExpr_2_2
    defExpr_2_1 = 
    defExpr_2_2 = ((symbol "exit") *> order)
    defExpr_3 = ((symbol ":=") *> assign)

{-
order ::= Choice(0,
  NonTerminal('BinaryExpr'),
  NonTerminal('RangeExpr'),
  NonTerminal('CompareExpr'),
  NonTerminal('prefix'))
-}
order = binaryExpr
  <|> rangeExpr
  <|> compareExpr
  <|> prefix

{-
BinaryExpr ::= Choice(0,
  Sequence(NonTerminal('prefix'),
           "**", NonTerminal('order')),
  Sequence(NonTerminal('prefix'),
           Choice(0, "*", "/", "//", "%"), NonTerminal('order')),
  Sequence(NonTerminal('prefix'),
           Choice(0, "+", "-"), NonTerminal('order')),
  Sequence(NonTerminal('prefix'),
           Choice(0, "<<", ">>"), NonTerminal('order')))
-}
binaryExpr = BinaryExpr <$> binaryExpr_1
  <|> BinaryExpr <$> binaryExpr_2
  <|> BinaryExpr <$> binaryExpr_3
  <|> BinaryExpr <$> binaryExpr_4
  where
    binaryExpr_1 = prefix (symbol "**") order
    binaryExpr_2 = prefix binaryExpr_2_2 order
    binaryExpr_2_2 = (symbol "*")
      <|> (symbol "/")
      <|> (symbol "//")
      <|> (symbol "%")
    binaryExpr_3 = prefix binaryExpr_3_2 order
    binaryExpr_3_2 = (symbol "+")
      <|> (symbol "-")
    binaryExpr_4 = prefix binaryExpr_4_2 order
    binaryExpr_4_2 = (symbol "<<")
      <|> (symbol ">>")

{-
CompareExpr ::= Sequence(NonTerminal('prefix'),
         Choice(0, ">", "<", ">=", "<=", "<=>"), NonTerminal('order'))
-}
compareExpr = CompareExpr <$> prefix <*> compareExpr_2 <*> order
  where
    compareExpr_2 = (symbol ">")
      <|> (symbol "<")
      <|> (symbol ">=")
      <|> (symbol "<=")
      <|> (symbol "<=>")

{-
RangeExpr ::= Sequence(NonTerminal('prefix'),
         Choice(0, "..", "..!"), NonTerminal('order'))
-}
rangeExpr = RangeExpr <$> prefix <*> rangeExpr_2 <*> order
  where
    rangeExpr_2 = (symbol "..")
      <|> (symbol "..!")

{-
prim ::= Choice(
 0,
 NonTerminal('LiteralExpr'),
 NonTerminal('quasiliteral'),
 NonTerminal('NounExpr'),
 Brackets("(", NonTerminal('expr'), ")"),
 NonTerminal('HideExpr'),
 NonTerminal('MapComprehensionExpr'),
 NonTerminal('ListComprehensionExpr'),
 NonTerminal('MapExpr'),
 NonTerminal('ListExpr'))
-}
prim = literalExpr
  <|> quasiliteral
  <|> nounExpr
  <|> prim_4
  <|> hideExpr
  <|> mapComprehensionExpr
  <|> listComprehensionExpr
  <|> mapExpr
  <|> listExpr
  where
    prim_4 = ((symbol "(") *> expr <* (symbol ")"))

{-
HideExpr ::= Brackets("{", SepBy(NonTerminal('expr'), ';', fun='wrapSequence'), "}")
-}
hideExpr = HideExpr <$> ((symbol "{") *> hideExpr_2 <* (symbol "}"))
  where
    hideExpr_2 = (wrapSequence expr (symbol ";"))

{-
NounExpr ::= Choice(0, "IDENTIFIER", Sigil("::", ".String."))
-}
nounExpr = NounExpr <$> parseIdentifier
  <|> NounExpr <$> nounExpr_2
  where
    nounExpr_2 = ((symbol "::") *> parseString)

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
FinalPatt ::= Sequence(Choice(0, "IDENTIFIER", Sigil("::", ".String.")),
         NonTerminal('guardOpt'))
-}
finalPatt = FinalPatt <$> finalPatt_1 <*> guardOpt
  where
    finalPatt_1 = parseIdentifier
      <|> finalPatt_1_2
    finalPatt_1_2 = ((symbol "::") *> parseString)

{-
IntExpr ::= Sequence(Terminal(".int."))
-}
intExpr = IntExpr <$> parseint

{-
DoubleExpr ::= Sequence(Terminal(".float64."))
-}
doubleExpr = DoubleExpr <$> parsefloat64

{-
CharExpr ::= Sequence(Terminal(".char."))
-}
charExpr = CharExpr <$> parseChar

{-
StrExpr ::= Sequence(Terminal(".String."))
-}
strExpr = StrExpr <$> parseString

{-
ListExpr ::= Brackets("[", SepBy(NonTerminal('expr'), ','), "]")
-}
listExpr = ListExpr <$> ((symbol "[") *> listExpr_2 <* (symbol "]"))
  where
    listExpr_2 = (sepBy expr (symbol ","))

{-
MapExpr ::= Brackets("[",
         SepBy(Pair(NonTerminal('expr'), "=>", NonTerminal('expr')),
               ','),
         "]")
-}
mapExpr = MapExpr <$> ((symbol "[") *> mapExpr_2 <* (symbol "]"))
  where
    mapExpr_2 = (sepBy mapExpr_2_2_1 (symbol ","))
    mapExpr_2_2_1 = pair <$> expr <*> ((symbol "=>") *> expr)

{-
LiteralExpr ::= Choice(0,
       NonTerminal('StrExpr'),
       NonTerminal('IntExpr'),
       NonTerminal('DoubleExpr'),
       NonTerminal('CharExpr'))
-}
literalExpr = strExpr
  <|> intExpr
  <|> doubleExpr
  <|> charExpr
