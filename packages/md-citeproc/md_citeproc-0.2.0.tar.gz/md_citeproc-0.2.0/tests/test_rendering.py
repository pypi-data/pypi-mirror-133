import unittest

from md_citeproc.structures import NotationStyle, OutputStyle, PlainReference
from md_citeproc.processors import InlinePreproc, InlineFootnotePreproc, FootnotePreproc

from . import TestHelpers


class TestRendering(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_inline_rendered(self):
        config = TestHelpers.get_t_config(
            notation=NotationStyle.INLINE,
            output=OutputStyle.INLINE,
            stylefile="cambridge.csl",
            csljson="lib.json"
        )
        testdoc = TestHelpers.get_fixture_list("renderingtests.md")[0]
        preproc = InlinePreproc(config)
        preproc.testable_render(testdoc)
        self.assertEqual(preproc.citations[0].rendered, "(Büchner, Georg 2011)")
        self.assertEqual(preproc.citations[1].rendered, "(prefix Jelinek, Elfriede 2008, suffix)")
        self.assertEqual(len(preproc.citations), 2)

    def test_footnote_rendered(self):
        config = TestHelpers.get_t_config(
            notation=NotationStyle.FOOTNOTE,
            output=OutputStyle.INLINE,
            stylefile="dtphilologie.csl",
            csljson="lib.json"
        )
        testdoc = TestHelpers.get_fixture_list("renderingtests.md")[1]
        preproc = FootnotePreproc(config)
        preproc.testable_render(testdoc)
        self.assertEqual(preproc.citations[0].rendered, "Büchner, Georg: Leonce und Lena, Berlin 2011.")
        self.assertEqual(preproc.citations[1].rendered, "Jelinek, Elfriede: Ein Sportstück, Reineck bei Hamburg 2008.")
        self.assertEqual(len(preproc.citations[1].uses), 2)
        self.assertEqual(preproc.citations[2].rendered, "ct. Büchner, Georg: Leonce und Lena, Berlin 2011, p. 42.")
        self.assertEqual(preproc.citations[3].rendered, "Jelinek, Elfriede: Das Werk, in: In den Alpen. Drei Dramen, Berlin 2004.")

    def test_inline_footnote_rendered(self):
        config = TestHelpers.get_t_config(
            notation=NotationStyle.INLINE_FOOTNOTE,
            output=OutputStyle.NUM_FOOTNOTES,
            stylefile="dtphilologie.csl",
            csljson="lib.json"
        )
        testdoc = TestHelpers.get_fixture_list("renderingtests.md")[2]
        preproc = InlineFootnotePreproc(config)
        preproc.testable_render(testdoc)
        self.assertEqual(preproc.citations[0].rendered, "ct. Büchner, Georg: Leonce und Lena, Berlin 2011, p. 12.")
        self.assertEqual(preproc.citations[1].rendered, "no key")
        self.assertEqual(len(preproc.citations), 2)

    def test_rendering_without_csl(self):
        config = TestHelpers.get_t_config(
            csljson="lib.json",
            notation=NotationStyle.INLINE_FOOTNOTE,
            output=OutputStyle.NUM_FOOTNOTES,
            stylefile=None
        )
        testdoc = TestHelpers.get_fixture_list("renderingtests.md")[2]
        preproc = InlineFootnotePreproc(config)
        preproc.testable_render(testdoc)
        self.assertEqual(len(preproc.citations), 2)
        for i in preproc.citations:
            self.assertEqual(len(i.references), 1)
            self.assertTrue(isinstance(i.references[0], PlainReference))

    def test_rendering_without_csljson(self):
        config = TestHelpers.get_t_config(
            csljson=None,
            notation=NotationStyle.INLINE_FOOTNOTE,
            output=OutputStyle.NUM_FOOTNOTES,
            stylefile="dtphilologie.csl"
        )
        testdoc = TestHelpers.get_fixture_list("renderingtests.md")[2]
        preproc = InlineFootnotePreproc(config)
        rendered = preproc.testable_render(testdoc)
        self.assertEqual(len(preproc.citations), 2)
        for i in preproc.citations:
            self.assertEqual(len(i.references), 1)
            self.assertTrue(isinstance(i.references[0], PlainReference))
