from pathlib import Path

import pytest
from gherkin.parser import Parser

from gherlint.objectmodel import Document

TESTDATA = (Path(__file__).parent.parent / "testdata").absolute()


@pytest.mark.parametrize("file", ["empty_file.feature", "test.feature"])
def test_parse_feature(file):
    filepath = str(TESTDATA / file)
    doc = Document.from_dict(Parser().parse(filepath))
    assert isinstance(doc, Document)
