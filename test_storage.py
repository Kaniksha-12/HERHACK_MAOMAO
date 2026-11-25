from pathlib import Path
from tempfile import TemporaryDirectory

from hashchain import EventLog
from storage import load_log, save_log


def test_jsonl_round_trip_preserves_entries():
    with TemporaryDirectory() as directory:
        path = Path(directory) / "events.jsonl"
        original = EventLog()
        original.add({"kind": "detection", "zone": "north"})
        original.add({"kind": "review", "status": "confirmed"})
        save_log(original, path)
        restored = load_log(path)
        assert restored.entries == original.entries
        assert restored.verify()


def test_loading_missing_file_returns_empty_log():
    with TemporaryDirectory() as directory:
        log = load_log(Path(directory) / "missing.jsonl")
        assert log.entries == []
        assert log.verify()


def test_tampered_record_is_rejected():
    with TemporaryDirectory() as directory:
        path = Path(directory) / "events.jsonl"
        log = EventLog()
        log.add({"kind": "detection", "zone": "north"})
        save_log(log, path)
        text = path.read_text(encoding="utf-8").replace("north", "south")
        path.write_text(text, encoding="utf-8")
        try:
            load_log(path)
        except ValueError as exc:
            assert "invalid log at line 1" in str(exc)
        else:
            raise AssertionError("tampered record was accepted")
