from typing import List

from gherlint.checkers.base_checker import BaseChecker
from gherlint.objectmodel.nodes import Node


class ASTWalker:
    """
    A class which walks through the inidvidual notes of an abstract syntax tree
    representing a Gherkin feature file and calls the callbacks.
    """

    def __init__(self, checkers: List[BaseChecker]) -> None:
        self.checkers = checkers

    def walk(self, node: Node) -> None:
        for checker in self.checkers:
            callback = getattr(
                checker, f"visit_{node.__class__.__name__.lower()}", None
            )
            if callback:
                callback(node)
        children = getattr(node, "children", ())
        for child_node in children:
            self.walk(child_node)
        for checker in self.checkers:
            callback = getattr(
                checker, f"leave_{node.__class__.__name__.lower()}", None
            )
            if callback:
                callback(node)
