#ifndef BYTECODES_H_
#define BYTECODES_H_

#define OP_POP                  1
#define OP_SWAP                 2
#define OP_DUP                  3
#define OP_ROT                  4
#define OP_LITERAL              5
#define OP_NOUN_OUTER           6
#define OP_SLOT_OUTER           7
#define OP_NOUN_LOCAL           8
#define OP_SLOT_LOCAL           9
#define OP_BIND                 10
#define OP_BINDSLOT             11
#define OP_CALL                 12
#define OP_LIST_PATT            13
#define OP_SIMPLEVARSLOT        14
#define OP_GUARDEDVARSLOT       15
#define OP_COERCETOSLOT         16
#define OP_ASSIGN_LOCAL         17
#define OP_EJECTOR              18
#define OP_UNWIND               19
#define OP_TRY                  20
#define OP_END_HANDLER          21
#define OP_JUMP                 22
#define OP_EJECTOR_ONLY         23
#define OP_BRANCH               24
#define OP_OBJECT               25
#define OP_BINDOBJECT           26
#define OP_VAROBJECT            27
#define OP_NOUN_FRAME           28
#define OP_ASSIGN_FRAME         29
#define OP_SLOT_FRAME           30
#define OP_ASSIGN_OUTER         31

#endif /*BYTECODES_H_*/
