"""Prototype cutover alias support from before RC83 market rows."""


def _slot_hour(payload, default=9):
    if "slot_hour" in payload and payload["slot_hour"] not in (None, ""):
        return int(payload["slot_hour"])
    if "slotHour" in payload and payload["slotHour"] not in (None, ""):
        return int(payload["slotHour"])
    return default


def build_cutover_slot(payload, defaults=None):
    defaults = {"slot_hour": 9, **(defaults or {})}
    slot_hour = _slot_hour(payload, defaults["slot_hour"])
    return {
        "tenant_id": payload["tenant_id"],
        "destination": payload.get("destination") or payload.get("market") or "default",
        "batch_id": payload["batch_id"],
        "slot_hour": slot_hour,
        "window": "midnight" if slot_hour == 0 else "business",
        "source": "mainline-cutover-alias",
    }
