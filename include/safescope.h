#ifndef ECRU_SAFESCOPE_H
#define ECRU_SAFESCOPE_H

/// Compares E references for equality of primitive types, or pointer equality. 
_Bool e_same(e_Ref ref1, e_Ref ref2);

/// The safe-scope object for performing equality comparisons.
extern e_Ref e_equalizer;
extern e_Script e__equalizer_script;
extern e_Method equalizer_methods[];

extern e_Selector op__cmp, belowZero, atMostZero, isZero, atLeastZero, aboveZero;

/// The safe-scope object for performing comparisons.
extern e_Ref e_comparer;
extern e_Script e__comparer_script;
extern e_Method comparer_methods[];

/// The safe-scope object for created ordered spaces (used by the `..' operator)
extern e_Ref e_makeOrderedSpace;
extern e_Script e__makeOrderedSpace_script;
extern e_Script e__orderedSpace_script;
extern e_Script e__descender_script;
extern e_Method makeOrderedSpace_methods[];
extern e_Method orderedSpace_methods[];
extern e_Method descender_methods[];


/// The safe-scope object for 'while' loops.
extern e_Ref e_looper;
extern e_Script e__looper_script;
extern e_Method looper_methods[];

/// The thrower object. Bound as 'throw' in the universal scope.
extern e_Ref e_thrower;
extern e_Script thrower_script;
extern e_Method thrower_methods[];

/// The safe-scope object bound to '__makeList'.
extern e_Ref e_makeList;
extern e_Script e__makeList_script;
extern e_Method makeList_methods[];
e_Ref makeList_dispatch(e_Ref receiver, e_Selector *selector, e_Ref *args);



/// The safe-scope object bound to '__makeMap'.
extern e_Ref e_makeMap;
extern e_Script e__makeMap_script;
extern e_Method makeMap_methods[];


/// The safe-scope object 'require'.
extern e_Ref e_require;
extern e_Script e__require_script;
extern e_Method require_methods[];

/// The safe-scope object '__Test'.
extern e_Ref e__Test;
extern e_Script e__test_script;
extern e_Method test_methods[];

/// The safe-scope object '__bind'.
extern e_Ref e__bind;
extern e_Script e__bind_script;
extern e_Method bind_methods[];
extern e_Script viafunc1_script;
extern e_Method viafunc1_methods[];
extern e_Script viafunc2_script;
extern e_Method viafunc2_methods[];

/// The safe-scope object '__is'.
extern e_Ref e__is;
extern e_Script e__is_script;
extern e_Method is_methods[];
extern e_Script isSameFunc_script;
extern e_Method isSameFunc_methods[];

/// The safe-scope object '__makeVerbFacet'.
extern e_Ref e__makeVerbFacet;
extern e_Script e__makeVerbFacet_script;
extern e_Method makeVerbFacet_methods[];
extern e_Script verbFacet_script;
e_Ref verbFacet_dispatch(e_Ref self, e_Selector *selector, e_Ref *args);

/// The safe-scope object '__suchThat'.
extern e_Ref e__suchThat;
extern e_Script e__suchThat_script;
extern e_Method suchThat_methods[];
extern e_Script suchThatFuncFalse_script;
extern e_Method suchThatFuncFalse_methods[];
extern e_Script suchThatFuncTrue_script;
extern e_Method suchThatFuncTrue_methods[];


/// The safe-scope object 'simple__quasiParser'.
extern e_Ref e_simple__quasiParser;
extern e_Script simple__quasiParser_script;
extern e_Method simple__quasiParser_methods[];
extern e_Script substituter_script;
extern e_Method substituter_methods[];

/// The safe-scope object 'import__uriGetter'.
extern e_Ref e_import__uriGetter;
extern e_Script import__uriGetter_script;
extern e_Method import__uriGetter_methods[];


/// The safe-scope object 'E'.
extern e_Ref THE_E;
extern e_Script THE_E_script;
extern e_Method THE_E_methods[];


/// The safe-scope object 'traceln'.
extern e_Ref e_traceln;
extern e_Script e__traceln_script;
extern e_Method e__traceln_methods[];


/// The scope in which code with no capabilities is evaluated.
extern e_Ref e_safeScope;

#endif
