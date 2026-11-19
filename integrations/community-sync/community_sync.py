#!/usr/bin/env python3
"""community_sync -- sync a Slack community into the Attio CRM.

Purpose
-------
Paul Gibbons runs an "Adaptive Adoption" community in Slack and wants its
members mirrored into Attio: each member upserted as a People record (keyed by
email) and added to a dedicated People list so the group can be segmented and
worked in the CRM. This tool makes that repeatable and idempotent -- safe to
run on a schedule -- rather than a one-off manual export.

It has two subcommands:

    pull-slack   Fetch the members of a Slack channel and write a roster file.
    sync         Upsert each roster member into Attio People and add them to the
                 target People list (find-or-create), skipping anyone already a
                 member. Supports --dry-run to preview without any writes.

Secrets come exclusively from environment variables and are only required for
the operation actually being performed:

    ATTIO_API_KEY     required for live Attio access (sync, non-dry-run)
    SLACK_BOT_TOKEN   required for live Slack access (pull-slack, or sync --channel)

A --dry-run sync fed from a roster file needs no credentials and makes no
network calls at all. Missing secrets produce a friendly message, never a
traceback.
"""

from __future__ import annotations

import argparse
import os
import sys

import roster as roster_mod
from attio_client import AttioClient, AttioError
from slack_client import SlackClient, SlackError

DEFAULT_LIST_NAME = "Adaptive Adoption Community (Slack)"


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def _fail(message: str, code: int = 1) -> "int":
    """Print a friendly error to stderr and return an exit code."""
    print(f"error: {message}", file=sys.stderr)
    return code


def _require_env(var: str) -> str | None:
    """Return the value of env var ``var`` or ``None`` if unset/empty."""
    value = os.environ.get(var, "").strip()
    return value or None


def _roster_from_slack(channel: str, token: str) -> list[dict[str, str]]:
    """Build a roster by walking a Slack channel's membership.

    Bot and deleted users are skipped. Members without an email are kept but
    will be reported and skipped at upsert time (email is the Attio match key).
    """
    client = SlackClient(token)
    print(f"Resolving Slack channel {channel!r} ...", file=sys.stderr)
    channel_id = client.resolve_channel(channel)
    print(f"  -> channel id {channel_id}", file=sys.stderr)

    member_ids = client.channel_member_ids(channel_id)
    print(f"Found {len(member_ids)} channel member(s); fetching profiles ...",
          file=sys.stderr)

    records: list[dict[str, str]] = []
    for user_id in member_ids:
        profile = client.user_profile(user_id)
        if profile["is_bot"] or profile["deleted"]:
            continue
        records.append(roster_mod.normalise_record(profile))
    return records


# --------------------------------------------------------------------------- #
# Subcommand: pull-slack
# --------------------------------------------------------------------------- #
def cmd_pull_slack(args: argparse.Namespace) -> int:
    token = _require_env("SLACK_BOT_TOKEN")
    if not token:
        return _fail(
            "SLACK_BOT_TOKEN not set. Export a Slack bot token (scopes: "
            "channels:read/groups:read, users:read, users:read.email) to pull "
            "channel members. See .env.example."
        )

    try:
        records = _roster_from_slack(args.channel, token)
    except SlackError as exc:
        return _fail(str(exc))

    # Default the output filename to match --format so the extension always
    # agrees with the bytes written (sync's load_roster picks its parser by
    # extension). When --out is given explicitly, warn -- but don't hard-fail --
    # if its extension conflicts with the chosen format.
    out = args.out or f"roster.{args.format}"
    if args.out:
        ext = os.path.splitext(args.out)[1].lower().lstrip(".")
        if ext in ("json", "csv") and ext != args.format:
            print(
                f"warning: --out {args.out!r} has a .{ext} extension but "
                f"--format is {args.format!r}; the file will contain "
                f"{args.format} data. Note that `sync` loads a roster by its "
                f"file extension, so this mismatch will likely break loading.",
                file=sys.stderr,
            )

    roster_mod.save_roster(records, out, fmt=args.format)
    with_email = sum(1 for r in records if r["email"])
    print(f"Wrote {len(records)} member(s) ({with_email} with email) to {out} "
          f"as {args.format}.")
    return 0


# --------------------------------------------------------------------------- #
# Subcommand: sync
# --------------------------------------------------------------------------- #
def _load_sync_roster(args: argparse.Namespace) -> list[dict[str, str]]:
    """Resolve the roster for ``sync`` from --roster (file) or --channel (live)."""
    if args.roster:
        return roster_mod.load_roster(args.roster)

    # Live pull requires a Slack token even in dry-run (it reads from Slack).
    token = _require_env("SLACK_BOT_TOKEN")
    if not token:
        raise SlackError(
            "SLACK_BOT_TOKEN not set, required to pull members with --channel. "
            "Either export the token or pass --roster <file>."
        )
    return _roster_from_slack(args.channel, token)


def cmd_sync(args: argparse.Namespace) -> int:
    if not args.roster and not args.channel:
        return _fail("sync requires either --roster <file> or --channel <name-or-id>.")

    exclude = {e.strip().lower() for e in (args.exclude or "").split(",") if e.strip()}

    # 1. Load the roster (from file, or live from Slack).
    try:
        records = _load_sync_roster(args)
    except SlackError as exc:
        return _fail(str(exc))
    except (OSError, ValueError) as exc:
        return _fail(f"could not load roster: {exc}")

    # 2. Partition into actionable / skipped.
    actionable: list[dict[str, str]] = []
    skipped_excluded: list[str] = []
    skipped_no_email: list[str] = []
    for rec in records:
        if not rec["email"]:
            skipped_no_email.append(rec["full_name"] or rec["slack_user_id"] or "(unknown)")
            continue
        if rec["email"] in exclude:
            skipped_excluded.append(rec["email"])
            continue
        actionable.append(rec)

    list_name = args.list_name
    print(f"Roster: {len(records)} member(s) | to sync: {len(actionable)} | "
          f"excluded: {len(skipped_excluded)} | no email: {len(skipped_no_email)}")
    if skipped_no_email:
        print(f"  (skipping {len(skipped_no_email)} without email: "
              f"{', '.join(skipped_no_email[:5])}{' ...' if len(skipped_no_email) > 5 else ''})")

    # 3. DRY RUN -- print the plan and make absolutely no network calls.
    if args.dry_run:
        print("\n--- DRY RUN: no changes will be made ---")
        print(f"Would find-or-create People list: {list_name!r}")
        for rec in actionable:
            print(f"  upsert People <{rec['email']}> "
                  f"name={rec['full_name']!r} (first={rec['first_name']!r}, "
                  f"last={rec['last_name']!r}) -> then add to list {list_name!r}")
        print(f"\nPlanned: {len(actionable)} upsert(s) + list membership checks. "
              f"0 network calls made (dry run).")
        return 0

    # 4. LIVE -- Attio credentials required.
    api_key = _require_env("ATTIO_API_KEY")
    if not api_key:
        return _fail(
            "ATTIO_API_KEY not set. Export your Attio API key (Workspace settings "
            "-> Developers -> API keys) to run a live sync, or use --dry-run to "
            "preview without credentials. See .env.example."
        )

    try:
        attio = AttioClient(api_key)

        # Resolve and VALIDATE the target list BEFORE upserting any people.
        # find_list raises if an existing list by this name belongs to a
        # different object, so an incompatible list aborts the run cleanly with
        # zero record writes. If the list doesn't exist yet it is created here,
        # exactly as before.
        existing_list_id = attio.find_list(list_name)
        if existing_list_id:
            list_id, created = existing_list_id, False
        else:
            list_id, created = attio.create_list(list_name), True
        print(f"List {list_name!r}: {'created' if created else 'found'} (id {list_id}).")

        # Fetch current membership once so adds are idempotent and cheap.
        existing_ids = attio.list_entry_record_ids(list_id)

        upserted = 0
        added = 0
        already = 0
        for rec in actionable:
            record_id = attio.assert_person(
                rec["email"], rec["first_name"], rec["last_name"], rec["full_name"]
            )
            upserted += 1
            if not record_id:
                print(f"  ! upserted <{rec['email']}> but no record id returned; "
                      f"skipping list add.")
                continue
            if record_id in existing_ids:
                already += 1
                continue
            attio.add_to_list(list_id, record_id)
            existing_ids.add(record_id)
            added += 1
            print(f"  + added <{rec['email']}> to {list_name!r}")

        print(f"\nDone. Upserted {upserted} person/people; added {added} to the list; "
              f"{already} already present.")
        return 0
    except AttioError as exc:
        return _fail(str(exc))


# --------------------------------------------------------------------------- #
# Argument parsing
# --------------------------------------------------------------------------- #
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="community_sync",
        description="Sync Slack community members into the Attio CRM.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # pull-slack
    p_pull = sub.add_parser(
        "pull-slack", help="Fetch Slack channel members and write a roster file."
    )
    p_pull.add_argument("--channel", required=True,
                        help="Channel name (e.g. all-adaptiveadoptioncop) or id (Cxxxx).")
    p_pull.add_argument("--out", default=None,
                        help="Output roster path (default: roster.<format>, i.e. "
                             "roster.json for --format json or roster.csv for "
                             "--format csv).")
    p_pull.add_argument("--format", choices=["json", "csv"], default="json",
                        help="Roster output format (default: json).")
    p_pull.set_defaults(func=cmd_pull_slack)

    # sync
    p_sync = sub.add_parser(
        "sync", help="Upsert roster members into Attio and add them to the People list."
    )
    source = p_sync.add_mutually_exclusive_group()
    source.add_argument("--roster", help="Roster file to load (json or csv).")
    source.add_argument("--channel", help="Pull members live from this Slack channel.")
    p_sync.add_argument("--list-name", dest="list_name", default=DEFAULT_LIST_NAME,
                        help=f"Target People list name (default: {DEFAULT_LIST_NAME!r}).")
    p_sync.add_argument("--exclude", default="",
                        help="Comma-separated emails to skip (e.g. Paul himself).")
    p_sync.add_argument("--dry-run", action="store_true",
                        help="Print the planned actions and make no writes/network calls.")
    p_sync.set_defaults(func=cmd_sync)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
