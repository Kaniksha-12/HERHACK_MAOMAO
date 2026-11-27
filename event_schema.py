"""Small, explicit validation helpers for prototype detection events."""

REQUIRED_FIELDS = {"kind", "camera", "label", "confidence"}


def validate_detection(event: dict) -> None:
    """Raise ValueError unless event has the demo's expected detection shape."""
    missing = REQUIRED_FIELDS - event.keys()
    if missing:
        raise ValueError(f"missing detection fields: {', '.join(sorted(missing))}")
    if event["kind"] != "detection":
        raise ValueError("kind must be 'detection'")
    if not isinstance(event["camera"], str) or not event["camera"].strip():
        raise ValueError("camera must be a non-empty string")
    if not isinstance(event["label"], str) or not event["label"].strip():
        raise ValueError("label must be a non-empty string")
    confidence = event["confidence"]
    if isinstance(confidence, bool) or not isinstance(confidence, (int, float)):
        raise ValueError("confidence must be a number")
    if not 0 <= confidence <= 1:
        raise ValueError("confidence must be between 0 and 1")
