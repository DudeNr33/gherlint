Architecture
============

This section documents the most important architectural elements of :py:mod:`gherlint`.

Main Concept
------------

The linting process is coordinated by :py:class:`GherkinLinter`.
It constructs abstract syntax trees for each file and passes them to :py:class:`ASTWalker`,
together with a list of checkers which where discovered by the :py:class:`CheckerRegistry`.
The checker classes implement a ``Visitor`` pattern:
each checker can implement :py:func:`visit_nodetype` and :py:func:`leave_nodetype` methods for the elements it is interested.
The :py:class:`ASTWalker` calls those methods on the checkers for each node while it traverses the tree.
The checkers themselves define one or several :py:class:`Message` which are registered in a central :py:class:`MessageStore`
and can be emitted through a class that inherits from :py:class:`Reporter` (or defines the necessary methods).

.. image:: ../diagrams/static_representation.png


Startup Phase
-------------

The user invokes :py:mod:`gherlint` through the command line, where he can specify additional options
like the :py:class:`Reporter` class to use or what additional checkers to load.
The :py:func:`main` function constructs a :py:class:`Config` object which is passed to :py:class:`GherkinLinter`.
According to the configuration the :py:class:`GherkinLinter` creates the reporter, checker instances and
the walker which will be necessary for running the linting operation.
The linting itself is described in the next section.

.. image:: ../diagrams/startup_phase.png


The linting process is started by calling the :py:func:`run` method on :py:class:`GherkinLinter`.
For each file in the directory which was passed to the :py:func:`__init__` of :py:class:`GherkinLinter`,
it will construct a :py:class:`Document` object which contains the full abstract syntax tree (AST)
of the file. This root node is passed to the :py:class:`ASTWalker`'s :py:func:`walk` method.
The :py:class:`ASTWalker` will first call the :py:func:`visit_nodetype` method (where ``nodetype`` is
the lowertype class name of the ``node``) on all checkers that implement them, before
it recursively calls :py:func:`walk(child_node)` for all the ``node``'s children (if any) on itself.
Afterwards the :py:func:`leave_nodetype` method is called analogous to the :py:func:`enter_nodetype` method.

.. image:: ../diagrams/linting_phase.png


Message Handling
----------------

Each checker has a number of messages it can emit.
:py:class:`Message` instances are stored in a central :py:class:`MessageStore`.
The individual :py:func:`vist_<node>` and :py:func:`leave_<node>` methods are responsible to determine
whether a specific message shall be emitted. They use the :py:class:`Reporter` to add a message to emit
by passing the ``name`` or ``id`` of the message. The :py:class:`Reporter` looks up the message instance
through the :py:class:`MessageStore`.

.. image:: ../diagrams/message_handling_static.png

.. image:: ../diagrams/message_handling_dynamic.png
