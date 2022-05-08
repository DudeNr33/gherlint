import re
from typing import Optional, Pattern, Union

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


class ConventionChecker(BaseChecker):
    options: ConventionCheckerOptions

    MESSAGES = [
        Message(
            "C401",
            "feature-tags-pattern-mismatch",
            "Feature tags do not follow the pattern: {pattern}",
        ),
        Message(
            "C402",
            "scenario-tags-pattern-mismatch",
            "Scenario tags do not follow the pattern: {pattern}",
        ),
    ]

    def visit_feature(self, node: nodes.Feature) -> None:
        if self.options.feature_tags_pattern:
            self._check_node_tags_with_pattern(
                node,
                self.options.feature_tags_pattern,
                "feature-tags-pattern-mismatch",
            )

    def visit_scenario(self, node: nodes.Scenario) -> None:
        if self.options.scenario_tags_pattern:
            self._check_node_tags_with_pattern(
                node,
                self.options.scenario_tags_pattern,
                "scenario-tags-pattern-mismatch",
            )

    def visit_scenariooutline(self, node: nodes.ScenarioOutline) -> None:
        if self.options.scenario_tags_pattern:
            self._check_node_tags_with_pattern(
                node,
                self.options.scenario_tags_pattern,
                "scenario-tags-pattern-mismatch",
            )

    def _check_node_tags_with_pattern(
        self,
        node: Union[nodes.Feature, nodes.Scenario, nodes.ScenarioOutline],
        pattern: Pattern,
        message_id_or_name: str,
    ) -> None:
        if not pattern.fullmatch(" ".join(tag.name for tag in node.tags)):
            self.reporter.add_message(message_id_or_name, node, pattern=pattern.pattern)


def register_checker(registry: CheckerRegistry) -> None:
    registry.register(ConventionChecker)
