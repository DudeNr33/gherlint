from typing import List

import pytest

from gherlint.objectmodel.nodes import (
    Background,
    Document,
    Examples,
    Feature,
    Node,
    Scenario,
    ScenarioOutline,
    Step,
    Tag,
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
        tags = [
            {
                "id": "3",
                "location": {"line": 5, "column": 5},
                "name": "@tag1",
            },
            {
                "id": "3",
                "location": {"line": 6, "column": 5},
                "name": "@tag2",
            },
        ]
        feature_data["tags"] = tags
        feature = Feature.from_dict(feature_data, parent=None)
        assert feature.tags[0].name == "@tag1"
        assert feature.tags[1].name == "@tag2"

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


class TestBackground:
    @staticmethod
    @pytest.fixture
    def background_data():
        return {
            "id": "1",
            "location": {"line": 5, "column": 5},
            "keyword": "Background",
            "name": "Test Background",
            "description": "",
            "steps": [],
        }

    @staticmethod
    def test_empty_background(background_data):
        background = Background.from_dict(background_data, parent=None)
        assert isinstance(background, Background)
        assert len(background.steps) == 0

    @staticmethod
    def test_steps_are_instantiated(background_data):
        steps = [
            {
                "id": "0",
                "location": {"line": 7, "column": 9},
                "keyword": "Given ",
                "text": "a precondition relevant for all tests",
            }
        ]
        background_data["steps"] = steps
        background = Background.from_dict(background_data, parent=None)
        assert len(background.steps) == 1
        assert all(isinstance(child, Step) for child in background.steps)


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

    @staticmethod
    def test_parameter_extraction(scenario_data):
        scenario_data["name"] = "Scenario with <one> parameter"
        scenario = Scenario.from_dict(scenario_data, parent=None)
        assert scenario.parameters == ("one",)


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


class TestStep:
    @staticmethod
    @pytest.fixture
    def example_step():
        return {
            "id": "0",
            "keyword": "Given ",
            "location": {"column": 9, "line": 7},
            "text": "the precondition is met",
        }

    @staticmethod
    def test_simple_given_step(example_step):
        step = Step.from_dict(example_step, parent=None)
        assert isinstance(step, Step)

    @staticmethod
    @pytest.mark.parametrize(
        "used_keyword, expected_type",
        [
            ("Given ", "given"),
            ("given ", "given"),  # test once that lookup works case insensitive
            ("Angenommen ", "given"),
            ("angenommen ", "given"),
            ("When ", "when"),
            ("Wenn ", "when"),
            ("Then ", "then"),
            ("Dann ", "then"),
            ("But ", "but"),
            ("Aber ", "but"),
            ("And ", "and"),
            ("Und ", "and"),
        ],
    )
    def test_keyword_is_recognized_independent_of_language(
        example_step, used_keyword, expected_type
    ):
        example_step["keyword"] = used_keyword
        step = Step.from_dict(example_step, parent=None)
        assert step.type == expected_type

    @staticmethod
    @pytest.mark.parametrize(
        "step_text, parameters",
        [
            ("a single <parameter> occurs", ["parameter"]),
            ("a <first> parameter followed by a <second>", ["first", "second"]),
            ("two <consecutive> <parameters> occur", ["consecutive", "parameters"]),
        ],
    )
    def test_step_with_example_usage(example_step, step_text, parameters):
        parametrized_step = example_step
        parametrized_step["text"] = step_text
        step = Step.from_dict(parametrized_step, parent=None)
        assert all(param in step.parameters for param in parameters)
        assert len(parameters) == len(step.parameters)

    @staticmethod
    @pytest.mark.parametrize("keyword", ["Given ", "When ", "Then "])
    def test_inferred_type(keyword):
        scenario = Scenario(0, 0, None, [], "test", "", [], [])
        steps = [
            Step(scenario, 0, 0, keyword, "first"),
            Step(scenario, 0, 0, "And ", "first"),
            Step(scenario, 0, 0, "But ", "first"),
            Step(scenario, 0, 0, "And ", "first"),
        ]
        scenario.steps = steps
        assert all(step.inferred_type == keyword.lower().strip() for step in steps)

    @staticmethod
    def test_infer_with_given_when_then_structure():
        scenario = Scenario(0, 0, None, [], "test", "", [], [])
        steps = [
            Step(scenario, 0, 0, "Given ", ""),
            Step(scenario, 0, 0, "And ", ""),
            Step(scenario, 0, 0, "When ", ""),
            Step(scenario, 0, 0, "But ", ""),
            Step(scenario, 0, 0, "Then ", ""),
            Step(scenario, 0, 0, "And ", ""),
        ]
        scenario.steps = steps
        assert steps[1].inferred_type == "given"
        assert steps[3].inferred_type == "when"
        assert steps[5].inferred_type == "then"

    @staticmethod
    def test_inferred_type_returns_unknown_if_uninferable():
        scenario = Scenario(0, 0, None, [], "test", "", [], [])
        steps = [
            Step(scenario, 0, 0, "And ", "first"),
            Step(scenario, 0, 0, "And ", "first"),
            Step(scenario, 0, 0, "And ", "first"),
            Step(scenario, 0, 0, "But ", "first"),
        ]
        scenario.steps = steps
        assert all(step.inferred_type == "unknown" for step in steps)


class TestMisc:
    @staticmethod
    @pytest.fixture
    def example_data():
        return {
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

    @staticmethod
    def test_get_root(example_data):
        def get_all_children(node: Node, child_nodes: List[Node]) -> List[Node]:
            if hasattr(node, "children"):
                child_nodes.extend(node.children)  # type: ignore
                for child in node.children:  # type: ignore
                    get_all_children(child, child_nodes)
            return child_nodes

        root_node = Document.from_dict(example_data)
        child_nodes = [root_node.feature]
        get_all_children(root_node.feature, child_nodes)
        assert all(child.get_root() is root_node for child in child_nodes)

    @staticmethod
    def test_get_parents(example_data):
        def check_parents(node: Node, parents: List[Node]) -> None:
            assert node.parents == parents
            if hasattr(node, "children"):
                parents = parents[:]
                parents[0:0] = [node]
                for child in node.children:  # type: ignore
                    check_parents(child, parents)

        current_node = Document.from_dict(example_data)
        check_parents(current_node, parents=[])


class TestTags:
    @staticmethod
    @pytest.fixture
    def example_data():
        return {
            "id": "3",
            "location": {"line": 5, "column": 5},
            "name": "@alreadyonfeature",
        }

    @staticmethod
    def test_create_tag(example_data):
        tag = Tag.from_dict(example_data, parent=None)
        assert isinstance(tag, Tag)
