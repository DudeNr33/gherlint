"""Parser for Gherkin feature files."""
from pathlib import Path
from typing import NamedTuple, Optional

import parse
from gherkin.dialect import DIALECTS
from gherkin.parser import CompositeParserException, Parser

from gherlint.objectmodel import nodes


class ParseResult(NamedTuple):
    document: nodes.Document
    content: str
    exception: Optional[CompositeParserException]
    added_language_tag: bool
    fixed_language_tag: bool


class GherkinParser:
    def __init__(self) -> None:
        self.parser = Parser()
        self.language = "en"
        self.content = ""
        self.offset = 0
        self.added_language_tag = False
        self.fixed_language_tag = False

    def parse(self, filepath: Path) -> ParseResult:
        self.content = filepath.read_text("utf8")
        self._detect_language()
        if self.language not in ("en", "unknown"):
            self._check_and_fix_language()
        try:
            data = self.parser.parse(self.content)
            data["filename"] = str(filepath)
            data["offset"] = self.offset
            document = nodes.Document.from_dict(data)
            exception = None
        except CompositeParserException as exc:
            document = nodes.Document(
                line=0, column=0, filename=str(filepath), feature=None, comments=[]
            )
            exception = exc
        return ParseResult(
            document=document,
            content=self.content,
            exception=exception,
            added_language_tag=self.added_language_tag,
            fixed_language_tag=self.fixed_language_tag,
        )

    def _detect_language(self) -> None:
        if "Feature:" in self.content:
            self.language = "en"
        for language, keywords in DIALECTS.items():
            if any(keyword in self.content for keyword in keywords["feature"]):
                self.language = language
                break
        else:
            self.language = "unknown"

    def _check_and_fix_language(self) -> None:
        match = parse.search("# language: {:l}\n", self.content)
        if not match:
            self.added_language_tag = True
            self.offset += 1
            self.content = f"# language: {self.language}\n" + self.content
        elif match[0] != self.language:
            self.fixed_language_tag = True
            self.content = self.content.replace(
                f"# language: {match[0]}", f"# language: {self.language}"
            )
