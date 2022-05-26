"""Helper script to build the list of options for checkers, reporters etc."""
import inspect
from typing import Any, Dict

from sphinx.application import Sphinx
from sphinx.util import logging
from utils import TableWriter

from gherlint import reporting
from gherlint.options import Options
from gherlint.registry import CheckerRegistry

logger = logging.getLogger(__name__)

TABLE_HEADINGS = ["Option", "Type", "Description"]


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
            options_table = _render_options(options_class)
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
            options_table = _render_options(options_class)
            file.write(str(options_table))


def _is_options_class(obj: Any) -> bool:
    return inspect.isclass(obj) and issubclass(obj, Options) and not obj is Options


def _render_options(options_class: Options) -> TableWriter:
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
    return options_table


def setup(app: Sphinx) -> Dict[str, str]:
    app.connect("builder-inited", main)
    return {"version": "0.1"}
