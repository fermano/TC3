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
    if requested is not None and requested < 0:
        raise ValueError("retry budget must be non-negative")
    return default if requested is None else requested


def filter_handoff_rows(
    rows: Iterable[HandoffRow],
    *,
    severities: Iterable[str] | None = None,
    owners: Iterable[str] | None = None,
) -> list[HandoffRow]:
    """Return copied handoff rows limited to requested severities and owners."""
    row_list = list(rows)
    if severities is None and owners is None:
        return row_list

    allowed_severities = (
        None
        if severities is None
        else {severity.strip().lower() for severity in severities}
    )
    allowed_owners = (
        None if owners is None else {owner.strip().lower() for owner in owners}
    )
    return [
        row
        for row in row_list
        if (
            (allowed_severities is None or row["severity"].strip().lower() in allowed_severities)
            and (
                allowed_owners is None
                or row["owner"].strip().lower() in allowed_owners
            )
        )
    ]


def extract_release_marker(note: str) -> str:
    """Return the final non-empty release marker line from copied intake notes."""
    lines = [line.strip() for line in note.splitlines() if line.strip()]
    if not lines:
        return ""

    marker = lines[-1]
    prefix, separator, value = marker.partition(":")
    if separator and prefix.strip().lower() == "release":
        return value.strip()
    return marker
