import pytest

from src.rc103_cobalt_slot_gate import build_slot


def test_absent_start_delay_inherits_route_default():
    slot = build_slot(
        {"tenant": "cobalt", "slot_id": "slot-319"},
        {"route": "cutover", "default_start_after_seconds": 600, "manifest_bucket": "candidate", "cutover_key": "co-a", "release_channel": "rc103-final"},
    )

    assert slot["status"] == "held"
    assert slot["start_after_seconds"] == 600
    assert slot["manifest_bucket"] == "candidate"
    assert slot["cutover_key"] == "co-a"
    assert slot["release_channel"] == "rc103-final"


def test_positive_snake_start_delay_is_applied():
    slot = build_slot(
        {"tenant": "cobalt", "slot_id": "slot-320", "start_after_seconds": "45"},
        {"route": "cutover", "default_start_after_seconds": 600},
    )

    assert slot["status"] == "held"
    assert slot["start_after_seconds"] == 45
    assert slot["release_channel"] == "candidate"


def test_snake_zero_start_opens_slot():
    slot = build_slot(
        {"tenant": "cobalt", "slot_id": "slot-321", "start_after_seconds": "0"},
        {"route": "cutover", "default_start_after_seconds": 600, "cutover_key": "co-a"},
    )

    assert slot["status"] == "open"
    assert slot["start_after_seconds"] == 0
    assert slot["cutover_key"] == "co-a"


@pytest.mark.parametrize("field", ["startAfterSeconds", "start_after_seconds"])
@pytest.mark.parametrize(
    "value, seconds, status",
    [(0, 0, "open"), ("0", 0, "open"), (45, 45, "held"), ("45", 45, "held")],
)
def test_explicit_start_delay_preserves_release_contract(field, value, seconds, status):
    payload = {"tenant": "cobalt", "slot_id": "slot-319", field: value}
    defaults = {
        "route": "cutover",
        "default_start_after_seconds": 600,
        "manifest_bucket": "candidate",
        "cutover_key": "co-a",
        "release_channel": "rc103-final",
    }
    original_payload, original_defaults = payload.copy(), defaults.copy()

    assert build_slot(payload, defaults) == {
        "tenant": "cobalt",
        "slot_id": "slot-319",
        "route": "cutover",
        "status": status,
        "start_after_seconds": seconds,
        "manifest_bucket": "candidate",
        "cutover_key": "co-a",
        "release_channel": "rc103-final",
    }
    assert payload == original_payload
    assert defaults == original_defaults


@pytest.mark.parametrize(
    "fields",
    [{}, {"startAfterSeconds": None}, {"startAfterSeconds": ""},
     {"start_after_seconds": None}, {"start_after_seconds": ""}],
)
@pytest.mark.parametrize(
    "configured_default, seconds",
    [({}, 600), ({"default_start_after_seconds": 120}, 120),
     ({"default_start_after_seconds": 0}, 0)],
)
def test_missing_delay_inherits_defaults(fields, configured_default, seconds):
    slot = build_slot(
        {"tenant": "cobalt", "slot_id": "slot-319", **fields},
        {"route": "cutover", **configured_default},
    )

    assert slot == {
        "tenant": "cobalt",
        "slot_id": "slot-319",
        "route": "cutover",
        "status": "held" if seconds else "open",
        "start_after_seconds": seconds,
        "manifest_bucket": "rc103",
        "cutover_key": "unset",
        "release_channel": "candidate",
    }


@pytest.mark.parametrize(
    "partner, snake, seconds",
    [("0", "45", 0), (0, "45", 0), ("45", "0", 45),
     (None, "0", 600), ("", "0", 600)],
)
def test_partner_field_presence_takes_precedence(partner, snake, seconds):
    slot = build_slot(
        {"tenant": "cobalt", "slot_id": "slot-319",
         "startAfterSeconds": partner, "start_after_seconds": snake},
        {"route": "cutover"},
    )

    assert slot["start_after_seconds"] == seconds
    assert slot["status"] == ("held" if seconds else "open")


@pytest.mark.parametrize(
    "fields",
    [{"startAfterSeconds": "invalid"}, {"start_after_seconds": "invalid"},
     {"startAfterSeconds": "invalid", "start_after_seconds": "0"}],
)
def test_invalid_selected_delay_is_not_silently_defaulted(fields):
    with pytest.raises(ValueError):
        build_slot({"tenant": "cobalt", "slot_id": "slot-319", **fields}, {"route": "cutover"})
