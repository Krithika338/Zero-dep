import os
import tempfile
import unittest


from src.search.engine import SearchEngine


class TestSearchEngine(unittest.TestCase):

    def setUp(self):
        self.engine = SearchEngine()

    def test_add_and_search(self):
        self.engine.add_document(
            1,
            "Python is easy to learn"
        )

        result = self.engine.search("python")

        self.assertEqual(result, {1})

    def test_multiple_documents(self):
        self.engine.add_document(
            1,
            "Python storage"
        )

        self.engine.add_document(
            2,
            "Python database"
        )

        result = self.engine.search("python")

        self.assertEqual(result, {1, 2})

    def test_remove_document(self):
        self.engine.add_document(
            1,
            "Python storage"
        )

        self.engine.remove_document(1)

        result = self.engine.search("python")

        self.assertEqual(result, set())

    def test_update_document(self):
        self.engine.add_document(
            1,
            "Python storage"
        )

        self.engine.update_document(
            1,
            "Python database"
        )

        self.assertEqual(
            self.engine.search("storage"),
            set()
        )

        self.assertEqual(
            self.engine.search("database"),
            {1}
        )

    def test_engine_persists_documents(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "index.json")

            engine1 = SearchEngine(path)

            engine1.add_document(
                1,
                "Python storage"
            )

            engine2 = SearchEngine(path)

            self.assertEqual(
                engine2.search("python"),
                {1}
            )

    def test_engine_persists_updates(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "index.json")

            engine1 = SearchEngine(path)

            engine1.add_document(
                1,
                "Python storage"
            )

            engine1.update_document(
                1,
                "Python database"
            )

            engine2 = SearchEngine(path)

            self.assertEqual(
                engine2.search("database"),
                {1}
            )

            self.assertEqual(
                engine2.search("storage"),
                set()
            )

    def test_index_storage(self):
        class FakeStorage:

            def iter_documents(self):
                return [
                    {
                        "id": 1,
                        "title": "Python",
                        "content": "Python is easy"
                    },
                    {
                        "id": 2,
                        "title": "Storage",
                        "content": "Python storage"
                    },
                    {
                        "id": 3,
                        "title": "Database",
                        "content": "Database storage"
                    }
                ]

        storage = FakeStorage()

        self.engine.index_storage(storage)

        self.assertEqual(
            self.engine.search("python"),
            {1, 2}
        )

        self.assertEqual(
            self.engine.search("storage"),
            {2, 3}
        )

    def test_sync_add(self):
        document = {
            "id": 10,
            "title": "Python",
            "content": "Python programming"
        }

        self.engine.sync_add(document)

        self.assertEqual(
            self.engine.search("python"),
            {10}
        )

    def test_sync_remove(self):
        self.engine.add_document(
            10,
            "Python programming"
        )

        self.engine.sync_remove(10)

        self.assertEqual(
            self.engine.search("python"),
            set()
        )

    def test_sync_update(self):
        self.engine.add_document(
            10,
            "Python easy"
        )

        document = {
            "id": 10,
            "title": "Python",
            "content": "Python powerful"
        }

        self.engine.sync_update(document)

        self.assertEqual(
            self.engine.search("easy"),
            set()
        )

        self.assertEqual(
            self.engine.search("powerful"),
            {10}
        )