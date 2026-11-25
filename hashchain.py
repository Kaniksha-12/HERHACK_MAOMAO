import hashlib, json, time


class EventLog:
    """Append-only log where each entry stores the hash of the previous one."""

    def __init__(self):
        self.entries = []

    def add(self, event: dict) -> dict:
        prev = self.entries[-1]["hash"] if self.entries else "0" * 64
        body = {"ts": time.time(), "event": event, "prev": prev}
        digest = hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()
        entry = {**body, "hash": digest}
        self.entries.append(entry)
        return entry

    def verify(self) -> bool:
        prev = "0" * 64
        for e in self.entries:
            body = {k: e[k] for k in ("ts", "event", "prev")}
            h = hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()
            if e["prev"] != prev or e["hash"] != h:
                return False
            prev = e["hash"]
        return True
