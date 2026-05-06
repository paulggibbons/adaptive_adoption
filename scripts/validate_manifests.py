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
    slugs = []

    for entry in tools:
        slug = entry.get("slug", f"<no-slug id={entry.get('supabase_id', '?')}>")
        slugs.append(slug)

        for err in validator.iter_errors(entry):
            field = " → ".join(str(p) for p in err.absolute_path) or "(root)"
            msg = f"slug={slug!r} [{field}]: {err.message}"
            errors.append(msg)
            logger.error(f"FAIL {msg}")

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
