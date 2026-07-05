import unittest
from ocr_engine import _merge_unique_words, should_keep_word


class OCRLogicTests(unittest.TestCase):
    def test_merge_preserves_known_words_with_lower_confidence_candidates(self):
        merged = _merge_unique_words([
            "VOR",
            "VOICE OF REHMAT",
        ])
        self.assertIn("VOR", merged)
        self.assertIn("VOICE OF REHMAT", merged)

    def test_should_keep_word_allows_longer_words_with_medium_confidence(self):
        self.assertTrue(should_keep_word("VOICE", 58.0))
        self.assertTrue(should_keep_word("REHMAT", 55.0))
        self.assertTrue(should_keep_word("VOR", 95.0))

    def test_should_keep_word_rejects_short_or_garbage_tokens(self):
        self.assertFalse(should_keep_word("CY", 55.0))
        self.assertFalse(should_keep_word("IA", 40.0))
        self.assertFalse(should_keep_word("#", 95.0))


if __name__ == "__main__":
    unittest.main()
