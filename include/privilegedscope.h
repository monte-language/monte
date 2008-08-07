
/// The privileged-scope object 'timer'.
extern e_Ref e_timer;
extern e_Script e__timer_script;
extern e_Method timer_methods[];

/// The privileged-scope object 'print'.
extern e_Ref e_print_object;
extern e_Script e__print_script;
extern e_Ref print_collectArgs(e_Ref self, e_Selector *sel, e_Ref *args);

/// The privileged-scope object 'println'.
extern e_Ref e_println_object;
extern e_Script e__println_script;
extern e_Ref println_collectArgs(e_Ref self, e_Selector *sel, e_Ref *args);

/// The scope containing all capabilities exposed by this runtime.
/** The default top-level scope for non-interactive code. */
extern e_Ref e_privilegedScope;
