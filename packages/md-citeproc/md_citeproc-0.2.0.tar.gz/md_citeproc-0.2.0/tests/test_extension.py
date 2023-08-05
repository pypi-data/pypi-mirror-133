import unittest
import markdown

from md_citeproc import CiteprocExtension
from md_citeproc.structures import NotationStyle, OutputStyle
from . import TestHelpers


class TestExtension(unittest.TestCase):

    def test_ex1(self):
        ext = [CiteprocExtension(
            csljson=TestHelpers.get_fixture_dir() / "lib.json",
            cslfile=TestHelpers.get_fixture_dir() / "dtphilologie.csl",
            notation=NotationStyle.INLINE_FOOTNOTE,
            output=OutputStyle.NUM_FOOTNOTES
        )]
        raw_md = TestHelpers.get_fixture_text("extensiontests.md")
        rendered = markdown.markdown(raw_md, extensions=ext)
        prerendered = TestHelpers.get_fixture_text("test_ex1_rendered.html")
        self.assertEqual(rendered, prerendered)
