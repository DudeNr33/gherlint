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

    def __init__(self, parent: Optional[Node]):
        self.parent = parent

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any], parent: Optional[Node]) -> Node:
        """Create a node instance from the dictionary returned by the gherkin parser."""


class Document(Node):
    """Represents the file itself"""

    def __init__(
        self,
        filename: str,
        feature: Optional[Feature],
        comments: List[str],
        parent=None,
    ):
        super().__init__(parent=parent)
        self.filename = filename
        self.feature = feature
        self.comments = comments
        self.children = [feature]

    @classmethod
    def from_dict(cls, data: Dict[str, Any], parent: Node = None) -> Document:
        feature_data = data.get("feature")
        instance = cls(
            filename=data["filename"],
            feature=None,
            comments=data["comments"],
        )
        if feature_data:
            instance.feature = Feature.from_dict(feature_data, parent=instance)
        return instance


class Feature(Node):
    """Represents a Feature in a file."""

    def __init__(
        self,
        parent: Optional[Node],
        tags: List[str],
        language: str,
        name: str,
        description: str,
        children: List[Scenario],
    ):
        super().__init__(parent=parent)
        self.tags = tags
        self.language = language
        self.name = name
        self.description = description
        self.children = children

    @classmethod
    def from_dict(cls, data: Dict[str, Any], parent: Optional[Node]) -> Feature:
        instance = cls(
            parent=parent,
            tags=data["tags"],
            language=data["language"],
            name=data["name"],
            description=data["description"],
            children=[],
        )
        instance.children = [
            Scenario.from_dict(d["scenario"], parent=instance)
            if d["scenario"]["keyword"] == "Scenario"
            else ScenarioOutline.from_dict(d["scenario"], parent=instance)
            for d in data["children"]
        ]
        return instance


class Scenario(Node):
    """Represents a scenario of a feature."""

    def __init__(
        self,
        parent: Optional[Node],
        tags: List[str],
        name: str,
        description: str,
        examples: List[Examples],
        children: List[Step],
    ):
        super().__init__(parent=parent)
        self.tags = tags
        self.name = name
        self.description = description
        self.examples = examples
        self.children = children

    @classmethod
    def from_dict(cls, data: Dict[str, Any], parent: Optional[Node]) -> Scenario:
        instance = cls(
            parent=parent,
            tags=data["tags"],
            name=data["name"],
            description=data["description"],
            examples=[],
            children=[],
        )
        instance.examples = [
            Examples.from_dict(d, parent=instance) for d in data["examples"]
        ]
        instance.children = [Step.from_dict(s, parent=instance) for s in data["steps"]]
        return instance


class ScenarioOutline(Scenario):
    """Represents a scenario outline of a feature"""


class Step(Node):
    def __init__(self, parent: Optional[Node], keyword: str, text: str):
        super().__init__(parent=parent)
        self.keyword = keyword
        self.text = text

    @classmethod
    def from_dict(cls, data: Dict[str, Any], parent: Optional[Node]) -> Step:
        return cls(parent, data["keyword"], data["text"])


class Examples(Node):
    def __init__(
        self,
        parent: Optional[Node],
        tags: List[str],
        name: str,
        description: str,
        parameters: List[str],
        values: Dict[str, List[str]],
    ):
        super().__init__(parent=parent)
        self.tags = tags
        self.name = name
        self.description = description
        self.parameters = parameters
        self.values = values

    @classmethod
    def from_dict(cls, data: Dict[str, Any], parent: Optional[Node]) -> Examples:
        parameters: List[str] = [cell["value"] for cell in data["tableHeader"]["cells"]]
        values: Dict[str, List[str]] = {param: [] for param in parameters}
        for row in data["tableBody"]:
            for param, entry in zip(parameters, row["cells"]):
                values[param].append(entry["value"])
        return cls(
            parent=parent,
            tags=data["tags"],
            name=data["name"],  # can this be filled?!
            description=data["description"],
            parameters=parameters,
            values=values,
        )
