"""
Checker focussing on complexity issues.
These may be constructs that may be simplified, or are too long or complex which makes it harder to understand.
"""

from gherlint.checkers.base_checker import BaseChecker
from gherlint.objectmodel import nodes
from gherlint.registry import CheckerRegistry
from gherlint.reporting import Message


class ComplexityChecker(BaseChecker):
    MESSAGES = [
        Message(
            "R201",
            "outline-could-be-a-scenario",
            "This outline contains no or only one example, consider using a normal scenario instead",
        )
    ]

    def visit_scenariooutline(self, node: nodes.ScenarioOutline) -> None:
        total_example_values = sum(
            example_set.number_of_entries for example_set in node.examples
        )
        if total_example_values < 2:
            self.reporter.add_message("outline-could-be-a-scenario", node)


def register_checker(registry: CheckerRegistry) -> None:
    registry.register(ComplexityChecker)
