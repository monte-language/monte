/* Copyright 2003 Darius Bacon under the terms of the MIT X license
   found at http://www.opensource.org/licenses/mit-license.html */

#ifndef ELIB_PRIVATE_H
#define ELIB_PRIVATE_H

extern e_Selector respondsTo, order, whenBroken, whenMoreResolved,
                  whenMoreResolved_ev, optSealedDispatch, conformTo,
                  printOn, optUncall, getAllegedType, reactToLostClient,
                  E_AUDITED_BY;

extern char e__setup_done;

/** We must call this before any e_intern() calls. */
void e__set_up_interner (void);

/** Load the scripts for promises, etc. */
void e__ref_set_up();

/** Load selectors for miranda methods */
void e__miranda_set_up();

/** Load scope objects */
void e__scope_set_up();

/** Load guard objects */
void e__guards_set_up();

/** Load objects that wrap elib behaviour for the safe scope */
void e__safescope_set_up();

/** Load objects that wrap elib behaviour for the unsafe scope */
void e__privilegedscope_set_up();

#endif /* ELIB_PRIVATE_H */
