from pathlib import Path
from textwrap import dedent

import pytest
from py._path.local import LocalPath

from gherlint.config import Config


@pytest.fixture
def gherlint_toml(tmpdir: LocalPath) -> Path:
    cfgfile = Path(tmpdir) / "gherlint.toml"
    content = """
    [checkers]
    my_checker = true
    """

    cfgfile.write_text(dedent(content), encoding="utf8")
    return cfgfile


@pytest.fixture
def pyproject_toml(tmpdir: LocalPath) -> Path:
    cfgfile = Path(tmpdir) / "pyproject.toml"
    content = """
    [tool.gherlint.checkers]
    my_checker = false
    """

    cfgfile.write_text(dedent(content), encoding="utf8")
    return cfgfile


def test_load_explicit_config_file(gherlint_toml: Path) -> None:
    config = Config(config_file=gherlint_toml)
    assert config["checkers"]["my_checker"] is True


def test_load_implicit_gherlint_toml(gherlint_toml: Path) -> None:
    config = Config(search_path=gherlint_toml.parent)
    assert config["checkers"]["my_checker"] is True


def test_load_implicit_pyproject_toml(pyproject_toml: Path) -> None:
    config = Config(search_path=pyproject_toml.parent)
    assert config["checkers"]["my_checker"] is False


@pytest.mark.usefixtures("gherlint_toml", "pyproject_toml")
def test_gherlint_toml_takes_precedence(tmpdir: LocalPath) -> None:
    config = Config(search_path=Path(tmpdir))
    assert config["checkers"]["my_checker"] is True
