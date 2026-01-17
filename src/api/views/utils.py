from __future__ import annotations

from datetime import date


def parse_date(value: str | None) -> date | None:
    if value is None:
        return None

    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        return None
