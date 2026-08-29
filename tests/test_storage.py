
from src.storage.engine import StorageEngine
from src.storage.records import (
    TYPE_DELETE,
    TYPE_PUT,
    decode_payload,
    decode_record,
    encode_delete,
    encode_put,
)

def test_put_and_get(tmp_path):
    db = StorageEngine(str(tmp_path / "test.db"))

    db.put("name", "Moonpie")

    assert db.get("name") == "Moonpie"
def test_delete(tmp_path):
    db = StorageEngine(str(tmp_path / "test.db"))

    db.put("name", "Moonpie")
    db.delete("name")

    assert db.get("name") is None
def test_update(tmp_path):
    db = StorageEngine(str(tmp_path / "test.db"))

    db.put("name", "Moonpie")
    db.put("name", "Krithika")

    assert db.get("name") == "Krithika"
def test_multiple_keys(tmp_path):
    db = StorageEngine(str(tmp_path / "test.db"))

    db.put("name", "Moonpie")
    db.put("course", "Python")

    assert db.get("name") == "Moonpie"
    assert db.get("course") == "Python"
def test_missing_key(tmp_path):
    db = StorageEngine(str(tmp_path / "test.db"))

    assert db.get("missing") is None

def test_persistence(tmp_path):
    path = str(tmp_path / "test.db")

    db = StorageEngine(path)
    db.put("name", "Moonpie")

    db = StorageEngine(path)

    assert db.get("name") == "Moonpie"
def test_corrupted_record(tmp_path):
    path = str(tmp_path / "test.db")

    db = StorageEngine(path)
    db.put("name", "Moonpie")

    with open(path, "r+b") as file:
        data = bytearray(file.read())
        data[-1] ^= 1
        file.seek(0)
        file.write(data)

    try:
        db.get("name")
        assert False, "Expected checksum error"
    except ValueError as error:
        assert str(error) == "Checksum mismatch"
def test_empty_key_rejected(tmp_path):
    db = StorageEngine(str(tmp_path / "test.db"))

    try:
        db.put("", "value")
        assert False, "Expected empty key to be rejected"
    except ValueError as error:
        assert str(error) == "Key cannot be empty"


def test_non_string_key_rejected(tmp_path):
    db = StorageEngine(str(tmp_path / "test.db"))

    try:
        db.put(123, "value")
        assert False, "Expected non-string key to be rejected"
    except TypeError as error:
        assert str(error) == "Key must be a string"
def test_incomplete_final_record_is_ignored(tmp_path):
    path = str(tmp_path / "test.db")

    db = StorageEngine(path)
    db.put("name", "Moonpie")

    with open(path, "ab") as file:
        file.write(b"ZDEP")

    assert db.get("name") == "Moonpie"

def test_scan(tmp_path):
    db = StorageEngine(str(tmp_path / "test.db"))

    db.put("name", "Moonpie")
    db.put("course", "Python")

    records = list(db.scan())

    assert ("name", "Moonpie") in records
    assert ("course", "Python") in records

def test_scan_returns_latest_records(tmp_path):
    db = StorageEngine(str(tmp_path / "test.db"))

    db.put("name", "Moonpie")
    db.put("name", "Krithika")
    db.put("course", "Python")
    db.delete("course")

    records = list(db.scan())

    assert records == [("name", "Krithika")]
def test_scan_persistence(tmp_path):
    path = str(tmp_path / "test.db")

    db = StorageEngine(path)
    db.put("name", "Moonpie")
    db.put("course", "Python")

    db = StorageEngine(path)

    assert list(db.scan()) == [
        ("name", "Moonpie"),
        ("course", "Python"),
    ]
def test_search_engine_interface(tmp_path):
    db = StorageEngine(str(tmp_path / "test.db"))

    db.put("doc1", "Python programming language")
    db.put("doc2", "Storage engine implementation")

    assert db.get("doc1") == "Python programming language"

    documents = dict(db.scan())

    assert documents["doc1"] == "Python programming language"
    assert documents["doc2"] == "Storage engine implementation"

def test_decode_payload_rejects_incomplete_key_length():
    try:
        decode_payload(TYPE_PUT, b"\x00\x00")
        assert False, "Expected incomplete key length error"
    except ValueError as error:
        assert str(error) == "Incomplete key length"


def test_decode_payload_rejects_incomplete_key():
    payload = b"\x00\x00\x00\x05abc"

    try:
        decode_payload(TYPE_PUT, payload)
        assert False, "Expected incomplete key error"
    except ValueError as error:
        assert str(error) == "Incomplete key"


def test_decode_payload_rejects_incomplete_value_length():
    payload = (
        b"\x00\x00\x00\x03"
        + b"abc"
        + b"\x00\x00"
    )

    try:
        decode_payload(TYPE_PUT, payload)
        assert False, "Expected incomplete value length error"
    except ValueError as error:
        assert str(error) == "Incomplete value length"


def test_decode_payload_rejects_incomplete_value():
    payload = (
        b"\x00\x00\x00\x03"
        + b"abc"
        + b"\x00\x00\x00\x05"
        + b"xy"
    )

    try:
        decode_payload(TYPE_PUT, payload)
        assert False, "Expected incomplete value error"
    except ValueError as error:
        assert str(error) == "Incomplete value"


def test_decode_payload_rejects_unknown_record_type():
    payload = b"\x00\x00\x00\x03abc"

    try:
        decode_payload(99, payload)
        assert False, "Expected unknown record type error"
    except ValueError as error:
        assert str(error) == "Unknown record type"
def test_encode_put_round_trip():
    record = encode_put("name", "Moonpie")

    record_type, payload = decode_record(record)
    key, value = decode_payload(record_type, payload)

    assert record_type == TYPE_PUT
    assert key == "name"
    assert value == "Moonpie"


def test_encode_delete_round_trip():
    record = encode_delete("name")

    record_type, payload = decode_record(record)
    key, value = decode_payload(record_type, payload)

    assert record_type == TYPE_DELETE
    assert key == "name"
    assert value is None


def test_unicode_round_trip():
    record = encode_put("名前", "こんにちは")

    record_type, payload = decode_record(record)
    key, value = decode_payload(record_type, payload)

    assert key == "名前"
    assert value == "こんにちは"


def test_decode_record_rejects_truncated_record():
    record = encode_put("name", "Moonpie")

    truncated = record[:-1]

    try:
        decode_record(truncated)
        assert False, "Expected incomplete record error"
    except ValueError as error:
        assert str(error) == "Incomplete record"

def test_decode_record_rejects_unknown_record_type():
    record = encode_put("name", "Moonpie")

    header = bytearray(record[:10])

    header[5] = 99

    corrupted_record = bytes(header) + record[10:]

    try:
        decode_record(corrupted_record)
        assert False, "Expected unknown record type error"
    except ValueError as error:
        assert str(error) == "Unknown record type"