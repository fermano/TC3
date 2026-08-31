import pytest

from src.tc3_rc83_cutover_slot import ARTIFACT_SCHEMA, build_cutover_slot


def test_cutover_slot_uses_market_shape():
    row = build_cutover_slot({
        "tenant_id": "cobalt",
        "market": "br-south",
        "batch_id": "batch-283",
        "slot_hour": 6,
    })
    assert row["market"] == "br-south"
    assert row["slot_hour"] == 6
    assert row["source"] == "rc83-market-cutover"
    assert row["artifact_schema"] == ARTIFACT_SCHEMA
    assert row["cutover_key"] == "br-south:batch-283:business"


def test_missing_slot_uses_business_default():
    row = build_cutover_slot({"tenant_id": "cobalt", "market": "br-east", "batch_id": "batch-117"})
    assert row["slot_hour"] == 9
    assert row["window"] == "business"


def test_midnight_zero_is_preserved_in_snake_case_fixture():
    row = build_cutover_slot({
        "tenant_id": "cobalt",
        "market": "br-south",
        "batch_id": "batch-283",
        "slot_hour": 0,
    })
    assert row["slot_hour"] == 0
    assert row["window"] == "midnight"


def test_release_artifact_camel_case_midnight_retains_current_schema():
    row = build_cutover_slot({
        "tenant_id": "cobalt",
        "market": "br-south",
        "batch_id": "batch-283",
        "slotHour": "0",
    })
    assert row == {
        "tenant_id": "cobalt",
        "market": "br-south",
        "batch_id": "batch-283",
        "slot_hour": 0,
        "window": "midnight",
        "source": "rc83-market-cutover",
        "artifact_schema": "rc83.cutover.v2",
        "cutover_key": "br-south:batch-283:midnight",
    }


@pytest.mark.parametrize("slots,defaults,expected", [
    ({"slot_hour": 0}, None, 0),
    ({"slot_hour": "0"}, None, 0),
    ({"slotHour": 0}, None, 0),
    ({"slotHour": "0"}, None, 0),
    ({"slot_hour": 0, "slotHour": 6}, None, 0),
    ({"slot_hour": 6, "slotHour": "0"}, None, 6),
    ({"slot_hour": "0", "slotHour": "invalid"}, None, 0),
    ({"slot_hour": None, "slotHour": "0"}, None, 0),
    ({"slot_hour": "", "slotHour": "0"}, None, 0),
    ({"slotHour": "6"}, None, 6),
    ({}, None, 9),
    ({"slot_hour": None}, None, 9),
    ({"slot_hour": ""}, None, 9),
    ({"slotHour": None}, None, 9),
    ({"slotHour": ""}, None, 9),
    ({"slot_hour": None, "slotHour": ""}, None, 9),
    ({"slot_hour": "", "slotHour": None}, {"slot_hour": 4}, 4),
    ({}, {"slot_hour": 0}, 0),
    ({}, {"slot_hour": "0"}, 0),
    ({"slotHour": ""}, {"slot_hour": "6"}, 6),
    ({"slotHour": "0"}, {"slot_hour": 6}, 0),
    ({"slot_hour": 6}, {"slot_hour": 0}, 6),
])
def test_slot_precedence_and_defaults(slots, defaults, expected):
    row = build_cutover_slot({
        "tenant_id": "cobalt",
        "market": "br-south",
        "batch_id": "batch-283",
        **slots,
    }, defaults)
    window = "midnight" if expected == 0 else "business"
    assert row["slot_hour"] == expected
    assert type(row["slot_hour"]) is int
    assert row["window"] == window
    assert row["cutover_key"] == f"br-south:batch-283:{window}"


@pytest.mark.parametrize("location,expected", [
    ({"market": "br-south", "destination": "legacy"}, "br-south"),
    ({"destination": "br-south"}, "br-south"),
    ({"market": "", "destination": "br-south"}, "br-south"),
    ({}, "default"),
])
def test_alias_keeps_release_market_selection(location, expected):
    row = build_cutover_slot({
        "tenant_id": "cobalt", "batch_id": "batch-283", "slotHour": "0",
        **location,
    })
    assert row["market"] == expected
    assert "destination" not in row
    assert row["cutover_key"] == f"{expected}:batch-283:midnight"


@pytest.mark.parametrize("slots", [
    {"slot_hour": "invalid", "slotHour": "0"},
    {"slot_hour": None, "slotHour": "invalid"},
])
def test_invalid_selected_slot_is_not_silently_replaced(slots):
    with pytest.raises(ValueError):
        build_cutover_slot({
            "tenant_id": "cobalt", "batch_id": "batch-283", **slots,
        })
