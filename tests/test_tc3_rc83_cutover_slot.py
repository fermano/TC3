from src.tc3_rc83_cutover_slot import build_cutover_slot


def test_camel_slot_zero_maps_to_midnight():
    row = build_cutover_slot({
        "tenant_id": "cobalt",
        "destination": "br-south",
        "batch_id": "batch-283",
        "slotHour": "0",
    })
    assert row["slot_hour"] == 0
    assert row["window"] == "midnight"
