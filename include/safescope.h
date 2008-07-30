#ifndef ECRU_SAFESCOPE_H
#define ECRU_SAFESCOPE_H

/// Compares E references for equality of primitive types, or pointer equality. 
_Bool e_same(e_Ref ref1, e_Ref ref2);

/// The safe-scope object for performing equality comparisons.
extern e_Ref e_equalizer;
extern e_Script e__equalizer_script;
extern e_Method equalizer_methods[];

e_Selector op__cmp, belowZero, atMostZero, isZero, atLeastZero, aboveZero;

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

/// The thrower object. Bound as 'throw' in the universal scope.
extern e_Ref e_thrower;

/// The safe-scope object bound to '__makeList'.
extern e_Ref e_makeList;

/// The safe-scope object for 'while' loops.
extern e_Ref e_looper;

/// The safe-scope object 'require'.
extern e_Ref e_require;

/// The safe-scope object '__Test'.
extern e_Ref e__Test;

/// The safe-scope object '__bind'.
extern e_Ref e__bind;

/// The safe-scope object '__is'.
extern e_Ref e__is;

/// The safe-scope object '__makeVerbFacet'.
extern e_Ref e__makeVerbFacet;

/// The safe-scope object '__suchThat'.
extern e_Ref e__suchThat;

/// The safe-scope object 'simple__quasiParser'.
extern e_Ref e_simple__quasiParser;

/// The safe-scope object 'import__uriGetter'.
extern e_Ref e_import__uriGetter;

/// The safe-scope object 'E'.
extern e_Ref THE_E;

/// The safe-scope object 'traceln'.
extern e_Ref e_traceln;

/// The privileged-scope object 'timer'.
extern e_Ref e_timer;

/// The privileged-scope object 'print'.
extern e_Ref e_print_object;

/// The privileged-scope object 'println'.
extern e_Ref e_println_object;

/// The scope in which code with no capabilities is evaluated.
extern e_Ref e_safeScope;

#endif
