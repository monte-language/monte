Toolchain around Monte and its documentation
============================================

Restructured text
-----------------

The docs are written in `restructured text`_. 

Sphinx
------

The docs are built with `Sphinx`_ and hosted on `readthedocs`_. 

The virtualenv for building the docs is separate from the main Monte
virtualenv. Create a separate virtualenv and ``pip install -r
docs_requirements.txt``, then ``make html`` to make the docs. Locally built
docs will show up in the docs/build directory. 

Travis
------

`Travis`_ is used for Monte's continuous integration testing. This means that
it will automatically rebuild and test the project every time a commit is
pushed or branch is merged into master. 

Since we don't need to run the tests and spam the IRC channel every time a
change is pushed to the documentation, it's possible to make Travis skip
building a given commit by adding ``[skip ci]`` or ``[ci skip]`` to the body
of the commit message. There are more docs on skipping commits `here`_.

.. _restructured text: http://docutils.sourceforge.net/docs/user/rst/quickref.html
.. _Sphinx: http://sphinx-doc.org/
.. _readthedocs: https://readthedocs.org/projects/monte/
.. _Travis: https://travis-ci.org/monte-language/monte
.. _here: http://docs.travis-ci.com/user/how-to-skip-a-build/


Editor Syntax Highlighting
==========================

Atom
----

Make changes to the grammar as needed and commit those changes. Atom's package
manager, apm, will handle package.json updating for you. When ready to publish
the new version run

    apm publish minor

unless it's a major version change, then

    apm publish major
