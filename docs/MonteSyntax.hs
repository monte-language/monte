
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
    prim_4 = (tok "(") *> expr <* (tok ")")

{-
HideExpr ::= Brackets("{", ZeroOrMore(NonTerminal('expr'), ';'), "}")
-}
hideExpr = (tok "{") *> hideExpr_2 <* (tok "}")
  where
    hideExpr_2 = hideExpr_2_1
      <|> hideExpr_2_2
    hideExpr_2_1 = 
    hideExpr_2_2 = expr
      <|> hideExpr_2_2 (tok ";") expr

{-
NounExpr ::= Choice(0, "IDENTIFIER", Sequence(Sigil("::", ".String.")))
-}
nounExpr = (tok "IDENTIFIER")
  <|> nounExpr_2
  where
    nounExpr_2 = nounExpr_2_1
    nounExpr_2_1 = (tok "::") *> parseString

{-
ListExpr ::= Brackets("[", ZeroOrMore(NonTerminal('expr'), ','), "]")
-}
listExpr = (tok "[") *> listExpr_2 <* (tok "]")
  where
    listExpr_2 = listExpr_2_1
      <|> listExpr_2_2
    listExpr_2_1 = 
    listExpr_2_2 = expr
      <|> listExpr_2_2 (tok ",") expr

{-
MapExpr ::= Brackets("[",
         OneOrMore(Sequence(NonTerminal('expr'),
                            Sigil("=>", NonTerminal('expr'))),
                   ','), "]")
-}
mapExpr = (tok "[") *> mapExpr_2 <* (tok "]")
  where
    mapExpr_2 = mapExpr_2_1
      <|> mapExpr_2 (tok ",") mapExpr_2_1
    mapExpr_2_1 = expr mapExpr_2_1_2
    mapExpr_2_1_2 = (tok "=>") *> expr

{-
LiteralExpr ::= Choice(0,
       Terminal('.String.'),
       Terminal('.int.'),
       Terminal('.float64.'),
       Terminal('.char.'))
-}
literalExpr = parseString
  <|> parseint
  <|> parsefloat64
  <|> parsechar
