"""Helper script to build the list of options for checkers, reporters etc."""
import inspect
from typing import Any

from sphinx.application import Sphinx
from sphinx.util import logging

from gherlint import reporting
from gherlint.options import Options
from gherlint.registry import CheckerRegistry

logger = logging.getLogger(__name__)

TABLE_HEADINGS = ["Option", "Type", "Description"]


class TableWriter:
    def __init__(self) -> None:
        self._lines: list[str] = []

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
        return "\n".join(self._lines) + "\n\n"


def main(app: Sphinx) -> None:
    with open(
        f"{app.srcdir}/options/list_of_options.rst", "w", encoding="utf8"
    ) as file:
        logger.info("Processing Reporter Options...")
        file.write("Reporter Options\n")
        file.write("================\n\n")
        for _, options_class in inspect.getmembers(
            reporting, predicate=_is_options_class
        ):
            logger.info("Processing options class %s", options_class.__name__)
            file.write(f"Config section: **[{options_class.config_section}]**\n\n")
            options_table = TableWriter()
            options_table.add_directive()
            options_table.add_header(*TABLE_HEADINGS)
            for name, field in options_class.__fields__.items():
                logger.info("Processing option %s", name)
                options_table.add_row(
                    name,
                    field._type_display(),  # pylint: disable=protected-access
                    field.field_info.description,
                )
            file.write(str(options_table))

        logger.info("Processing Checker Options...")
        file.write("Checker Options\n")
        file.write("===============\n\n")
        registry = CheckerRegistry()
        registry.discover()
        for checker in registry:
            logger.info("Processing checker %s", checker.__name__)
            options_class = checker.get_options_class()
            if options_class is None:
                logger.info("Checker has no options, skipping.")
                continue
            file.write(f"{checker.__name__}\n")
            file.write(f"{'-' * len(checker.__name__)}\n\n")
            file.write(f"Config section: **[{options_class.config_section}]**\n\n")
            options_table = TableWriter()
            options_table.add_directive()
            options_table.add_header(*TABLE_HEADINGS)
            for name, field in options_class.__fields__.items():
                logger.info("Processing option %s", name)
                options_table.add_row(
                    name,
                    field._type_display(),  # pylint: disable=protected-access
                    field.field_info.description,
                )
            file.write(str(options_table))


def _is_options_class(obj: Any) -> bool:
    return inspect.isclass(obj) and issubclass(obj, Options) and not obj is Options


def setup(app: Sphinx) -> dict[str, str]:
    app.connect("builder-inited", main)
    return {"version": "0.1"}
