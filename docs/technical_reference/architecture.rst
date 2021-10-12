Architecture
============

This section documents the most important architectural elements of :py:mod:`gherlint`.

Main Concept
------------

The linting process is coordinated by :py:class:`GherkinLinter`.
It constructs abstract syntax trees for each file and passes them to :py:class:`ASTWalker`.
The :py:class:`ASTWalker` has a list of checker classes (concrete implementations of
:py:class:`BaseChecker`) which implement a ``Visitor`` pattern:
each checker implements :py:func:`visit_nodetype` and :py:func:`leave_nodetype` methods for the elements it is interested.
The :py:class:`ASTWalker` calls those methods on the checkers that have implemented them for each node while
it traverses the tree.
The checkers themselves define one or several :py:class:`Message` which can be emitted through a class that
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

The user invokes :py:mod:`gherlint` through the command line, where he can specify additional options
like the :py:class:`Reporter` class to use or what additional checkers to load.
The :py:func:`main` function constructs a :py:class:`Config` object which is passed to :py:class:`GherkinLinter`.
According to the configuration the :py:class:`GherkinLinter` creates the reporter, checker instances and
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


The linting process is started by calling the :py:func:`run` method on :py:class:`GherkinLinter`.
For each file in the directory which was passed to the :py:func:`__init__` of :py:class:`GherkinLinter`,
it will construct a :py:class:`Document` object which contains the full abstract syntax tree (AST)
of the file. This root node is passed to the :py:class:`ASTWalker`'s :py:func:`walk` method.
The :py:class:`ASTWalker` will first call the :py:func:`visit_nodetype` method (where ``nodetype`` is
the lowertype class name of the ``node``) on all checkers that implement them, before
it recursively calls :py:func:`walk(child_node)` for all the ``node``'s children (if any) on itself.
Afterwards the :py:func:`leave_nodetype` method is called analogous to the :py:func:`enter_nodetype` method.

.. uml::
    :caption: Linting Phase

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


Message Handling
----------------

Each checker has a number of messages it can emit.
:py:class:`Message` instances are stored in a central :py:class:`MessageStore`.
The individual :py:func:`vist_<node>` and :py:func:`leave_<node>` methods are responsible to determine
whether a specific message shall be emitted. They use the :py:class:`Reporter` to add a message to emit
by passing the ``name`` or ``id`` of the message. The :py:class:`Reporter` looks up the message instance
through the :py:class:`MessageStore`.

.. uml::
    :caption: Message Handling (Static View)

    class Reporter {
        add_message(msg: Message, node: Node)
    }
    class Message {
        id : str
        name: str
        description : str
    }
    class MessageStore {
        messages : List[Message]
        register_message(msg: Message) -> None
        get_by_id(id: str) -> Message
        get_by_name(name: str) -> Message
    }
    class Checker {
        messages : List[Message]
        visit_<node>(node: Node) -> None
        leave_<node>(node: Node) -> None
    }

    Checker "1" *-down- "n" Message
    MessageStore "1" *-up- "n" Message
    Checker *-- Reporter
    Checker --> MessageStore : uses
    Reporter --> MessageStore : uses


.. uml::
    :caption: Message Handling (Dynamic View)

    participant Checker
    participant Reporter
    participant MessageStore
    group Initialization of Checker
        loop for message in messages
            Checker --> MessageStore ++ : register_message(message)
            return
        end
    end
    group Linting Process
        Checker --> Reporter ++ : add_message(id_or_name)
            alt matches_id_pattern
                Reporter --> MessageStore ++ : get_by_id(id_or_name)
                return message
            else matches_name_pattern
                Reporter --> MessageStore ++ : get_by_name(id_or_name)
                return message
            end
            Reporter->Reporter ++ : emit(message)
            return
        return
    end
