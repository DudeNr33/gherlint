import sys
from pathlib import Path

import pytest

from gherlint import registry
from gherlint.registry import CheckerRegistry

TESTDATA = Path(__file__).parent.parent / "testdata"


class TestCheckerRegistry:
    @staticmethod
    @pytest.fixture(autouse=True, scope="class")
    def set_import_paths():
        """Make the registry load the checkers from the test directory instead."""
        sys.path.append(str(TESTDATA))
        registry.PREFIX = "dummy_checkers"
        registry.CHECKER_PATH = TESTDATA / "dummy_checkers" / "checkers"
        yield
        sys.path.pop()

    @staticmethod
    def test_register_checkers():
        checker_registry = CheckerRegistry()
        checker_registry.discover()
        assert len(checker_registry._checkers) == 3  # pylint: disable=protected-access
