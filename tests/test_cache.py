import unittest

from src.search.cache import LRUCache


class TestLRUCache(unittest.TestCase):

    def test_put_and_get(self):
        cache = LRUCache(2)

        cache.put("python", [1, 2])

        self.assertEqual(
            cache.get("python"),
            [1, 2]
        )

    def test_cache_miss(self):
        cache = LRUCache(2)

        self.assertIsNone(
            cache.get("missing")
        )

    def test_lru_eviction(self):
        cache = LRUCache(2)

        cache.put("python", [1])
        cache.put("storage", [2])

        cache.get("python")

        cache.put("database", [3])

        self.assertEqual(
            cache.get("python"),
            [1]
        )

        self.assertIsNone(
            cache.get("storage")
        )

    def test_update_existing_key(self):
        cache = LRUCache(2)

        cache.put("python", [1])
        cache.put("python", [1, 2])

        self.assertEqual(
            cache.get("python"),
            [1, 2]
        )

    def test_clear(self):
        cache = LRUCache(2)

        cache.put("python", [1])
        cache.put("storage", [2])

        cache.clear()

        self.assertEqual(len(cache), 0)