from src.storage.engine import StorageEngine


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