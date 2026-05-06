#!/usr/bin/env python3
"""
Seed data/tools.yml from Supabase public.tools table.

Required environment variables:
  SUPABASE_URL   — https://<project>.supabase.co
  SUPABASE_KEY   — service_role or anon key (read-only access to public.tools)

Usage:
  python scripts/seed_tools.py

Outputs:
  data/tools.yml  — canonical tools manifest (schema v1.1)

Idempotent: safe to re-run; overwrites existing data/tools.yml.
"""

import logging
import os
import sys
import re
from datetime import date, datetime
from pathlib import Path

import requests
import yaml

# ──────────────────────────────────────────────────────────────────────────────
# Path setup — makes `from lib.transformers import ...` work
# ──────────────────────────────────────────────────────────────────────────────
SCRIPTS_DIR = Path(__file__).parent
REPO_ROOT = SCRIPTS_DIR.parent
sys.path.insert(0, str(SCRIPTS_DIR))

from lib.transformers import (
    slug_from_name, domain_from_supabase, status_from_supabase,
    type_from_supabase, pillar_slug, version_from_epistemic_label,
    tags_from_entry, is_pillar_unmapped,
)

# ──────────────────────────────────────────────────────────────────────────────
# Logging — INFO progress, WARNING skipped/transformed, ERROR failures; stderr only
# ──────────────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)

TODAY = date.today().isoformat()
EXPECTED_ROW_COUNT = 88
ROW_COUNT_TOLERANCE = 0.10
MAX_OUTPUT_BYTES = 1_000_000
MAX_OUTPUT_LINES = 5_000

# ──────────────────────────────────────────────────────────────────────────────
# Special-case overrides (per brief §2c–2f)
# ──────────────────────────────────────────────────────────────────────────────
SLUG_OVERRIDES = {
    2:  "ai-knowledge-quick-quiz",
    87: "ai-mastery-assessment",
    60: "agentic-trust-level",
}
NAME_OVERRIDES = {
    2:  "AI Knowledge Quick Quiz",
    60: "Agentic Trust Level",
}
ALIASES_OVERRIDES = {
    2:  ["AI Mastery Self-Assessment"],
    60: ["Autonomy Map", "Trust Thermometer"],
}
SHORT_DESC_OVERRIDES = {
    2: (
        "12 questions. Quick gateway diagnostic — Know/Do/Build × 4 levels. "
        "Lightweight introduction before the full 7-dimension AI Mastery Self-Assessment."
    ),
}
CARD_PILLAR_LABEL_OVERRIDES = {
    2: "PILLAR 1 · MASTER THE CRAFT",
}
SOURCE_OVERRIDES = {
    60: "Original — Gibbons 2026; extends Nate Jones — five levels of agent autonomy",
}
GREYED_PILLAR_LABEL_OVERRIDES = {
    60: "AGENT AUTHORITY · NATE JONES 5",
}

# ──────────────────────────────────────────────────────────────────────────────
# Aspirational entries — Step 3 (not in Supabase; verified during Cowork session)
# ──────────────────────────────────────────────────────────────────────────────
ASPIRATIONAL_ENTRIES = [
    {
        "supabase_id": None,
        "slug": "adoption-friction-mapper",
        "name": "Adoption Friction Mapper",
        "aliases": [],
        "type": "canvas",
        "status": "planned",
        "version": None,
        "short_description": (
            "Process-level tool that maps where users disengage in an AI adoption "
            "journey, where workarounds emerge, and where value leaks. Combines user "
            "journey mapping with behavioural observation. Distinct from CMTO "
            "(id 22) which is the four-factor diagnostic."
        ),
        "long_description": None,
        "framework_mapping": {
            "domain": "change-agility",
            "pillar": "06-prioritize-behavior",
            "pillar_num": 6,
            "pillar_name": "Prioritize Behavior",
        },
        "astro_url": None,
        "supabase": {"table": None, "notes": ""},
        "source": "Original — Gibbons 2026",
        "epistemic": {"level": 1, "label": "Original — Gibbons 2026 · Conceptual · v0.1"},
        "card_display": {
            "pillar_label": None, "time": None,
            "is_greyed": False, "greyed_pillar_label": None, "greyed_time": None,
        },
        "related_tools": [],
        "dates": {"created": TODAY, "last_updated": TODAY, "built": None, "archived": None},
        "archived_reason": None,
        "aspirational_notes": None,
        "sort_order": 9001,
        "tags": ["aspirational", "change-agility", "behaviour", "planned"],
    },
    {
        "supabase_id": None,
        "slug": "social-frictions-allies-assessment",
        "name": "Social Frictions-Allies Assessment",
        "aliases": ["Stakeholder Influence Audit"],
        "type": "assessment",
        "status": "planned",
        "version": None,
        "short_description": (
            "Behavioural mapping of stakeholder dynamics affecting AI adoption — who "
            "enables, who blocks, who is affected but unheard. Pilot→prototype→scaling "
            "governance layer."
        ),
        "long_description": None,
        "framework_mapping": {
            "domain": "behavioral-governance",
            "pillar": None,
            "pillar_num": None,
            "pillar_name": None,
        },
        "astro_url": None,
        "supabase": {"table": None, "notes": ""},
        "source": (
            "Adapted from canonical change-management stakeholder mapping; "
            "relocated to governance layer per Adaptive Adoption synthesis"
        ),
        "epistemic": {
            "level": 1,
            "label": "Original synthesis — Gibbons 2026 · Conceptual · v0.1",
        },
        "card_display": {
            "pillar_label": None, "time": None,
            "is_greyed": False, "greyed_pillar_label": None, "greyed_time": None,
        },
        "related_tools": [],
        "dates": {"created": TODAY, "last_updated": TODAY, "built": None, "archived": None},
        "archived_reason": None,
        "aspirational_notes": None,
        "sort_order": 9002,
        "tags": ["aspirational", "behavioral-governance", "stakeholders", "planned"],
    },
    {
        "supabase_id": None,
        "slug": "conditions-audit",
        "name": "Conditions Audit",
        "aliases": [],
        "type": "diagnostic",
        "status": "planned",
        "version": None,
        "short_description": (
            "Diagnostic assessing whether the six organisational conditions necessary "
            "for the Leadership Delta to close are present. Sponsorship, reinforcement, "
            "structural enablers, peer norms, time/space, consequence alignment."
        ),
        "long_description": None,
        "framework_mapping": {
            "domain": "leadership-delta",
            "pillar": None,
            "pillar_num": None,
            "pillar_name": None,
        },
        "astro_url": None,
        "supabase": {"table": None, "notes": ""},
        "source": "Beer, Finnstrom & Schrader (2016); original Adaptive Adoption synthesis",
        "epistemic": {"level": 2, "label": "Research-grounded · Beer et al. 2016 · v0.1"},
        "card_display": {
            "pillar_label": None, "time": None,
            "is_greyed": False, "greyed_pillar_label": None, "greyed_time": None,
        },
        "related_tools": [],
        "dates": {"created": TODAY, "last_updated": TODAY, "built": None, "archived": None},
        "archived_reason": None,
        "aspirational_notes": None,
        "sort_order": 9003,
        "tags": ["aspirational", "leadership-delta", "organisational-conditions", "planned"],
    },
    {
        "supabase_id": None,
        "slug": "governance-dashboard",
        "name": "Governance Dashboard",
        "aliases": [],
        "type": "scorecard",
        "status": "speculative",
        "version": None,
        "short_description": (
            "Board-level governance readout aggregating decision rights, agent "
            "authority, risk intelligence, and strategic coherence into a single view."
        ),
        "long_description": None,
        "framework_mapping": {
            "domain": "behavioral-governance",
            "pillar": None,
            "pillar_num": None,
            "pillar_name": None,
        },
        "astro_url": None,
        "supabase": {"table": None, "notes": ""},
        "source": "Original — Gibbons 2026",
        "epistemic": {"level": 1, "label": "Original — Gibbons 2026 · Conceptual · v0.1"},
        "card_display": {
            "pillar_label": None, "time": None,
            "is_greyed": False, "greyed_pillar_label": None, "greyed_time": None,
        },
        "related_tools": [],
        "dates": {"created": TODAY, "last_updated": TODAY, "built": None, "archived": None},
        "archived_reason": None,
        "aspirational_notes": (
            "Scope is broad — likely splits into 2-3 separate dashboards once defined. "
            "Speculative until decomposed."
        ),
        "sort_order": 9004,
        "tags": ["speculative", "behavioral-governance", "dashboard", "board-level"],
    },
]


# ──────────────────────────────────────────────────────────────────────────────
# Supabase pull
# ──────────────────────────────────────────────────────────────────────────────
def get_supabase_rows() -> list[dict]:
    supabase_url = os.environ.get("SUPABASE_URL", "").rstrip("/")
    supabase_key = (
        os.environ.get("SUPABASE_KEY")
        or os.environ.get("SUPABASE_ANON_KEY")
        or os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    )

    if not supabase_url or not supabase_key:
        logger.error("Missing SUPABASE_URL or SUPABASE_KEY. Aborting.")
        sys.exit(1)

    url = f"{supabase_url}/rest/v1/tools"
    params = {
        "select": ",".join([
            "id", "domain", "pillar", "pillar_num", "tool", "type", "status",
            "source", "notes", "url", "sort_order", "is_greyed_card",
            "greyed_pillar_label", "greyed_time", "card_pillar_label",
            "card_time", "epistemic_level", "epistemic_label", "updated_at",
        ]),
        "order": "sort_order.asc,id.asc",
    }
    headers = {
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}",
        "Content-Type": "application/json",
    }

    logger.info(f"Pulling tools from {supabase_url}/rest/v1/tools")
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=30)
    except requests.RequestException as exc:
        logger.error(f"Supabase request failed: {exc}")
        sys.exit(1)

    if resp.status_code != 200:
        logger.error(f"Supabase {resp.status_code}: {resp.text[:500]}")
        sys.exit(1)

    rows = resp.json()
    count = len(rows)
    logger.info(f"Received {count} rows")

    delta = abs(count - EXPECTED_ROW_COUNT) / EXPECTED_ROW_COUNT
    if delta > ROW_COUNT_TOLERANCE:
        logger.warning(
            f"Row count {count} differs from expected {EXPECTED_ROW_COUNT} "
            f"by {delta:.0%} (tolerance {ROW_COUNT_TOLERANCE:.0%}). "
            "Verify Supabase data before committing."
        )

    return rows


# ──────────────────────────────────────────────────────────────────────────────
# Row → manifest entry
# ──────────────────────────────────────────────────────────────────────────────
def _parse_date(raw: str | None) -> str | None:
    if not raw:
        return None
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00")).date().isoformat()
    except (ValueError, AttributeError):
        return None


def transform_row(row: dict) -> dict:
    row_id = row["id"]

    # ── Identity ──
    raw_name = (row.get("tool") or "").strip()
    name = NAME_OVERRIDES.get(row_id, raw_name)
    slug = SLUG_OVERRIDES.get(row_id, slug_from_name(name))
    aliases = ALIASES_OVERRIDES.get(row_id, [])

    # ── Classification ──
    domain = domain_from_supabase(row.get("domain"))
    status = status_from_supabase(row.get("status"))
    tool_type = type_from_supabase(row.get("type"))

    # ── Pillar ──
    pillar_name_raw = (row.get("pillar") or "").strip() or None
    pillar_num_raw = row.get("pillar_num")
    pillar_num = int(pillar_num_raw) if pillar_num_raw is not None else None
    computed_pillar = pillar_slug(domain, pillar_name_raw)
    unmapped = is_pillar_unmapped(domain, pillar_name_raw)

    if unmapped:
        logger.warning(
            f"PILLAR_UNMAPPED id={row_id} name={name!r} "
            f"domain={domain!r} pillar={pillar_name_raw!r}"
        )

    # ── Epistemic ──
    epistemic_label = row.get("epistemic_label")
    epistemic_level_raw = row.get("epistemic_level")
    epistemic_level = int(epistemic_level_raw) if epistemic_level_raw is not None else None
    version = version_from_epistemic_label(epistemic_label)

    # ── Dates ──
    updated_at_date = _parse_date(row.get("updated_at"))
    created_date = updated_at_date or TODAY
    built_date = updated_at_date if status == "live" else None

    # ── URL ──
    astro_url = row.get("url") or None
    if astro_url == "":
        astro_url = None

    # ── Card display ──
    is_greyed = bool(row.get("is_greyed_card"))
    card_pillar_label = CARD_PILLAR_LABEL_OVERRIDES.get(row_id, row.get("card_pillar_label"))
    greyed_pillar_label = GREYED_PILLAR_LABEL_OVERRIDES.get(row_id, row.get("greyed_pillar_label"))

    # ── Other fields ──
    source = SOURCE_OVERRIDES.get(row_id, row.get("source"))
    short_desc = SHORT_DESC_OVERRIDES.get(row_id, row.get("notes"))
    sort_order_raw = row.get("sort_order")
    sort_order = int(sort_order_raw) if sort_order_raw is not None else 9999
    supabase_table = "diagnostic_responses" if status == "live" else None
    tags = tags_from_entry(domain, status, tool_type, is_greyed)

    return {
        "supabase_id": row_id,
        "slug": slug,
        "name": name,
        "aliases": aliases,
        "type": tool_type,
        "status": status,
        "version": version,
        "short_description": short_desc,
        "long_description": None,
        "framework_mapping": {
            "domain": domain,
            "pillar": computed_pillar,
            "pillar_num": pillar_num,
            "pillar_name": pillar_name_raw,
        },
        "astro_url": astro_url,
        "supabase": {"table": supabase_table, "notes": ""},
        "source": source,
        "epistemic": {"level": epistemic_level, "label": epistemic_label},
        "card_display": {
            "pillar_label": card_pillar_label,
            "time": row.get("card_time"),
            "is_greyed": is_greyed,
            "greyed_pillar_label": greyed_pillar_label,
            "greyed_time": row.get("greyed_time"),
        },
        "related_tools": [],
        "dates": {
            "created": created_date,
            "last_updated": TODAY,
            "built": built_date,
            "archived": None,
        },
        "archived_reason": None,
        "aspirational_notes": "PILLAR_UNMAPPED — Paul to verify" if unmapped else None,
        "sort_order": sort_order,
        "tags": tags,
    }


# ──────────────────────────────────────────────────────────────────────────────
# YAML output helpers — preserve insertion order, use literal block for multiline
# ──────────────────────────────────────────────────────────────────────────────
class _LiteralStr(str):
    pass

def _literal_representer(dumper, data):
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")

class _ManifestDumper(yaml.Dumper):
    pass

_ManifestDumper.add_representer(_LiteralStr, _literal_representer)

def _prep(obj):
    """Recursively convert multiline strings to _LiteralStr for block-style output."""
    if isinstance(obj, dict):
        return {k: _prep(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_prep(v) for v in obj]
    if isinstance(obj, str) and "\n" in obj:
        return _LiteralStr(obj)
    return obj


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────
def main():
    logger.info("=== seed_tools.py start ===")

    rows = get_supabase_rows()

    entries = []
    slug_set: set[str] = set()
    pillar_unmapped: list[tuple] = []

    for row in rows:
        entry = transform_row(row)
        slug = entry["slug"]

        if slug in slug_set:
            logger.warning(f"DUPLICATE_SLUG id={row['id']} slug={slug!r} — check SLUG_OVERRIDES")
        slug_set.add(slug)

        if entry.get("aspirational_notes") and "PILLAR_UNMAPPED" in entry["aspirational_notes"]:
            pillar_unmapped.append((
                row["id"], entry["name"],
                entry["framework_mapping"]["domain"],
                entry["framework_mapping"]["pillar_name"],
            ))

        entries.append(entry)

    logger.info(f"Transformed {len(entries)} Supabase entries")

    # Append aspirational entries
    asp_added = 0
    for asp in ASPIRATIONAL_ENTRIES:
        if asp["slug"] in slug_set:
            logger.warning(f"Aspirational slug {asp['slug']!r} conflicts with Supabase entry — skipping")
            continue
        slug_set.add(asp["slug"])
        entries.append(asp)
        asp_added += 1

    logger.info(f"Appended {asp_added} aspirational entries → {len(entries)} total")

    if pillar_unmapped:
        count = len(pillar_unmapped)
        logger.warning(
            f"PILLAR_UNMAPPED total: {count} — "
            + "; ".join(f"id={i} {n!r}" for i, n, _, _ in pillar_unmapped)
        )
        if count > 3:
            logger.error(
                f"Stop-condition: {count} PILLAR_UNMAPPED entries exceeds threshold of 3. "
                "Resolve before committing (see aspirational_notes fields in output)."
            )
    else:
        logger.info("No PILLAR_UNMAPPED entries.")

    # Write manifest
    output_path = REPO_ROOT / "data" / "tools.yml"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    manifest = {
        "schema_version": "1.1.0",
        "last_updated": TODAY,
        "generator": "scripts/seed_tools.py",
        "tools": [_prep(e) for e in entries],
    }

    with open(output_path, "w", encoding="utf-8") as f:
        yaml.dump(
            manifest,
            f,
            Dumper=_ManifestDumper,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
            width=120,
        )

    size_bytes = output_path.stat().st_size
    line_count = sum(1 for _ in open(output_path, encoding="utf-8"))

    if size_bytes > MAX_OUTPUT_BYTES or line_count > MAX_OUTPUT_LINES:
        logger.error(
            f"Output sanity check failed: {size_bytes:,} bytes, {line_count:,} lines. "
            "Possible infinite loop — halting."
        )
        sys.exit(1)

    logger.info(f"Wrote {output_path} ({size_bytes:,} bytes, {line_count:,} lines)")
    logger.info("=== seed_tools.py done ===")

    # ── Summary to stdout for Paul ──
    from collections import Counter
    by_status = Counter(e["status"] for e in entries)
    by_domain = Counter(e["framework_mapping"]["domain"] for e in entries)

    print(f"\n{'='*60}")
    print(f"Seed complete: {len(entries)} total entries")
    print(f"  Supabase rows: {len(rows)}")
    print(f"  Aspirational:  {asp_added}")
    print(f"\nBy status:")
    for s, n in sorted(by_status.items()):
        print(f"  {s:<20} {n}")
    print(f"\nBy domain:")
    for d, n in sorted(by_domain.items()):
        print(f"  {d:<30} {n}")
    if pillar_unmapped:
        print(f"\nPILLAR_UNMAPPED ({len(pillar_unmapped)}):")
        for i, n, dom, pil in pillar_unmapped:
            print(f"  id={i:<4} {n!r:<45} domain={dom} pillar={pil!r}")
    else:
        print("\nPILLAR_UNMAPPED: none")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
