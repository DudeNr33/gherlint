"""Helper script to convert all .puml/.plantuml files stored under docs/diagrams into images."""

from __future__ import annotations

from itertools import chain
from pathlib import Path
from typing import Dict

import plantuml
from sphinx.application import Sphinx
from sphinx.util import logging

logger = logging.getLogger(__name__)


def convert(app: Sphinx) -> None:
    """Convert all .puml/.plantuml files stored under docs/diagrams into images."""
    logger.info("Converting PlantUML diagrams...")
    diagrams = app.config.plantuml_diagrams
    for filename in chain(diagrams.rglob("*.puml"), diagrams.rglob("*.plantuml")):
        logger.info(f"Processing {filename}...")
        plantuml.PlantUML(app.config.plantuml_server).processes_file(filename)
    else:  # pylint: disable=useless-else-on-loop
        logger.info("No PlantUML diagrams found.")


def setup(app: Sphinx) -> Dict[str, str]:
    """Register the extension."""
    # plantuml_diagrams = Path(__file__).parent / "diagrams"
    # plantuml_server = "http://www.plantuml.com/plantuml/img/"
    app.add_config_value("plantuml_diagrams", Path(app.srcdir) / "diagrams", "html")
    app.add_config_value(
        "plantuml_server", "http://www.plantuml.com/plantuml/img/", "html"
    )
    app.connect("builder-inited", convert)
    return {"version": "0.1"}
