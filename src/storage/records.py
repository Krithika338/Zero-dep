import hashlib
import struct


MAGIC = b"ZDEP"
VERSION = 1

TYPE_PUT = 1
TYPE_DELETE = 2

HEADER_FORMAT = ">4sBBI"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

CHECKSUM_SIZE = 32

MAX_PAYLOAD_SIZE = 16 * 1024 * 1024


def calculate_checksum(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def encode_put(key: str, value: str) -> bytes:
    if not isinstance(key, str):
        raise TypeError("Key must be a string")

    if not isinstance(value, str):
        raise TypeError("Value must be a string")

    if not key:
        raise ValueError("Key cannot be empty")

    key_bytes = key.encode("utf-8")
    value_bytes = value.encode("utf-8")

    payload = (
        struct.pack(">I", len(key_bytes))
        + key_bytes
        + struct.pack(">I", len(value_bytes))
        + value_bytes
    )

    return encode_record(TYPE_PUT, payload)


def encode_delete(key: str) -> bytes:
    if not isinstance(key, str):
        raise TypeError("Key must be a string")

    if not key:
        raise ValueError("Key cannot be empty")

    key_bytes = key.encode("utf-8")

    payload = struct.pack(">I", len(key_bytes)) + key_bytes

    return encode_record(TYPE_DELETE, payload)



def encode_record(record_type: int, payload: bytes) -> bytes:
    if len(payload) > MAX_PAYLOAD_SIZE:
        raise ValueError("Payload exceeds maximum allowed size")

    header = struct.pack(
        HEADER_FORMAT,
        MAGIC,
        VERSION,
        record_type,
        len(payload),
    )

    checksum = calculate_checksum(header + payload)

    return header + payload + checksum

def decode_record(data: bytes):
    if len(data) < HEADER_SIZE:
        raise ValueError("Incomplete record header")

    header = data[:HEADER_SIZE]

    magic, version, record_type, payload_size = struct.unpack(
        HEADER_FORMAT, header
    )

    if magic != MAGIC:
        raise ValueError("Invalid magic")

    if version != VERSION:
        raise ValueError("Unsupported version")

    if record_type not in (TYPE_PUT, TYPE_DELETE):
        raise ValueError("Unknown record type")

    if payload_size > MAX_PAYLOAD_SIZE:
        raise ValueError("Payload exceeds maximum allowed size")

    payload_start = HEADER_SIZE
    payload_end = payload_start + payload_size
    record_end = payload_end + CHECKSUM_SIZE

    if len(data) < record_end:
        raise ValueError("Incomplete record")

    payload = data[payload_start:payload_end]

    checksum = data[payload_end:record_end]

    expected_checksum = calculate_checksum(header + payload)

    if checksum != expected_checksum:
        raise ValueError("Checksum mismatch")

    return record_type, payload

def decode_payload(record_type: int, payload: bytes):
    if len(payload) < 4:
        raise ValueError("Incomplete key length")

    key_length = struct.unpack(">I", payload[:4])[0]

    key_start = 4
    key_end = key_start + key_length

    if key_end > len(payload):
        raise ValueError("Incomplete key")

    key = payload[key_start:key_end].decode("utf-8")

    if not key:
        raise ValueError("Key cannot be empty")

    if record_type == TYPE_PUT:
        if len(payload) < key_end + 4:
            raise ValueError("Incomplete value length")

        value_length = struct.unpack(
            ">I",
            payload[key_end:key_end + 4]
        )[0]

        value_start = key_end + 4
        value_end = value_start + value_length

        if value_end > len(payload):
            raise ValueError("Incomplete value")

        value = payload[value_start:value_end].decode("utf-8")

        if value_end != len(payload):
            raise ValueError("Unexpected trailing data")

        return key, value

    if record_type == TYPE_DELETE:
        if key_end != len(payload):
            raise ValueError("Unexpected trailing data")

        return key, None

    raise ValueError("Unknown record type")