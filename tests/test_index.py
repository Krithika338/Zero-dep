import unittest

from src.search.index import InvertedIndex


class TestInvertedIndex(unittest.TestCase):

    def setUp(self):
        self.index = InvertedIndex()

    def test_add_document(self):
        self.index.add(1, "Python is easy")

        self.assertEqual(self.index.search("python"), {1})
        self.assertEqual(self.index.search("easy"), {1})

    def test_multiple_documents(self):
        self.index.add(1, "Python is easy")
        self.index.add(2, "Python is powerful")

        self.assertEqual(self.index.search("python"), {1, 2})
        self.assertEqual(self.index.search("easy"), {1})
        self.assertEqual(self.index.search("powerful"), {2})

    def test_duplicate_words(self):
        self.index.add(1, "Python Python Python")

        self.assertEqual(self.index.search("python"), {1})

    def test_unknown_word(self):
        self.index.add(1, "Python is easy")

        self.assertEqual(self.index.search("database"), set())

    def test_case_insensitive_search(self):
        self.index.add(1, "Python is easy")

        self.assertEqual(self.index.search("PYTHON"), {1})

    def test_remove_document(self):
        self.index.add(1, "Python is easy")
        self.index.add(2, "Python is powerful")

        self.index.remove(1)

        self.assertEqual(self.index.search("python"), {2})
        self.assertEqual(self.index.search("easy"), set())
        self.assertEqual(self.index.search("powerful"), {2})

    def test_remove_nonexistent_document(self):
        self.index.add(1, "Python is easy")

        self.index.remove(99)

        self.assertEqual(self.index.search("python"), {1})

    def test_update_document(self):
        self.index.add(1, "Python is easy")

        self.index.update(1, "Python is powerful")

        self.assertEqual(self.index.search("python"), {1})
        self.assertEqual(self.index.search("powerful"), {1})
        self.assertEqual(self.index.search("easy"), set())

    def test_multi_word_query(self):
        self.index.add(1, "Python is easy")
        self.index.add(2, "Python uses storage")
        self.index.add(3, "Storage is important")

        result = self.index.search_query("python storage")

        self.assertEqual(result, {2})

    def test_multi_word_query_no_match(self):
        self.index.add(1, "Python is easy")
        self.index.add(2, "Storage is useful")

        result = self.index.search_query("python database")

        self.assertEqual(result, set())

    def test_empty_query(self):
        self.index.add(1, "Python is easy")

        result = self.index.search_query("")

        self.assertEqual(result, set())

    def test_rank_query(self):
        self.index.add(1, "Python is easy")
        self.index.add(2, "Python storage is useful")
        self.index.add(3, "Storage is important")

        result = self.index.rank_query("python storage")

        self.assertEqual(result[0], (2, 2))
        self.assertEqual(result[1], (1, 1))
        self.assertEqual(result[2], (3, 1))

    def test_rank_empty_query(self):
        result = self.index.rank_query("")

        self.assertEqual(result, [])

    def test_tf_idf(self):
        self.index.add(1, "python python")
        self.index.add(2, "python storage storage")
        self.index.add(3, "storage")

        result = self.index.tf_idf("storage")

        self.assertEqual(result[0][0], 2)
        self.assertGreater(result[0][1], result[1][1])

    def test_tf_idf_empty_query(self):
        result = self.index.tf_idf("")

        self.assertEqual(result, [])

    def test_search_cache(self):
        self.index.add(1, "python storage")
        self.index.add(2, "python")

        first_result = self.index.tf_idf("python")

        cached_result = self.index.cache.get("python")

        self.assertIsNotNone(cached_result)
        self.assertEqual(first_result, cached_result)

    def test_cache_invalidated_after_add(self):
        self.index.add(1, "python")

        self.index.tf_idf("python")

        self.assertIsNotNone(
            self.index.cache.get("python")
        )

        self.index.add(2, "python")

        self.assertIsNone(
            self.index.cache.get("python")
        )

    def test_cache_invalidated_after_remove(self):
        self.index.add(1, "python")

        self.index.tf_idf("python")

        self.assertIsNotNone(
            self.index.cache.get("python")
        )

        self.index.remove(1)

        self.assertIsNone(
            self.index.cache.get("python")
        )


if __name__ == "__main__":
    unittest.main()