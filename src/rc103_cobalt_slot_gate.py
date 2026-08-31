DEFAULT_START_AFTER_SECONDS = 600


def _coerce_seconds(value, default):
    if value:
        return int(value)
    return default


def build_slot(payload, route_defaults):
    start_after_seconds = _coerce_seconds(
        payload.get("start_after_seconds"),
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
    }
