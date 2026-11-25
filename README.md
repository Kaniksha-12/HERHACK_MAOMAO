# HERHACK MAOMAO event log

A small Python prototype of a tamper-evident event log for a border-surveillance dashboard. Each event is linked to the previous record with a SHA-256 digest. Editing a saved record breaks verification.

## Setup

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

## Try it

Append a sample detection and write it to `events.jsonl`:

```bash
python demo.py
```

Verify the saved chain:

```bash
python demo.py --verify
```

Choose another log file with `python demo.py --log path/to/events.jsonl`.

## Modules

- `hashchain.py`: builds and checks an in-memory hash chain.
- `storage.py`: saves and loads JSON Lines, rejecting malformed or changed records.
- `demo.py`: adds a sample event and offers a verification command.
- `test_storage.py`: focused persistence and tamper-detection tests.

This is a prototype, not a production surveillance system. Hash chaining detects edits within the log, but by itself does not prevent deletion or replacement of the entire file, and the demo uses a fixed sample event rather than a live camera feed.
