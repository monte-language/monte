
Monte Grammar
=============

.. note:: Lexical details such as indented blocks are
          not captured in this grammar.

.. todo:: finish grammar productions marked @@.
          Meanwhile, see `monte_parser.mt`__ for details.

__ https://github.com/monte-language/typhon/blob/master/mast/lib/monte/monte_parser.mt

.. productionlist::
   blockExpr: `FunctionExpr` 
   : | `ObjectExpr` 
   : | `bind` 
   : | `def` 
   : | `InterfaceExpr` 
   : | `IfExpr` 
   : | `ForExpr` 
   : | `WhileExpr` 
   : | `SwitchExpr` 
   : | `EscapeExpr` 
   : | `TryExpr` 
   : | `WhenExpr` 
   : | `LambdaExpr` 
   : | `MetaExpr` 
   block:  "{"  (`sequence`  | "pass" ) "}" 
   HideExpr:   "{"  ((`expr`  ";" )+  | /* empty */) "}" 
   IfExpr:  "if"  "("  `expr`  ")"  `block`  [ "else"  ( "if"  /* blockExpr@@ */  | `block` )] 
   SwitchExpr:  "switch"  "("  `expr`  ")"  "{"  `matchers`  "}" 
   matchers: ( "match"  `pattern`  `block`  )+ 
   TryExpr:  "try"  `block`  `catchers` 
   catchers:  [( "catch"  `pattern`  `block`  )+ ]  [ "finally"  `block` ] 
   EscapeExpr:  "escape"  `pattern`  `blockCatch` 
   WhileExpr:  "while"  "("  `expr`  ")"  `blockCatch` 
   ForExpr:  "for"  `pattern`  [ "=>"  `pattern` ]  "in"  `comp`  `blockCatch` 
   blockCatch:  `block`  [ "catch"  `pattern`  `block` ] 
   WhenExpr:  "when"  "("  (`expr`  "," )+  ")"  "->"  `block`  `catchers` 
   LambdaExpr:  "fn"  [(`pattern`  "," )+ ]  `block` 
   def:  "def"  ( ( "bind"  `name`  [`guard` ]  | `name` ) (/* objectFunction@@ */  | `assign` ) | `assign` )
   bind:  "bind"  `name`  [`guard` ]  `objectExpr` 
   ObjectExpr:  "object"  ( "bind"  `name`  | "_"  | `name` ) `objectExpr` 
   objectExpr:  [ "extends"  `order` ]  `auditors`  "{"  [(`objectScript`  ";" )+ ]  "}" 
   objectScript:  [`doco` ]  ("pass"  | [("@@meth"  )+ ] ) ("pass"  | [(`matchers`  )+ ] )
   matchers: ( "match"  `pattern`  `block`  )+ 
   doco: .String.
   FunctionExpr:  "def"  "("  [(`pattern`  "," )+ ]  ")"  `block` 
   InterfaceExpr:  "interface"  `namePatt`  [ "guards"  `pattern` ]  [ "extends"  (`order`  "," )+ ]  /* implements_@@ */  /* msgs@@ */ 
   guardOpt:  ":"  `guard` 
   : | /* empty */
   guard:   IDENTIFIER  "["  ((`expr`  "," )+  | /* empty */) "]" 
   : |  IDENTIFIER
   : |  "("  `expr`  ")" 
   module_header:   "imports"  `StrExpr`   "=~"  ((`namePatt`  )+ ) [`exports` ]  `sequence` 
   exports:  "exports"   "("  ((`name`  "," )+  | /* empty */) ")" 
   sequence: ((`blockExpr`  | `expr` ) ";" )+ 
   : | /* empty */
   assign:   "def"  `pattern`  [ "exit"  `order` ]   ":="  `assign` 
   : |  (`VarPatt`  | `BindPatt` )  /* empty */  ":="  `assign` 
   : |  `lval`   ":="  `assign` 
   : | `VerbAssignExpr` 
   : | `order` 
   lval:   `order`   "["  ((`expr`  "," )+  | /* empty */) "]" 
   : |  `name` 
   VerbAssignExpr:  `lval`   VERB_ASSIGN `assign` 
   logical_or:  `logical_and`  [ "||"  `logical_or` ] 
   logical_and:  `comp`  [ "&&"  `logical_and` ] 
   comp:  `order`  (("=~"  | "!~" ) | ("=="  | "!=" ) | "&!"  | ("^"  | "&"  | "|" )) `comp` 
   : | `order` 
   order: `CompareExpr` 
   : | `RangeExpr` 
   : | `BinaryExpr` 
   : | `prefix` 
   CompareExpr:  `prefix`  (">"  | "<"  | ">="  | "<="  | "<=>" ) `order` 
   RangeExpr:  `prefix`  (.. | ..!) `order` 
   shift:  `prefix`  ("<<"  | ">>" ) `order` 
   additiveExpr:  `multiplicativeExpr`  ("+"  | "-" ) `additiveExpr` 
   multiplicativeExpr:  `exponentiationExpr`  ("*"  | "/"  | "//"  | "%" ) `order` 
   exponentiationExpr:  `prefix`  "**"  `order` 
   prefix:  "-"  `prim` 
   : |  ("~"  | "!" ) `calls` 
   : | `SlotExpr` 
   : | `BindingExpr` 
   : | `CoerceExpr` 
   : | `calls` 
   SlotExpr:   "&"  `name` 
   BindingExpr:   "&&"  `name` 
   MetaExpr:  "meta"  . ( "context"  "("  ")"  |  "getState"  "("  ")" )
   CoerceExpr:  `calls`   ":"  `guard` 
   calls:  `prim`  ((( ( `call`  |  `send` ) |  `index` ) )+ ) [`curryTail` ] 
   call:  [ . `verb` ]  `argList` 
   send:  "<-"   [`verb` ]  `argList` 
   curryTail:   . `verb` 
   : |   "<-"  `verb` 
   index:  "["  ((`expr`  "," )+  | /* empty */) "]" 
   verb: IDENTIFIER
   : | .String.
   argList:  "("  ((`expr`  "," )+  | /* empty */) ")" 
   pattern: `postfixPatt` 
   postfixPatt: `SuchThatPatt` 
   : | `prefixPatt` 
   prefixPatt: `MapPatt` 
   : | `ListPatt` 
   : | `SamePatt` 
   : | `NotSamePatt` 
   : | `QuasiliteralPatt` 
   : | `ViaPatt` 
   : | `IgnorePatt` 
   : | `namePatt` 
   namePatt: `FinalPatt` 
   : | `VarPatt` 
   : | `BindPatt` 
   : | `SlotPatt` 
   : | `BindingPatt` 
   SuchThatPatt:  `prefixPatt`   "?"   "("  `expr`  ")" 
   ListPatt:   "["  ((`pattern`  "," )+  | /* empty */) "]"  [ "+"  `pattern` ] 
   MapPatt:   "["  (`mapPattItem`  "," )+  "]"  [ "|"  `pattern` ] 
   mapPattItem:  (  (`LiteralExpr`  |  "("  `expr`  ")" )  "=>"  `pattern`  |   "=>"  `namePatt` ) [ ":="  `order` ] 
   SamePatt:   "=="  `prim` 
   NotSamePatt:   "!="  `prim` 
   QuasiliteralPatt:  [IDENTIFIER]   "`"  ((( QUASI_TEXT |  ( AT_IDENT |  "@{"  `pattern`  "}" )) )+ ) "`" 
   ViaPatt:   "via"   "("  `expr`  ")"  `pattern` 
   FinalPatt:  `name`  `guardOpt` 
   VarPatt:   "var"  `name`  `guardOpt` 
   BindPatt:   "bind"  `name`  `guardOpt` 
   SlotPatt:   "&"  `name`  `guardOpt` 
   BindingPatt:   "&&"  `name` 
   IgnorePatt:   "_"  `guardOpt` 
   prim:  "("  `expr`  ")" 
   : | `LiteralExpr` 
   : | `quasiliteral` 
   : | `NounExpr` 
   : | `HideExpr` 
   : | `MapComprehensionExpr` 
   : | `ListComprehensionExpr` 
   : | `ListExpr` 
   : | `MapExpr` 
   expr: `assign` 
   : |  ("continue"  | "break"  | "return" ) ( "("  ")"  | ";"  | `blockExpr` )
   NounExpr:  `name` 
   name: IDENTIFIER
   : |  "::"  `stringLiteral` 
   LiteralExpr: `StrExpr` 
   : | `IntExpr` 
   : | `DoubleExpr` 
   : | `CharExpr` 
   quasiliteral:  [IDENTIFIER]   "`"  ((( QUASI_TEXT |  ( DOLLAR_IDENT |  "${"  `expr`  "}" )) )+ ) "`" 
   ListExpr:   "["  ((`expr`  "," )+  | /* empty */) "]" 
   comprehension:  `pattern`  "in"  `iter`  `expr` 
   : |  `pattern`  "=>"  `pattern`  "in"  `iter`  `expr`  "=>"  `expr` 
   iter:  `order`  [ "if"  `comp` ] 
   MapExpr:   "["  (`mapItem`  "," )+  "]" 
   mapItem:   `expr`   "=>"  `expr` 
   : |   "=>"  (`SlotExpr`  | `BindingExpr`  | `NounExpr` )
   IntExpr:  (`hexLiteral`  | `decLiteral` )
   decLiteral:  `digits` 
   digits:   `digit`  (((`digit`  | "_" ) )+ )+
   digit: /* one of: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 */ 
   hexLiteral:   "0"   ("x"  | X) `hexDigits` 
   hexDigits:   `hexDigit`  (((`hexDigit`  | "_" ) )+ )+
   hexDigit: /* one of: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, a, b, c, d, e, f, A, B, C, D, E, F */ 
   DoubleExpr:  `floatLiteral` 
   floatLiteral:   `digits`  (  . `digits`  [`floatExpn` ]  | `floatExpn` )
   floatExpn:  /* one of: e, E */   [ /* one of: -, + */ ]  `digits` 
   CharExpr:   "'"  `charConstant`  "'" 
   charConstant:  (( "\"  /* newline */  )+ )+ (/* none of: ', \, tab */  |  "\"  ( ( U  /* 8 x */  `hexDigit`  |  "u"   /* 4 x */  `hexDigit`  |  "x"   /* 2 x */  `hexDigit` ) |  /* one of: b, t, n, f, r, \, ', " */ ))
   StrExpr:  `stringLiteral` 
   stringLiteral:  '"'  ((`charConstant`  )+ )+ '"'
