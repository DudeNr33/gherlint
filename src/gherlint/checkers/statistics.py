"""Not a real checker in the sense that it might complain about stuff.
It will generate a statistic of the number of features, scenarios etc. instead."""

from collections import Counter
from typing import Tuple

from gherlint.checkers.base_checker import BaseChecker
from gherlint.objectmodel import nodes


class Statistics(BaseChecker):
    counter: Counter = Counter()
    elements: Tuple[str, ...] = ("Features", "Scenario Outlines", "Scenarios", "Steps")

    def visit_feature(self, _: nodes.Feature) -> None:
        self.counter.update(["Features"])

    def visit_scenario(self, _: nodes.Scenario) -> None:
        self.counter.update(["Scenarios"])

    def visit_scenariooutline(self, _: nodes.ScenarioOutline) -> None:
        self.counter.update(["Scenario Outlines"])

    def visit_step(self, _: nodes.Step) -> None:
        self.counter.update(["Steps"])

    def print_summary(self):
        max_element_length: int = max(len(element) for element in self.elements)
        max_count_length: int = int(max(self.counter.values()) / 10)
        for element in self.elements:
            print("-" * (max_element_length + max_count_length + 7))
            print(
                f"| {element:<{max_element_length}} | {self.counter[element]:>{max_count_length}} |"
            )
        print("-" * (max_element_length + max_count_length + 7))
