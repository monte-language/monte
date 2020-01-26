Colophon: Monte Documentation Build Tools
=========================================

Restructured text
-----------------

The docs are written in `restructured text`_. 

.. _restructured text: http://docutils.sourceforge.net/docs/user/rst/quickref.html

Sphinx
------

The docs are built with `Sphinx`_ and hosted on `readthedocs`_. 

To locally build the docs, use Nix.

.. code-block:: shell

    $ nix-shell -p pythonPackages.sphinx --run 'make -C docs html'

The generated HTML will be in ``docs/build/html``. Point a browser at
``docs/build/html/index.html`` to preview your changes.

.. _Sphinx: http://sphinx-doc.org/
.. _readthedocs: https://readthedocs.org/projects/monte/

Syntax Railroad Diagrams and Haskell Parser
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``rr_ext.py`` is an extension that integrates the
`railroad-diagrams`__ library by Tab Atkins into the build process.
It provides a custom ``.. syntax::`` directive.

__ https://github.com/tabatkins/railroad-diagrams

If `syntax_dest` is set in `conf.py`, the syntax diagram info
is written to a file in JSON format. download:`rr_grammar.py` converts
this format to a `sphinx grammar production display`__.

__ http://www.sphinx-doc.org/en/stable/markup/para.html#grammar-production-displays

download:`rr_happy.py` is work-in-progress to generate a haskell monadic
parser.

Doctests
--------

Use `make doctest` to extract the `source/docs_examples.mt` test suite
from the documentation. Then run it a la `typhon loader test
docs_examples`.

