import logging
from pathlib import Path

from gherlint.parser import GherkinParser
from gherlint.utils import iter_feature_files

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
logger.addHandler(handler)


class LanguageFixer:
    def __init__(self, path: Path) -> None:
        self.path = path

    def run(self, modify: bool) -> None:
        if not modify:
            logger.warning("Dry run enabled! No files will be modified.")
        for file in iter_feature_files(self.path):
            parse_result = GherkinParser().parse(file)
            if parse_result.added_language_tag or parse_result.fixed_language_tag:
                logger.info(
                    "Patching %s, reason: %s language tag",
                    file,
                    "no" if parse_result.added_language_tag else "wrong",
                )
                if modify:
                    file.write_text(parse_result.content, "utf8")
