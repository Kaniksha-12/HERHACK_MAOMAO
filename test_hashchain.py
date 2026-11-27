from hashchain import EventLog


def test_empty_log_verifies():
    assert EventLog().verify()


def test_entries_link_in_order():
    log = EventLog()
    first = log.add({"kind": "detection", "camera": "north"})
    second = log.add({"kind": "review", "status": "confirmed"})
    assert first["prev"] == "0" * 64
    assert second["prev"] == first["hash"]
    assert log.verify()


def test_event_edit_breaks_verification():
    log = EventLog()
    log.add({"kind": "detection", "camera": "north"})
    log.entries[0]["event"]["camera"] = "south"
    assert not log.verify()


def test_reordering_breaks_verification():
    log = EventLog()
    log.add({"kind": "detection", "camera": "north"})
    log.add({"kind": "review", "status": "confirmed"})
    log.entries.reverse()
    assert not log.verify()
