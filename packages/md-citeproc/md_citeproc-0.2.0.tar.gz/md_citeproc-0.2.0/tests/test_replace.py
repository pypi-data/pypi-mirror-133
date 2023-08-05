import unittest

from md_citeproc.processors import InlinePreproc, InlineFootnotePreproc, FootnotePreproc
from md_citeproc.structures import NotationStyle, OutputStyle
from . import TestHelpers


class TestReplace(unittest.TestCase):

    def test_inline_replaced(self):
        config = TestHelpers.get_t_config(
            notation=NotationStyle.INLINE,
            output=OutputStyle.INLINE,
            stylefile="cambridge.csl",
            csljson="lib.json"
        )
        testdoc = TestHelpers.get_fixture_list("renderingtests.md")[0]
        preproc = InlinePreproc(config)
        preproc.testable_render(testdoc)
