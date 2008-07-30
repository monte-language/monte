#include <string.h>
#include "elib.h"


#if OLD_GIO
#include <gio/gmemoryoutputstream.h>
#include <gio/gseekable.h>
#endif


e_Ref e_looper, e_thrower, e_require,
      e_makeOrderedSpace, e_makeMap, e_makeList, e__Test, e__bind,
      e__is, e__makeVerbFacet, e__suchThat, e_simple__quasiParser,
      e_import__uriGetter, THE_E, e_traceln, e_safeScope;





e_Ref e_loop(e_Ref self, e_Ref *args) {
  //XXX selector pooling
  e_Selector run0;
  e_make_selector(&run0, "run", 0);
  e_Ref val;
  do {
    val = e_call_0(args[0], &run0);
    E_ERROR_CHECK(val);
  } while (e_same(val, e_true));
  return e_null;
}

static e_Script e__looper_script;
static e_Method looper_methods[] = {
  {"run/1", e_loop},
  {NULL}
};

e_Ref makeList_dispatch(e_Ref receiver, e_Selector *selector,
                               e_Ref *args) {
  if (strncmp("run", selector->verb, 3) == 0) {
    return e_constlist_from_array(selector->arity, args);
  } else {
    return otherwise_miranda_methods(receiver, selector, args);
  }
}

static e_Script e__makeList_script;
static e_Method makeList_methods[] = {
  {NULL}
};

e_Ref e_makeMap_fromPairs(e_Ref self, e_Ref *args) {
  //XXX selector pooling
  e_Selector get, put, size;
  e_make_selector(&get, "get", 1);
  e_make_selector(&put, "put", 1);
  e_make_selector(&size, "size", 0);

  e_Ref sizeObj = e_call_0(args[0],  &size);
  E_ERROR_CHECK(sizeObj);
  int length = sizeObj.data.fixnum;
  e_Ref newMap = e_make_flexmap(length);
  //XXX we oughta get an iterate method someday
  for (int i = 0; i < length; i++) {
    e_Ref pairObj = e_call_1(args[0], &get, e_make_fixnum(i));
    E_ERROR_CHECK(pairObj);
    e_Ref keyObj = e_call_1(pairObj, &get, e_make_fixnum(0));
    E_ERROR_CHECK(keyObj);
    e_Ref valueObj = e_call_1(pairObj, &get, e_make_fixnum(1));
    E_ERROR_CHECK(valueObj);
    e_call_2(newMap, &put, keyObj, valueObj);
  }
  newMap.script = &e__constmap_script;
  return newMap;
}

static e_Ref e_makeMap_fromColumns(e_Ref self, e_Ref *args) {
  //XXX selector pooling
  e_Selector coerce, get, size;
  e_make_selector(&coerce, "coerce", 2);
  e_make_selector(&get, "get", 1);
  e_make_selector(&size, "size", 0);

  e_Ref sizeObj = e_call_0(args[0],  &size);
  E_ERROR_CHECK(sizeObj);
  e_Ref vsizeObj = e_call_0(args[1],  &size);
  E_ERROR_CHECK(vsizeObj);
  sizeObj = e_call_2(e_IntGuard, &coerce, sizeObj, e_null);
  vsizeObj = e_call_2(e_IntGuard, &coerce, vsizeObj, e_null);
  int siz = sizeObj.data.fixnum;
  int vsiz = vsizeObj.data.fixnum;

  if (siz != vsiz) {
    return e_throw_cstring("Arity mismatch in __makeMap.fromColumns");
  }
  e_Ref result = e_make_constmap(siz);
  for (int i = 0; i < siz; i++) {
    e_Ref k = e_call_1(args[0], &get, e_make_fixnum(i));
    E_ERROR_CHECK(k);
    e_Ref v = e_call_1(args[1], &get, e_make_fixnum(i));
    E_ERROR_CHECK(v);
    e_Ref args[] = {k, v};
    E_ERROR_CHECK(e_flexmap_put(result, args));
  }
  return result;
}

static e_Script e__makeMap_script;
static e_Method makeMap_methods[] = {
  {"fromPairs/1", e_makeMap_fromPairs},
  {"fromColumns/2", e_makeMap_fromColumns},
  {NULL}
};

e_Ref require_run(e_Ref self, e_Ref *args) {
  if (args[0].script != &e__boolean_script) {
    return e_throw_cstring("Argument to 'require' was not a boolean");
  }
  if (e_same(args[0], e_false)) {
    return e_throw(args[1]);
  }
  return e_null;
}

e_Ref require_run1(e_Ref self, e_Ref *args) {
  e_Ref newArgs[] = {args[0], e_make_string("required condition failed")};
  return require_run(self, newArgs);
}

static e_Script e__require_script;
static e_Method require_methods[] = {
  {"run/1", require_run1},
  {"run/2", require_run},
  {NULL}};

static e_Ref test_coerce(e_Ref self, e_Ref *args) {
  if (e_same(args[0], e_true)) {
    return e_true;
  } else {
    return e_ejectOrThrow(args[1], "condition was false", e_false);
  }
}

static e_Script e__test_script;
static e_Method test_methods[] = {
  {"coerce/2", test_coerce},
  {NULL}};

static e_Ref viaFunc1(e_Ref self, e_Ref *args) {
  //XXX selector pooling
  e_Selector resolve;
  e_make_selector(&resolve, "resolve", 1);

  E_ERROR_CHECK(e_call_1(self.data.refs[0], &resolve, args[0]));
  return e_null;
}

static e_Script viafunc1_script;
static e_Method viafunc1_methods[] = {
  {"run/2", viaFunc1},
  {NULL}};

static e_Ref viaFunc2(e_Ref self, e_Ref *args) {
  //XXX selector pooling
  e_Selector resolve, coerce;
  e_make_selector(&resolve, "resolve", 1);
  e_make_selector(&coerce, "coerce", 2);

  e_Ref obj = e_call(self.data.refs[1], &coerce, args);
  E_ERROR_CHECK(obj);
  E_ERROR_CHECK(e_call_1(self.data.refs[0], &resolve, obj));
  return e_null;
}

static e_Script viafunc2_script;
static e_Method viafunc2_methods[] = {
  {"run/2", viaFunc2},
  {NULL}};


static e_Ref bind_run1(e_Ref self, e_Ref *args) {
  e_Ref viafunc;
  viafunc.script = &viafunc1_script;
  viafunc.data.refs = e_malloc(sizeof(e_Ref));
  viafunc.data.refs[0] = args[0];
  return viafunc;
}

static e_Ref bind_run2(e_Ref self, e_Ref *args) {
  e_Ref viafunc;
  viafunc.script = &viafunc2_script;
  viafunc.data.refs = e_malloc(sizeof(e_Ref) * 2);
  viafunc.data.refs[0] = args[0];
  viafunc.data.refs[1] = args[1];
  return viafunc;
}

static e_Script e__bind_script;
static e_Method bind_methods[] = {
  {"run/1", bind_run1},
  {"run/2", bind_run2},
  {NULL}};

static e_Ref isSameFunc_run(e_Ref self, e_Ref *args) {
  if (e_same(self.data.refs[0], args[0])) {
    return args[0];
  } else {
    return e_ejectOrThrow(args[1], "doesn't equal-match", args[0]);
  }
}

static e_Script isSameFunc_script;
static e_Method isSameFunc_methods[] = {
  {"run/2", isSameFunc_run},
  {NULL}};

static e_Ref is_run(e_Ref self, e_Ref *args) {
  e_Ref isSameFunc;
  isSameFunc.script = &isSameFunc_script;
  isSameFunc.data.refs = e_malloc(sizeof(e_Ref));
  isSameFunc.data.refs[0] = args[0];
  return isSameFunc;
}

static e_Script e__is_script;
static e_Method is_methods[] = {
  {"run/1", is_run},
  {NULL}};

e_Ref verbFacet_dispatch(e_Ref self, e_Selector *selector, e_Ref *args) {
  e_Selector currySel;
  if (strncmp(selector->verb, "run", 3) != 0) {
    return otherwise_miranda_methods(self, selector, args);
  }
  e_make_selector(&currySel, self.data.refs[1].data.gstring->str, selector->arity);
  return e_call(self.data.refs[0], &currySel, args);
}

static e_Script verbFacet_script;

static e_Ref makeVerbFacet_curryCall(e_Ref self, e_Ref *args) {
  e_Ref facet;
  facet.script = &verbFacet_script;
  facet.data.refs = e_malloc(sizeof(e_Ref) * 2);
  facet.data.refs[0] = args[0];
  facet.data.refs[1] = args[1];
  return facet;
}
static e_Script e__makeVerbFacet_script;
static e_Method makeVerbFacet_methods[] = {
  {"curryCall/2", makeVerbFacet_curryCall},
  {NULL}};

static e_Ref suchThatFuncFalse_run(e_Ref self, e_Ref *args) {
  return e_ejectOrThrow(args[1], "such-that expression was", e_false);
}

static e_Script suchThatFuncFalse_script;
static e_Method suchThatFuncFalse_methods[] = {
  {"run/2", suchThatFuncFalse_run},
  {NULL}};

static e_Ref suchThatFuncTrue_run(e_Ref self, e_Ref *args) {
  return e_null;
}

static e_Script suchThatFuncTrue_script;
static e_Method suchThatFuncTrue_methods[] = {
  {"run/2", suchThatFuncTrue_run},
  {NULL}};


static e_Ref suchThat_run2(e_Ref self, e_Ref *args) {
  return e_constlist_from_array(2, args);
}

static e_Ref suchThat_run1(e_Ref self, e_Ref *args) {
  e_Ref func;
  e_Ref boolguard_args[] = {args[0], e_null};
  e_Ref flag = booleanguard_coerce(e_null, boolguard_args);
  E_ERROR_CHECK(flag);
  if (e_same(flag, e_true)) {
    func.script = &suchThatFuncTrue_script;
  } else {
    func.script = &suchThatFuncFalse_script;
  }
  return func;
}

static e_Script e__suchThat_script;
static e_Method suchThat_methods[] = {
  {"run/2", suchThat_run2},
  {"run/1", suchThat_run1},
  {NULL}};


/// Throw a problem.
static e_Ref thrower_run(e_Ref self, e_Ref *args) {
  return e_throw(args[0]);
}

static e_Ref thrower_eject(e_Ref self, e_Ref *args) {
  return e_ejectOrThrow_problem(args[0], args[1]);
}

static e_Script thrower_script;
static e_Method thrower_methods[] = {
  {"run/1", thrower_run},
  {"eject/2", thrower_eject},
  {NULL}
};


enum segmentType {SEG_LITERAL, SEG_VALUE, SEG_PATTERN};

typedef struct template_segment {
  char *start;
  int size;
  enum segmentType type;
  char position;
} template_segment;

typedef struct template_segments {
  int size;
  int allocated;
  int matchSize;
  template_segment *segs;
} template_segments;


static e_Ref substituter_substitute(e_Ref self, e_Ref *args) {
  //XXX selector pooling
  e_Selector get;
  e_make_selector(&get, "get", 1);

  e_Ref listguard_args[] = {args[0], e_null};
  e_Ref inputs = elistguard_coerce(e_null, listguard_args);
  E_ERROR_CHECK(inputs);
  template_segments *segments = self.data.other;
  int len = segments->size;
  e_Ref memWriter = e_make_string_writer();
  GOutputStream *stream = memWriter.data.refs[0].data.other;
  GError *err;
  for (int i = 0; i < len; i++) {
    template_segment *seg = segments->segs + i;
    if (seg->type == SEG_LITERAL) {
      if (seg->size == 0) {
        continue;
      }
      _Bool win = g_output_stream_write_all(stream, seg->start, seg->size,
                                            NULL, NULL, &err);
      if (!win) {
        return e_throw_pair(err->message, e_make_fixnum(err->code));
      }
    } else if (seg->type == SEG_VALUE) {
      e_Ref item = e_call_1(inputs, &get, e_make_fixnum(seg->position));
      E_ERROR_CHECK(item);
      E_ERROR_CHECK(e_print(memWriter, item));
    } else {
      return e_throw_pair("can't substitute() with a pattern", self);
    }
  }
  return e_string_writer_get_string(memWriter);
}

static e_Script substituter_script;
static e_Method substituter_methods[] = {
  {"substitute/1", substituter_substitute},
  {NULL}};

static template_segment *new_segment(template_segments *segments) {
  if (segments->size == segments->allocated) {
    template_segment *oldsegs = segments->segs;
    segments->segs = e_malloc(2 * segments->allocated * sizeof *segments->segs);
    memcpy(segments->segs, oldsegs, segments->size * sizeof *segments->segs);
    segments->allocated *= 2;
  }

    segments->segs[segments->size].type = SEG_LITERAL;
    segments->size++;
    return segments->segs + segments->size - 1;
}

static e_Ref make_substituter(e_Ref self, e_Ref *args) {
  e_Ref stringguard_args[] = {args[0], e_null};
  e_Ref templateObj = stringguard_coerce(e_null, stringguard_args);
  E_ERROR_CHECK(templateObj);
  GString *template = templateObj.data.gstring;
  template_segments *segments;
  segments = e_malloc(sizeof *segments);
  segments->segs = e_malloc(sizeof *segments->segs);
  segments->size = 1;
  segments->allocated = 1;
  template_segment *current_seg = segments->segs;
  current_seg->start = template->str;
  current_seg->size = 0;
  current_seg->type = SEG_LITERAL;
  int len = template->len;
  for (int i = 0; i < len; i++) {
    char c1 = template->str[i];
    if ('$' != c1 && '@' != c1) {
      //not a marker
      current_seg->size++;
    } else if (i >= len - 1) {
      //terminal marker
      current_seg->size++;
    } else {
      i++;
      char c2 = template->str[i];
      if (c1 == c2) {
        //doubled marker character, drop one
        current_seg = new_segment(segments);
        current_seg->start = template->str + i;
        current_seg->size = 0;
      } else if ('{' != c2) {
        i--;
        //not special, so back up and act normal
        current_seg->size++;
      } else {
        // found one
        if (current_seg->size != 0) {
          current_seg = new_segment(segments);
        }
        int index = 0;
        for (i++; i < len; i++) {
          c2 = template->str[i];
          if ('}' == c2) {
            break;
          } else if (c2 >= '0' || c2 <= '9') {
            index = index * 10 + c2 - '0';
          } else {
            return e_throw_pair("missing '}'", templateObj);
          }
        }
        if ('@' == c1) {
          if (index + 1 > segments->matchSize) {
            segments->matchSize = index + 1;
          }
          current_seg->type = SEG_PATTERN;
        } else {
          current_seg->type = SEG_VALUE;
        }
        current_seg->position = index;

        current_seg = new_segment(segments);
        current_seg->start = template->str + i + 1;
        current_seg->size = 0;
      }
    }
  }
  e_Ref result;
  result.script = &substituter_script;
  result.data.other = segments;
  return result;
}

static e_Script simple__quasiParser_script;
static e_Method simple__quasiParser_methods[] = {
  {"valueMaker/1", make_substituter},
  {NULL}};

static e_Ref module_import_method(e_Ref self, e_Ref *args) {
  e_Ref stringguard_args[] = {args[0], e_null};
  e_Ref modName = stringguard_coerce(e_null, stringguard_args);
  E_ERROR_CHECK(modName);
  return e_module_import(modName.data.gstring);
}

static e_Script import__uriGetter_script;
static e_Method import__uriGetter_methods[] = {
  {"get/1", module_import_method},
  {NULL}
};

static e_Ref e_traceln_run(e_Ref self, e_Ref *args) {
  return e_println(e_stderr, args[0]);
}

static e_Script e__traceln_script;
static e_Method e__traceln_methods[] = {
  {"run/1", e_traceln_run},
  {NULL},
};

static e_Ref e_callWithPair(e_Ref self, e_Ref *args) {
  //XXX selector pooling
  e_Selector get;
  e_make_selector(&get, "get", 1);

  e_Ref receiver = args[0];
  e_Ref argPair = elistguard_coerce(e_null, args + 1);
  E_ERROR_CHECK(argPair);
  e_Ref verb = e_call_1(argPair, &get, e_make_fixnum(0));
  E_ERROR_CHECK(verb);
  verb = stringguard_coerce(e_null, &verb);
  E_ERROR_CHECK(verb);
  e_Ref arglist = e_call_1(argPair, &get, e_make_fixnum(1));
  E_ERROR_CHECK(arglist);
  elistguard_coerce(e_null, &arglist);
  E_ERROR_CHECK(arglist);
  e_Ref *newArgs = ((Flexlist_data *)arglist.data.other)->elements;
  int arity = ((Flexlist_data *)arglist.data.other)->size;
  e_Selector sel;
  e_make_selector(&sel, (verb.data.gstring)->str, arity);
  return e_call(receiver, &sel, newArgs);

}

static e_Ref e_toString(e_Ref self, e_Ref *args) {
  e_Ref memWriter = e_make_string_writer();
  E_ERROR_CHECK(e_print(memWriter, args[0]));
  return e_string_writer_get_string(memWriter);
}

static e_Script THE_E_script;
static e_Method THE_E_methods[] = {
  {"callWithPair/2", e_callWithPair},
  {"toString/1", e_toString},
  {NULL}
};

void e__safescope_set_up() {
  e_make_script(&e__equalizer_script, NULL, equalizer_methods, "Equalizer");
  e_make_script(&e__comparer_script, NULL, comparer_methods, "Comparer");
  e_make_script(&e__looper_script, NULL, looper_methods, "Loop");
  e_make_script(&e__makeList_script, makeList_dispatch, makeList_methods,
                "ConstList__Maker");
  e_make_script(&e__makeMap_script, NULL, makeMap_methods,
                "ConstMap__Maker");
  e_make_script(&e__orderedSpace_script, NULL, orderedSpace_methods,
                "OrderedRegion");
  e_make_script(&e__descender_script, NULL, descender_methods,
                "descender");
  e_make_script(&e__makeOrderedSpace_script, NULL, makeOrderedSpace_methods,
                "makeOrderedRegion");
  e_make_script(&e__require_script, NULL, require_methods,
                "require");
  e_make_script(&e__test_script, NULL, test_methods,
                "__Test");
  e_make_script(&viafunc1_script, NULL, viafunc1_methods, "viaFunc1");
  e_make_script(&viafunc2_script, NULL, viafunc2_methods, "viaFunc2");
  e_make_script(&e__bind_script, NULL, bind_methods, "__bind");
  e_make_script(&isSameFunc_script, NULL, isSameFunc_methods, "__isSameFunc");
  e_make_script(&e__is_script, NULL, is_methods, "__is");
  e_make_script(&verbFacet_script, verbFacet_dispatch, no_methods,
                "verbFacet");
  e_make_script(&e__makeVerbFacet_script, NULL, makeVerbFacet_methods,
                "__makeVerbFacet");
  e_make_script(&e__suchThat_script, NULL, suchThat_methods,
                "__suchThat");
  e_make_script(&suchThatFuncFalse_script, NULL, suchThatFuncFalse_methods,
                "suchThatFunc");
  e_make_script(&suchThatFuncTrue_script, NULL, suchThatFuncTrue_methods,
                "suchThatFunc");
  e_make_script(&thrower_script, NULL, thrower_methods,
                "thrower");
  e_make_script(&simple__quasiParser_script, NULL, simple__quasiParser_methods,
                "simple__quasiParser");
  e_make_script(&substituter_script, NULL, substituter_methods,
                "textSubstituter");
  e_make_script(&import__uriGetter_script, NULL, import__uriGetter_methods,
                "import__uriGetter");
  e_make_script(&THE_E_script, NULL, THE_E_methods, "E");
  e_make_script(&e__traceln_script, NULL, e__traceln_methods, "traceln");
  e_thrower.script = &thrower_script;
  e_equalizer.script = &e__equalizer_script;
  e_comparer.script = &e__comparer_script;
  e_looper.script = &e__looper_script;
  e_makeList.script = &e__makeList_script;
  e_makeMap.script = &e__makeMap_script;
  e_require.script = &e__require_script;
  e_makeOrderedSpace.script = &e__makeOrderedSpace_script;
  e__Test.script = &e__test_script;
  e__bind.script = &e__bind_script;
  e__is.script = &e__is_script;
  e__makeVerbFacet.script = &e__makeVerbFacet_script;
  e__suchThat.script = &e__suchThat_script;
  e_simple__quasiParser.script = &simple__quasiParser_script;
  e_import__uriGetter.script = &import__uriGetter_script;
  e_traceln.script = &e__traceln_script;
  THE_E.script = &THE_E_script;
  e_make_selector(&op__cmp, "op__cmp", 1);
  e_make_selector(&belowZero, "belowZero", 0);
  e_make_selector(&atMostZero, "atMostZero", 0);
  e_make_selector(&isZero, "isZero", 0);
  e_make_selector(&atLeastZero, "atLeastZero", 0);
  e_make_selector(&aboveZero, "aboveZero", 0);
}
