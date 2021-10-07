from typing import List

import pytest

from gherlint.objectmodel import Document
from gherlint.objectmodel.nodes import (
    Examples,
    Feature,
    Node,
    Scenario,
    ScenarioOutline,
    Step,
)


class TestDocument:
    @staticmethod
    def test_empty_document():
        document = Document.from_dict({"filename": "", "comments": []})
        assert isinstance(document, Document)
        assert document.feature is None
        assert document.comments == []

    @staticmethod
    def test_document_can_have_comments():
        comments = ["This is the first comment", "This is the second comment"]
        document = Document.from_dict({"filename": "", "comments": comments})
        assert document.comments == comments

    @staticmethod
    def test_feature_object_is_created_automatically():
        data = {
            "filename": "",
            "feature": {
                "tags": [],
                "location": {"line": 1, "column": 1},
                "language": "en",
                "keyword": "Feature",
                "name": "Test feature",
                "description": "",
                "children": [],
            },
            "comments": [],
        }
        document = Document.from_dict(data)
        assert isinstance(document.feature, Feature)


class TestFeature:
    @staticmethod
    @pytest.fixture
    def feature_data():
        return {
            "children": [],
            "description": "",
            "keyword": "Feature",
            "language": "en",
            "location": {"column": 1, "line": 1},
            "name": "",
            "tags": [],
        }

    @staticmethod
    def test_empty_feature(feature_data):
        feature = Feature.from_dict(feature_data, parent=None)
        assert isinstance(feature, Feature)
        assert feature.children == []

    @staticmethod
    def test_tagged_feature(feature_data):
        tags = ["tag1", "tag2"]
        feature_data["tags"] = tags
        feature = Feature.from_dict(feature_data, parent=None)
        assert feature.tags == tags

    @staticmethod
    def test_scenarios_are_instantiated(feature_data):
        scenarios = [
            {
                "scenario": {
                    "description": "Scenario 1",
                    "examples": [],
                    "id": "3",
                    "keyword": "Scenario",
                    "location": {"column": 5, "line": 5},
                    "name": "Test scenario",
                    "steps": [],
                    "tags": [],
                }
            },
            {
                "scenario": {
                    "id": "10",
                    "tags": [],
                    "location": {"line": 11, "column": 5},
                    "keyword": "Scenario Outline",
                    "name": "Test scenario outline",
                    "description": "",
                    "steps": [],
                    "examples": [],
                }
            },
        ]
        feature_data["children"] = scenarios
        feature = Feature.from_dict(feature_data, parent=None)
        assert len(feature.children) == 2
        assert isinstance(feature.children[0], Scenario)
        assert isinstance(feature.children[1], ScenarioOutline)


class TestScenario:
    @staticmethod
    @pytest.fixture
    def scenario_data():
        return {
            "description": "Scenario 1",
            "examples": [],
            "id": "3",
            "keyword": "Scenario",
            "location": {"column": 5, "line": 5},
            "name": "Test scenario",
            "steps": [],
            "tags": [],
        }

    @staticmethod
    def test_empty_scenario(scenario_data):
        scenario = Scenario.from_dict(scenario_data, parent=None)
        assert isinstance(scenario, Scenario)
        assert len(scenario.children) == 0

    @staticmethod
    def test_steps_are_instantiated(scenario_data):
        steps = [
            {
                "id": "0",
                "keyword": "Given ",
                "location": {"column": 9, "line": 7},
                "text": "the precondition " "is met",
            },
            {
                "id": "1",
                "keyword": "When ",
                "location": {"column": 9, "line": 8},
                "text": "I do something",
            },
            {
                "id": "2",
                "keyword": "Then ",
                "location": {"column": 9, "line": 9},
                "text": "the expected " "response should " "happen",
            },
        ]
        scenario_data["steps"] = steps
        scenario = Scenario.from_dict(scenario_data, parent=None)
        assert len(scenario.children) == 3
        assert all(isinstance(child, Step) for child in scenario.children)


class TestExamples:
    @staticmethod
    @pytest.fixture
    def examples_data():
        return {
            "description": "",
            "id": "10",
            "keyword": "Examples",
            "location": {"column": 9, "line": 18},
            "name": "",
            "tableBody": [
                {
                    "cells": [
                        {"location": {"column": 15, "line": 20}, "value": "1"},
                        {"location": {"column": 19, "line": 20}, "value": "2"},
                    ],
                    "id": "9",
                    "location": {"column": 13, "line": 20},
                },
                {
                    "cells": [
                        {"location": {"column": 15, "line": 21}, "value": "a"},
                        {"location": {"column": 19, "line": 21}, "value": "b"},
                    ],
                    "id": "9",
                    "location": {"column": 13, "line": 20},
                },
            ],
            "tableHeader": {
                "cells": [
                    {"location": {"column": 15, "line": 19}, "value": "x"},
                    {"location": {"column": 19, "line": 19}, "value": "y"},
                ],
                "id": "8",
                "location": {"column": 13, "line": 19},
            },
            "tags": [],
        }

    @staticmethod
    def test_example_creation(examples_data):
        examples = Examples.from_dict(examples_data, parent=None)
        assert isinstance(examples, Examples)
        assert examples.parameters == ["x", "y"]
        assert examples.values == {"x": ["1", "a"], "y": ["2", "b"]}


class TestMisc:
    @staticmethod
    def test_get_root():
        data = {
            "filename": "foo.feature",
            "feature": {
                "tags": [],
                "location": {"line": 1, "column": 1},
                "language": "en",
                "keyword": "Feature",
                "name": "Test feature",
                "description": "",
                "children": [
                    {
                        "scenario": {
                            "id": "3",
                            "tags": [],
                            "location": {"line": 5, "column": 5},
                            "keyword": "Scenario",
                            "name": "Test scenario",
                            "description": "",
                            "steps": [
                                {
                                    "id": "0",
                                    "location": {"line": 7, "column": 9},
                                    "keyword": "Given ",
                                    "text": "the precondition is met",
                                },
                                {
                                    "id": "1",
                                    "location": {"line": 8, "column": 9},
                                    "keyword": "When ",
                                    "text": "I do something",
                                },
                                {
                                    "id": "2",
                                    "location": {"line": 9, "column": 9},
                                    "keyword": "Then ",
                                    "text": "the expected response should happen",
                                },
                            ],
                            "examples": [],
                        }
                    }
                ],
            },
            "comments": [],
        }

        def get_all_children(node: Node, child_nodes: List[Node]) -> List[Node]:
            if hasattr(node, "children"):
                child_nodes.extend(node.children)  # type: ignore
                for child in node.children:  # type: ignore
                    get_all_children(child, child_nodes)
            return child_nodes

        root_node = Document.from_dict(data)
        child_nodes = [root_node.feature]
        get_all_children(root_node.feature, child_nodes)
        assert all(child.get_root() is root_node for child in child_nodes)
