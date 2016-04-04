Colophon: Monte Documentation Build Tools
=========================================

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

.. _restructured text: http://docutils.sourceforge.net/docs/user/rst/quickref.html
.. _Sphinx: http://sphinx-doc.org/
.. _readthedocs: https://readthedocs.org/projects/monte/

Syntax Railroad Diagrams and Haskell Parser
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``rr_ext.py`` is an extension that integrates the
`railroad-diagrams`__ library by Tab Atkins into the build process.
It provides a custom ``.. syntax::`` directive.

__ https://github.com/tabatkins/railroad-diagrams

``rr_happy.py`` is work-in-progress to generate a haskell monadic
parser from the syntax diagram directives.

Doctests
--------

Use `make doctest` to extract the `source/docs_examples.mt` test suite
from the documentation. Then run it a la `typhon loader test
docs_examples`.

TODO List
---------

.. todolist::
