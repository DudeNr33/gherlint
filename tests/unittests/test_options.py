from pathlib import Path
from textwrap import dedent

import pytest

from gherlint.checkers.base_checker import BaseChecker
from gherlint.config import Config
from gherlint.options import Options
from gherlint.reporting import TextReporter


class MyOptions(Options):
    config_section = "my_options"

    first_option: str = "abc"
    second_option: bool = True


class CheckerWithOptions(BaseChecker):
    options: MyOptions


class CheckerWithoutOptions(BaseChecker):
    pass


class CheckerWithWrongOptionsType(BaseChecker):
    options: str  # type: ignore


@pytest.fixture
def setup_configfile(tmpdir):
    cfgfile = Path(tmpdir) / "gherlint.toml"
    content = """
    [my_options]
    first_option = "ghi"
    second_option = false
    """

    cfgfile.write_text(dedent(content), encoding="utf8")
    # request config file once to make sure it is loaded from our tmpdir
    Config.get_config(config_file=cfgfile)
    yield
    # Reset internal config instance after test to avoid side effects on other
    # tests during the same session.
    Config._config = None  # pylint: disable=protected-access


def test_options_init_with_matching_args():
    options = MyOptions(first_option="def", second_option=False)
    assert options.config_section == "my_options"
    assert options.first_option == "def"
    assert options.second_option is False


def test_options_with_missing_args():
    options = MyOptions()
    assert options.first_option == "abc"
    assert options.second_option is True


def test_options_with_extra_args():
    options = MyOptions(first_option="def", extra_option="xyz")
    assert options.first_option == "def"
    assert options.second_option is True
    assert not hasattr(options, "extra_option")


def test_options_are_instantiated_on_checker():
    checker = CheckerWithOptions(reporter=TextReporter())
    assert isinstance(checker.options, MyOptions)


def test_checker_without_options():
    checker = CheckerWithoutOptions(reporter=TextReporter())
    assert checker.options is None


@pytest.mark.usefixtures("setup_configfile")
def test_options_from_configfile() -> None:
    checker = CheckerWithOptions(reporter=TextReporter())
    assert checker.options.first_option == "ghi"
    assert checker.options.second_option is False


def test_wrong_options_type_raises_type_error() -> None:
    with pytest.raises(TypeError):
        CheckerWithWrongOptionsType(reporter=TextReporter())
