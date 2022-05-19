import re
from typing import Optional, Pattern

from pydantic import validator

from gherlint.checkers.base_checker import BaseChecker
from gherlint.objectmodel import nodes
from gherlint.options import Options
from gherlint.registry import CheckerRegistry
from gherlint.reporting import Message


class ConventionsCheckerOptions(Options):
    config_section = "convention"

    feature_tags_pattern: Optional[Pattern]
    scenario_tags_pattern: Optional[Pattern]

    # pylint: disable=no-self-argument, disable=no-self-use
    @validator("feature_tags_pattern", "scenario_tags_pattern", pre=True)
    def compile_regex(cls, value: str) -> Optional[Pattern]:
        if value:
            return re.compile(value, re.X)

        return None


class ConventionsChecker(BaseChecker):
    options: ConventionsCheckerOptions

    MESSAGES = [
        Message(
            "C401",
            "feature-tags-pattern-mismatch",
            "Feature tag {tag} do not follow the pattern: {pattern}",
        ),
        Message(
            "C402",
            "scenario-tags-pattern-mismatch",
            "Scenario tag {tag} do not follow the pattern: {pattern}",
        ),
    ]

    def visit_tag(self, node: nodes.Tag) -> None:
        if isinstance(node.parent, nodes.Feature) and self.options.feature_tags_pattern:
            self._check_tag_with_pattern(
                node,
                self.options.feature_tags_pattern,
                "feature-tags-pattern-mismatch",
            )
        elif (
            isinstance(node.parent, (nodes.Scenario, nodes.ScenarioOutline))
            and self.options.scenario_tags_pattern
        ):
            self._check_tag_with_pattern(
                node,
                self.options.scenario_tags_pattern,
                "scenario-tags-pattern-mismatch",
            )

    def _check_tag_with_pattern(
        self,
        node: nodes.Tag,
        pattern: Pattern,
        message_id_or_name: str,
    ) -> None:
        if not pattern.match(node.name):
            self.reporter.add_message(
                message_id_or_name, node, tag=node.name, pattern=pattern.pattern
            )


def register_checker(registry: CheckerRegistry) -> None:
    registry.register(ConventionsChecker)
