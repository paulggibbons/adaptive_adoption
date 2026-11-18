# community-sync — Slack → Attio community sync

A small, repeatable CLI that mirrors the members of a Slack community channel
into the [Attio](https://attio.com) CRM. Each member is **upserted** as a People
record (matched by email) and added to a dedicated **People list**, so the
community can be segmented and worked inside Attio.

It is designed to be **idempotent** and **automatable**: run it as often as you
like (manually, via cron, or a scheduled task) and it will converge Attio to the
current Slack membership without creating duplicates.

> Built for the `#all-adaptiveadoptioncop` community. The tool itself is generic
> — point it at any channel and list name.

---

## What it does

1. **`pull-slack`** — resolves a Slack channel, walks its membership (paginated),
   reads each user's profile (name + email), and writes a **roster** file
   (`roster.json` or CSV).
2. **`sync`** — loads a roster (from a file, or live from Slack), then for each
   member:
   - **Upserts** a People record in Attio, matching on `email_addresses`
     (`PUT /v2/objects/people/records?matching_attribute=email_addresses`).
     Re-running updates rather than duplicates.
   - **Find-or-creates** the target People list by name.
   - **Adds** the person to the list **only if not already a member**
     (membership is checked up-front, so re-runs add nothing new).

---

## Prerequisites

- **Python 3.10+**
- `pip install -r requirements.txt` (only dependency: `requests`)
- Two secrets, provided as **environment variables** (never hardcoded):

  | Variable | Needed for | Where to get it |
  | --- | --- | --- |
  | `ATTIO_API_KEY` | live `sync` | Attio → **Workspace settings → Developers → API keys** |
  | `SLACK_BOT_TOKEN` | `pull-slack`, or `sync --channel` | A Slack app's **bot token** (`xoxb-…`) |

### Required Slack bot scopes

| Scope | Why |
| --- | --- |
| `channels:read` | list / resolve **public** channels |
| `groups:read` | list / resolve **private** channels (if the community is private) |
| `users:read` | read user profiles (names) |
| `users:read.email` | read the `email` field — `users:read` alone is **not** sufficient |

Invite the bot to the target channel (`/invite @your-bot`) so it can read
membership.

See [`.env.example`](./.env.example) for a template. Copy it to `.env` and fill
in real values — the real `.env` is **git-ignored** and must never be committed.

---

## Quickstart

```bash
cd integrations/community-sync
pip install -r requirements.txt

# Provide secrets (example: load a local .env)
export ATTIO_API_KEY=...      # or: set -a; source .env; set +a
export SLACK_BOT_TOKEN=xoxb-...

# 1) Pull the current Slack roster to a file
python community_sync.py pull-slack --channel all-adaptiveadoptioncop --out roster.json

# 2) Sync into Attio, excluding Paul himself
python community_sync.py sync --roster roster.json \
    --exclude williampaulgibbons@gmail.com

# Or do it in one shot (pull live + sync):
python community_sync.py sync --channel all-adaptiveadoptioncop \
    --exclude williampaulgibbons@gmail.com
```

The target list defaults to **`Adaptive Adoption Community (Slack)`**; override
with `--list-name "Some Other List"`.

### Dry-run demo (no credentials, no network)

A dry run prints the planned actions and makes **zero** network calls. Fed from a
file it needs **no** environment variables at all — great for a safe preview:

```bash
python community_sync.py sync --dry-run \
    --roster sample_roster.csv \
    --exclude williampaulgibbons@gmail.com
```

`sample_roster.csv` ships with three obviously-fake members so this works out of
the box.

---

## Commands & flags

### `pull-slack`
| Flag | Default | Meaning |
| --- | --- | --- |
| `--channel` | *(required)* | Channel name (`all-adaptiveadoptioncop`) or id (`C…`) |
| `--out` | `roster.json` | Output path |
| `--format` | `json` | `json` or `csv` |

### `sync`
| Flag | Default | Meaning |
| --- | --- | --- |
| `--roster` | — | Roster file to load (`.json` / `.csv`) |
| `--channel` | — | Pull members live from this channel (alternative to `--roster`) |
| `--list-name` | `Adaptive Adoption Community (Slack)` | Target People list |
| `--exclude` | — | Comma-separated emails to skip (e.g. Paul himself) |
| `--dry-run` | off | Print the plan; make no writes / no network calls |

`--roster` and `--channel` are mutually exclusive; supply exactly one.

---

## Roster format

A roster is a list of members with these fields:

| Field | Notes |
| --- | --- |
| `slack_user_id` | e.g. `U0123ABCD` (optional) |
| `full_name` | display/real name |
| `first_name` | derived from `full_name` if absent |
| `last_name` | derived from `full_name` if absent |
| `email` | **the Attio match key**; members without one are skipped |

JSON (a list of objects) and CSV (header + rows) are both supported; the format
is inferred from the file extension.

---

## Idempotency

Safe to re-run any time:

- **People** are upserted with `matching_attribute=email_addresses`, so an
  existing person is updated, never duplicated.
- **List entries**: current membership is fetched first, and a person is added
  only if their record id is not already present.
- Email matching is **case-insensitive** (emails are lower-cased on load).

---

## Scheduling (ongoing auto-sync)

Because the sync is idempotent, just run it on a timer.

**cron** (every day at 07:30, loading secrets from a local env file):

```cron
30 7 * * *  cd /path/to/integrations/community-sync && \
  set -a && . ./.env && set +a && \
  /usr/bin/python3 community_sync.py sync --channel all-adaptiveadoptioncop \
    --exclude williampaulgibbons@gmail.com >> sync.log 2>&1
```

**Claude Code scheduled task**: create a recurring task whose prompt runs the
same `sync --channel …` command, with `ATTIO_API_KEY` and `SLACK_BOT_TOKEN`
available as environment secrets. Each firing reconciles Slack → Attio.

---

## Troubleshooting

| Symptom | Likely cause / fix |
| --- | --- |
| `ATTIO_API_KEY not set` | Export the key, or use `--dry-run` to preview without it. |
| `SLACK_BOT_TOKEN not set` | Needed for `pull-slack` / `sync --channel`. Use `--roster` to work offline. |
| `Channel '…' not found` | Check the name, invite the bot to the channel, and ensure `channels:read` / `groups:read`. |
| Members have no email | The bot lacks `users:read.email`, or the users genuinely have no email. Members without email are reported and skipped. |
| `missing_scope` from Slack | Add the scope named in the error and **reinstall** the Slack app. |
| Attio `HTTP 4xx` with a body | The error includes Attio's response body verbatim — read it for the offending field. |
| Rate limited | Slack 429s are retried with backoff automatically. |

---

## Files

| File | Purpose |
| --- | --- |
| `community_sync.py` | CLI entry point (`pull-slack`, `sync`) |
| `attio_client.py` | Attio v2 REST client (upsert, lists, entries) |
| `slack_client.py` | Slack Web API client (channels, members, profiles) |
| `roster.py` | Roster load/save + name splitting |
| `requirements.txt` | `requests` |
| `.env.example` | Documents the two secrets + Slack scopes |
| `sample_roster.csv` | Fake data for the dry-run demo |
| `tests/test_community_sync.py` | Offline pytest suite (no network) |

---

## Testing

```bash
pip install requests pytest
pytest tests/ -q
```

All tests run offline with `requests` mocked; none touch the network.
