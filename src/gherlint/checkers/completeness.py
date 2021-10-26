"""
Checker focussing of completeness of feature files, e. g. that every scenario must have a name,
every parameter that is used in a scenario outline has to be defined in the examples, etc.
"""

from typing import Union

from gherlint.checkers.base_checker import BaseChecker
from gherlint.exceptions import InternalError
from gherlint.objectmodel import nodes
from gherlint.registry import CheckerRegistry
from gherlint.reporting import Message


class CompletenessChecker(BaseChecker):
    """Concerned about things like missing examples etc."""

    MESSAGES = [
        Message("W001", "missing-feature-name", "Feature has no name"),
        Message("W002", "missing-scenario-name", "Scenario has no name"),
        Message(
            "E001",
            "missing-parameter",
            "At least one of the used parameters is not defined in the Examples section",
        ),
        Message("W003", "file-has-no-feature", "No Feature given in file"),
        Message("W004", "empty-feature", "Feature has no scenarios"),
        Message("W005", "empty-scenario", "Scenario does not contain any steps"),
        Message(
            "C001", "missing-given-step", "Scenario does not contain any Given step"
        ),
        Message("C002", "missing-when-step", "Scenario does not contain any When step"),
        Message("C003", "missing-then-step", "Scenario does not contain any Then step"),
    ]

    def visit_document(self, node: nodes.Document) -> None:
        if not node.feature:
            self.reporter.add_message("file-has-no-feature", node)

    def visit_feature(self, node: nodes.Feature) -> None:
        if not node.name.strip():
            self.reporter.add_message("missing-feature-name", node)
        if not node.children:
            self.reporter.add_message("empty-feature", node)

    def visit_scenario(
        self, node: Union[nodes.Scenario, nodes.ScenarioOutline]
    ) -> None:
        if not node.name.strip():
            self.reporter.add_message("missing-scenario-name", node)
        if not node.children:
            self.reporter.add_message("empty-scenario", node)
        self._check_missing_step_type(node)

    def visit_scenariooutline(self, node: nodes.ScenarioOutline) -> None:
        # all checks relevant to normal scenarios apply for outlines as well
        self.visit_scenario(node)
        self._check_missing_parameter(node)

    def visit_step(self, node: nodes.Step) -> None:
        if isinstance(node.parent, nodes.ScenarioOutline):
            self._check_missing_parameter(node)

    def _check_missing_parameter(
        self, node: Union[nodes.ScenarioOutline, nodes.Step]
    ) -> None:
        if not node.parameters:
            return
        if isinstance(node, nodes.Step):
            if not isinstance(node.parent, nodes.ScenarioOutline):
                raise InternalError(node)
            outline = node.parent
        else:
            outline = node
        found = False
        for examples in outline.examples:
            found = all(param in examples.parameters for param in node.parameters)
        if not found:
            self.reporter.add_message("missing-parameter", node)

    def _check_missing_step_type(
        self, node: Union[nodes.Scenario, nodes.ScenarioOutline]
    ):
        if not node.children:
            # We have an own message for this, don't need to clutter the output with
            # redundant information
            return
        required_step_types = ("given", "when", "then")
        for step_type in required_step_types:
            if not any(step.type == step_type for step in node.children):
                self.reporter.add_message(f"missing-{step_type}-step", node)


def register_checker(registry: CheckerRegistry) -> None:
    registry.register(CompletenessChecker)
