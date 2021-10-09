from pathlib import Path

import pytest

from gherlint.linter import GherkinLinter

feature_files = list(Path(__file__).parent.rglob("*.feature"))
result_files = [file.parent / (file.stem + ".txt") for file in feature_files]


@pytest.mark.parametrize(
    "feature_file, expected_output", list(zip(feature_files, result_files))
)
def test_expected_outcome(feature_file: Path, expected_output: Path, capsys) -> None:
    linter = GherkinLinter(str(feature_file))
    linter.run()
    captured = capsys.readouterr()
    # replace full file paths with only the filename to be independent from the
    # runtime environment
    full_file_path = str(feature_file.absolute())
    filename_only = feature_file.name
    output = captured.out.replace(full_file_path, filename_only)
    assert output.strip() == expected_output.read_text("utf8").strip()
