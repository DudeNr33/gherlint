from contextlib import contextmanager
from pathlib import Path
from typing import Optional

import pytest

from gherlint.config import Config
from gherlint.linter import GherkinLinter

feature_files = list(Path(__file__).parent.rglob("*.feature"))
result_files = [file.parent / (file.stem + ".txt") for file in feature_files]


def idfn(val):
    """Generates names for the parametrized tests."""
    if str(val).endswith(".txt"):
        return val.stem
    return ""


# pylint: disable=protected-access
@contextmanager
def use_config(config: Optional[Path] = None):
    """Populates the cached config instance with the config specified for this test."""
    Config._config = None
    Config.get_config(config)

    try:
        yield
    finally:
        # reset cached config
        Config._config = None


@pytest.mark.parametrize(
    "feature_file, expected_output", list(zip(feature_files, result_files)), ids=idfn
)
def test_expected_outcome(feature_file: Path, expected_output: Path, capsys) -> None:
    if feature_file.with_suffix(".toml").exists():
        config = feature_file.with_suffix(".toml")
    else:
        config = None

    with use_config(config):
        linter = GherkinLinter(feature_file)
        linter.run()

    captured = capsys.readouterr()
    output = _patch_filename(feature_file, captured.out)

    assert output.strip() == expected_output.read_text("utf8").strip()


def _patch_filename(feature_file: Path, capture: str) -> str:
    # replace full file paths with only the filename to be independent from the
    # runtime environment
    full_file_path = str(feature_file.absolute())
    filename_only = feature_file.name
    output = capture.replace(full_file_path, filename_only)
    return output
