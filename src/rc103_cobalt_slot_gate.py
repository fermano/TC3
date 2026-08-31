DEFAULT_START_AFTER_SECONDS = 600


def _pick_start_after(payload):
    # Preserve the partner normalizer's precedence, including empty values.
    if "startAfterSeconds" in payload:
        return payload["startAfterSeconds"]
    return payload.get("start_after_seconds")


def _coerce_seconds(value, default):
    if value is None or value == "":
        return default
    return int(value)


def build_slot(payload, route_defaults):
    start_after_seconds = _coerce_seconds(
        _pick_start_after(payload),
        route_defaults.get("default_start_after_seconds", DEFAULT_START_AFTER_SECONDS),
    )
    return {
        "tenant": payload["tenant"],
        "slot_id": payload["slot_id"],
        "route": route_defaults["route"],
        "status": "held" if start_after_seconds else "open",
        "start_after_seconds": start_after_seconds,
        "manifest_bucket": route_defaults.get("manifest_bucket", "rc103"),
        "cutover_key": route_defaults.get("cutover_key", "unset"),
        "release_channel": route_defaults.get("release_channel", "candidate"),
    }
