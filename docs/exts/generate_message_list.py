"""Helper script to generate a table of all messages that gherlint emits."""

from typing import Dict, List

from sphinx.application import Sphinx

from gherlint.checkers.base_checker import BaseChecker
from gherlint.linter import GherkinLinter
from gherlint.registry import CheckerRegistry


class TableWriter:
    def __init__(self) -> None:
        self._lines: List[str] = []

    def add_directive(self) -> None:
        self._lines.append(".. list-table::")
        self._lines.append("   :header-rows: 1")
        self._lines.append("")

    def add_header(self, *headings: str) -> None:
        self.add_row(*headings)

    def add_row(self, *values: str) -> None:
        first = True
        for value in values:
            if first:
                content = f"   * - {value}"
                first = False
            else:
                content = f"     - {value}"
            self._lines.append(content)

    def __str__(self) -> str:
        return "\n".join(self._lines)


def main(app: Sphinx) -> None:
    table = TableWriter()
    table.add_directive()
    table.add_header("ID", "Name", "Description")
    registry = CheckerRegistry()
    registry.discover()
    for message in GherkinLinter.MESSAGES:
        table.add_row(message.id, message.name, message.text)
    for checker in sorted(registry, key=_get_msg_prefix):
        for message in checker.MESSAGES:
            table.add_row(message.id, message.name, message.text)
    with open(
        f"{app.srcdir}/messages/list_of_messages.rst", "w", encoding="utf8"
    ) as file:
        file.write("List of Messages\n")
        file.write("================\n\n")
        file.write(str(table))
        file.write("\n\n")


def _get_msg_prefix(checker: BaseChecker) -> int:
    return int(checker.MESSAGES[0].id[1:-2])


def setup(app: Sphinx) -> Dict[str, str]:
    app.connect("builder-inited", main)
    return {"version": "0.1"}
