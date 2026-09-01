def resolve_partner_value(payload, default=600):
    value = payload.get("start_after_seconds")
    if value is None:
        value = payload.get("startAfterSeconds")
    return default if value in (None, "") else value
