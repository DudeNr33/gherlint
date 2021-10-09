"""
Checker focussing of completeness of feature files, e. g. that every scenario must have a name,
every parameter that is used in a scenario outline has to be defined in the examples, etc.
"""

from gherlint.checkers.base_checker import BaseChecker
from gherlint.objectmodel.nodes import Feature
from gherlint.reporting import Message


class CompletenessChecker(BaseChecker):
    """Concerned about things like missing examples etc."""

    def visit_feature(self, node: Feature) -> None:
        if not node.name.strip():
            self.reporter.add_message(
                Message("missing-feature-name", "Feature has no name"), node
            )
