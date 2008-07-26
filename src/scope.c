#include "elib.h"
#include "ref.h"
#include "scope.h"
#include <string.h>

static e_Ref scopeLayout_getSynEnv(e_Ref self, e_Ref *args) {
  Scope_data *sc = self.data.other;
  e_Ref map = e_make_flexmap(sc->size);
  for (int i = 0; i < sc->size; i++) {
    // XXX later reference some AST nodes maybe? do we care?
    e_Ref putArgs[] = {e_make_string(sc->names[i]), e_null};
    e_flexmap_put(map, putArgs);
  }
  map.script = &e__constmap_script;
  return map;
}

static e_Ref scope_getScopeLayout(e_Ref self, e_Ref *args) {
  self.script = &e__scopeLayout_script;
  return self;
}

static e_Method scopeLayout_methods[] = {
  {"getSynEnv/0", scopeLayout_getSynEnv},
  {NULL}};

static e_Method scope_methods[] = {
  {"getScopeLayout/0", scope_getScopeLayout},
  {NULL}};

e_Script e__scope_script;
e_Script e__scopeLayout_script;

e_Ref e_make_scope(char **names, e_Ref *slots, int size) {
    Scope_data *sc = e_malloc(sizeof *sc);
    e_Ref scopeObj;
    sc->names = names;
    sc->slots = slots;
    sc->size = size;
    scopeObj.script = &e__scope_script;
    scopeObj.data.other = sc;
    return scopeObj;
}

e_Ref *e_scope_getEvalContext(e_Ref self) {
    Scope_data *sc = self.data.other;
    return sc->slots;
}

int e_scope_getSize(e_Ref self) {
    Scope_data *sc = self.data.other;
    return sc->size;
}


char *safeScope_names[] = {
  "null", "false", "true", "throw", "__loop", "__makeList", "__makeMap",
  "__makeProtocolDesc", "__makeMessageDesc", "__makeParamDesc", "any",
  "void", "boolean", "__makeOrderedSpace", "Guard", "require",
  "__makeVerbFacet", "__MatchContext", "__is", "__splitList", "__suchThat",
  "__bind", "__extract", "__Empty", "__matchBind", "__Test", "NaN",
  "Infinity", "__identityFunc", "__makeInt", "escape", "for", "if", "try",
  "while", "__makeFinalSlot", "__makeTwine", "__makeSourceSpan",
  "__auditedBy", "near", "pbc", "PassByCopy", "DeepPassByCopy",
  "Data", "Persistent", "DeepFrozen", "int", "float64", "char",
  "String", "Twine", "TextWriter", "List", "Map", "Set", "nullOk",
  "Tuple", "__Portrayal", "notNull", "vow", "rcvr", "ref", "nocall",
  "SturdyRef", "simple__quasiParser", "twine__quasiParser",
  "rx__quasiParser", "olde__quasiParser", "e__quasiParser",
  "epatt__quasiParser", "sml__quasiParser", "term__quasiParser",
  "__equalizer", "__comparer", "Ref", "E", "promiseAllFulfilled", "EIO",
  "help", "safeScope", "__eval", "resource__uriGetter", "type__uriGetter",
  "elib__uriGetter", "elang__uriGetter", "opaque__uriGetter",
  "__abortIncarnation", "when", "import__uriGetter", "traceln"
};

char *privilegedScope_names[] = {
  "file__uriGetter", "fileURL__uriGetter", "jar__uriGetter",
  "http__uriGetter", "ftp__uriGetter", "gopher__uriGetter",
  "news__uriGetter", "captp__uriGetter", "makeCommand", "stdout",
  "stderr", "stdin", "print", "println", "interp", "entropy", "timer",
  "introducer", "identityMgr", "makeSturdyRef", "timeMachine",
  "unsafe__uriGetter", "currentVat", "rune", "awt__uriGetter",
  "swing__uriGetter", "JPanel__quasiParser", "swt__uriGetter",
  "currentDisplay", "swtGrid__quasiParser", "swtWatch", "privilegedScope"
};

void e__scope_set_up() {

  e_make_script(&e__scopeLayout_script, NULL, scopeLayout_methods,
                "ScopeLayout");
  e_make_script(&e__scope_script, NULL, scope_methods, "Scope");

  e_Ref safeScope[] = {e_make_finalslot(e_null),
                       e_make_finalslot(e_false), e_make_finalslot(e_true),
                       e_make_finalslot(e_thrower),
                       e_make_finalslot(e_looper),
                       e_make_finalslot(e_makeList),
                       e_make_finalslot(e_makeMap),
                       e_null, e_null, e_null, e_null, e_null,
                       e_make_finalslot(e_BooleanGuard),
                       e_make_finalslot(e_makeOrderedSpace),
                       e_null,
                       e_make_finalslot(e_require),
                       e_make_finalslot(e__makeVerbFacet),
                       e_null, // __MatchContext
                       e_make_finalslot(e__is),
                       e_null, //__splitList
                       e_make_finalslot(e__suchThat),
                       e_make_finalslot(e__bind),
                       e_null, e_null, e_null,
                       e_make_finalslot(e__Test),
                       e_null, e_null, e_null, e_null, e_null, e_null,
                       e_null, e_null, e_null, e_null, e_null, e_null,
                       e_null, e_null, e_null, e_null, e_null, e_null,
                       e_null, e_null,
                       e_make_finalslot(e_IntGuard),
                       e_make_finalslot(e_Float64Guard),
                       e_make_finalslot(e_CharGuard),
                       e_make_finalslot(e_StringGuard),
                       e_null, e_null, e_null, e_null, e_null, e_null,
                       e_null, e_null, e_null, e_null, e_null, e_null,
                       e_null, e_null,
                       e_make_finalslot(e_simple__quasiParser),
                       e_null, e_null, e_null,
                       e_null, e_null, e_null, e_null,
                       e_make_finalslot(e_equalizer),
                       e_make_finalslot(e_comparer),
                       e_make_finalslot(THE_REF),
                       e_make_finalslot(THE_E), e_null, e_null, e_null,
                       e_empty_ref, // safeScope, filled in below
                       e_null,
                       e_null, e_null, e_null, e_null, e_null, e_null, e_null,
                       e_make_finalslot(e_import__uriGetter),
                       e_make_finalslot(e_traceln)
  };
  e_Ref *_safeScope = e_make_array(90);
  memcpy(_safeScope, safeScope, 90 * sizeof(e_Ref));
  e_safeScope = e_make_scope(safeScope_names, _safeScope, 90);
  // self-reference is awkward
  _safeScope[79] = e_make_finalslot(e_safeScope);

  e_Ref privilegedScope[] = {e_null, e_null, e_null,
                             e_null, e_null, e_null,
                             e_null, e_null, e_null,
                             e_make_finalslot(e_stdout),
                             e_make_finalslot(e_stderr),
                             e_make_finalslot(e_stdin),
                             e_make_finalslot(e_print_object),
                             e_make_finalslot(e_println_object),
                             e_null, e_null,
                             e_make_finalslot(e_timer),
                             e_null, e_null, e_null, e_null,
                             e_null, e_null, e_null, e_null,
                             e_null, e_null, e_null,
                             e_null, e_null, e_null, e_empty_ref,
  };
  e_Ref *_privilegedScope = e_make_array(122);
  char **_privilegedScope_names = e_malloc(122 * sizeof (char *));
  memcpy(_privilegedScope, _safeScope, 90 * sizeof(e_Ref));
  memcpy(_privilegedScope + 90, privilegedScope, 32 * sizeof(e_Ref));
  memcpy(_privilegedScope_names, safeScope_names, 90 * sizeof(char *));
  memcpy(_privilegedScope_names + 90, privilegedScope_names,
         32 * sizeof(char *));
  e_privilegedScope = e_make_scope(_privilegedScope_names, _privilegedScope,
                                   122);
  _privilegedScope[121] = e_make_finalslot(e_privilegedScope);

}
