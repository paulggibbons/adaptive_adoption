"""Offline tests for community-sync.

These run with no network access and no credentials. ``requests`` is mocked via
a tiny fake session, and HTTP activity is asserted to be absent where the design
promises it (notably ``sync --dry-run``).
"""

from __future__ import annotations

import os
import sys

import pytest

# Make the package modules importable when pytest is run from the repo root.
PKG_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PKG_DIR not in sys.path:
    sys.path.insert(0, PKG_DIR)

import attio_client  # noqa: E402
import community_sync  # noqa: E402
import roster as roster_mod  # noqa: E402


# --------------------------------------------------------------------------- #
# roster round-trip + name splitting
# --------------------------------------------------------------------------- #
def test_split_name_variants():
    assert roster_mod.split_name("Ada Lovelace") == ("Ada", "Lovelace")
    assert roster_mod.split_name("Cher") == ("Cher", "")
    assert roster_mod.split_name("Johannes van der Berg") == ("Johannes", "van der Berg")
    assert roster_mod.split_name("   ") == ("", "")
    assert roster_mod.split_name("") == ("", "")


def test_normalise_backfills_first_last_from_full_name():
    rec = roster_mod.normalise_record({"full_name": "Grace Hopper", "email": "G.H@Example.com"})
    assert rec["first_name"] == "Grace"
    assert rec["last_name"] == "Hopper"
    # Email is lower-cased for case-insensitive dedupe.
    assert rec["email"] == "g.h@example.com"


def test_normalise_builds_full_name_from_parts():
    rec = roster_mod.normalise_record({"first_name": "Alan", "last_name": "Turing"})
    assert rec["full_name"] == "Alan Turing"


def test_json_round_trip(tmp_path):
    original = [
        {"slack_user_id": "U1", "full_name": "Ada Lovelace", "email": "ada@example.com"},
        {"slack_user_id": "U2", "full_name": "Alan Turing", "email": "alan@example.com"},
    ]
    path = tmp_path / "roster.json"
    roster_mod.save_roster(original, str(path), fmt="json")
    loaded = roster_mod.load_roster(str(path))

    assert [r["email"] for r in loaded] == ["ada@example.com", "alan@example.com"]
    assert loaded[0]["first_name"] == "Ada"
    assert loaded[0]["last_name"] == "Lovelace"


def test_csv_round_trip(tmp_path):
    original = [{"slack_user_id": "U3", "full_name": "Grace Hopper", "email": "grace@example.com"}]
    path = tmp_path / "roster.csv"
    roster_mod.save_roster(original, str(path), fmt="csv")
    loaded = roster_mod.load_roster(str(path))

    assert loaded[0]["email"] == "grace@example.com"
    assert loaded[0]["first_name"] == "Grace"
    assert loaded[0]["last_name"] == "Hopper"


def test_sample_roster_loads():
    sample = os.path.join(PKG_DIR, "sample_roster.csv")
    loaded = roster_mod.load_roster(sample)
    assert len(loaded) == 3
    assert all(r["email"].endswith("@example.com") for r in loaded)


# --------------------------------------------------------------------------- #
# Fake requests session -- records calls, returns canned JSON
# --------------------------------------------------------------------------- #
class FakeResponse:
    def __init__(self, status_code=200, payload=None, text=""):
        self.status_code = status_code
        self._payload = payload if payload is not None else {}
        self.text = text or "{}"
        self.headers = {}

    def json(self):
        return self._payload


class FakeSession:
    """Records every request so tests can assert on (or forbid) HTTP activity."""

    def __init__(self, handler=None):
        self.calls = []
        self._handler = handler

    def request(self, method, url, **kwargs):
        self.calls.append((method, url, kwargs))
        if self._handler is None:
            return FakeResponse(200, {})
        return self._handler(method, url, kwargs)

    def get(self, url, **kwargs):
        return self.request("GET", url, **kwargs)


# --------------------------------------------------------------------------- #
# dedupe logic: list_has_record / list_entry_record_ids
# --------------------------------------------------------------------------- #
def test_list_has_record_dedupe():
    def handler(method, url, kwargs):
        # entries/query returns a single page with two known records.
        return FakeResponse(200, {
            "data": [
                {"parent_record_id": "rec-A"},
                {"parent_record_id": "rec-B"},
            ]
        })

    session = FakeSession(handler)
    client = attio_client.AttioClient("fake-key", session=session)

    assert client.list_has_record("list-1", "rec-A") is True
    assert client.list_has_record("list-1", "rec-Z") is False


def test_assert_person_uses_matching_attribute_and_name_shape():
    captured = {}

    def handler(method, url, kwargs):
        captured["method"] = method
        captured["url"] = url
        captured["params"] = kwargs.get("params")
        captured["json"] = kwargs.get("json")
        return FakeResponse(200, {"data": {"id": {"record_id": "rec-new"}}})

    session = FakeSession(handler)
    client = attio_client.AttioClient("fake-key", session=session)
    rid = client.assert_person("ada@example.com", "Ada", "Lovelace", "Ada Lovelace")

    assert rid == "rec-new"
    assert captured["method"] == "PUT"
    assert captured["url"].endswith("/v2/objects/people/records")
    assert captured["params"] == {"matching_attribute": "email_addresses"}
    values = captured["json"]["data"]["values"]
    assert values["name"] == {
        "first_name": "Ada", "last_name": "Lovelace", "full_name": "Ada Lovelace"
    }
    assert values["email_addresses"] == ["ada@example.com"]


def test_attio_error_includes_body_on_non_2xx():
    def handler(method, url, kwargs):
        return FakeResponse(422, {}, text='{"error":"bad request"}')

    session = FakeSession(handler)
    client = attio_client.AttioClient("fake-key", session=session)
    with pytest.raises(attio_client.AttioError) as excinfo:
        client.assert_person("x@example.com", "X", "Y", "X Y")
    assert "bad request" in str(excinfo.value)


# --------------------------------------------------------------------------- #
# sync --dry-run makes ZERO HTTP calls and needs no credentials
# --------------------------------------------------------------------------- #
def test_sync_dry_run_makes_no_http_calls(monkeypatch, capsys):
    # Ensure no credentials are present.
    monkeypatch.delenv("ATTIO_API_KEY", raising=False)
    monkeypatch.delenv("SLACK_BOT_TOKEN", raising=False)

    # Any attempt to construct a real requests.Session or client must fail loudly.
    def boom(*args, **kwargs):  # pragma: no cover - should never be called
        raise AssertionError("dry-run must not construct an HTTP client")

    monkeypatch.setattr(community_sync, "AttioClient", boom)
    monkeypatch.setattr(community_sync, "SlackClient", boom)

    sample = os.path.join(PKG_DIR, "sample_roster.csv")
    rc = community_sync.main([
        "sync", "--dry-run", "--roster", sample,
        "--exclude", "ada.lovelace@example.com",
    ])
    out = capsys.readouterr().out

    assert rc == 0
    assert "DRY RUN" in out
    assert "0 network calls" in out
    # Excluded member must not appear as an upsert target.
    assert "upsert People <ada.lovelace@example.com>" not in out
    assert "upsert People <alan.turing@example.com>" in out


def test_sync_missing_attio_key_exits_cleanly(monkeypatch, capsys):
    monkeypatch.delenv("ATTIO_API_KEY", raising=False)
    sample = os.path.join(PKG_DIR, "sample_roster.csv")
    rc = community_sync.main(["sync", "--roster", sample])
    err = capsys.readouterr().err

    assert rc == 1
    assert "ATTIO_API_KEY not set" in err
