
[![CI](https://github.com/DudeNr33/gherlint/actions/workflows/CI.yml/badge.svg)](https://github.com/DudeNr33/gherlint/actions/workflows/CI.yml)
[![Documentation Status](https://readthedocs.org/projects/gherlint/badge/?version=latest)](https://gherlint.readthedocs.io/en/latest/?badge=latest)
![PyPI](https://img.shields.io/pypi/v/gherlint)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/gherlint)
![PyPI - License](https://img.shields.io/pypi/l/gherlint)
# gherlint
Linter for Gherkin feature files, written in Python

## Install
Simply run ``pip install gherlint``.

## Linting Feature Files
``gherlint`` comes with a command line interface.
To recursively lint all feature files in a directory, run ``gherlint lint <path>``.

## Computing Metrics
``gherlint`` can also create some metrics for you if you want to know how many features, scenarios and steps you have
in your test suite. To do so, run ``gherlint stats <path>``.

## Disclaimer
``gherlint`` is still in an early development phase. New checks will be added over time.
If you want to contribute, feel free to open issues suggesting useful checkers, or open a pull request if you want to!

## Roadmap

The following work items are planned for the upcoming releases:

* V0.0.x - V0.1.0:
    * Parser and object model for feature files
    * Basic checkers to demonstrate workflow
    * Basic text based reporter
* V0.1.x - V1.0: **<-- we are here**
    * Add more checkers
    * Add more output formats
    * Extend object model as necessary for checkers
    * Reach a stable interface for object model, checkers and reporters
    * Add documentation
* V1.x - V2.0:
    * Support configuration to enable/disable individual messages
    * Implement plugin architecture to allow users to add custom checkers
