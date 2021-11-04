"""Checker focussing on consistency issues."""

from typing import Union

from gherlint.checkers.base_checker import BaseChecker
from gherlint.objectmodel import nodes
from gherlint.registry import CheckerRegistry
from gherlint.reporting import Message


class ConsistencyChecker(BaseChecker):
    MESSAGES = [
        Message(
            "E301",
            "examples-outside-scenario-outline",
            "Examples used outside a Scenario Outline",
        ),
        Message(
            "W301",
            "duplicated-tag",
            "Tag '{tag}' already present on the parent element",
        ),
    ]

    def visit_scenario(
        self, node: Union[nodes.Scenario, nodes.ScenarioOutline]
    ) -> None:
        for example in node.examples:
            self.reporter.add_message("examples-outside-scenario-outline", node=example)
        self._check_duplicated_tag(node)

    def visit_scenariooutline(self, node: nodes.ScenarioOutline) -> None:
        self._check_duplicated_tag(node)

    def visit_examples(self, node: nodes.Examples) -> None:
        self._check_duplicated_tag(node)

    def _check_duplicated_tag(
        self, node: Union[nodes.Scenario, nodes.ScenarioOutline, nodes.Examples]
    ) -> None:
        for tag in node.tags:
            if any(
                tag in parent.tags for parent in node.parents if hasattr(parent, "tags")  # type: ignore
            ):
                self.reporter.add_message("duplicated-tag", node, tag=tag.name)


def register_checker(registry: CheckerRegistry) -> None:
    registry.register(ConsistencyChecker)
