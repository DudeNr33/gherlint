from pathlib import Path
from typing import List

import parse
from gherkin.dialect import DIALECTS
from gherkin.parser import CompositeParserException, Parser

from gherlint.checkers.base_checker import BaseChecker
from gherlint.objectmodel.nodes import Document, Node
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

    def lint_file(self, filepath: Path):
        content = filepath.read_text("utf8")
        language = self.detect_language(content)
        if language not in ("en", "unknown"):
            content = self._check_and_fix_language(language, content, str(filepath))
        try:
            data = self.parser.parse(content)
        except CompositeParserException as exc:
            document = Document(
                line=0, column=0, filename=str(filepath), feature=None, comments=[]
            )
            self._handle_parser_error(exc, document)
        else:
            data["filename"] = str(filepath)
            document = Document.from_dict(data)
            self.walker.walk(document)

    @staticmethod
    def detect_language(content: str) -> str:
        if "Feature:" in content:
            return "en"
        for language, keywords in DIALECTS.items():
            if any(keyword in content for keyword in keywords["feature"]):
                return language
        return "unknown"

    def _check_and_fix_language(
        self, language: str, content: str, filepath: str
    ) -> str:
        match = parse.search("# language: {:l}\n", content)
        if not match:
            self.reporter.add_message(
                "missing-language-tag",
                Document(
                    line=0, column=0, filename=filepath, feature=None, comments=[]
                ),
            )
            return f"# language: {language}\n" + content
        if match[0] != language:
            self.reporter.add_message(
                "wrong-language-tag",
                Document(
                    line=0, column=0, filename=filepath, feature=None, comments=[]
                ),
            )
            return content.replace(f"# language: {match[0]}", f"# language: {language}")
        return content

    def _handle_parser_error(self, exc: CompositeParserException, node: Node) -> None:
        offending_lines = str(exc).splitlines()[1:]
        for offending_line in offending_lines:
            node.line, node.column, error_msg = parse.search(
                "({:d}:{:d}): {}, got", offending_line
            )
            self.reporter.add_message(
                "unparseable-file",
                node,
                error_msg=error_msg,
            )
