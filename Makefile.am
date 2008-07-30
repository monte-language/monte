AUTOMAKE_OPTIONS = subdir-objects
ACLOCAL_AMFLAGS = -I build-aux/m4
EXTRA_DIST = CREDITS DEPENDENCIES
ecrudir = $(libdir)/ecru
AM_CPPFLAGS = $(GLIB_CFLAGS) -DECRU_BYTECODE_DIR='"$(ecrudir)"' -I$(top_srcdir)/include
lib_LTLIBRARIES = libecru.la libmonte_bridge.la
libecru_la_SOURCES = src/prim/null.c include/null.h		\
	src/prim/stringobject.c include/stringobject.h		\
	src/prim/boolobject.c include/boolobject.h 		\
	src/prim/numberobject.c include/numberobject.h		\
	src/prim/charobject.c include/charobject.h		\
	src/prim/streamobject.c include/streamobject.h		\
	src/prim/problemobject.c include/problemobject.h	\
	src/prim/ejectorobject.c include/ejectorobject.h	\
	src/prim/mapobject.c include/mapobject.h		\
	src/prim/listobject.c include/listobject.h		\
	src/prim/setobject.c include/setobject.h		\
	src/prim/slotobject.c include/slotobject.h		\
	src/safescope/equalizer.c src/safescope/comparer.c	\
	include/safescope.h					\
	src/invoke.c src/prim.c src/intern.c src/elib_private.h		\
	src/bytecode_loader.h src/bytecode_loader.c src/vm.c src/ref.c	\
	src/safescope.c src/privilegedscope.c src/guards.c src/import.c	\
	src/scope.c src/scope.h include/elib.h src/bytecodes.h src/vm.h	\
	src/ref.h src/ref_private.h src/ecru.h

dist_ecru_DATA = bootstrap/com.twistedmatrix.ecru.bytecodeDumper.ec \
	bootstrap/com.twistedmatrix.ecru.compiler.ec \
	bootstrap/com.twistedmatrix.ecru.bytecodes.ec \
	bootstrap/com.twistedmatrix.ecru.debugDump.ec

libmonte_bridge_la_SOURCES = src/monte_bridge.c
libmonte_bridge_la_CPPFLAGS = -I/usr/include/python2.5 -I$(top_srcdir)/include  $(GLIB_CFLAGS)
libmonte_bridge_la_LIBADD = @GLIB_LIBS@ libecru.la

test_elib_SOURCES = src/tests/test_elib.c
test_elib_LDADD = @CHECK_LIBS@ @GLIB_LIBS@ libecru.la -lgmp
test_elib_CPPFLAGS = -I$(top_srcdir)/include $(CHECK_CFLAGS) $(GLIB_CFLAGS)

test_vm_SOURCES = src/tests/test_vm.c
test_vm_LDADD = @CHECK_LIBS@ @GLIB_LIBS@ libecru.la
test_vm_CPPFLAGS = -I$(top_srcdir)/include $(CHECK_CFLAGS) $(GLIB_CFLAGS)

test_invoke_SOURCES = src/tests/test_invoke.c
test_invoke_LDADD = @CHECK_LIBS@ @GLIB_LIBS@ libecru.la
test_invoke_CPPFLAGS = -I$(top_srcdir)/include $(CHECK_CFLAGS) $(GLIB_CFLAGS)

test_bytecode_loader_SOURCES = src/tests/test_bytecode_loader.c
test_bytecode_loader_LDADD = @CHECK_LIBS@ @GLIB_LIBS@ libecru.la
test_bytecode_loader_CPPFLAGS = -I$(top_srcdir)/include $(CHECK_CFLAGS) $(GLIB_CFLAGS)

test_ref_SOURCES = src/tests/test_ref.c
test_ref_LDADD = @CHECK_LIBS@ @GLIB_LIBS@ libecru.la
test_ref_CPPFLAGS = -I$(top_srcdir)/include $(CHECK_CFLAGS) $(GLIB_CFLAGS)

check_PROGRAMS = test_vm test_elib test_invoke test_bytecode_loader test_ref

ecru_SOURCES = src/driver.c
ecru_LDADD = @GLIB_LIBS@ libecru.la
bin_PROGRAMS = ecru
dist_bin_SCRIPTS = scripts/compile.e scripts/monte
CLEANFILES = src/tests/test_elib.c src/tests/test_vm.c src/tests/test_invoke.c src/tests/test_bytecode_loader.c
TESTS = $(check_PROGRAMS)

montedir = $(pythondir)/monte
pymetadir = $(pythondir)/pymeta
pymeta_PYTHON = pysrc/pymeta/__init__.py pysrc/pymeta/boot.py pysrc/pymeta/builder.py pysrc/pymeta/grammar.py pysrc/pymeta/runtime.py
monte_PYTHON = pysrc/monte/__init__.py pysrc/monte/api.py pysrc/monte/eparser.py pysrc/monte/nodes.py pysrc/monte/structlike.py

.ts.c:
	$(top_srcdir)/build-aux/checkmk $< > $@

