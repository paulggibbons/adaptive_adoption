"""Roster load/save helpers for the community-sync tool.

A *roster* is a simple list of community members. Each record is a plain
``dict`` with the following fields:

    - ``slack_user_id``  Slack user id (e.g. ``U0123ABCD``); may be empty.
    - ``full_name``      Display/real name (e.g. ``Ada Lovelace``).
    - ``first_name``     Given name; derived from ``full_name`` when absent.
    - ``last_name``      Family name; derived from ``full_name`` when absent.
    - ``email``          Primary email address (the upsert matching key).

Rosters are persisted either as JSON (a list of objects) or CSV (one row per
member with a fixed header). This module is deliberately dependency-free so it
can be imported and unit-tested without any network or third-party packages.
"""

from __future__ import annotations

import csv
import json
from typing import Any

# Canonical field order. Used as the CSV header and to normalise records.
ROSTER_FIELDS = ["slack_user_id", "full_name", "first_name", "last_name", "email"]


def split_name(full_name: str) -> tuple[str, str]:
    """Split a free-form full name into ``(first_name, last_name)``.

    The heuristic is intentionally simple and predictable:

    - Empty / whitespace-only input yields ``("", "")``.
    - A single token is treated as the first name with no last name.
    - Two or more tokens: the first token is the first name and the remainder
      (joined by spaces) is the last name. This keeps multi-part surnames such
      as "van der Berg" intact.

    It is not meant to be linguistically perfect -- only robust and stable so
    that re-running the sync produces the same first/last split every time.
    """
    tokens = (full_name or "").split()
    if not tokens:
        return "", ""
    if len(tokens) == 1:
        return tokens[0], ""
    return tokens[0], " ".join(tokens[1:])


def normalise_record(record: dict[str, Any]) -> dict[str, str]:
    """Return a record containing exactly ``ROSTER_FIELDS`` as stripped strings.

    Missing first/last names are back-filled from ``full_name``; a missing
    ``full_name`` is reconstructed from first/last when possible. Email is
    lower-cased so that de-duplication by email is case-insensitive.
    """
    rec = {field: str(record.get(field, "") or "").strip() for field in ROSTER_FIELDS}

    if not rec["first_name"] and not rec["last_name"] and rec["full_name"]:
        rec["first_name"], rec["last_name"] = split_name(rec["full_name"])

    if not rec["full_name"]:
        rec["full_name"] = " ".join(p for p in (rec["first_name"], rec["last_name"]) if p)

    rec["email"] = rec["email"].lower()
    return rec


def load_roster(path: str) -> list[dict[str, str]]:
    """Load a roster from ``path``, inferring the format from its extension.

    ``.csv`` files are read as delimited rows; everything else is treated as
    JSON. Every record is passed through :func:`normalise_record`.
    """
    if path.lower().endswith(".csv"):
        with open(path, newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
    else:
        with open(path, encoding="utf-8") as handle:
            rows = json.load(handle)
        if not isinstance(rows, list):
            raise ValueError(f"Roster JSON at {path} must be a list of objects.")

    return [normalise_record(row) for row in rows]


def save_roster(records: list[dict[str, Any]], path: str, fmt: str = "json") -> None:
    """Persist ``records`` to ``path`` as ``json`` or ``csv``.

    Records are normalised on the way out so the saved file always carries the
    full, canonical field set regardless of what the caller supplied.
    """
    normalised = [normalise_record(rec) for rec in records]

    if fmt == "csv":
        with open(path, "w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=ROSTER_FIELDS)
            writer.writeheader()
            writer.writerows(normalised)
    elif fmt == "json":
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(normalised, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
    else:
        raise ValueError(f"Unknown roster format: {fmt!r} (expected 'json' or 'csv').")
