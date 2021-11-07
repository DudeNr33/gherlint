"""Checker focussing on consistency issues."""

from typing import Set, Union

from gherlint.checkers.base_checker import BaseChecker
from gherlint.objectmodel import nodes
from gherlint.registry import CheckerRegistry
from gherlint.reporting import Message, Reporter


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
        Message(
            "C301",
            "duplicated-scenario-name",
            "Scenarios inside a Feature should have unique names",
        ),
        Message(
            "C302",
            "only-given-allowed-in-background",
            "Only 'Given' steps are allowed in a Background",
        ),
    ]

    def __init__(self, reporter: Reporter) -> None:
        super().__init__(reporter)
        self.feature_names: Set[str] = set()
        self.scenario_names: Set[str] = set()

    def visit_feature(self, node: nodes.Feature) -> None:
        self.scenario_names.clear()
        if node.name in self.feature_names:
            self.reporter.add_message("duplicated-feature-name", node)
        if node.name:
            self.feature_names.add(node.name)

    def visit_scenario(self, node: nodes.Scenario) -> None:
        for example in node.examples:
            self.reporter.add_message("examples-outside-scenario-outline", node=example)
        self._check_duplicated_scenario_name(node)
        self._check_duplicated_tag(node)

    def visit_scenariooutline(self, node: nodes.ScenarioOutline) -> None:
        self._check_duplicated_scenario_name(node)
        self._check_duplicated_tag(node)

    def visit_examples(self, node: nodes.Examples) -> None:
        self._check_duplicated_tag(node)

    def visit_step(self, node: nodes.Step) -> None:
        self._check_wrong_step_type_in_background(node)

    def _check_duplicated_scenario_name(
        self, node: Union[nodes.Scenario, nodes.ScenarioOutline]
    ):
        if not node.name:
            # if the scenario has no name, we do not need this check - missing-scenario-name will trigger here.
            return
        if node.name in self.scenario_names:
            self.reporter.add_message("duplicated-scenario-name", node)
        self.scenario_names.add(node.name)

    def _check_duplicated_tag(
        self, node: Union[nodes.Scenario, nodes.ScenarioOutline, nodes.Examples]
    ) -> None:
        for tag in node.tags:
            if any(
                tag in parent.tags for parent in node.parents if hasattr(parent, "tags")  # type: ignore
            ):
                self.reporter.add_message("duplicated-tag", node, tag=tag.name)

    def _check_wrong_step_type_in_background(self, node: nodes.Step) -> None:
        if isinstance(node.parent, nodes.Background) and node.inferred_type != "given":
            self.reporter.add_message("only-given-allowed-in-background", node)


def register_checker(registry: CheckerRegistry) -> None:
    registry.register(ConsistencyChecker)
