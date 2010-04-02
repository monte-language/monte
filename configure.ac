AC_PREREQ(2.64)
LT_PREREQ([2.2.6])
AC_INIT([Ecru], [0.3.0], [washort42@gmail.com], [ecru], [http://launchpad.net/ecru])
AC_CONFIG_AUX_DIR(build-aux)
AM_INIT_AUTOMAKE([1.11.1 foreign -Wall -Werror])
AM_SILENT_RULES([yes])
LT_INIT([dlopen])
AC_CONFIG_MACRO_DIR([build-aux/m4])
AC_DEFINE([OLD_GIO], [], ["Whether to use the old GIO API or not"])
AC_CONFIG_HEADERS([config.h])

AC_PROG_CC
AC_PROG_CC_C99
AM_PROG_CC_C_O
AC_TYPE_INT64_T

AC_CONFIG_SRCDIR([src/vm.c])
AC_CHECK_HEADERS([gc/gc.h], [],
                [AC_MSG_ERROR([No header files for Boehm GC found.])])
AC_CHECK_HEADERS([gmp.h], [],
                 [AC_MSG_ERROR([No header files for GNU MP found.])])

AC_CHECK_LIB(m, ceil)
AC_CHECK_LIB(gc, GC_malloc)
AC_CHECK_LIB(gmp, __gmpz_init)
PKG_CHECK_MODULES([CHECK], [check >= 0.9.4])
PKG_CHECK_MODULES([GLIB], [glib-2.0 >= 2.14 gio-2.0 >= 0.1.2 gio-unix-2.0 >= 0.1.2  gthread-2.0])
PKG_CHECK_EXISTS([gio-2.0 >= 2.15 gio-unix-2.0 >= 2.15],
                           [AC_DEFINE([OLD_GIO], [0], [])],
                           [AC_DEFINE([OLD_GIO], [1], [])])

AC_PYTHON_DEVEL([>= '2.5'])
# Directly based on code in ac_python_devel.m4. Gets us -fno-strict-aliasing.
AC_MSG_CHECKING([for flags required for compiling Python code])
PYTHON_CFLAGS=`$PYTHON -c "import distutils.sysconfig; \
		       conf = distutils.sysconfig.get_config_var; \
		       print conf('BASECFLAGS')"`
AC_MSG_RESULT([$PYTHON_CFLAGS])
AC_SUBST([PYTHON_CFLAGS])

AM_PATH_PYTHON([2.5])

AC_CONFIG_FILES([Makefile])
AC_OUTPUT
