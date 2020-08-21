========
Glossary
========

.. glossary::
    :sorted:

    message
        An object of the form ``[verb :Str, args :List, namedArgs :Map]``
        which is passed from calling objects to target objects to faciliate
        computation.

    verb
        A string which forms the first element of a message.

    ejector : Coercion
        An object which can be called once to prematurely end control flow.

    guard : Coercion
        An object which provides the coercion protocol.

    prize : Coercion
        The result of a successful coercion.

    quasiliteral
    QL
        An literal expression or pattern which is composed of both literal and
        variable pieces.

    quasiparser
    QP
        An object which provides the :ref:`quasiliteral` protocol.

    auditor
        An object which proves that other objects implement a behavior.

    audition
        The process by which auditors examine object behaviors. Auditors are
        invited to examine the AST and binding guards for audited objects.

    DeepFrozen
        An auditor which proves that its objects are transitively immutable
        and are either composed of plain data or references to other immutable
        objects.

    module
        A :ref:`DeepFrozen` object which provides the :ref:`module` protocol.
