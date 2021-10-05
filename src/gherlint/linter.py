from pathlib import Path
from typing import Union

from gherkin.parser import Parser

from gherlint.checkers.completeness import CompletenessChecker
from gherlint.checkers.statistics import Statistics
from gherlint.objectmodel.nodes import Document
from gherlint.walker import ASTWalker


class GherkinLinter:
    """Main linter class which orchestrates the linting process."""

    def __init__(self, path: str) -> None:
        self.path = Path(path)
        self.walker = ASTWalker(checkers=[CompletenessChecker(), Statistics()])
        self.parser = Parser()

    def run(self) -> None:
        """Lint all feature files"""
        if self.path.is_file():
            self.lint_file(self.path)
        else:
            for filepath in self.path.rglob("*.feature"):
                self.lint_file(filepath)
        Statistics().print_summary()

    def lint_file(self, filepath: Union[str, Path]):
        data = self.parser.parse(str(filepath))
        document = Document.from_dict(data)
        self.walker.walk(document)
