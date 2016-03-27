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

TODO List
---------

.. todolist::
