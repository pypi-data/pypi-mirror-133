import unittest
import markdown
from pathlib import Path
import tempfile
import json

from md_citeproc.utils import Utilities
from md_citeproc.exceptions import CiteprocStrictException
from md_citeproc.structures import NotationStyle, OutputStyle
from md_citeproc.processors import InlinePreproc, InlineFootnotePreproc, FootnotePreproc
from md_citeproc import CiteprocExtension, CiteprocWarning

from . import TestHelpers


def get_test_docs():
    return TestHelpers.get_fixture_list("warningtests.md")


class TestWarnings(unittest.TestCase):

    def test_inline_warning(self):
        config = TestHelpers.get_t_config(
            notation=NotationStyle.INLINE,
            output=OutputStyle.INLINE,
            stylefile="dummycsl.csl",
            csljson="dummylib.json",
            strict=False
        )
        proc = InlinePreproc(config)
        proc._find_tokens(get_test_docs()[0])
        self.assertEqual(len(proc.warnings), 1)
        warning = proc.warnings[0]
        self.assertEqual(warning.citekey, "citekey4")

    def test_inline_strict(self):
        config = TestHelpers.get_t_config(
            notation=NotationStyle.INLINE,
            output=OutputStyle.INLINE,
            stylefile="dummycsl.csl",
            csljson="dummylib.json",
            strict=True
        )
        proc = InlinePreproc(config)
        with self.assertRaises(CiteprocStrictException):
            proc._find_tokens(get_test_docs()[0])

    def test_inline_footnote_warning(self):
        config = TestHelpers.get_t_config(
            notation=NotationStyle.INLINE_FOOTNOTE,
            output=OutputStyle.INLINE,
            stylefile="dummycsl.csl",
            csljson="dummylib.json",
            strict=False
        )
        proc = InlineFootnotePreproc(config)
        proc._find_tokens(get_test_docs()[1])
        self.assertEqual(len(proc.warnings), 1)
        warning = proc.warnings[0]
        self.assertEqual(warning.citekey, "citekey4")

    def test_inline_footnote_strict(self):
        config = TestHelpers.get_t_config(
            notation=NotationStyle.INLINE_FOOTNOTE,
            output=OutputStyle.INLINE,
            stylefile="dummycsl.csl",
            csljson="dummylib.json",
            strict=True
        )
        proc = InlineFootnotePreproc(config)
        with self.assertRaises(CiteprocStrictException):
            proc._find_tokens(get_test_docs()[1])

    def test_footnote_warning(self):
        config = TestHelpers.get_t_config(
            notation=NotationStyle.FOOTNOTE,
            output=OutputStyle.INLINE,
            stylefile="dummycsl.csl",
            csljson="dummylib.json",
            strict=False
        )
        proc = FootnotePreproc(config)
        proc._find_tokens(get_test_docs()[2])
        self.assertEqual(len(proc.warnings), 1)
        warning = proc.warnings[0]
        self.assertEqual(warning.citekey, "citekey4")

    def test_footnote_strict(self):
        config = TestHelpers.get_t_config(
            notation=NotationStyle.FOOTNOTE,
            output=OutputStyle.INLINE,
            stylefile="dummycsl.csl",
            csljson="dummylib.json",
            strict=True
        )
        proc = FootnotePreproc(config)
        with self.assertRaises(CiteprocStrictException):
            proc._find_tokens(get_test_docs()[2])

    def test_footnote_marker_warning(self):
        config = TestHelpers.get_t_config(
            notation=NotationStyle.FOOTNOTE,
            output=OutputStyle.INLINE,
            stylefile="dummycsl.csl",
            csljson="dummylib.json",
            strict=False
        )
        proc = FootnotePreproc(config)
        proc._find_tokens(get_test_docs()[3])
        self.assertEqual(len(proc.warnings), 1)
        warning = proc.warnings[0]
        self.assertEqual(warning.marker, "2")

    def test_footnote_marker_strict(self):
        config = TestHelpers.get_t_config(
            notation=NotationStyle.FOOTNOTE,
            output=OutputStyle.INLINE,
            stylefile="dummycsl.csl",
            csljson="dummylib.json",
            strict=True
        )
        proc = FootnotePreproc(config)
        with self.assertRaises(CiteprocStrictException):
            proc._find_tokens(get_test_docs()[3])

    def test_getter(self):
        ext = CiteprocExtension(
            csljson=TestHelpers.get_fixture_dir() / "lib.json",
            cslfile=TestHelpers.get_fixture_dir() / "dtphilologie.csl",
            notation=NotationStyle.INLINE_FOOTNOTE,
            output=OutputStyle.NUM_FOOTNOTES
        )
        raw_md = TestHelpers.get_fixture_text("warningtests.md")
        markdown.markdown(raw_md, extensions=[ext])
        warnings = ext.get_warnings()
        self.assertEqual(len(warnings), 2)
        for i in warnings:
            self.assertTrue(isinstance(i, CiteprocWarning))
