"""
Nodes representing different elements of a Gherkin feature file.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class Node(ABC):
    """
    Base class for all concrete node types.
    """

    @abstractmethod
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Node:
        """Create a node instance from the dictionary returned by the gherkin parser."""


class Document(Node):
    """Represents the file itself"""

    def __init__(self, feature: Feature, comments: List[str]):
        self.name = ""
        self.feature = feature
        self.comments = comments
        self.children = [feature]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Document:
        return cls(
            feature=Feature.from_dict(data["feature"]), comments=data["comments"]
        )


class Feature(Node):
    """Represents a Feature in a file."""

    def __init__(
        self,
        tags: List[str],
        language: str,
        name: str,
        description: str,
        children: List[Scenario],
    ):
        self.tags = tags
        self.language = language
        self.name = name
        self.description = description
        self.children = children

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Feature:
        return cls(
            tags=data["tags"],
            language=data["language"],
            name=data["name"],
            description=data["description"],
            children=[Scenario.from_dict(d) for d in data["children"]],
        )


class Scenario(Node):
    """Represents a scenario of a feature."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Scenario:
        return cls()
