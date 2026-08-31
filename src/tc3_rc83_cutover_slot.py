"""RC83 cutover slot export helpers."""


def _slot(payload, name, default):
    if name in payload and payload[name] not in (None, ""):
        return payload[name]
    return default


def build_cutover_slot(payload, defaults=None):
    defaults = {"slot_hour": 9, **(defaults or {})}
    market = payload.get("market") or payload.get("destination") or "default"
    slot_hour = _slot(payload, "slot_hour", defaults["slot_hour"])
    slot_hour = int(slot_hour)
    return {
        "tenant_id": payload["tenant_id"],
        "market": market,
        "batch_id": payload["batch_id"],
        "slot_hour": slot_hour,
        "window": "midnight" if slot_hour == 0 else "business",
        "source": "rc83-market-cutover",
    }
