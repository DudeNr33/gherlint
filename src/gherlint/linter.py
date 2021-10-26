from pathlib import Path
from typing import List, Union

from gherkin.parser import CompositeParserException, Parser

from gherlint.checkers.base_checker import BaseChecker
from gherlint.objectmodel.nodes import Document
from gherlint.registry import CheckerRegistry
from gherlint.reporting import Message, TextReporter
from gherlint.walker import ASTWalker


class GherkinLinter(BaseChecker):
    """Main linter class which orchestrates the linting process."""

    MESSAGES = [Message("E001", "unparseable-file", "File could not be parsed")]

    def __init__(self, path: str) -> None:
        super().__init__(reporter=TextReporter())
        self.path = Path(path)
        self.checker_registry = CheckerRegistry()
        self.checker_registry.discover()
        self.checkers: List[BaseChecker] = [
            checker(self.reporter) for checker in self.checker_registry
        ]
        self.walker = ASTWalker(self.checkers)
        self.parser = Parser()

    def run(self) -> None:
        """Lint all feature files"""
        if self.path.is_file():
            self.lint_file(self.path)
        else:
            for filepath in self.path.rglob("*.feature"):
                self.lint_file(filepath)

    def lint_file(self, filepath: Union[str, Path]):
        try:
            data = self.parser.parse(str(filepath))
        except CompositeParserException:
            self.reporter.add_message(
                "unparseable-file",
                Document(
                    line=0, column=0, filename=str(filepath), feature=None, comments=[]
                ),
            )
        else:
            data["filename"] = str(filepath)
            document = Document.from_dict(data)
            self.walker.walk(document)
