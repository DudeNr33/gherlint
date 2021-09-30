"""
Checker focussing of completeness of feature files, e. g. that every scenario must have a name,
every parameter that is used in a scenario outline has to be defined in the examples, etc.
"""

from gherlint.checkers.base_checker import BaseChecker
from gherlint.objectmodel.nodes import Document, Feature


class CompletenessChecker(BaseChecker):
    """Concerned about things like missing examples etc."""

    @staticmethod
    def visit_document(node: Document) -> None:
        print(f"Visiting {node}")

    @staticmethod
    def leave_document(node: Document) -> None:
        print(f"Leaving {node}")

    @staticmethod
    def visit_feature(node: Feature) -> None:
        print(f"Visiting {node}")

    @staticmethod
    def leave_feature(node: Feature) -> None:
        print(f"Leaving {node}")
