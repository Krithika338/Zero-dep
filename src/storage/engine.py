import os
import struct
from pathlib import Path

from .records import (
    encode_put,
    encode_delete,
    decode_record,
    decode_payload,
    HEADER_SIZE,
    CHECKSUM_SIZE,
)


class StorageEngine:
    def __init__(self, path: str):
        self.path = Path(path)

        self.path.parent.mkdir(parents=True, exist_ok=True)

        if not self.path.exists():
            self.path.touch()

    def _validate_key(self, key: str) -> None:
        if not isinstance(key, str):
            raise TypeError("Key must be a string")

        if not key:
            raise ValueError("Key cannot be empty")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def put(self, key: str, value: str) -> None:
        self._validate_key(key)

        record = encode_put(key, value)

        with self.path.open("ab") as file:
            file.write(record)
            file.flush()
            os.fsync(file.fileno())

    def delete(self, key: str) -> None:
        self._validate_key(key)

        record = encode_delete(key)

        with self.path.open("ab") as file:
            file.write(record)
            file.flush()
            os.fsync(file.fileno())

    def _iter_records(self):
        if not self.path.exists():
            return

        data = self.path.read_bytes()
        position = 0

        while position < len(data):
            if len(data) - position < HEADER_SIZE:
                break

            header = data[position:position + HEADER_SIZE]

            _, _, _, payload_size = struct.unpack(
                ">4sBBI", header
            )

            record_size = HEADER_SIZE + payload_size + CHECKSUM_SIZE

            if len(data) - position < record_size:
                break

            record_data = data[position:position + record_size]

            record_type, payload = decode_record(record_data)
            record_key, record_value = decode_payload(
                record_type, payload
            )

            yield record_key, record_value

            position += record_size

    def get(self, key: str):
        self._validate_key(key)

        result = None

        for record_key, record_value in self._iter_records():
            if record_key == key:
                result = record_value

        return result


    def exists(self, key: str) -> bool:
        self._validate_key(key)

        result = False

        for record_key, record_value in self._iter_records():
            if record_key == key:
                result = record_value is not None

        return result

    def count(self) -> int:
        return sum(1 for _ in self.scan())

    def scan(self):
        records = {}

        for record_key, record_value in self._iter_records():
            if record_value is None:
                records.pop(record_key, None)
            else:
                records[record_key] = record_value

        yield from records.items()

    def compact(self) -> None:
        records = list(self.scan())

        temp_path = self.path.with_suffix(self.path.suffix + ".tmp")

        with temp_path.open("wb") as file:
            for key, value in records:
                file.write(encode_put(key, value))

            file.flush()
            os.fsync(file.fileno())

        os.replace(temp_path, self.path)