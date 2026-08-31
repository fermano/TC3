"""RC83 cutover slot export helpers."""

ARTIFACT_SCHEMA = "rc83.cutover.v2"


def _slot_hour(payload, default):
    """Prefer the canonical slot, then its replay alias; keep explicit zero."""
    for name in ("slot_hour", "slotHour"):
        if name in payload and payload[name] not in (None, ""):
            return payload[name]
    return default


def build_cutover_slot(payload, defaults=None):
    defaults = {"slot_hour": 9, **(defaults or {})}
    market = payload.get("market") or payload.get("destination") or "default"
    slot_hour = _slot_hour(payload, defaults["slot_hour"])
    slot_hour = int(slot_hour)
    window = "midnight" if slot_hour == 0 else "business"
    return {
        "tenant_id": payload["tenant_id"],
        "market": market,
        "batch_id": payload["batch_id"],
        "slot_hour": slot_hour,
        "window": window,
        "source": "rc83-market-cutover",
        "artifact_schema": ARTIFACT_SCHEMA,
        "cutover_key": f"{market}:{payload['batch_id']}:{window}",
    }
