# -*- fill-column: 72 -*-
AUTOMAKE_OPTIONS = subdir-objects
ACLOCAL_AMFLAGS = -I build-aux/m4
EXTRA_DIST = CREDITS DEPENDENCIES NEWS build-aux/checkmk
ecrudir = $(libdir)/ecru
AM_CPPFLAGS = $(GLIB_CFLAGS) -DECRU_BYTECODE_DIR='"$(ecrudir)"' -I$(top_srcdir)/include
lib_LTLIBRARIES = libecru.la
libecru_la_SOURCES = src/prim/null.c src/prim/stringobject.c		\
	src/prim/boolobject.c src/prim/numberobject.c			\
	src/prim/charobject.c src/prim/streamobject.c			\
	src/prim/problemobject.c src/prim/ejectorobject.c		\
	src/prim/mapobject.c src/prim/listobject.c src/prim/setobject.c	\
	src/prim/slotobject.c src/safescope/equalizer.c			\
	src/safescope/comparer.c src/safescope/orderedspace.c		\
	src/safescope/looper.c src/safescope/thrower.c			\
	src/safescope/makelist.c src/safescope/makemap.c		\
	src/safescope/simple_quasiparser.c src/safescope.c		\
	src/safescope/require.c src/safescope/test.c			\
	src/safescope/bind.c src/safescope/is.c				\
	src/safescope/verbfacet.c src/safescope/suchthat.c		\
	src/safescope/traceln.c src/safescope/eobject.c			\
	src/privilegedscope.c src/privilegedscope/timer.c		\
	src/privilegedscope/printobject.c src/guards/numberguard.c	\
	src/guards/listguard.c src/invoke.c src/prim.c src/intern.c	\
	src/vm.c src/ref.c src/bytecode_loader.c src/scope.c		\
	src/guards.c src/import.c src/vat.c

include_HEADERS = include/boolobject.h include/bytecode_loader.h	\
	include/bytecodes.h include/charobject.h include/ecru.h		\
	include/ecruobject.h include/ejectorobject.h include/elib.h	\
	include/elib_private.h include/guards.h include/invoke.h	\
	include/listobject.h include/mapobject.h include/null.h		\
	include/numberobject.h include/privilegedscope.h		\
	include/problemobject.h include/ref.h include/ref_private.h	\
	include/safescope.h include/scope.h include/setobject.h		\
	include/slotobject.h include/streamobject.h			\
	include/stringobject.h include/vm.h include/vat.h

dist_ecru_DATA = bootstrap/com.twistedmatrix.ecru.bytecodeDumper.ec	\
	bootstrap/com.twistedmatrix.ecru.compiler.ec			\
	bootstrap/com.twistedmatrix.ecru.bytecodes.ec			\
	bootstrap/com.twistedmatrix.ecru.debugDump.ec

test_elib_SOURCES = src/tests/test_elib.c
test_elib_LDADD = @CHECK_LIBS@ @GLIB_LIBS@ libecru.la -lgmp -lgc -lm
test_elib_CPPFLAGS = -I$(top_srcdir)/include $(CHECK_CFLAGS) $(GLIB_CFLAGS)

test_vm_SOURCES = src/tests/test_vm.c
test_vm_LDADD = @CHECK_LIBS@ @GLIB_LIBS@ libecru.la -lgmp -lgc -lm
test_vm_CPPFLAGS = -I$(top_srcdir)/include $(CHECK_CFLAGS) $(GLIB_CFLAGS)

test_invoke_SOURCES = src/tests/test_invoke.c
test_invoke_LDADD = @CHECK_LIBS@ @GLIB_LIBS@ libecru.la -lgmp -lgc -lm
test_invoke_CPPFLAGS = -I$(top_srcdir)/include $(CHECK_CFLAGS) $(GLIB_CFLAGS)

test_bytecode_loader_SOURCES = src/tests/test_bytecode_loader.c
test_bytecode_loader_LDADD = @CHECK_LIBS@ @GLIB_LIBS@ libecru.la -lgmp -lgc -lm
test_bytecode_loader_CPPFLAGS = -I$(top_srcdir)/include $(CHECK_CFLAGS)	\
                                $(GLIB_CFLAGS)

test_ref_SOURCES = src/tests/test_ref.c
test_ref_LDADD = @CHECK_LIBS@ @GLIB_LIBS@ libecru.la -lgmp -lgc -lm
test_ref_CPPFLAGS = -I$(top_srcdir)/include $(CHECK_CFLAGS) $(GLIB_CFLAGS)

test_same_SOURCES = src/tests/test_same.c
test_same_LDADD = @CHECK_LIBS@ @GLIB_LIBS@ libecru.la -lgmp -lgc -lm
test_same_CPPFLAGS = -I$(top_srcdir)/include $(CHECK_CFLAGS) $(GLIB_CFLAGS)

test_guards_SOURCES = src/tests/test_guards.c
test_guards_LDADD = @CHECK_LIBS@ @GLIB_LIBS@ libecru.la -lgmp -lgc -lm
test_guards_CPPFLAGS = -I$(top_srcdir)/include $(CHECK_CFLAGS) $(GLIB_CFLAGS)

test_vat_SOURCES = src/tests/test_vat.c
test_vat_LDADD = @CHECK_LIBS@ @GLIB_LIBS@ libecru.la -lgmp -lgc -lm
test_vat_CPPFLAGS = -I$(top_srcdir)/include $(CHECK_CFLAGS) $(GLIB_CFLAGS)

check_PROGRAMS = test_vm test_elib test_invoke test_bytecode_loader	\
                 test_ref test_same test_guards test_vat

ecru_driver_SOURCES = src/driver.c
ecru_driver_LDADD = @GLIB_LIBS@ libecru.la -lgmp -lm -lgc
bin_PROGRAMS = ecru_driver
dist_bin_SCRIPTS = scripts/compile.e scripts/ecru
CLEANFILES = src/tests/test_elib.c src/tests/test_vm.c			\
             src/tests/test_invoke.c src/tests/test_bytecode_loader.c
TESTS = $(check_PROGRAMS)

pyecrudir = $(pythondir)/ecru
pyecru_testdir = $(pythondir)/ecru/test
pymetadir = $(pythondir)/pymeta
pymeta_PYTHON = pysrc/pymeta/__init__.py pysrc/pymeta/boot.py	\
                pysrc/pymeta/builder.py pysrc/pymeta/grammar.py	\
                pysrc/pymeta/runtime.py
pyecru_PYTHON = pysrc/ecru/__init__.py pysrc/ecru/api.py	\
               pysrc/ecru/eparser.py pysrc/ecru/nodes.py	\
               pysrc/ecru/structlike.py
pyecru_test_PYTHON = pysrc/ecru/test/__init__.py	\
               pysrc/ecru/test/test_api.py		\
               pysrc/ecru/test/test_expander.py	\
               pysrc/ecru/test/test_eparser.py

pyecru_LTLIBRARIES = bridge.la
bridge_la_SOURCES = src/monte_bridge.c
bridge_la_LDFLAGS = -avoid-version -module $(PYTHON_LDFLAGS)
bridge_la_CPPFLAGS = $(PYTHON_CPPFLAGS) -I$(top_srcdir)/include $(GLIB_CFLAGS)
bridge_la_CFLAGS = $(PYTHON_CFLAGS) $(AM_CFLAGS)
bridge_la_LIBADD = @GLIB_LIBS@ libecru.la -lgc -lgmp

.ts.c:
	$(top_srcdir)/build-aux/checkmk $< > $@

