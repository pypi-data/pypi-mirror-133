import re
import unittest

from md_citeproc.structures import RePatterns


class TestRePatterns(unittest.TestCase):

    def _match_n(self, string, pattern, n_macthes):
        m = re.findall(pattern, string)
        self.assertEqual(len(m), n_macthes, "Tested string: {}".format(string))

    def test_citekey_pattern(self):
        self._match_n(" @citekey", RePatterns.CITEKEY, 1)
        self._match_n("[@citekey]", RePatterns.CITEKEY, 1)
        self._match_n("[@citekey; @citekey]", RePatterns.CITEKEY, 2)
        self._match_n("[@citekey;@citekey]", RePatterns.CITEKEY, 2)
        self._match_n("[^@citekey]", RePatterns.CITEKEY, 1)
        self._match_n("someone@domain.com", RePatterns.CITEKEY, 0)
        self._match_n("@citekey:", RePatterns.CITEKEY, 0)

    def test_inline_container_pattern(self):
        self._match_n("a[abc]", RePatterns.INLINE_CONTAINER, 1)
        self._match_n("[abc]", RePatterns.INLINE_CONTAINER, 0)
        self._match_n("a[abc] b[abc]", RePatterns.INLINE_CONTAINER, 2)
        self._match_n("a[^?@#%]", RePatterns.INLINE_CONTAINER, 1)

    def test_inline_footnote_pattern(self):
        self._match_n("a[abc]", RePatterns.INLINE_FOOTNOTE, 0)
        self._match_n("a[^abc]", RePatterns.INLINE_FOOTNOTE, 1)
        self._match_n("[^abc]", RePatterns.INLINE_FOOTNOTE, 0)
        self._match_n("a[^abc] b[^abc]", RePatterns.INLINE_FOOTNOTE, 2)
        self._match_n("a[^@citekey, ct. p. 8-9]", RePatterns.INLINE_FOOTNOTE, 1)
        self._match_n("a[^@citekey, ct. p. 8-9]", RePatterns.INLINE_FOOTNOTE, 1)
        self._match_n("a[^@?!$_;]", RePatterns.INLINE_FOOTNOTE, 1)

    def test_footnote_patterns(self):
        self._match_n("a[^abc]", RePatterns.FOOTNOTE_ANCHOR, 1)
        self._match_n("a[^abc]", RePatterns.FOOTNOTE, 0)
        self._match_n("[^abc]", RePatterns.FOOTNOTE_ANCHOR, 0)
        self._match_n("[^abc]", RePatterns.FOOTNOTE, 1)
        self._match_n("a[^abc] b[^def]", RePatterns.FOOTNOTE_ANCHOR, 2)
        self._match_n("a[^?!]", RePatterns.FOOTNOTE_ANCHOR, 0)
        self._match_n("[^?!]", RePatterns.FOOTNOTE, 0)
