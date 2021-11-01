"""Checker focussing on consistency issues."""

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
        )
    ]

    def visit_scenario(self, node: nodes.Scenario) -> None:
        for example in node.examples:
            self.reporter.add_message("examples-outside-scenario-outline", node=example)


def register_checker(registry: CheckerRegistry) -> None:
    registry.register(ConsistencyChecker)
