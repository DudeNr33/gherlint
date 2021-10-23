from pathlib import Path

import pytest
from gherkin.parser import Parser

from gherlint.objectmodel.nodes import Document

TESTDATA = (Path(__file__).parent.parent / "testdata").absolute()


@pytest.mark.parametrize(
    "file", ["empty_file.feature", "test.feature", "german.feature"]
)
def test_parse_feature(file):
    filepath = str(TESTDATA / file)
    data = Parser().parse(filepath)
    data["filename"] = filepath
    doc = Document.from_dict(data)
    assert isinstance(doc, Document)
