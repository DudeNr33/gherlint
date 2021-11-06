"""Unit tests for ConsistencyChecker"""
from unittest.mock import Mock

import pytest

from gherlint.checkers.consistency import ConsistencyChecker
from gherlint.objectmodel import nodes


class TestConsistencyChecker:
    checker: ConsistencyChecker
    reporter_mock: Mock

    @pytest.fixture(autouse=True)
    def setup_checker(self) -> None:
        self.reporter_mock = Mock()
        self.checker = ConsistencyChecker(self.reporter_mock)

    def test_duplicated_feature_name(self) -> None:
        """This check is not easy to do as a normal functional test, as these are designed to only run tests against
        a single file. But this test needs two."""
        unique_feature = nodes.Feature(
            parent=None,
            line=1,
            column=1,
            language="en",
            name="first",
            description="",
            tags=[],
            scenarios=[],
        )
        duplicated_feature_1 = nodes.Feature(
            parent=None,
            line=1,
            column=1,
            language="en",
            name="second",
            description="",
            tags=[],
            scenarios=[],
        )
        duplicated_feature_2 = nodes.Feature(
            parent=None,
            line=1,
            column=1,
            language="en",
            name="second",
            description="",
            tags=[],
            scenarios=[],
        )
        self.checker.visit_feature(unique_feature)
        self.checker.visit_feature(duplicated_feature_1)
        self.checker.visit_feature(duplicated_feature_2)
        self.reporter_mock.add_message.assert_called_once_with(
            "duplicated-feature-name", duplicated_feature_2
        )
