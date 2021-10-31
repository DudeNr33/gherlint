from collections import Counter
from pathlib import Path
from typing import Tuple

from gherkin.parser import Parser

from gherlint import utils
from gherlint.checkers.base_checker import BaseChecker
from gherlint.objectmodel import nodes
from gherlint.reporting import TextReporter
from gherlint.walker import ASTWalker


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

    def print_summary(self) -> None:
        max_element_length: int = max(len(element) for element in self.elements)
        max_count_length: int = int(max(self.counter.values()) / 10)
        for element in self.elements:
            print("-" * (max_element_length + max_count_length + 7))
            print(
                f"| {element:<{max_element_length}} | {self.counter[element]:>{max_count_length}} |"
            )
        print("-" * (max_element_length + max_count_length + 7))


def compute_metrics(path: Path) -> None:
    parser = Parser()
    statistics = Statistics(reporter=TextReporter())
    walker = ASTWalker(checkers=[statistics])
    for file in utils.iter_feature_files(path):
        data = parser.parse(str(file))
        data["filename"] = str(file)
        document = nodes.Document.from_dict(data)
        walker.walk(document)
    statistics.print_summary()
