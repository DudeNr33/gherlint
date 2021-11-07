# CHANGELOG

## V0.5.0
New checks:
* ``duplicated-scenario-name``
* ``duplicated-feature-name``
* ``only-given-allowed-in-background``

## V0.4.0
New checks:
* ``unused-parameter``
* ``empty-background``
* ``outline-could-be-a-scenario``
* ``consider-using-background``
* ``examples-outside-scenario-outline``
* ``duplicated-tag``

Other changes:
* ``unparseable-file`` is now issued for all nodes that offend the ``gherkin`` parser together with more error information provided by it
* ``missing-parameter`` now clearly states what parameter is not defined in the examples
* If ``gherlint`` patches the file contents with a forgotten ``# language`` tag the line numbers for messages
are no longer shifted
* Types of ``And`` and ``But`` steps are now inferred correctly
* New command ``fix-language-tags`` to automatically add or fix missing or incorrect language tags
* Rename some message codes to have a defined structure: each checker has its own hundreds digit.

## V0.3.0
New checks:
* ``missing-language-tag``
* ``wrong-language-tag``
* ``unparseable-file``

Other changes:
* ``gherlint`` can now automatically detect the language used and make sure that it can parse the files
even without a ``# language`` token present.

## V0.2.0
New checks:
* ``missing-given-step``
* ``missing-when-step``
* ``missing-then-step``
* ``empty-scenario``
* ``empty-feature``
* ``file-has-no-feature``
* ``missing-parameter``

Other changes:
* Support for ``Background``
* Determination of step type independent of language
* Distinction between ``Scenario`` and ``Scenario Outline`` independent of language

## V0.1.0
First package in alpha status:
* Parser and object model for feature files
* Basic checkers to demonstrate workflow
* Basic text based reporter
