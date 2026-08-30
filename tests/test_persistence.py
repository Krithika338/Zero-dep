import os
import tempfile
import unittest

from src.search.index import InvertedIndex
from src.search.persistence import (save_index, load_index, IndexCorruptionError,)


class TestPersistence(unittest.TestCase):

    def test_save_and_load_index(self):
        index = InvertedIndex()

        index.add(1, "python storage")
        index.add(2, "python database")

        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "index.json")

            save_index(index, path)

            loaded_index = InvertedIndex()
            load_index(loaded_index, path)

            self.assertEqual(
                loaded_index.search("python"),
                {1, 2}
            )

            self.assertEqual(
                loaded_index.search("storage"),
                {1}
            )

            self.assertEqual(
                loaded_index.search("database"),
                {2}
            )

    def test_term_frequencies_are_preserved(self):
        index = InvertedIndex()

        index.add(1, "python python storage")

        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "index.json")

            save_index(index, path)

            loaded_index = InvertedIndex()
            load_index(loaded_index, path)

            self.assertEqual(
                loaded_index.term_frequencies[1]["python"],
                2
            )

            self.assertEqual(
                loaded_index.term_frequencies[1]["storage"],
                1
            )

    def test_corrupted_json(self):
        index = InvertedIndex()

        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "index.json")

            with open(path, "w", encoding="utf-8") as file:
                file.write("{ this is not valid json")

            with self.assertRaises(IndexCorruptionError):
                load_index(index, path)

    def test_missing_required_field(self):
        index = InvertedIndex()

        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "index.json")

            with open(path, "w", encoding="utf-8") as file:
                file.write('{"index": {}}')

            with self.assertRaises(IndexCorruptionError):
                load_index(index, path)   