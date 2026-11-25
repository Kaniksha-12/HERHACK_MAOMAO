"""JSONL persistence helpers for the MAOMAO event log."""
import json
from pathlib import Path

from hashchain import EventLog


def save_log(log: EventLog, path: str | Path) -> None:
    """Write the current entries as UTF-8 JSON Lines."""
    target = Path(path)
    with target.open("w", encoding="utf-8") as stream:
        for entry in log.entries:
            stream.write(json.dumps(entry, sort_keys=True) + "\n")


def load_log(path: str | Path) -> EventLog:
    """Load entries and reject a file whose chain does not verify."""
    log = EventLog()
    target = Path(path)
    if not target.exists():
        return log
    with target.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
                body = {key: entry[key] for key in ("ts", "event", "prev")}
                import hashlib
                digest = hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()
                expected_prev = log.entries[-1]["hash"] if log.entries else "0" * 64
                if entry.get("prev") != expected_prev or entry.get("hash") != digest:
                    raise ValueError("hash chain mismatch")
                log.entries.append(entry)
            except (ValueError, KeyError, json.JSONDecodeError) as exc:
                raise ValueError(f"invalid log at line {line_number}: {exc}") from exc
    return log
