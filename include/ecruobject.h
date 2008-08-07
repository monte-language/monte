#ifndef ECRU_OBJECT_H
#define ECRU_OBJECT_H
/// @defgroup objects Objects
//@{
typedef union e_Data e_Data;
typedef struct e_Method e_Method;
typedef struct e_Ref e_Ref;
typedef struct e_Script e_Script;
typedef struct e_Selector e_Selector;

/** The possible types of state held by a ref.  Each must fit in a single
   machine word -- if bigger than that, or shared, use a pointer. */
union e_Data {
  long fixnum;			/**< small integer */
  mpz_t *bignum;
  unsigned short chr;
  GString *gstring;
  double *float64;
  e_Ref *refs;			/**< an array, size determined by the script */
  void *other;			/**< anything else */
};


/** A ref is a reference to an E object, represented by a fat pointer:
   the first part, the script, determines the object's behavior, while
   the second part determines its state, as interpreted by the
   script.

   In general, we may assume that everything a ref points to
   (transitively) has indefinite extent except where otherwise
   indicated.  Indefinite extent means it's stored statically or in
   the GCed heap, not on the stack. */
struct e_Ref {
  e_Script *script;
  e_Data data;
};

/** An exec func is the C code underlying a method.  'args' is an array
   of arguments of length equal to the method's arity.  The array may
   be allocated on the stack rather than the heap, so you must assume
   it may be of unchecked dynamic extent.  (But each individual arg is
   an ordinary garbage-collected ref.) */
typedef e_Ref e_Exec_Func (e_Ref self, e_Ref *args);

/** The C code handling a call. */
typedef e_Ref e_Call_Func (e_Ref self, e_Selector *selector, e_Ref *args);

/** The behavior of a ref. */
struct e_Script {
  int num_methods;
  e_Method *methods;		/**< an array of length num_methods */
  e_Call_Func *opt_otherwise;
  GString *typeName;
  /** TODO: add a send function, etc?  check the enative code */
};

/** A method bundles a mangled and interned verb with its behavior.
    Mangled: for example, "add/1" for a method called like foo.add(bar).
    The "/1" part gives its arity (that is, the number of parameters).
    Interned: uniquified by e_intern(), and so may be compared with ==.

    For our purposes at the moment we don't care about the string
    encoding -- we just treat it as a byte array.  But we'll want to
    nail it down later to use UTF8 or something.

    Note that we can't represent a verb with a null character inside it
    -- could that be a problem? */
struct e_Method {
  const char *verb;
  e_Exec_Func *exec_func;
};

/** For use with scripts with no methods. */
extern e_Method no_methods[];

//@}
/** @defgroup messages Messages
    A selector is the type of a message in a call or a send. */
struct e_Selector {
  const char *verb;
  int arity;			/**< Redundantly held for convenience */
  /** TODO: enative has stuff here for call-site caching, etc. */
};


/** @ingroup objects
    Initialize *script.
   'methods' is a an array terminated by an entry with a verb of NULL.
   In initializing, we intern the verbs in place. */
void e_make_script (e_Script *script,
		    e_Call_Func *opt_otherwise,
		    e_Method *methods,
                    const char *typeName);

/** @ingroup objects
    The default implementation of the Miranda methods. If you create a script
    with an "opt_otherwise" function, you must call this from it on any
    selectors you do not implement. */
e_Ref otherwise_miranda_methods(e_Ref self, e_Selector *selector, e_Ref *args);

/// The array of default Miranda method implementations.
extern e_Method e_miranda_methods[];
#define E_NUM_MIRANDA_METHODS 7

extern e_Ref e_empty_ref;

/// Compares E references for pointer equality.
static inline _Bool e_eq(e_Ref ref1, e_Ref ref2) {
  return ref1.script == ref2.script &&
    ref1.data.fixnum == ref2.data.fixnum;
}


#endif
