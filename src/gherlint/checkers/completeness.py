"""
Checker focussing of completeness of feature files, e. g. that every scenario must have a name,
every parameter that is used in a scenario outline has to be defined in the examples, etc.
"""

from typing import Set, Union

from gherlint.checkers.base_checker import BaseChecker
from gherlint.exceptions import InternalError
from gherlint.objectmodel import nodes
from gherlint.registry import CheckerRegistry
from gherlint.reporting import Message, Reporter


class CompletenessChecker(BaseChecker):
    """Concerned about things like missing examples etc."""

    MESSAGES = [
        Message("W101", "missing-feature-name", "Feature has no name"),
        Message("W102", "missing-scenario-name", "Scenario has no name"),
        Message(
            "E101",
            "missing-parameter",
            "'{parameter}' is not defined in the Examples section",
        ),
        Message("W103", "file-has-no-feature", "No Feature given in file"),
        Message("W104", "empty-feature", "Feature has no scenarios"),
        Message("W105", "empty-scenario", "Scenario does not contain any steps"),
        Message("W106", "empty-background", "Background does not contain any steps"),
        Message(
            "C101", "missing-given-step", "Scenario does not contain any Given step"
        ),
        Message("C102", "missing-when-step", "Scenario does not contain any When step"),
        Message("C103", "missing-then-step", "Scenario does not contain any Then step"),
        Message("R101", "unused-parameter", "Parameter '{parameter}' is not used"),
    ]

    def __init__(self, reporter: Reporter) -> None:
        super().__init__(reporter)
        self.used_parameters: Set[str] = set()

    def visit_document(self, node: nodes.Document) -> None:
        if not node.feature:
            self.reporter.add_message("file-has-no-feature", node)

    def visit_feature(self, node: nodes.Feature) -> None:
        if not node.name.strip():
            self.reporter.add_message("missing-feature-name", node)
        if not node.children:
            self.reporter.add_message("empty-feature", node)

    def visit_background(self, node: nodes.Background) -> None:
        if not node.steps:
            self.reporter.add_message("empty-background", node)

    def visit_scenario(
        self, node: Union[nodes.Scenario, nodes.ScenarioOutline]
    ) -> None:
        if not node.name.strip():
            self.reporter.add_message("missing-scenario-name", node)
        if node.steps:
            self._check_missing_step_type(node)
        else:
            self.reporter.add_message("empty-scenario", node)

    def visit_scenariooutline(self, node: nodes.ScenarioOutline) -> None:
        # all checks relevant to normal scenarios apply for outlines as well
        self.visit_scenario(node)
        for param in node.parameters:
            self.used_parameters.add(param)
        self._check_missing_parameter(node)

    def leave_scenariooutline(self, _: nodes.ScenarioOutline) -> None:
        self.used_parameters.clear()

    def visit_examples(self, node: nodes.Examples) -> None:
        if isinstance(node.parent, nodes.ScenarioOutline):
            # Don't run this check if we are inside a normal scenario.
            # If examples are used we have a separate check for this (examples-outside-scenario-outline).
            self._check_unused_parameter(node)

    def visit_step(self, node: nodes.Step) -> None:
        if isinstance(node.parent, nodes.ScenarioOutline):
            for param in node.parameters:
                self.used_parameters.add(param)
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
        for param in node.parameters:
            if not any(param in examples.parameters for examples in outline.examples):
                self.reporter.add_message("missing-parameter", node, parameter=param)

    def _check_missing_step_type(
        self, node: Union[nodes.Scenario, nodes.ScenarioOutline]
    ):
        if not node.children:
            # We have an own message for this, don't need to clutter the output with
            # redundant information
            return
        required_step_types = ("given", "when", "then")
        for step_type in required_step_types:
            if not any(step.type == step_type for step in node.steps):
                self.reporter.add_message(f"missing-{step_type}-step", node)

    def _check_unused_parameter(self, node: nodes.Examples) -> None:
        for param in node.parameters:
            if param not in self.used_parameters:
                self.reporter.add_message("unused-parameter", node, parameter=param)


def register_checker(registry: CheckerRegistry) -> None:
    registry.register(CompletenessChecker)
