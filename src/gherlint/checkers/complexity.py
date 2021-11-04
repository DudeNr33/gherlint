"""
Checker focussing on complexity issues.
These may be constructs that may be simplified, or are too long or complex which makes it harder to understand.
"""

from typing import Optional, Set, Union

from gherlint.checkers.base_checker import BaseChecker
from gherlint.objectmodel import nodes
from gherlint.registry import CheckerRegistry
from gherlint.reporting import Message, Reporter


class ComplexityChecker(BaseChecker):
    MESSAGES = [
        Message(
            "R201",
            "outline-could-be-a-scenario",
            "This outline contains no or only one example, consider using a normal scenario instead",
        ),
        Message(
            "R202",
            "consider-using-background",
            "Consider putting common 'Given' steps in a Background",
        ),
    ]

    def __init__(self, reporter: Reporter) -> None:
        super().__init__(reporter)
        self.common_given_steps: Optional[Set[str]] = None

    def visit_feature(self, _: nodes.Feature) -> None:
        self.common_given_steps = None

    def visit_scenario(
        self, node: Union[nodes.Scenario, nodes.ScenarioOutline]
    ) -> None:
        given_steps = set(
            step.text for step in node.steps if step.inferred_type == "given"
        )
        if self.common_given_steps is None:
            self.common_given_steps = given_steps
        else:
            self.common_given_steps &= given_steps

    def visit_scenariooutline(self, node: nodes.ScenarioOutline) -> None:
        self.visit_scenario(node)
        total_example_values = sum(
            example_set.number_of_entries for example_set in node.examples
        )
        if total_example_values < 2:
            self.reporter.add_message("outline-could-be-a-scenario", node)

    def leave_feature(self, node: nodes.Feature) -> None:
        if len(node.scenarios) > 1 and self.common_given_steps:
            for scenario in (child_node for child_node in node.scenarios):
                for step in scenario.steps:
                    if (
                        step.inferred_type == "given"
                        and step.text in self.common_given_steps
                    ):
                        self.reporter.add_message("consider-using-background", step)


def register_checker(registry: CheckerRegistry) -> None:
    registry.register(ComplexityChecker)
