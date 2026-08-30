import unittest

from src.search.storage_adapter import StorageAdapter
from src.storage.engine import StorageEngine

class FakeStorage:

    def __init__(self):
        self.documents = {
            1: {
                "id": 1,
                "title": "Python",
                "content": "Python is easy"
            },
            2: {
                "id": 2,
                "title": "Storage",
                "content": "Storage is important"
            }
        }

    def get_document(self, document_id):
        return self.documents.get(document_id)

    def iter_documents(self):
        return self.documents.values()


class TestStorageAdapter(unittest.TestCase):

    def setUp(self):
        self.storage = FakeStorage()
        self.adapter = StorageAdapter(self.storage)

    def test_get_document(self):
        document = self.adapter.get_document(1)

        self.assertEqual(
            document["content"],
            "Python is easy"
        )

    def test_missing_document(self):
        document = self.adapter.get_document(999)

        self.assertIsNone(document)

    def test_iter_documents(self):
        documents = list(
            self.adapter.iter_documents()
        )

        self.assertEqual(len(documents), 2)

    def test_real_storage_engine(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            storage = StorageEngine(
                f"{tmp}/test.db"
            )

            storage.put(
                "doc1",
                "Python programming language"
            )
            storage.put(
                "doc2",
                "Storage engine implementation"
            )

            adapter = StorageAdapter(storage)

            self.assertEqual(
                adapter.get_document("doc1"),
                {
                    "id": "doc1",
                    "content": "Python programming language",
                },
            )

            documents = list(
                adapter.iter_documents()
            )

            self.assertEqual(
                documents,
                [
                    {
                        "id": "doc1",
                        "content": "Python programming language",
                    },
                    {
                        "id": "doc2",
                        "content": "Storage engine implementation",
                    },
                ],
            )
    def test_storage_to_search_engine(self):
        import tempfile

        from src.search.engine import SearchEngine

        with tempfile.TemporaryDirectory() as tmp:
            storage = StorageEngine(f"{tmp}/test.db")

            storage.put(
                "doc1",
                "Python programming language"
            )
            storage.put(
                "doc2",
                "Storage engine implementation"
            )

            adapter = StorageAdapter(storage)

            search_engine = SearchEngine()

            search_engine.index_storage(adapter)

            results = search_engine.search("Python")

            self.assertEqual(results, {"doc1"})
