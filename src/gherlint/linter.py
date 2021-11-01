from pathlib import Path
from typing import List

import parse

from gherlint.checkers.base_checker import BaseChecker
from gherlint.parser import GherkinParser, ParseResult
from gherlint.registry import CheckerRegistry
from gherlint.reporting import Message, TextReporter
from gherlint.walker import ASTWalker


class GherkinLinter(BaseChecker):
    """Main linter class which orchestrates the linting process."""

    MESSAGES = [
        Message("E001", "unparseable-file", "File could not be parsed: {error_msg}"),
        Message(
            "E002",
            "missing-language-tag",
            (
                "A feature file which uses an other language than English should declare "
                "this with a '# language: <lang>' tag at the beginning of the file."
            ),
        ),
        Message(
            "E003",
            "wrong-language-tag",
            "Language tag does not match the language used",
        ),
    ]

    def __init__(self, path: Path) -> None:
        super().__init__(reporter=TextReporter())
        self.path = path
        self.checker_registry = CheckerRegistry()
        self.checker_registry.discover()
        self.checkers: List[BaseChecker] = [
            checker(self.reporter) for checker in self.checker_registry
        ]
        self.walker = ASTWalker(self.checkers)

    def run(self) -> None:
        """Lint all feature files"""
        if self.path.is_file():
            self.lint_file(self.path)
        else:
            for filepath in self.path.rglob("*.feature"):
                self.lint_file(filepath)

    def lint_file(self, filepath: Path) -> None:
        result = GherkinParser().parse(filepath)
        if result.exception:
            self._handle_parser_error(result)
            return
        if result.added_language_tag:
            self.reporter.add_message(
                "missing-language-tag",
                result.document,
            )
        elif result.fixed_language_tag:
            self.reporter.add_message(
                "wrong-language-tag",
                result.document,
            )
        self.walker.walk(result.document)

    def _handle_parser_error(self, result: ParseResult) -> None:
        offending_lines = str(result.exception).splitlines()[1:]
        for offending_line in offending_lines:
            result.document.line, result.document.column, error_msg = parse.search(
                "({:d}:{:d}): {}, got", offending_line
            )
            self.reporter.add_message(
                "unparseable-file",
                result.document,
                error_msg=error_msg,
            )
