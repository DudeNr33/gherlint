from pathlib import Path

import pytest

from gherlint.fixer import LanguageFixer


class TestLanguageFixer:
    GOOD_FILE = "good_file.feature"
    MISSING_TAG = "missing_tag.feature"
    WRONG_TAG = "wrong_tag.feature"

    @pytest.fixture()
    def testfiles(self, tmpdir):
        """Set up some files to test with in a temporary directory"""
        (tmpdir / self.GOOD_FILE).write_text(
            """# language: de
Funktionalität: Test
        """,
            encoding="utf8",
        )
        (tmpdir / self.MISSING_TAG).write_text(
            """Funktionalität: Test
        """,
            encoding="utf8",
        )
        (tmpdir / self.WRONG_TAG).write_text(
            """# language: es
Funktionalität: Test
        """,
            encoding="utf8",
        )
        yield tmpdir

    def test_nothing_to_fix(self, testfiles):
        target = Path(testfiles / self.GOOD_FILE)
        original_content = target.read_bytes()
        LanguageFixer(target).run(modify=True)
        assert target.read_bytes() == original_content

    def test_missing_language_tag(self, testfiles):
        target = Path(testfiles / self.MISSING_TAG)
        LanguageFixer(target).run(modify=True)
        assert target.read_bytes() == Path(testfiles / self.GOOD_FILE).read_bytes()

    def test_wrong_language_tag(self, testfiles):
        target = Path(testfiles / self.WRONG_TAG)
        LanguageFixer(target).run(modify=True)
        assert target.read_bytes() == Path(testfiles / self.GOOD_FILE).read_bytes()

    def test_no_modify(self, testfiles):
        target = Path(testfiles / self.WRONG_TAG)
        original_content = target.read_bytes()
        LanguageFixer(target).run(modify=False)
        assert target.read_bytes() == original_content
