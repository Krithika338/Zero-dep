class StorageAdapter:

    def __init__(self, storage):
        self.storage = storage

    def get_document(self, document_id):
        return self.storage.get_document(document_id)

    def iter_documents(self):
        return self.storage.iter_documents()