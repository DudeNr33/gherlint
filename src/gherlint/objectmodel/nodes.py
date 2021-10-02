"""
Nodes representing different elements of a Gherkin feature file.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class Node(ABC):
    """
    Base class for all concrete node types.
    """

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> Node:
        """Create a node instance from the dictionary returned by the gherkin parser."""


class Document(Node):
    """Represents the file itself"""

    def __init__(self, feature: Optional[Feature], comments: List[str]):
        self.name = ""
        self.feature = feature
        self.comments = comments
        self.children = [feature]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Document:
        feature_data = data.get("feature")
        return cls(
            feature=Feature.from_dict(feature_data) if feature_data else None,
            comments=data["comments"],
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
            children=[
                Scenario.from_dict(d["scenario"])
                if d["scenario"]["keyword"] == "Scenario"
                else ScenarioOutline.from_dict(d["scenario"])
                for d in data["children"]
            ],
        )


class Scenario(Node):
    """Represents a scenario of a feature."""

    def __init__(
        self,
        tags: List[str],
        name: str,
        description: str,
        examples: List[Examples],
        children: List[Step],
    ):
        self.tags = tags
        self.name = name
        self.description = description
        self.examples = examples
        self.children = children

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Scenario:
        return cls(
            tags=data["tags"],
            name=data["name"],
            description=data["description"],
            examples=[Examples.from_dict(d) for d in data["examples"]],
            children=[Step.from_dict(s) for s in data["steps"]],
        )


class ScenarioOutline(Scenario):
    """Represents a scenario outline of a feature"""


class Step(Node):
    def __init__(self, keyword: str, text: str):
        self.keyword = keyword
        self.text = text

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Step:
        return cls(data["keyword"], data["text"])


class Examples(Node):
    def __init__(
        self,
        tags: List[str],
        name: str,
        description: str,
        parameters: List[str],
        values: Dict[str, List[str]],
    ):
        self.tags = tags
        self.name = name
        self.description = description
        self.parameters = parameters
        self.values = values

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Examples:
        parameters: List[str] = [cell["value"] for cell in data["tableHeader"]["cells"]]
        values: Dict[str, List[str]] = {param: [] for param in parameters}
        for row in data["tableBody"]:
            for param, entry in zip(parameters, row["cells"]):
                values[param].append(entry["value"])
        return cls(
            tags=data["tags"],
            name=data["name"],  # can this be filled?!
            description=data["description"],
            parameters=parameters,
            values=values,
        )
