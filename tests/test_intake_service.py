import pytest

from src.intake_service import (
    extract_release_marker,
    filter_handoff_rows,
    resolve_retry_budget,
)


def test_retry_budget_uses_default_when_omitted() -> None:
    assert resolve_retry_budget(None, 3) == 3


def test_retry_budget_accepts_positive_override() -> None:
    assert resolve_retry_budget(2, 3) == 2


def test_retry_budget_accepts_zero_override() -> None:
    assert resolve_retry_budget(0, 3) == 0


def test_retry_budget_rejects_negative_override() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        resolve_retry_budget(-1, 3)


def test_handoff_rows_keep_input_order() -> None:
    rows = [
        {"owner": "platform", "severity": "high", "summary": "Queue delay"},
        {"owner": "support", "severity": "low", "summary": "Copy cleanup"},
    ]

    assert filter_handoff_rows(rows) == rows


def test_handoff_rows_filter_requested_severities() -> None:
    rows = [
        {"owner": "support", "severity": "low", "summary": "Copy cleanup"},
        {"owner": "platform", "severity": "HIGH", "summary": "Queue delay"},
        {"owner": "release", "severity": "Critical", "summary": "Marker drift"},
    ]

    assert filter_handoff_rows(rows, severities={"high", "critical"}) == rows[1:]


def test_release_marker_trims_surrounding_whitespace() -> None:
    assert extract_release_marker("  20260530-rc2  ") == "20260530-rc2"


def test_release_marker_uses_last_non_empty_line_from_notes() -> None:
    note = "\nSupport pasted context here\n\n  2026.05.30-internal-202605301145  \n"

    assert extract_release_marker(note) == "2026.05.30-internal-202605301145"
