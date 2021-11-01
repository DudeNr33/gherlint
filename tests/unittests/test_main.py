"""
Scope of these tests:
Check if the command line commands and options are parsed correctly and the right classes/methods are
called with the expected set of parameters.

Out of scope:
End-to-end tests which actually execute any code outside ``__main__.py``
"""
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from gherlint.__main__ import cli


class TestGlobalOptions:
    @staticmethod
    @pytest.mark.parametrize("option", ["-h", "--help"])
    def test_global_help(option: str) -> None:
        output = CliRunner().invoke(cli, [option]).output
        # the normal CLI returns "Usage: gherlint [OPTIONS] ...", but the CliRunner uses the name of the function.
        assert (
            output.strip()
            == """
Usage: cli [OPTIONS] COMMAND [ARGS]...

  gherlint is a linter for Cucumber Gherkin feature files.

Options:
  -h, --help  Show this message and exit.

Commands:
  lint   Perform linting of feature files
  stats  Compute metrics over your feature files
        """.strip()
        )


class TestLintCommand:
    linter_class_mock: MagicMock
    linter_mock: MagicMock

    @pytest.fixture(autouse=True)
    def setup_gherkin_linter_mock(self):
        self.linter_mock = MagicMock()  # reset the mock before each test
        with patch("gherlint.__main__.GherkinLinter") as self.linter_class_mock:
            self.linter_class_mock.return_value = self.linter_mock
            yield

    def test_lint_without_options(self):
        CliRunner().invoke(cli, ["lint", "/my/path"])
        self.linter_class_mock.assert_called_once_with(Path("/my/path"))
        self.linter_mock.run.assert_called_once()


class TestStatsCommand:
    compute_metrics_mock: MagicMock

    @pytest.fixture(autouse=True)
    def setup_mock(self):
        with patch("gherlint.__main__.compute_metrics") as self.compute_metrics_mock:
            yield

    def test_stats_without_options(self):
        CliRunner().invoke(cli, ["stats", "/my/path"])
        self.compute_metrics_mock.assert_called_once_with(Path("/my/path"))


class TestFixLanguageTagsCommand:
    language_fixer_class_mock: MagicMock
    language_fixer_mock: MagicMock

    @pytest.fixture(autouse=True)
    def setup_mock(self):
        self.language_fixer_mock = MagicMock()
        with patch("gherlint.__main__.LanguageFixer") as self.language_fixer_class_mock:
            self.language_fixer_class_mock.return_value = self.language_fixer_mock
            yield

    def test_fix_without_options(self):
        CliRunner().invoke(cli, ["fix-language-tags", "/my/path"])
        self.language_fixer_class_mock.assert_called_once_with(Path("/my/path"))
        self.language_fixer_mock.run.assert_called_once_with(modify=True)

    def test_dry_run(self):
        CliRunner().invoke(cli, ["fix-language-tags", "--dry-run", "/my/path"])
        self.language_fixer_mock.run.assert_called_once_with(modify=False)
