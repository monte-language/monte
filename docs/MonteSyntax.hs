
{-
guardOpt ::= Maybe(Sigil(':',
 Choice(
     0,
     Ap('GetExpr',
        Ap('NounExpr', 'IDENTIFIER'),
        Brackets('[', SepBy(NonTerminal('expr'), ','), ']')),
     Ap('NounExpr', 'IDENTIFIER'),
     Brackets('(', NonTerminal('expr'), ')'))))
-}
guardOpt = optionMaybe guardOpt_1
  where
    guardOpt_1 = ((symbol ":") *> guardOpt_1_2)
    guardOpt_1_2 = guardOpt_1_2_1
      <|> guardOpt_1_2_2
      <|> guardOpt_1_2_3
    guardOpt_1_2_1 = GetExpr <$> guardOpt_1_2_1_1 <*> guardOpt_1_2_1_2
    guardOpt_1_2_1_1 = NounExpr <$> parseIdentifier
    guardOpt_1_2_1_2 = ((bra "[") *> guardOpt_1_2_1_2_2 <* (ket "]"))
    guardOpt_1_2_1_2_2 = (sepBy expr (symbol ","))
    guardOpt_1_2_2 = NounExpr <$> parseIdentifier
    guardOpt_1_2_3 = ((bra "(") *> expr <* (ket ")"))

{-
DefExpr ::= Ap('DefExpr', Sigil('def', NonTerminal('pattern')),
         Maybe(Sigil("exit", NonTerminal('order'))),
         Sigil(":=", NonTerminal('assign')))
-}
defExpr = DefExpr <$> defExpr_1 <*> defExpr_2 <*> defExpr_3
  where
    defExpr_1 = ((symbol "def") *> pattern)
    defExpr_2 = optionMaybe defExpr_2_1
    defExpr_2_1 = ((symbol "exit") *> order)
    defExpr_3 = ((symbol ":=") *> assign)

{-
calls ::= Ap('callExpr',
    NonTerminal('prim'),
    SepBy(
      Choice(0,
        Ap('Right',
          Choice(0,
            Ap('Right', NonTerminal('call')),
            Ap('Left', NonTerminal('send')))),
        Ap('Left', NonTerminal('index')))),
    Maybe(NonTerminal('curryTail')))
-}
calls = callExpr <$> prim <*> calls_2 <*> calls_3
  where
    calls_2 = (many0 calls_2_1_1)
    calls_2_1_1 = calls_2_1_1_1
      <|> calls_2_1_1_2
    calls_2_1_1_1 = Right <$> calls_2_1_1_1_1
    calls_2_1_1_1_1 = calls_2_1_1_1_1_1
      <|> calls_2_1_1_1_1_2
    calls_2_1_1_1_1_1 = Right <$> call
    calls_2_1_1_1_1_2 = Left <$> send
    calls_2_1_1_2 = Left <$> index
    calls_3 = optionMaybe curryTail

{-
call ::= Ap('pair', Maybe(Sigil(".", NonTerminal('verb'))), NonTerminal('argList'))
-}
call = pair <$> call_1 <*> argList
  where
    call_1 = optionMaybe call_1_1
    call_1_1 = ((symbol ".") *> verb)

{-
send ::= Sigil("<-", Ap('pair', Maybe(NonTerminal('verb')), NonTerminal('argList')))
-}
send = ((symbol "<-") *> send_2)
  where
    send_2 = pair <$> send_2_1 <*> argList
    send_2_1 = optionMaybe verb

{-
curryTail ::= Choice(0,
  Ap('Right', Sigil(".", NonTerminal('verb'))),
  Ap('Left', Sigil("<-", NonTerminal('verb'))))
-}
curryTail = curryTail_1
  <|> curryTail_2
  where
    curryTail_1 = Right <$> curryTail_1_1
    curryTail_1_1 = ((symbol ".") *> verb)
    curryTail_2 = Left <$> curryTail_2_1
    curryTail_2_1 = ((symbol "<-") *> verb)

{-
index ::= Brackets("[", SepBy(NonTerminal('expr'), ','), "]")
-}
index = ((bra "[") *> index_2 <* (ket "]"))
  where
    index_2 = (sepBy expr (symbol ","))

{-
verb ::= Choice(0, "IDENTIFIER", ".String.")
-}
verb = parseIdentifier
  <|> parseString

{-
argList ::= Brackets("(", SepBy(NonTerminal('expr'), ","), ")")
-}
argList = ((bra "(") *> argList_2 <* (ket ")"))
  where
    argList_2 = (sepBy expr (symbol ","))

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
  Ap('BinaryExpr', NonTerminal('prefix'),
           "**", NonTerminal('order')),
  Ap('BinaryExpr', NonTerminal('prefix'),
           Choice(0, "*", "/", "//", "%"), NonTerminal('order')),
  Ap('BinaryExpr', NonTerminal('prefix'),
           Choice(0, "+", "-"), NonTerminal('order')),
  Ap('BinaryExpr', NonTerminal('prefix'),
           Choice(0, "<<", ">>"), NonTerminal('order')))
-}
binaryExpr = binaryExpr_1
  <|> binaryExpr_2
  <|> binaryExpr_3
  <|> binaryExpr_4
  where
    binaryExpr_1 = BinaryExpr <$> prefix <*> (symbol "**") <*> order
    binaryExpr_2 = BinaryExpr <$> prefix <*> binaryExpr_2_2 <*> order
    binaryExpr_2_2 = (symbol "*")
      <|> (symbol "/")
      <|> (symbol "//")
      <|> (symbol "%")
    binaryExpr_3 = BinaryExpr <$> prefix <*> binaryExpr_3_2 <*> order
    binaryExpr_3_2 = (symbol "+")
      <|> (symbol "-")
    binaryExpr_4 = BinaryExpr <$> prefix <*> binaryExpr_4_2 <*> order
    binaryExpr_4_2 = (symbol "<<")
      <|> (symbol ">>")

{-
CompareExpr ::= Ap('CompareExpr', NonTerminal('prefix'),
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
RangeExpr ::= Ap('RangeExpr', NonTerminal('prefix'),
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
    prim_4 = ((bra "(") *> expr <* (ket ")"))

{-
HideExpr ::= Ap('HideExpr',
   Brackets("{", SepBy(NonTerminal('expr'), ';', fun='wrapSequence'), "}"))
-}
hideExpr = HideExpr <$> hideExpr_1
  where
    hideExpr_1 = ((bra "{") *> hideExpr_1_2 <* (ket "}"))
    hideExpr_1_2 = (wrapSequence expr (symbol ";"))

{-
NounExpr ::= Ap('NounExpr', Choice(0, "IDENTIFIER", Sigil("::", ".String.")))
-}
nounExpr = NounExpr <$> nounExpr_1
  where
    nounExpr_1 = parseIdentifier
      <|> nounExpr_1_2
    nounExpr_1_2 = ((symbol "::") *> parseString)

{-
FinalPatt ::= Ap('FinalPatt', Choice(0, "IDENTIFIER", Sigil("::", ".String.")),
         NonTerminal('guardOpt'))
-}
finalPatt = FinalPatt <$> finalPatt_1 <*> guardOpt
  where
    finalPatt_1 = parseIdentifier
      <|> finalPatt_1_2
    finalPatt_1_2 = ((symbol "::") *> parseString)

{-
quasiliteral ::= Ap('QuasiParserExpr',
 Maybe(Terminal("IDENTIFIER")),
 Brackets('`',
 SepBy(
     Choice(0,
       Ap('Left', Terminal('QUASI_TEXT')),
       Ap('Right',
         Choice(0,
           Ap('NounExpr', Terminal('DOLLAR_IDENT')),
           Brackets('${', NonTerminal('expr'), '}'))))),
 '`'))
-}
quasiliteral = QuasiParserExpr <$> quasiliteral_1 <*> quasiliteral_2
  where
    quasiliteral_1 = optionMaybe parseIdentifier
    quasiliteral_2 = ((bra "`") *> quasiliteral_2_2 <* (ket "`"))
    quasiliteral_2_2 = (many0 quasiliteral_2_2_1_1)
    quasiliteral_2_2_1_1 = quasiliteral_2_2_1_1_1
      <|> quasiliteral_2_2_1_1_2
    quasiliteral_2_2_1_1_1 = Left <$> parseQuasiText
    quasiliteral_2_2_1_1_2 = Right <$> quasiliteral_2_2_1_1_2_1
    quasiliteral_2_2_1_1_2_1 = quasiliteral_2_2_1_1_2_1_1
      <|> quasiliteral_2_2_1_1_2_1_2
    quasiliteral_2_2_1_1_2_1_1 = NounExpr <$> parseDollarIdent
    quasiliteral_2_2_1_1_2_1_2 = ((bra "${") *> expr <* (ket "}"))

{-
IntExpr ::= Ap('IntExpr', Terminal(".int."))
-}
intExpr = IntExpr <$> parseint

{-
DoubleExpr ::= Ap('DoubleExpr', Terminal(".float64."))
-}
doubleExpr = DoubleExpr <$> parsefloat64

{-
CharExpr ::= Ap('CharExpr', Terminal(".char."))
-}
charExpr = CharExpr <$> parseChar

{-
StrExpr ::= Ap('StrExpr', Terminal(".String."))
-}
strExpr = StrExpr <$> parseString

{-
ListExpr ::= Ap('ListExpr', Brackets("[", SepBy(NonTerminal('expr'), ','), "]"))
-}
listExpr = ListExpr <$> listExpr_1
  where
    listExpr_1 = ((bra "[") *> listExpr_1_2 <* (ket "]"))
    listExpr_1_2 = (sepBy expr (symbol ","))

{-
MapExpr ::= Ap('MapExpr',
  Brackets("[",
           SepBy(Ap('pair', NonTerminal('expr'),
                            Sigil("=>", NonTerminal('expr'))),
                 ','),
           "]"))
-}
mapExpr = MapExpr <$> mapExpr_1
  where
    mapExpr_1 = ((bra "[") *> mapExpr_1_2 <* (ket "]"))
    mapExpr_1_2 = (sepBy mapExpr_1_2_1_1 (symbol ","))
    mapExpr_1_2_1_1 = pair <$> expr <*> mapExpr_1_2_1_1_2
    mapExpr_1_2_1_1_2 = ((symbol "=>") *> expr)

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
