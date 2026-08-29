import unittest

from src.search.tokenizer import tokenize


class TestTokenizer(unittest.TestCase):

    def test_basic_text(self):
        result = tokenize("Python is GREAT!")
        self.assertEqual(result, ["python", "is", "great"])

    def test_punctuation(self):
        result = tokenize("Python, Python!!!")
        self.assertEqual(result, ["python", "python"])

    def test_hyphen(self):
        result = tokenize("hello-world")
        self.assertEqual(result, ["hello", "world"])

    def test_numbers(self):
        result = tokenize("123 Python")
        self.assertEqual(result, ["123", "python"])

    def test_empty_text(self):
        result = tokenize("")
        self.assertEqual(result, [])
        
    def test_unicode(self):
        result = tokenize("Python café 東京")
        self.assertEqual(result, ["python", "café", "東京"])


if __name__ == "__main__":
    unittest.main()