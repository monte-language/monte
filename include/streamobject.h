#ifndef ECRU_STREAM_H
#define ECRU_STREAM_H

extern e_Ref e_stdin;
extern e_Ref e_stdout;
extern e_Ref e_stderr;

extern e_Script e__writer_script;
extern e_Script e__reader_script;
extern e_Method writer_methods[];
extern e_Method reader_methods[];

e_Ref e_make_writer(GOutputStream *stream);

static inline e_Ref e_make_reader(GInputStream *stream) {
  e_Ref ref;
  ref.script = &e__reader_script;
  ref.data.other = stream;
  return ref;
}

e_Ref e_make_string_writer();
e_Ref e_string_writer_get_string(e_Ref writer);

extern e_Selector e_do_printOn;
extern e_Selector e_do_print;
extern e_Selector e_do_quote_print;
extern e_Selector e_do_println;

static inline e_Ref e_print(e_Ref out, e_Ref ref) {
  return e_call_1 (out, &e_do_print, ref);
}

static inline e_Ref e_println(e_Ref out, e_Ref ref) {
  return e_call_1 (out, &e_do_println, ref);
}

static inline e_Ref e_print_on(e_Ref ref, e_Ref out) {
  return e_call_1 (ref, &e_do_printOn, out);
}

static inline e_Ref
e_quote_print(e_Ref out, e_Ref ref) {
  return e_call_1 (out, &e_do_quote_print, ref);
}

#endif
