import math

from src.search.tokenizer import tokenize
from src.search.cache import LRUCache


class InvertedIndex:

    def __init__(self):
        self.index = {}
        self.term_frequencies = {}
        self .cache = LRUCache(100)  # Cache for search results

    def add(self, document_id, text):
        tokens = tokenize(text)

        self.term_frequencies[document_id] = {}

        for token in tokens:
            if token not in self.index:
                self.index[token] = set()

            self.index[token].add(document_id)

            frequencies = self.term_frequencies[document_id]
            frequencies[token] = frequencies.get(token, 0) + 1
        self.cache.clear()  # Clear cache when the index is updated

    def remove(self, document_id):
        empty_terms = []

        for term, document_ids in self.index.items():
            document_ids.discard(document_id)

            if not document_ids:
                empty_terms.append(term)

        for term in empty_terms:
            del self.index[term]
        self.term_frequencies.pop(document_id, None)   
        self.cache.clear()  # Clear cache when the index is updated     


    def update(self, document_id, new_text):
        self.remove(document_id)
        self.add(document_id, new_text)

    def search(self, term):
        term = term.lower()
        return self.index.get(term, set())

    def search_query(self, query):
        terms = tokenize(query)

        if not terms:
            return set()

        result = self.search(terms[0])

        for term in terms[1:]:
            result = result & self.search(term)

        return result

    def rank_query(self, query):
        terms = tokenize(query)

        if not terms:
            return []

        scores = {}

        for term in terms:
            document_ids = self.search(term)

            for document_id in document_ids:
                scores[document_id] = scores.get(document_id, 0) + 1

        return sorted(
            scores.items(),
            key=lambda item: (-item[1], item[0])
        )

    def tf_idf(self, query):
        terms = tokenize(query)

        if not terms:
            return []

        cache_key = " ".join(terms)

        cached_result = self.cache.get(cache_key)

        if cached_result is not None:
            return cached_result

        total_documents = len(self.term_frequencies)

        if total_documents == 0:
            return []

        scores = {}

        for term in terms:
            document_ids = self.search(term)

            if not document_ids:
                continue

            document_frequency = len(document_ids)

            idf = math.log(
                total_documents / document_frequency
            )

            for document_id in document_ids:
                frequency = self.term_frequencies[document_id].get(term, 0)

                score = frequency * idf

                scores[document_id] = scores.get(document_id, 0) + score

        result = sorted(
            scores.items(),
            key=lambda item: (-item[1], item[0])
        )

        self.cache.put(cache_key, result)

        return result