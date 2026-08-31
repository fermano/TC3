DEFAULT_START_AFTER_SECONDS = 600


def _pick_start_after(payload):
    if "startAfterSeconds" in payload:
        return payload["startAfterSeconds"]
    return payload.get("start_after_seconds")


def _coerce_seconds(value, default):
    if value is None or value == "":
        return default
    return int(value)


def build_slot(payload, route_defaults):
    start_after_seconds = _coerce_seconds(_pick_start_after(payload), route_defaults.get("default_start_after_seconds", DEFAULT_START_AFTER_SECONDS))
    return {
        "tenant": payload["tenant"],
        "slot_id": payload["slot_id"],
        "route": route_defaults["route"],
        "status": "held" if start_after_seconds else "open",
        "start_after_seconds": start_after_seconds,
    }
