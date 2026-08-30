import unittest

from src.search.results import SearchResult


class TestSearchResult(unittest.TestCase):

    def test_search_result(self):
        result = SearchResult(42, 1.5)

        self.assertEqual(result.document_id, 42)
        self.assertEqual(result.score, 1.5)