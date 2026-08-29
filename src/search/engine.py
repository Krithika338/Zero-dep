from src.search.index import InvertedIndex
from src.search.persistence import save_index, load_index, IndexCorruptionError


class SearchEngine:

    def __init__(self, index_path=None):
        self.index_path = index_path
        self.index = InvertedIndex()

        if self.index_path is not None:
            self._load()

    def _load(self):
        try:
            load_index(self.index, self.index_path)
        except IndexCorruptionError:
            # A new engine may not have an index file yet.
            return

    def _save(self):
        if self.index_path is not None:
            save_index(self.index, self.index_path)

    def add_document(self, document_id, text):
        self.index.add(document_id, text)
        self._save()

    def remove_document(self, document_id):
        self.index.remove(document_id)
        self._save()

    def update_document(self, document_id, text):
        self.index.update(document_id, text)
        self._save()

    def search(self, query):
        return self.index.search_query(query)

    def rank(self, query):
        return self.index.rank_query(query)

    def index_storage(self, storage):
        for document in storage.iter_documents():
            document_id = document["id"]
            content = document.get("content", "")

            self.index.add(document_id, content)

        self._save()

    def sync_add(self, document):
        document_id = document["id"]
        content = document.get("content", "")

        self.index.add(document_id, content)

        self._save()

    def sync_remove(self, document_id):
        self.index.remove(document_id)
        self._save()

    def sync_update(self, document):
        document_id = document["id"]
        content = document.get("content", "")

        self.index.update(document_id, content)

        self._save()