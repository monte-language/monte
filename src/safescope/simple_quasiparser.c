#include "elib.h"
#include <string.h>

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
  e_Ref inputs = listguard_coerce(e_null, listguard_args);
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

e_Script substituter_script;
e_Method substituter_methods[] = {
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

e_Script simple__quasiParser_script;
e_Method simple__quasiParser_methods[] = {
  {"valueMaker/1", make_substituter},
  {NULL}};

e_Ref e_simple__quasiParser;
