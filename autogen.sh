#!/bin/sh

set -e

srcdir=`dirname $0`
test -z "$srcdir" && srcdir=.
cd $srcdir

autoreconf

exec $srcdir/configure "$@"
