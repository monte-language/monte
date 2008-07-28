#ifndef ECRU_PROBLEM_H
#define ECRU_PROBLEM_H

extern e_Script problem_script;
extern e_Method problem_methods[];

/** Return a new problem. */
e_Ref e_make_problem (const char *complaint, e_Ref irritant);

/** Throw a problem.  'complaint' must have indefinite extent. */
e_Ref e_throw_pair (const char *complaint, e_Ref irritant);

/** Throw 'cstring' as a problem, converting it into an E string. */
e_Ref e_throw_cstring (const char *cstring);

/** Throw an error according to the last C library error code in errno. */
void e_throw_errno (void);

#endif
