"""Thin Slack Web API client used by the community-sync tool.

Only the handful of read endpoints we need are implemented:

    - ``resolve_channel``      channel name (or id) -> channel id
    - ``channel_member_ids``   paginated member ids of a channel
    - ``user_profile``         a user's name + email

The client speaks the Slack Web API (base ``https://slack.com/api``) using a
bot token supplied via the ``SLACK_BOT_TOKEN`` environment variable. Slack
returns HTTP 200 with an ``{"ok": false, "error": ...}`` envelope for logical
errors, so every call is routed through :meth:`SlackClient._get`, which checks
``ok`` and raises :class:`SlackError`. Rate limiting (HTTP 429 with a
``Retry-After`` header, or ``error == "ratelimited"``) is retried with a simple
backoff.

Required Slack scopes (bot token):
    - ``channels:read`` and/or ``groups:read``  -- list/resolve channels
    - ``users:read``                            -- read user profiles
    - ``users:read.email``                      -- read the ``email`` field

Docs confirmed 2026-11-18:
    conversations.list    https://docs.slack.dev/reference/methods/conversations.list
    conversations.members https://docs.slack.dev/reference/methods/conversations.members
    users.info            https://docs.slack.dev/reference/methods/users.info
"""

from __future__ import annotations

import time
from typing import Any

import requests

SLACK_API_BASE = "https://slack.com/api"


class SlackError(RuntimeError):
    """Raised when Slack returns ``ok: false`` or an unrecoverable HTTP error."""


class SlackClient:
    """Minimal Slack Web API client (read-only endpoints)."""

    def __init__(self, token: str, *, base_url: str = SLACK_API_BASE,
                 session: requests.Session | None = None, max_retries: int = 5) -> None:
        if not token:
            # Callers should have validated this already; guard anyway.
            raise SlackError("SLACK_BOT_TOKEN is not set.")
        self.token = token
        self.base_url = base_url.rstrip("/")
        self.session = session or requests.Session()
        self.max_retries = max_retries

    def _get(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Call a Slack Web API method, handling rate limits and the ``ok`` envelope."""
        url = f"{self.base_url}/{method}"
        headers = {"Authorization": f"Bearer {self.token}"}

        attempt = 0
        while True:
            attempt += 1
            response = self.session.get(url, headers=headers, params=params or {}, timeout=30)

            # HTTP-level rate limiting: honour Retry-After and try again.
            if response.status_code == 429:
                if attempt > self.max_retries:
                    raise SlackError(f"{method}: rate limited after {self.max_retries} retries.")
                self._sleep_for_retry(response.headers.get("Retry-After"), attempt)
                continue

            if response.status_code >= 400:
                raise SlackError(f"{method}: HTTP {response.status_code}: {response.text}")

            payload = response.json()
            if not payload.get("ok", False):
                error = payload.get("error", "unknown_error")
                # Logical rate limiting is also surfaced via the envelope.
                if error == "ratelimited" and attempt <= self.max_retries:
                    self._sleep_for_retry(response.headers.get("Retry-After"), attempt)
                    continue
                raise SlackError(f"{method}: Slack API error: {error}")
            return payload

    @staticmethod
    def _sleep_for_retry(retry_after: str | None, attempt: int) -> None:
        """Sleep according to ``Retry-After`` or an exponential fallback."""
        try:
            delay = float(retry_after) if retry_after is not None else 0.0
        except ValueError:
            delay = 0.0
        if delay <= 0:
            delay = min(2 ** attempt, 30)
        time.sleep(delay)

    def resolve_channel(self, name_or_id: str) -> str:
        """Return the channel id for ``name_or_id``.

        If the argument already looks like a channel id (``C``/``G``/``D``
        prefix) it is returned unchanged. Otherwise public and private channels
        are paged via ``conversations.list`` and matched by name (a leading
        ``#`` is ignored).
        """
        candidate = name_or_id.strip()
        if candidate.startswith("#"):
            candidate = candidate[1:]

        # Heuristic: Slack ids are upper-case and start with C/G/D.
        if candidate[:1] in {"C", "G", "D"} and candidate.isupper() and " " not in candidate:
            return candidate

        wanted = candidate.lower()
        cursor = ""
        while True:
            params = {
                "types": "public_channel,private_channel",
                "limit": 200,
                "exclude_archived": "false",
            }
            if cursor:
                params["cursor"] = cursor
            payload = self._get("conversations.list", params)
            for channel in payload.get("channels", []):
                if (channel.get("name") or "").lower() == wanted:
                    return channel["id"]
            cursor = (payload.get("response_metadata") or {}).get("next_cursor") or ""
            if not cursor:
                break

        raise SlackError(
            f"Channel {name_or_id!r} not found. Check the name, or ensure the bot "
            f"is a member and has channels:read / groups:read scopes."
        )

    def channel_member_ids(self, channel_id: str) -> list[str]:
        """Return all member user ids of ``channel_id`` (cursor-paginated)."""
        members: list[str] = []
        cursor = ""
        while True:
            params = {"channel": channel_id, "limit": 200}
            if cursor:
                params["cursor"] = cursor
            payload = self._get("conversations.members", params)
            members.extend(payload.get("members", []))
            cursor = (payload.get("response_metadata") or {}).get("next_cursor") or ""
            if not cursor:
                break
        return members

    def user_profile(self, user_id: str) -> dict[str, Any]:
        """Return a normalised profile dict for ``user_id``.

        Keys: ``slack_user_id``, ``full_name``, ``first_name``, ``last_name``,
        ``email``, ``is_bot``, ``deleted``. The ``email`` field requires the
        ``users:read.email`` scope; it may be empty if the user has no email.
        """
        payload = self._get("users.info", {"user": user_id})
        user = payload.get("user", {}) or {}
        profile = user.get("profile", {}) or {}

        full_name = (profile.get("real_name") or profile.get("display_name") or "").strip()
        return {
            "slack_user_id": user_id,
            "full_name": full_name,
            "first_name": (profile.get("first_name") or "").strip(),
            "last_name": (profile.get("last_name") or "").strip(),
            "email": (profile.get("email") or "").strip(),
            "is_bot": bool(user.get("is_bot", False)),
            "deleted": bool(user.get("deleted", False)),
        }
