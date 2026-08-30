import json
from pathlib import Path


class IndexCorruptionError(Exception):
    pass


def save_index(index, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "index": {
            term: list(document_ids)
            for term, document_ids in index.index.items()
        },
        "term_frequencies": {
            str(document_id): frequencies
            for document_id, frequencies in index.term_frequencies.items()
        },
    }

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def load_index(index, path):
    path = Path(path)

    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError) as exc:
        raise IndexCorruptionError(
            "Invalid or corrupted index file"
        ) from exc

    required_fields = {
        "index",
        "term_frequencies",
    }

    if not required_fields.issubset(data):
        raise IndexCorruptionError("Missing required field")

    try:
        index.index = {
            term: set(document_ids)
            for term, document_ids in data["index"].items()
        }

        index.term_frequencies = {
            int(document_id): frequencies
            for document_id, frequencies in data["term_frequencies"].items()
        }

        index.cache.clear()

    except (TypeError, ValueError, AttributeError) as exc:
        raise IndexCorruptionError(
            "Invalid index data"
        ) from exc