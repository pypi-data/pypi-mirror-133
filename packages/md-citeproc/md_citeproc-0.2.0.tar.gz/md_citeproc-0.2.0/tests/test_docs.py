import unittest
import markdown

from md_citeproc import CiteprocExtension
from md_citeproc.structures import NotationStyle, OutputStyle
from . import TestHelpers


class TestExtension(unittest.TestCase):

    def test_doc1(self):
        ext = [CiteprocExtension(
            csljson=TestHelpers.get_fixture_dir() / "lib.json",
            cslfile=TestHelpers.get_fixture_dir() / "cambridge-university-press-author-date.csl",
            notation=NotationStyle.INLINE,
            output=OutputStyle.INLINE
        )]
        rawmd = "I shall continue my journal concerning the stranger at intervals, should I have any fresh incidents to record.[@shelleyFrankenstein2020, Letter 4] Something completely different.[@missingCitekey]"
        print(markdown.markdown(rawmd, extensions=ext))

    def test_doc2(self):
        ext = [CiteprocExtension(
            csljson=TestHelpers.get_fixture_dir() / "lib.json",
            cslfile=TestHelpers.get_fixture_dir() / "cambridge-university-press-note.csl",
            notation=NotationStyle.INLINE,
            output=OutputStyle.NUM_FOOTNOTES
        )]
        rawmd = """
I shall continue my journal concerning the stranger at intervals, should I have any fresh incidents to record.[@shelleyFrankenstein2020, Letter 4] Something completely different.[@missingCitekey]

[FOOTNOTES]
"""
        print(markdown.markdown(rawmd, extensions=ext))