"""Helpers used by support intake and release coordination paths."""

from __future__ import annotations

from collections.abc import Iterable
from typing import TypedDict


class HandoffRow(TypedDict):
    owner: str
    severity: str
    summary: str


def resolve_retry_budget(requested: int | None, default: int) -> int:
    """Return the configured retry count unless a request overrides it."""
    return default if requested is None else requested


def filter_handoff_rows(
    rows: Iterable[HandoffRow],
    *,
    severities: Iterable[str] | None = None,
) -> list[HandoffRow]:
    """Return copied handoff rows, optionally limited to requested severities."""
    row_list = list(rows)
    if severities is None:
        return row_list

    allowed_severities = {severity.strip().lower() for severity in severities}
    return [
        row
        for row in row_list
        if row["severity"].strip().lower() in allowed_severities
    ]


def extract_release_marker(note: str) -> str:
    """Return the final non-empty release marker line from copied intake notes."""
    lines = [line.strip() for line in note.splitlines() if line.strip()]
    if not lines:
        return ""
    return lines[-1]
