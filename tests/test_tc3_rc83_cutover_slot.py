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
