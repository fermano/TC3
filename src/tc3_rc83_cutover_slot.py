"""RC83 cutover slot export helpers."""

ARTIFACT_SCHEMA = "rc83.cutover.v2"


def build_cutover_slot(payload, defaults=None):
    defaults = {"slot_hour": 9, **(defaults or {})}
    market = payload.get("market") or payload.get("destination") or "default"
    slot_hour = payload.get("slot_hour") or defaults["slot_hour"]
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
