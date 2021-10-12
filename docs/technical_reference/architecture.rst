Architecture
============

This section documents the most important architectural elements of ``gherlint``.

Main Concept
------------

The linting process is coordinated by :py:class:`gherlint.linter.GherkinLinter`.
It constructs abstract syntax trees for each file and passes them to :py:class:`gherlint.walker.ASTWalker`.
The :py:class:`gherlint.walker.ASTWalker` has a list of checker classes (concrete implementations of
:py:class:`gherlint.checkers.base_checker.BaseChecker`) which implement a ``Visitor`` pattern:
each checker implements ``visit_<nodetype>`` and ``leave_<nodetype>`` methods for the elements it is interested.
The :py:class:`ASTWalker` calls those methods on the checkers that have implemented them for each node while
it traverses the tree.
The checkers themselves define one or several :py:class:`Message`s which can be emitted through a class that
implements the :py:class:`Reporter` protocol.

.. uml::
    :caption: Static Representation

    set namespaceSeparator none
    class "ASTWalker" as gherlint.walker.ASTWalker {
    }
    class "BaseChecker" as gherlint.checkers.base_checker.BaseChecker {
    }
    class "GherkinLinter" as gherlint.linter.GherkinLinter {
    }
    class "Message" as gherlint.reporting.Message {
    }
    class "Reporter" as gherlint.reporting.Reporter {
    }
    gherlint.reporting.Reporter -up-* gherlint.linter.GherkinLinter : reporter
    gherlint.walker.ASTWalker -up-* gherlint.linter.GherkinLinter : walker
    gherlint.reporting.Reporter --* gherlint.checkers.base_checker.BaseChecker : reporter
    gherlint.walker.ASTWalker "1" *-- "n" gherlint.checkers.base_checker.BaseChecker: checkers
    gherlint.checkers.base_checker.BaseChecker "1" *-- "n" gherlint.reporting.Message


Startup Phase
-------------

The user invokes ``gherlint`` through the command line, where he can specify additional options
like the ``Reporter`` class to use or what additional checkers to load.
The ``main`` function constructs a ``Config`` object which is passed to ``GherkinLinter``.
According to the configuration the ``GherkinLinter`` creates the reporter, checker instances and
the walker which will be necessary for running the linting operation.
The linting itself is described in the next section.

.. uml::
    :caption: Startup Phase

    actor User

    User --> main ++ : gherlint lint (options)
        main->main ++ : create_config(options)
        return config
        main --> GherkinLinter ++ : init(config)
            GherkinLinter --> Reporter : init(config)
            GherkinLinter->GherkinLinter ++ : load_checkers()
            return checkers
            GherkinLinter --> ASTWalker: init(checkers)
            return linter
        main --> GherkinLinter ++ : run
        note right: the logic of the *run* method is described in a separate diagram
        return exit_code
    return sys.exit(exit_code)


The linting process is started by calling the ``run`` method on ``GherkinLinter``.
For each file in the directory which was passed to the ``__init__`` of ``GherkinLinter``,
it will construct a ``Document`` object which contains the full abstract syntax tree (AST)
of the file. This root node is passed to the ``ASTWalker``'s ``walk`` method.
The ``ASTWalker`` will first call the ``visit_<node>`` method (where ``<node>`` is
the lowertype class name of the ``node``) on all checkers that implement them, before
it recursively calls ``walk(child_node)`` for all the ``node``'s children (if any) on itself.
Afterwards the ``leave_<node>`` method is called analogous to the ``enter_<node>`` method.

.. uml::
    :caption: Lintin Phase

    main --> GherkinLinter ++ : run
        loop for file in path
            GherkinLinter->GherkinLinter ++ : lint_file(filepath)
            GherkinLinter --> Document ++ : from_dict(data)
            note right: This will recursively create the AST
            return document
            GherkinLinter --> ASTWalker ++ : walk(document)
            loop for checker in checkers
            opt implements visit_<node>
                ASTWalker --> Checker ++ : visit_<node>(node)
                return
            end
            end
            loop for child_node in children
            ASTWalker->ASTWalker ++ : walk(child_node)
            note right: recursively traverse AST
            return
            end
            loop for checker in checkers
            opt implements leave_<node>
                ASTWalker --> Checker ++ : leave_<node>(node)
                return
            end
            end
            return
        end
        return
    return
