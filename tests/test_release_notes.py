import pytest

from src.release_notes import (
    OperationSignal,
    build_release_marker,
    group_signal_owners,
    highest_severity,
)


def test_blank_release_marker_channel_uses_internal_default():
    assert build_release_marker("2026.06.24", "") == "2026.06.24-internal"
    assert build_release_marker("2026.06.24", "   ") == "2026.06.24-internal"


def test_generator_backed_severity_uses_highest_signal():
    signals = (
        OperationSignal("platform", severity)
        for severity in ("low", "critical", "medium")
    )

    assert highest_severity(signals) == "critical"


def test_highest_severity_normalizes_support_values():
    signals = (
        OperationSignal("platform", severity)
        for severity in (" low ", "HIGH", " Critical ")
    )

    assert highest_severity(signals) == "critical"


def test_highest_severity_rejects_unknown_values():
    signals = (OperationSignal("docs", "notice"),)

    with pytest.raises(ValueError, match="severity must be"):
        highest_severity(signals)


def test_blank_owner_uses_configured_fallback():
    signals = (OperationSignal(owner, "high") for owner in ("", "platform"))

    assert group_signal_owners(signals, "engineering-ops") == (
        "engineering-ops",
        "platform",
    )


def test_release_marker_channel_is_normalized_to_slug():
    assert build_release_marker("1.2.0", " Public Beta ") == "1.2.0-public-beta"
    assert build_release_marker("1.2.0", "HOTFIX/QA") == "1.2.0-hotfix-qa"
