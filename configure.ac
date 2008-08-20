AC_INIT([Ecru], [0.1.3], [washort@divmod.com])
AC_CONFIG_AUX_DIR(build-aux)
AM_INIT_AUTOMAKE([foreign])
AC_PREREQ(2.60)
AC_DEFINE([OLD_GIO], [], ["Whether to use the old GIO API or not"])
AM_CONFIG_HEADER(config.h)
AC_LIBTOOL_DLOPEN
AC_PROG_LIBTOOL
AC_PROG_CC
AC_PROG_CC_C99
AM_PROG_CC_C_O
AC_TYPE_INT64_T

AC_CONFIG_SRCDIR([src/vm.c])
AC_CHECK_LIB(m, ceil)
AC_CHECK_LIB(gc, GC_malloc)
AC_CHECK_LIB(gmp, __gmpz_init)
PKG_CHECK_MODULES([CHECK], [check >= 0.9.4])
PKG_CHECK_MODULES([GLIB], [glib-2.0 >= 2.14 gio-2.0 >= 0.1.2 gio-unix-2.0 >= 0.1.2])
PKG_CHECK_EXISTS([gio-2.0 >= 2.15 gio-unix-2.0 >= 2.15],
                           [AC_DEFINE([OLD_GIO], [0], [])],
                           [AC_DEFINE([OLD_GIO], [1], [])])
AM_PATH_PYTHON([2.5])
AC_CONFIG_FILES([Makefile])
AC_OUTPUT
