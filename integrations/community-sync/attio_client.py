"""Thin Attio REST API (v2) client used by the community-sync tool.

Base URL ``https://api.attio.com``, Bearer authentication with an API key from
the ``ATTIO_API_KEY`` environment variable. Only the operations the sync needs
are implemented:

    - ``assert_person``    upsert a People record, matching on email
    - ``find_list``        locate a People list by name
    - ``create_list``      create a People list
    - ``list_has_record``  test whether a record is already a list entry
    - ``add_to_list``      add a record to a list

Every non-2xx response raises :class:`AttioError` carrying Attio's response
body, so failures are legible.

Docs confirmed 2026-11-18:
    Upsert a record  PUT  /v2/objects/{object}/records?matching_attribute=...
                     https://docs.attio.com/rest-api/endpoint-reference/records/upsert-a-record
    Lists            GET/POST /v2/lists
                     https://docs.attio.com/rest-api/endpoint-reference/lists/create-a-list
    Create entry     POST /v2/lists/{list}/entries
    Query entries    POST /v2/lists/{list}/entries/query
                     https://docs.attio.com/rest-api/endpoint-reference/entries/list-entries

Personal-name values are written as an object with ``first_name``,
``last_name`` and ``full_name``. ``email_addresses`` is a multiselect attribute
and is written as a list of strings.
"""

from __future__ import annotations

import re
from typing import Any

import requests

ATTIO_API_BASE = "https://api.attio.com"


class AttioError(RuntimeError):
    """Raised when the Attio API returns a non-2xx response."""


def slugify(name: str) -> str:
    """Convert a human list name to a snake_case ``api_slug``.

    Example: ``"Adaptive Adoption Community (Slack)"`` ->
    ``"adaptive_adoption_community_slack"``.
    """
    slug = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    return slug or "list"


class AttioClient:
    """Minimal Attio v2 REST client."""

    def __init__(self, api_key: str, *, base_url: str = ATTIO_API_BASE,
                 session: requests.Session | None = None, object_slug: str = "people") -> None:
        if not api_key:
            raise AttioError("ATTIO_API_KEY is not set.")
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.session = session or requests.Session()
        self.object_slug = object_slug

    def _request(self, method: str, path: str, *, params: dict[str, Any] | None = None,
                 json_body: dict[str, Any] | None = None) -> dict[str, Any]:
        """Issue a request and return the parsed JSON body, raising on non-2xx."""
        url = f"{self.base_url}{path}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        response = self.session.request(
            method, url, headers=headers, params=params, json=json_body, timeout=30
        )
        if not (200 <= response.status_code < 300):
            raise AttioError(
                f"{method} {path} -> HTTP {response.status_code}: {response.text}"
            )
        if not response.text:
            return {}
        return response.json()

    def assert_person(self, email: str, first_name: str, last_name: str,
                      full_name: str) -> str:
        """Upsert a People record keyed on ``email_addresses`` and return its id.

        Matching is done server-side by Attio: if a person with ``email``
        already exists it is updated, otherwise one is created. This makes the
        operation idempotent -- re-running never creates a duplicate.
        """
        if not email:
            raise AttioError("assert_person requires a non-empty email (the matching key).")

        body = {
            "data": {
                "values": {
                    "name": {
                        "first_name": first_name,
                        "last_name": last_name,
                        "full_name": full_name,
                    },
                    "email_addresses": [email],
                }
            }
        }
        result = self._request(
            "PUT",
            f"/v2/objects/{self.object_slug}/records",
            params={"matching_attribute": "email_addresses"},
            json_body=body,
        )
        return result.get("data", {}).get("id", {}).get("record_id", "")

    def find_list(self, name: str) -> str | None:
        """Return the ``list_id`` of the People list named ``name``, or ``None``.

        Matching is case-insensitive on the list's display ``name`` and also
        accepts a match on the derived ``api_slug`` so the lookup is stable.

        When a name/slug match is found, its ``parent_object`` must match this
        client's target object (``self.object_slug``). A list that happens to
        share the name but belongs to a different object (e.g. a Deals or
        Companies list) is *not* a valid sync target -- adding People records to
        it would fail -- so an incompatible match raises :class:`AttioError`
        rather than being returned silently.
        """
        result = self._request("GET", "/v2/lists")
        wanted_name = name.strip().lower()
        wanted_slug = slugify(name)
        for entry in result.get("data", []):
            entry_name = (entry.get("name") or "").strip().lower()
            entry_slug = entry.get("api_slug") or ""
            if entry_name == wanted_name or entry_slug == wanted_slug:
                parent = entry.get("parent_object") or ""
                if parent != self.object_slug:
                    raise AttioError(
                        f"List {name!r} exists but its parent object is "
                        f"{parent!r}, not {self.object_slug!r}. Refusing to sync "
                        f"into an incompatible list. Choose a different "
                        f"--list-name or remove/rename the conflicting list."
                    )
                return entry.get("id", {}).get("list_id")
        return None

    def create_list(self, name: str) -> str:
        """Create a People list named ``name`` and return its ``list_id``.

        The list is created with ``full-access`` so it is usable immediately;
        Attio requires either full workspace access or at least one
        full-access member on a new list.
        """
        body = {
            "data": {
                "name": name,
                "api_slug": slugify(name),
                "parent_object": self.object_slug,
                "workspace_access": "full-access",
                "workspace_member_access": [],
            }
        }
        result = self._request("POST", "/v2/lists", json_body=body)
        return result.get("data", {}).get("id", {}).get("list_id", "")

    def find_or_create_list(self, name: str) -> tuple[str, bool]:
        """Return ``(list_id, created)`` for the list named ``name``."""
        existing = self.find_list(name)
        if existing:
            return existing, False
        return self.create_list(name), True

    def list_entry_record_ids(self, list_id: str) -> set[str]:
        """Return the set of ``parent_record_id`` values already in ``list_id``.

        Entries are fetched via ``POST /v2/lists/{list}/entries/query`` and
        paged with ``limit``/``offset``; membership is evaluated client-side.
        This avoids relying on a server-side ``parent_record_id`` filter whose
        exact shape is not documented.
        """
        record_ids: set[str] = set()
        offset = 0
        page_size = 500
        while True:
            result = self._request(
                "POST",
                f"/v2/lists/{list_id}/entries/query",
                json_body={"limit": page_size, "offset": offset},
            )
            entries = result.get("data", [])
            for entry in entries:
                parent = entry.get("parent_record_id")
                if parent:
                    record_ids.add(parent)
            if len(entries) < page_size:
                break
            offset += page_size
        return record_ids

    def list_has_record(self, list_id: str, record_id: str) -> bool:
        """Return ``True`` if ``record_id`` is already an entry in ``list_id``."""
        return record_id in self.list_entry_record_ids(list_id)

    def add_to_list(self, list_id: str, record_id: str) -> str:
        """Add ``record_id`` to ``list_id`` and return the new ``entry_id``."""
        body = {
            "data": {
                "parent_record_id": record_id,
                "parent_object": self.object_slug,
                "entry_values": {},
            }
        }
        result = self._request("POST", f"/v2/lists/{list_id}/entries", json_body=body)
        return result.get("data", {}).get("id", {}).get("entry_id", "")
