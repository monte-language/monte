#include "elib.h"

#if OLD_GIO
#include <gio/gsocketoutputstream.h>
#include <gio/gsocketinputstream.h>
#else
#include <gio/gunixoutputstream.h>
#include <gio/gunixinputstream.h>
#endif


static e_Ref writer_print(e_Ref self, e_Ref *args, int numItems) {
  GOutputStream *stream = self.data.refs[0].data.other;
  GError *err = NULL;
  for (int i = 0; i < numItems; i++) {
    e_Ref arg = e_ref_target(args[i]);
    if (e_is_string(arg)) {
      _Bool win = g_output_stream_write_all(stream, arg.data.gstring->str,
                                            arg.data.gstring->len,
                                            NULL, NULL, &err);
      if (!win) {
        if (err != NULL) {
          return e_throw_pair(err->message, e_make_fixnum(err->code));
        } else {
          return e_throw_cstring("Unspecified error in writer_print");
        }
      }
    } else {
      E_ERROR_CHECK(e_print_on(arg, self));
    }
  }
  return e_null;
}

static e_Ref writer_print1(e_Ref self, e_Ref *args) {
  return writer_print(self, args, 1);
}

static e_Ref writer_print2(e_Ref self, e_Ref *args) {
  return writer_print(self, args, 2);
}

static e_Ref writer_print3(e_Ref self, e_Ref *args) {
  return writer_print(self, args, 3);
}

static e_Ref writer_print4(e_Ref self, e_Ref *args) {
  return writer_print(self, args, 4);
}

static e_Ref writer_print5(e_Ref self, e_Ref *args) {
  return writer_print(self, args, 5);
}

static e_Ref writer_print6(e_Ref self, e_Ref *args) {
  return writer_print(self, args, 6);
}

static e_Ref writer_print7(e_Ref self, e_Ref *args) {
  return writer_print(self, args, 7);
}

static e_Ref writer_println0(e_Ref self, e_Ref *args) {
  return e_print(self, self.data.refs[1]);
}

static e_Ref writer_println(e_Ref self, e_Ref *args) {
  E_ERROR_CHECK(writer_print1(self, args));
  E_ERROR_CHECK(e_print(self, self.data.refs[1]));
  return e_null;
}

static e_Ref writer_quotePrint(e_Ref self, e_Ref *args) {
  e_Ref arg = e_ref_target(args[0]);
  if (e_is_string(arg)) {
    GString *original = arg.data.other;
    e_Ref escapedString = e_make_string(g_strescape(original->str, NULL));
    E_ERROR_CHECK(e_print(self, e_make_string("\"")));
    E_ERROR_CHECK(writer_print1(self, &escapedString));
    E_ERROR_CHECK(e_print(self, e_make_string("\"")));
  } else {
    E_ERROR_CHECK(writer_print1(self, args));
  }
  return e_null;
}

static e_Ref writer_printOn(e_Ref self, e_Ref *args) {
  E_ERROR_CHECK(e_print(args[0], e_make_string("<writer>")));
  return e_null;
}

static e_Ref writer_indent(e_Ref self, e_Ref *args) {
  e_Ref new = e_make_writer(self.data.refs[0].data.other);
  e_Selector add;
  e_make_selector(&add, "add", 1);
  e_Ref newline = e_call_1(self.data.refs[1], &add, args[0]);
  E_ERROR_CHECK(newline);
  new.data.refs[1] = newline;
  return new;
}

e_Ref e_make_writer(GOutputStream *stream) {
  e_Ref result;
  e_Ref *bits = e_malloc(2 * sizeof *bits);
  bits[0].data.other = stream;
  bits[1] = e_make_string("\n");
  result.script = &e__writer_script;
  result.data.other = bits;
  return result;
}

e_Method writer_methods[] = {
  {"print/1", writer_print1},
  {"print/2", writer_print2},
  {"print/3", writer_print3},
  {"print/4", writer_print4},
  {"print/5", writer_print5},
  {"print/6", writer_print6},
  {"print/7", writer_print7},
  {"println/1", writer_println},
  {"println/0", writer_println0},
  {"quote/1", writer_quotePrint},
  {"__printOn/1", writer_printOn},
  {"indent/1", writer_indent},
  {NULL}
};
e_Script e__writer_script;

e_Ref e_make_string_writer() {
#if OLD_GIO
  GOutputStream *stream = g_memory_output_stream_new(NULL);
#else
#ifdef NO_GC
  GOutputStream *stream = g_memory_output_stream_new(NULL, 0, realloc, NULL);
#else
  GOutputStream *stream = g_memory_output_stream_new(NULL, 0, GC_realloc, NULL);
#endif //NO_GC
#endif //OLD_GIO
  return e_make_writer(stream);
}
e_Ref e_string_writer_get_string(e_Ref writer) {
  GMemoryOutputStream *stream = writer.data.refs[0].data.other;
#if OLD_GIO
   char *output = g_memory_output_stream_get_data(stream)->data;
#else
   char *output = g_memory_output_stream_get_data(stream);
#endif
  return e_make_gstring(
           g_string_new_len(output,
             g_seekable_tell((GSeekable *)stream)));
}


e_Script e__reader_script;
e_Method reader_methods[] = {
  {NULL},
};

e_Ref e_stdin;
e_Ref e_stdout;
e_Ref e_stderr;

