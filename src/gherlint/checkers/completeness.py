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
    ]

    def visit_document(self, node: nodes.Document) -> None:
        if not node.feature:
            self.reporter.add_message("file-has-no-feature", node)

    def visit_feature(self, node: nodes.Feature) -> None:
        if not node.name.strip():
            self.reporter.add_message("missing-feature-name", node)
        if not node.children:
            self.reporter.add_message("empty-feature", node)

    def visit_scenario(self, node: nodes.Scenario) -> None:
        self._check_missing_scenario_name(node)

    def visit_scenariooutline(self, node: nodes.ScenarioOutline) -> None:
        self._check_missing_scenario_name(node)
        self._check_missing_parameter(node)

    def visit_step(self, node: nodes.Step) -> None:
        self._check_missing_parameter(node)

    def _check_missing_scenario_name(
        self, node: Union[nodes.Scenario, nodes.ScenarioOutline]
    ) -> None:
        if not node.name.strip():
            self.reporter.add_message("missing-scenario-name", node)

    def _check_missing_parameter(
        self, node: Union[nodes.ScenarioOutline, nodes.Step]
    ) -> None:
        if not node.parameters:
            return
        if isinstance(node, nodes.Step):
            if not isinstance(node.parent, nodes.ScenarioOutline):
                raise InternalError()
            outline = node.parent
        else:
            outline = node
        found = False
        for examples in outline.examples:
            found = all(param in examples.parameters for param in node.parameters)
        if not found:
            self.reporter.add_message("missing-parameter", node)


def register_checker(registry: CheckerRegistry) -> None:
    registry.register(CompletenessChecker)
