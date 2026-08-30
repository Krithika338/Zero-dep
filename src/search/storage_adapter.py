class StorageAdapter:

    def __init__(self, storage):
        self.storage = storage

    def get_document(self, document_id):
        if hasattr(self.storage, "get_document"):
            return self.storage.get_document(document_id)

        value = self.storage.get(str(document_id))

        if value is None:
            return None

        return {
            "id": document_id,
            "content": value,
        }

    def iter_documents(self):
        if hasattr(self.storage, "iter_documents"):
            yield from self.storage.iter_documents()
            return

        for document_id, content in self.storage.scan():
            yield {
               "id": document_id,
               "content": content,
            }