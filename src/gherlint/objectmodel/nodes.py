"""
Nodes representing different elements of a Gherkin feature file.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Union

import parse

from gherlint import utils
from gherlint.exceptions import InternalError


class Node(ABC):
    """
    Base class for all concrete node types.
    """

    def __init__(self, parent: Optional[Node], line: int, column: int):
        self.parent = parent
        self.line = line
        self.column = column
        root = self.get_root()
        if isinstance(root, Document) and root is not self:
            # shift the line number if the ``Document`` root node has an offset
            self.line -= root.offset

    def __repr__(self):
        return f"{self.__class__.__name__}(line={self.line}, column={self.column})"

    @property
    def parents(self) -> List[Node]:
        if self.parent:
            return [self.parent] + self.parent.parents
        return []

    def get_root(self) -> Node:
        """Get the root node, i.e. the topmost parent in the hierarchy."""
        current = self
        while current.parent is not None:
            current = current.parent
        return current

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any], parent: Optional[Node]) -> Node:
        """Create a node instance from the dictionary returned by the gherkin parser."""


class Document(Node):
    """Represents the file itself"""

    def __init__(
        self,
        line: int,
        column: int,
        filename: str,
        feature: Optional[Feature],
        comments: List[str],
        parent=None,
        offset: int = 0,
    ):
        super().__init__(parent, line, column)
        self.filename = filename
        self.feature = feature
        self.comments = comments
        # if we added a language tag we must shift all messages to refer to the correct line numbers
        self.offset = offset

    @property
    def children(self):
        return [self.feature]

    @classmethod
    def from_dict(cls, data: Dict[str, Any], parent: Node = None) -> Document:
        feature_data = data.get("feature")
        instance = cls(
            line=0,
            column=0,
            filename=data["filename"],
            feature=None,
            comments=data["comments"],
            offset=data.get("offset", 0),
        )
        if feature_data:
            instance.feature = Feature.from_dict(feature_data, parent=instance)
        return instance


class Feature(Node):
    """Represents a Feature in a file."""

    def __init__(
        self,
        line: int,
        column: int,
        parent: Optional[Node],
        tags: List[Tag],
        language: str,
        name: str,
        description: str,
        scenarios: List[Union[Scenario, ScenarioOutline]],
        background: Background = None,
    ):
        super().__init__(parent, line, column)
        self.tags = tags
        self.language = language
        self.name = name
        self.description = description
        self.background = background
        self.scenarios = scenarios

    @property
    def children(self) -> List[Union[Tag, Background, Scenario, ScenarioOutline]]:
        children: List[Union[Tag, Background, Scenario, ScenarioOutline]] = []
        children.extend(self.tags)
        if self.background:
            children.append(self.background)
        children.extend(self.scenarios)
        return children

    @classmethod
    def from_dict(cls, data: Dict[str, Any], parent: Optional[Node]) -> Feature:
        instance = cls(
            line=data["location"]["line"],
            column=data["location"]["column"],
            parent=parent,
            tags=[],
            language=data["language"],
            name=data["name"],
            description=data["description"],
            scenarios=[],
        )
        instance.tags = [Tag.from_dict(tag, parent=instance) for tag in data["tags"]]
        for child in data["children"]:
            for keyword, child_data in child.items():
                if _is_background(keyword, child_data):
                    instance.background = Background.from_dict(
                        child_data, parent=instance
                    )
                elif _is_scenario(keyword, child_data):
                    instance.scenarios.append(
                        Scenario.from_dict(child_data, parent=instance)
                    )
                elif _is_outline(keyword, child_data):
                    instance.scenarios.append(
                        ScenarioOutline.from_dict(child_data, parent=instance)
                    )
        return instance


def _is_scenario(keyword: str, data: Dict[str, Any]) -> bool:
    return keyword == "scenario" and data["keyword"] in utils.get_keyword_candidates(
        "scenario"
    )


def _is_outline(keyword: str, data: Dict[str, Any]) -> bool:
    return keyword == "scenario" and data["keyword"] in utils.get_keyword_candidates(
        "scenarioOutline"
    )


def _is_background(keyword: str, _: Dict[str, Any]) -> bool:
    return keyword == "background"


class Background(Node):
    """Represents a background of a feature."""

    def __init__(
        self,
        line: int,
        column: int,
        parent: Optional[Node],
        name: str,
        description: str,
        steps: List[Step],
    ):
        super().__init__(parent, line, column)
        self.name = name
        self.description = description
        self.steps = steps

    @property
    def children(self):
        return self.steps

    @classmethod
    def from_dict(cls, data: Dict[str, Any], parent: Optional[Node]) -> Background:
        instance = cls(
            line=data["location"]["line"],
            column=data["location"]["column"],
            parent=parent,
            name=data["name"],
            description=data["description"],
            steps=[],
        )
        instance.steps = [Step.from_dict(s, parent=instance) for s in data["steps"]]
        return instance


class Scenario(Node):
    """Represents a scenario of a feature."""

    def __init__(
        self,
        line: int,
        column: int,
        parent: Optional[Node],
        tags: List[Tag],
        name: str,
        description: str,
        examples: List[Examples],
        steps: List[Step],
    ):
        super().__init__(parent, line, column)
        self.tags = tags
        self.name = name
        self.description = description
        self.examples = examples
        self.steps = steps
        self.parameters = extract_parameters(name)

    @property
    def children(self):
        return self.tags + self.steps + self.examples

    @classmethod
    def from_dict(cls, data: Dict[str, Any], parent: Optional[Node]) -> Scenario:
        instance = cls(
            line=data["location"]["line"],
            column=data["location"]["column"],
            parent=parent,
            tags=[],
            name=data["name"],
            description=data["description"],
            examples=[],
            steps=[],
        )
        instance.tags = [Tag.from_dict(tag, instance) for tag in data["tags"]]
        instance.examples = [
            Examples.from_dict(d, parent=instance) for d in data["examples"]
        ]
        instance.steps = [Step.from_dict(s, parent=instance) for s in data["steps"]]
        return instance


class ScenarioOutline(Scenario):
    """Represents a scenario outline of a feature"""


class Step(Node):
    def __init__(
        self, parent: Optional[Node], line: int, column: int, keyword: str, text: str
    ):
        super().__init__(parent, line, column)
        self.type = self._get_english_keyword(keyword)
        self.text = text
        self.parameters = extract_parameters(text)

    @property
    def inferred_type(self) -> str:
        if not self.type in ("and", "but"):
            return self.type
        if not isinstance(self.parent, (Background, Scenario, ScenarioOutline)):
            raise InternalError(
                node=self, message="Unexpected type for parent of 'Step'"
            )
        current_step_index = self.parent.steps.index(self)
        while current_step_index > 0:
            current_step_index -= 1
            previous_step = self.parent.steps[current_step_index]
            if previous_step.type not in ("and", "but"):
                return previous_step.type
        return "unknown"

    @staticmethod
    def _get_english_keyword(keyword: str) -> str:
        """Get the corresponding english step keyword in lowercase from input in any (supported) language."""
        if keyword.strip() == "*":
            return "*"
        english_keywords = ("given", "when", "then", "and", "but")
        for english_keyword in english_keywords:
            if keyword.lower() in [
                kw.lower() for kw in utils.get_keyword_candidates(english_keyword)
            ]:
                return english_keyword
        raise ValueError(f"Unable to look up english step keyword for {keyword}")

    @classmethod
    def from_dict(cls, data: Dict[str, Any], parent: Optional[Node]) -> Step:
        return cls(
            line=data["location"]["line"],
            column=data["location"]["column"],
            parent=parent,
            keyword=data["keyword"],
            text=data["text"],
        )


class Examples(Node):
    def __init__(
        self,
        parent: Optional[Node],
        line: int,
        column: int,
        tags: List[Tag],
        name: str,
        description: str,
        parameters: List[str],
        values: Dict[str, List[str]],
    ):
        super().__init__(parent, line, column)
        self.tags = tags
        self.name = name
        self.description = description
        self.parameters = parameters
        self.values = values
        self.number_of_entries = len(values[parameters[0]])

    @property
    def children(self) -> List[Tag]:
        return self.tags

    @classmethod
    def from_dict(cls, data: Dict[str, Any], parent: Optional[Node]) -> Examples:
        parameters: List[str] = [cell["value"] for cell in data["tableHeader"]["cells"]]
        values: Dict[str, List[str]] = {param: [] for param in parameters}
        for row in data["tableBody"]:
            for param, entry in zip(parameters, row["cells"]):
                values[param].append(entry["value"])
        instance = cls(
            line=data["location"]["line"],
            column=data["location"]["column"],
            parent=parent,
            tags=[],
            name=data["name"],  # can this be filled?!
            description=data["description"],
            parameters=parameters,
            values=values,
        )
        instance.tags = [Tag.from_dict(tag, parent=instance) for tag in data["tags"]]
        return instance


class Tag(Node):
    def __init__(self, parent: Optional[Node], line: int, column: int, name: str):
        super().__init__(parent, line, column)
        self.name = name

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Tag) and self.name == other.name

    @classmethod
    def from_dict(cls, data: Dict[str, Any], parent: Optional[Node]) -> Tag:
        return cls(
            parent=parent,
            line=data["location"]["line"],
            column=data["location"]["column"],
            name=data["name"],
        )


def extract_parameters(text: str) -> Tuple[str]:
    """Extract parameters from a string (e. g. a step text).
    'Parameters' are placeholders defined in the Examples section of a
    Scenario Outline and are delimited with ``< >``."""
    pattern = "<{}>"
    return tuple(match.fixed[0] for match in parse.findall(pattern, text))  # type: ignore
