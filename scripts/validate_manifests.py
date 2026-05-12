#!/usr/bin/env python3
"""
Validate data/*.yml against schemas/*.schema.json.

Usage:
  python scripts/validate_manifests.py

Exits 0 on success, non-zero on any hard-fail.
Used in CI from Phase 2.
"""

import json
import logging
import sys
from collections import Counter
from pathlib import Path

import yaml
import jsonschema
from jsonschema import Draft202012Validator

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT / "data"
SCHEMAS_DIR = REPO_ROOT / "schemas"


LIVE_REQUIRED_FIELDS = ("long_description", "hero_image", "hero_image_alt", "cta")
RELATIONSHIP_ENUM = {"predecessor", "successor", "complementary", "see-also"}
EMBED_TYPE_ENUM = {"iframe", "typeform", "google_form", "custom_html"}


def check_v12_rules(entry: dict, all_slugs: set[str]) -> list[str]:
    """v1.2 conditional checks not expressible in JSON Schema alone.

    Lives here (not in the schema) so non-live entries can carry partial
    data while live entries get the full strict treatment.
    """
    slug = entry.get("slug", "<no-slug>")
    errs: list[str] = []

    if entry.get("status") == "live":
        for field in LIVE_REQUIRED_FIELDS:
            if not entry.get(field):
                errs.append(f"{slug}: status=live requires '{field}'")
        cta = entry.get("cta") or {}
        primary = cta.get("primary") if isinstance(cta, dict) else None
        if not primary:
            errs.append(f"{slug}: cta.primary is required for status=live")
        elif not (primary.get("text") and primary.get("url")):
            errs.append(f"{slug}: cta.primary needs both 'text' and 'url'")

    for rel in entry.get("related_tools", []) or []:
        ref = rel.get("slug") if isinstance(rel, dict) else None
        if not ref:
            errs.append(f"{slug}: related_tools entry missing 'slug'")
            continue
        if ref not in all_slugs:
            errs.append(f"{slug}: related_tools references unknown slug {ref!r}")
        relationship = rel.get("relationship")
        if relationship not in RELATIONSHIP_ENUM:
            errs.append(
                f"{slug}: related_tools[{ref}] has invalid relationship {relationship!r}"
            )

    embed = entry.get("embed")
    if isinstance(embed, dict):
        etype = embed.get("type")
        if etype not in EMBED_TYPE_ENUM:
            errs.append(f"{slug}: invalid embed.type {etype!r}")
        elif etype == "custom_html" and not embed.get("html"):
            errs.append(f"{slug}: embed.type=custom_html requires 'html'")
        elif etype in {"iframe", "typeform", "google_form"} and not embed.get("url"):
            errs.append(f"{slug}: embed.type={etype} requires 'url'")

    return errs


def validate_manifest(manifest_path: Path, schema: dict) -> tuple[int, int]:
    """Validate one manifest. Returns (error_count, warning_count)."""
    with open(manifest_path, encoding="utf-8") as f:
        manifest = yaml.safe_load(f)

    if not isinstance(manifest, dict) or "tools" not in manifest:
        logger.error(f"{manifest_path.name}: Missing top-level 'tools' key")
        return 1, 0

    tools = manifest["tools"]
    validator = Draft202012Validator(schema)
    errors = []
    warnings = []
    slugs = [
        entry.get("slug", f"<no-slug id={entry.get('supabase_id', '?')}>")
        for entry in tools
    ]
    all_slugs = set(slugs)

    for entry in tools:
        slug = entry.get("slug", f"<no-slug id={entry.get('supabase_id', '?')}>")

        for err in validator.iter_errors(entry):
            field = " → ".join(str(p) for p in err.absolute_path) or "(root)"
            msg = f"slug={slug!r} [{field}]: {err.message}"
            errors.append(msg)
            logger.error(f"FAIL {msg}")

        for v12_err in check_v12_rules(entry, all_slugs):
            errors.append(v12_err)
            logger.error(f"FAIL {v12_err}")

        # Warn-only: PILLAR_UNMAPPED in aspirational_notes
        note = entry.get("aspirational_notes") or ""
        if "PILLAR_UNMAPPED" in note:
            warnings.append(f"WARN slug={slug!r}: PILLAR_UNMAPPED — Paul to verify")

    # Slug uniqueness check (not enforceable in JSON Schema alone)
    for slug, count in Counter(slugs).items():
        if count > 1:
            msg = f"DUPLICATE_SLUG {slug!r} appears {count} times"
            errors.append(msg)
            logger.error(msg)

    for w in warnings:
        logger.warning(w)

    logger.info(
        f"{manifest_path.name}: {len(tools)} entries — "
        f"{len(errors)} errors, {len(warnings)} warnings"
    )
    return len(errors), len(warnings)


def main():
    logger.info("=== validate_manifests.py start ===")

    schema_path = SCHEMAS_DIR / "tools.schema.json"
    if not schema_path.exists():
        logger.error(f"Schema not found: {schema_path}")
        sys.exit(1)

    with open(schema_path, encoding="utf-8") as f:
        schema = json.load(f)

    manifest_paths = sorted(DATA_DIR.glob("*.yml"))
    if not manifest_paths:
        logger.error(f"No .yml files found in {DATA_DIR}")
        sys.exit(1)

    total_errors = 0
    total_warnings = 0
    for mp in manifest_paths:
        e, w = validate_manifest(mp, schema)
        total_errors += e
        total_warnings += w

    if total_errors == 0:
        logger.info(f"=== All manifests valid ({total_warnings} warnings) ===")
        sys.exit(0)
    else:
        logger.error(f"=== Validation FAILED: {total_errors} errors, {total_warnings} warnings ===")
        sys.exit(1)


if __name__ == "__main__":
    main()
