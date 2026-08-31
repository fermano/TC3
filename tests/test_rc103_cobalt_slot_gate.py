from src.rc103_cobalt_slot_gate import build_slot


def test_absent_start_delay_inherits_route_default():
    slot = build_slot(
        {"tenant": "cobalt", "slot_id": "slot-319"},
        {"route": "cutover", "default_start_after_seconds": 600, "manifest_bucket": "candidate", "cutover_key": "co-a"},
    )

    assert slot["status"] == "held"
    assert slot["start_after_seconds"] == 600
    assert slot["manifest_bucket"] == "candidate"
    assert slot["cutover_key"] == "co-a"


def test_positive_snake_start_delay_is_applied():
    slot = build_slot(
        {"tenant": "cobalt", "slot_id": "slot-320", "start_after_seconds": "45"},
        {"route": "cutover", "default_start_after_seconds": 600},
    )

    assert slot["status"] == "held"
    assert slot["start_after_seconds"] == 45
