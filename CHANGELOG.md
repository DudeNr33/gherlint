# CHANGELOG


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
