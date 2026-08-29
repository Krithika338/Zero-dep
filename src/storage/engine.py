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

    def put(self, key: str, value: str) -> None:
        record = encode_put(key, value)

        with self.path.open("ab") as file:
            file.write(record)

    def delete(self, key: str) -> None:
        record = encode_delete(key)

        with self.path.open("ab") as file:
            file.write(record)

            
    def get(self, key: str):
        if not self.path.exists():
            return None

        data = self.path.read_bytes()

        if not data:
            return None

        position = 0
        result = None

        while position < len(data):
            header = data[position:position + HEADER_SIZE]

            _, _, _, payload_size = __import__("struct").unpack(
                ">4sBBI", header
            )

            record_size = HEADER_SIZE + payload_size + CHECKSUM_SIZE
            record_data = data[position:position + record_size]

            record_type, payload = decode_record(record_data)
            record_key, record_value = decode_payload(record_type, payload)

            if record_key == key:
                result = record_value

            position += record_size

        return result