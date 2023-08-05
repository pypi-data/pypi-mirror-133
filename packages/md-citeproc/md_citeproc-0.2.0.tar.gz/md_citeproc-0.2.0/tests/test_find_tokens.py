import unittest

from md_citeproc.structures import NotationStyle, OutputStyle
from md_citeproc.processors import InlinePreproc, InlineFootnotePreproc, FootnotePreproc

from . import TestHelpers


def get_test_docs():
    return TestHelpers.get_fixture_list("tokentests.md")


class TestFindTokens(unittest.TestCase):

    def test_inline_single(self):
        config = TestHelpers.get_t_config(
            csljson="dummylib.json",
            stylefile="dummycsl.csl",
            notation=NotationStyle.INLINE,
            output=OutputStyle.INLINE,
            strict=False
        )
        proc = InlinePreproc(config)
        proc._find_tokens(get_test_docs()[0])
        self.assertEqual(len(proc.citations), 3)
        self.assertEqual(proc.citations[0].references[0].citekey, "citekey1")
        self.assertIsNone(getattr(proc.citations[0].references[0], "uses", None))
        self.assertEqual(proc.citations[1].references[0].citekey, "citekey2")
        self.assertEqual(proc.citations[2].references[0].citekey, "citekey3")
        self.assertEqual(proc.citations[2].references[0].prefix, "prefix ")
        self.assertEqual(proc.citations[2].references[0].suffix, ", suffix")

    def test_inline_footnote_single(self):
        config = TestHelpers.get_t_config(
            notation=NotationStyle.INLINE_FOOTNOTE,
            output=OutputStyle.INLINE,
            stylefile="dummycsl.csl",
            csljson="dummylib.json"
        )
        proc = InlineFootnotePreproc(config)
        proc._find_tokens(get_test_docs()[1])
        a = "a[^@citekey1] and b[^prefix @citekey2, suffix] and c[^no_key] and d[^@unknownkey]"
        self.assertEqual(len(proc.citations), 4)
        self.assertEqual(proc.citations[0].references[0].citekey, "citekey1")
        self.assertIsNone(getattr(proc.citations[0].references[0], "uses", None))
        self.assertEqual(proc.citations[1].references[0].citekey, "citekey2")
        self.assertEqual(proc.citations[1].references[0].prefix, "prefix ")
        self.assertEqual(proc.citations[1].references[0].suffix, ", suffix")
        self.assertEqual(proc.citations[2].references[0].content, "no_key")
        self.assertEqual(proc.citations[2].references[0].citekey, None)
        self.assertEqual(proc.citations[3].references[0].content, "@unknownkey")
        self.assertEqual(proc.citations[3].references[0].citekey, None)

    def test_footnote_single(self):
        config = TestHelpers.get_t_config(
            notation=NotationStyle.FOOTNOTE,
            output=OutputStyle.INLINE,
            stylefile="dummycsl.csl",
            csljson="dummylib.json"
        )
        proc = FootnotePreproc(config)
        proc._find_tokens(get_test_docs()[2])
        self.assertEqual(len(proc.citations), 4)
        self.assertEqual(proc.citations[0].references[0].citekey, "citekey1")
        self.assertEqual(proc.citations[0].marker, "1")
        self.assertEqual(len(proc.citations[0].uses), 2)
        self.assertEqual(proc.citations[1].references[0].citekey, "citekey2")
        self.assertEqual(proc.citations[1].references[0].prefix, "prefix ")
        self.assertEqual(proc.citations[1].references[0].suffix, ", suffix")
        self.assertEqual(proc.citations[1].marker, "2")
        self.assertEqual(len(proc.citations[1].uses), 0)
        self.assertEqual(proc.citations[2].references[0].content, "@unknownkey")
        self.assertEqual(proc.citations[2].references[0].citekey, None)
        self.assertEqual(proc.citations[2].marker, "3")
        self.assertEqual(len(proc.citations[2].uses), 1)
        self.assertEqual(proc.citations[3].references[0].content, "no_key")
        self.assertEqual(proc.citations[3].references[0].citekey, None)
        self.assertEqual(proc.citations[3].marker, "4")
        self.assertEqual(len(proc.citations[3].uses), 1)

    def test_inline_multi(self):
        config = TestHelpers.get_t_config(
            notation=NotationStyle.INLINE,
            output=OutputStyle.INLINE,
            stylefile="dummycsl.csl",
            csljson="dummylib.json"
        )
        proc = InlinePreproc(config)
        proc._find_tokens(get_test_docs()[3])
        self.assertEqual(len(proc.citations), 6)
        self.assertEqual(len(proc.citations[0].references), 3)
        self.assertEqual(proc.citations[0].references[0].citekey, "citekey1")
        self.assertEqual(proc.citations[0].references[1].citekey, "citekey2")
        self.assertEqual(proc.citations[0].references[2].citekey, "citekey3")
        self.assertEqual(proc.citations[0].references[1].prefix, "")
        self.assertEqual(proc.citations[0].references[1].suffix, "")
        self.assertEqual(len(proc.citations[1].references), 1)
        self.assertEqual(proc.citations[1].references[0].prefix, "prefix;")
        self.assertEqual(proc.citations[1].references[0].suffix, ":post1;post2")
        self.assertEqual(len(proc.citations[2].references), 2)
        self.assertEqual(proc.citations[2].references[0].prefix, "prefix ")
        self.assertEqual(proc.citations[2].references[0].suffix, " suffix")
        self.assertEqual(proc.citations[2].references[1].prefix, " pre2 ")
        self.assertEqual(proc.citations[2].references[1].suffix, ": post2")
        self.assertEqual(len(proc.citations[3].references), 2)
        self.assertEqual(proc.citations[3].references[0].suffix, ": irregular suffix ")
        self.assertEqual(proc.citations[3].references[1].suffix, "")
        self.assertEqual(len(proc.citations[4].references), 1)
        self.assertEqual(proc.citations[4].references[0].suffix, " suffix @invalid")
        self.assertEqual(len(proc.citations[5].references), 1)
        self.assertEqual(proc.citations[5].references[0].citekey, None)
        self.assertEqual(proc.citations[5].references[0].content, "@invalid1; @invalid2")

    def test_inline_footnote_multi(self):
        config = TestHelpers.get_t_config(
            notation=NotationStyle.INLINE_FOOTNOTE,
            output=OutputStyle.INLINE,
            stylefile="dummycsl.csl",
            csljson="dummylib.json"
        )
        proc = InlineFootnotePreproc(config)
        proc._find_tokens(get_test_docs()[4])
        self.assertEqual(len(proc.citations), 6)
        self.assertEqual(len(proc.citations[0].references), 3)
        self.assertEqual(proc.citations[0].references[0].citekey, "citekey1")
        self.assertEqual(proc.citations[0].references[1].citekey, "citekey2")
        self.assertEqual(proc.citations[0].references[2].citekey, "citekey3")
        self.assertEqual(proc.citations[0].references[1].prefix, "")
        self.assertEqual(proc.citations[0].references[1].suffix, "")
        self.assertEqual(len(proc.citations[1].references), 1)
        self.assertEqual(proc.citations[1].references[0].prefix, "prefix;")
        self.assertEqual(proc.citations[1].references[0].suffix, ":post1;post2")
        self.assertEqual(len(proc.citations[2].references), 2)
        self.assertEqual(proc.citations[2].references[0].prefix, "prefix ")
        self.assertEqual(proc.citations[2].references[0].suffix, " suffix")
        self.assertEqual(proc.citations[2].references[1].prefix, " pre2 ")
        self.assertEqual(proc.citations[2].references[1].suffix, ": post2")
        self.assertEqual(len(proc.citations[3].references), 2)
        self.assertEqual(proc.citations[3].references[0].suffix, ": irregular suffix ")
        self.assertEqual(proc.citations[3].references[1].suffix, "")
        self.assertEqual(len(proc.citations[4].references), 1)
        self.assertEqual(proc.citations[4].references[0].suffix, " suffix @invalid")
        self.assertEqual(len(proc.citations[5].references), 1)
        self.assertEqual(proc.citations[5].references[0].citekey, None)
        self.assertEqual(proc.citations[5].references[0].content, "@invalid1; @invalid2")

    def test_footnote_multi(self):
        config = TestHelpers.get_t_config(
            notation=NotationStyle.FOOTNOTE,
            output=OutputStyle.INLINE,
            stylefile="dummycsl.csl",
            csljson="dummylib.json"
        )
        proc = FootnotePreproc(config)
        proc._find_tokens(get_test_docs()[5])
        self.assertEqual(len(proc.citations), 6)
        self.assertEqual(len(proc.citations[0].references), 3)
        self.assertEqual(proc.citations[0].references[0].citekey, "citekey1")
        self.assertEqual(proc.citations[0].references[1].citekey, "citekey2")
        self.assertEqual(proc.citations[0].references[2].citekey, "citekey3")
        self.assertEqual(proc.citations[0].references[1].prefix, "")
        self.assertEqual(proc.citations[0].references[1].suffix, "")
        self.assertEqual(len(proc.citations[1].references), 1)
        self.assertEqual(proc.citations[1].references[0].prefix, "prefix;")
        self.assertEqual(proc.citations[1].references[0].suffix, ":post1;post2")
        self.assertEqual(len(proc.citations[2].references), 2)
        self.assertEqual(proc.citations[2].references[0].prefix, "prefix ")
        self.assertEqual(proc.citations[2].references[0].suffix, " suffix")
        self.assertEqual(proc.citations[2].references[1].prefix, " pre2 ")
        self.assertEqual(proc.citations[2].references[1].suffix, ": post2")
        self.assertEqual(len(proc.citations[3].references), 2)
        self.assertEqual(proc.citations[3].references[0].suffix, ": irregular suffix ")
        self.assertEqual(proc.citations[3].references[1].suffix, "")
        self.assertEqual(len(proc.citations[4].references), 1)
        self.assertEqual(proc.citations[4].references[0].suffix, " suffix @invalid")
        self.assertEqual(len(proc.citations[5].references), 1)
        self.assertEqual(proc.citations[5].references[0].citekey, None)
        self.assertEqual(proc.citations[5].references[0].content, "@invalid1; @invalid2")

    def test_ignore_code_inline(self):
        config = TestHelpers.get_t_config(
            notation=NotationStyle.INLINE,
            output=OutputStyle.INLINE,
            stylefile="dummycsl.csl",
            csljson="dummylib.json"
        )
        proc = InlinePreproc(config)
        proc._find_tokens(get_test_docs()[6])
        self.assertEqual(len(proc.citations), 2)
        self.assertEqual(proc.citations[0].references[0].citekey, "citekey1")
        self.assertEqual(proc.citations[1].references[0].citekey, "citekey2")

    def test_ignore_code_inline_footnote(self):
        config = TestHelpers.get_t_config(
            notation=NotationStyle.INLINE_FOOTNOTE,
            output=OutputStyle.INLINE,
            stylefile="dummycsl.csl",
            csljson="dummylib.json"
        )
        proc = InlineFootnotePreproc(config)
        proc._find_tokens(get_test_docs()[7])
        self.assertEqual(len(proc.citations), 2)
        self.assertEqual(proc.citations[0].references[0].citekey, "citekey1")
        self.assertEqual(proc.citations[1].references[0].citekey, "citekey2")

    def test_ignore_code_footnote(self):
        config = TestHelpers.get_t_config(
            notation=NotationStyle.FOOTNOTE,
            output=OutputStyle.INLINE,
            stylefile="dummycsl.csl",
            csljson="dummylib.json"
        )
        proc = FootnotePreproc(config)
        proc._find_tokens(get_test_docs()[8])
        self.assertEqual(len(proc.citations), 2)
        self.assertEqual(proc.citations[0].references[0].citekey, "citekey1")
        self.assertEqual(len(proc.citations[0].uses), 1)
        self.assertEqual(proc.citations[0].uses[0].line_no, 2)
        self.assertEqual(proc.citations[1].references[0].citekey, "citekey2")
        self.assertEqual(len(proc.citations[1].uses), 1)
        self.assertEqual(len(proc.citations[1].uses), 1)
        self.assertEqual(proc.citations[1].uses[0].line_no, 9)

    def test_collection_tokens(self):
        config = TestHelpers.get_t_config(
            notation=NotationStyle.INLINE_FOOTNOTE,
            output=OutputStyle.NUM_FOOTNOTES,
            stylefile="dummycsl.csl",
            csljson="dummylib.json"
        )
        proc1 = InlinePreproc(config)
        proc1._find_tokens(get_test_docs()[9])
        proc2 = InlineFootnotePreproc(config)
        proc2._find_tokens(get_test_docs()[9])
        proc3 = FootnotePreproc(config)
        proc3._find_tokens(get_test_docs()[9])
        for i in [proc1, proc2, proc3]:
            self.assertEqual(i.collections["bibliography"][0], 9)
            self.assertEqual(i.collections["footnotes"][0], 10)
