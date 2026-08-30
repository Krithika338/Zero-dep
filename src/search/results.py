from dataclasses import dataclass


@dataclass
class SearchResult:
    document_id: int
    score: float