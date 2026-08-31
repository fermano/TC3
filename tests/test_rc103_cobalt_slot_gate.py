from src.rc103_cobalt_slot_gate import build_slot


def test_partner_zero_start_alias_opens_slot():
    slot = build_slot(
        {"tenant": "cobalt", "slot_id": "slot-319", "startAfterSeconds": "0"},
        {"route": "cutover", "default_start_after_seconds": 600, "cutover_key": "co-a"},
    )

    assert slot["status"] == "open"
    assert slot["start_after_seconds"] == 0
