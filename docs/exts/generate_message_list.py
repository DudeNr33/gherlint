"""Helper script to generate a table of all messages that gherlint emits."""

from sphinx.application import Sphinx
from utils import TableWriter

from gherlint.checkers.base_checker import BaseChecker
from gherlint.linter import GherkinLinter
from gherlint.registry import CheckerRegistry


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


def setup(app: Sphinx) -> dict[str, str]:
    app.connect("builder-inited", main)
    return {"version": "0.1"}
