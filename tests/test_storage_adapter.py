import unittest

from src.search.storage_adapter import StorageAdapter


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