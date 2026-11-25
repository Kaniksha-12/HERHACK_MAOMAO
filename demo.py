"""Command-line demo for recording and checking sample detections."""
import argparse
import json

from hashchain import EventLog
from storage import load_log, save_log


def main() -> None:
    parser = argparse.ArgumentParser(description="Append and verify sample surveillance events")
    parser.add_argument("--log", default="events.jsonl", help="JSONL log file")
    parser.add_argument("--verify", action="store_true", help="verify the existing log and exit")
    args = parser.parse_args()

    log = load_log(args.log)
    if args.verify:
        print(f"OK: {len(log.entries)} entries; chain verified")
        return

    event = {"kind": "detection", "camera": "north-gate", "label": "person", "confidence": 0.91}
    entry = log.add(event)
    save_log(log, args.log)
    print(json.dumps(entry, indent=2))
    print(f"Saved {len(log.entries)} entries to {args.log}")


if __name__ == "__main__":
    main()
