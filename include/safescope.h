#ifndef ECRU_SAFESCOPE_H
#define ECRU_SAFESCOPE_H

/// Compares E references for equality of primitive types, or pointer equality. 
_Bool e_same(e_Ref ref1, e_Ref ref2);

/// The safe-scope object for performing equality comparisons.
extern e_Ref e_equalizer;

extern e_Script e__equalizer_script;
extern e_Method equalizer_methods[];

e_Selector op__cmp, belowZero, atMostZero, isZero, atLeastZero, aboveZero;

extern e_Ref e_comparer;
extern e_Script e__comparer_script;
extern e_Method comparer_methods[];

#endif
