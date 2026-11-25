"""Verify the hash-chain logic without requiring a test framework."""
from hashchain import EventLog


def run() -> None:
    log = EventLog()
    assert log.verify(), "empty chain should be valid"
    first = log.add({"kind": "detection", "camera": "north"})
    second = log.add({"kind": "review", "status": "confirmed"})
    assert first["prev"] == "0" * 64
    assert second["prev"] == first["hash"]
    assert log.verify(), "untouched chain should verify"

    log.entries[0]["event"]["camera"] = "altered"
    assert not log.verify(), "edited event must fail verification"
    print("OK: links connect and edited event is detected")


if __name__ == "__main__":
    run()
