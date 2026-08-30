# Zero-dep

An offline, zero-dependency knowledge search and indexing engine built entirely with Python's standard library.

## Features

- Add documents
- Search documents
- Update documents
- Remove documents
- Boolean-style multi-term search
- Ranked search
- TF-IDF scoring
- LRU search-result caching
- Persistent inverted index
- Persistent storage engine
- Binary record validation
- Checksums for storage integrity
- Storage compaction
- Unicode text support
- Command-line interface
- Automated test suite

## Requirements

- Python 3.12+
- No third-party runtime dependencies

## One-Command Run

From the repository root:

```bash
python main.py add 1 "Python is a programming language"# Zero-dep
An offline knowledge search and indexing engine.
