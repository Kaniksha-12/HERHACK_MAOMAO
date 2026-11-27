import pytest

from event_schema import validate_detection


def valid_event():
    return {"kind": "detection", "camera": "north-gate", "label": "person", "confidence": 0.91}


def test_valid_detection_is_accepted():
    assert validate_detection(valid_event()) is None


def test_missing_required_field_is_rejected():
    event = valid_event()
    del event["camera"]
    with pytest.raises(ValueError, match="missing detection fields"):
        validate_detection(event)


@pytest.mark.parametrize("confidence", [-0.1, 1.1, True, "0.9"])
def test_invalid_confidence_is_rejected(confidence):
    event = valid_event()
    event["confidence"] = confidence
    with pytest.raises(ValueError, match="confidence"):
        validate_detection(event)


def test_empty_label_is_rejected():
    event = valid_event()
    event["label"] = "  "
    with pytest.raises(ValueError, match="label"):
        validate_detection(event)
