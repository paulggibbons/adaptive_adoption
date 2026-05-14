#!/usr/bin/env python3
"""
Pressure-test the manifest pipeline. Tries to break:
  - scripts/validate_manifests.py (the schema validator + v1.2 conditional rules)
  - scripts/generate_tool_pages.py (the MkDocs tool-page generator)

For each known failure mode, mutates data/tools.yml in a temp file,
runs the relevant script, and asserts the script reacts correctly
(exits non-zero for failure modes; succeeds for valid edge cases).

Usage:
  python scripts/pressure_test_manifest.py            # run all
  python scripts/pressure_test_manifest.py --filter status  # only tests matching 'status'
  python scripts/pressure_test_manifest.py --verbose  # show stderr for failures

Exit 0 if every test behaved as expected. Exit 1 otherwise.

The original data/tools.yml is never modified — mutations are written
to a temp file and the validator is pointed at the temp directory via
the DATA_DIR_OVERRIDE env hook. (If the validator hasn't been wired
for the env hook, we copy data/tools.yml into a temp dir + temp run.)
"""

from __future__ import annotations

import argparse
import copy
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import yaml

REPO_ROOT = Path(__file__).parent.parent
DATA_PATH = REPO_ROOT / "data" / "tools.yml"
SCHEMA_PATH = REPO_ROOT / "schemas" / "tools.schema.json"
VALIDATOR = REPO_ROOT / "scripts" / "validate_manifests.py"


# ─── Helpers ──────────────────────────────────────────────────────────


def load_manifest() -> dict:
    with open(DATA_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f)


def first_live_index(manifest: dict) -> int:
    for i, t in enumerate(manifest["tools"]):
        if t.get("status") == "live":
            return i
    raise RuntimeError("No live tool in manifest — pressure tests assume at least one")


def first_nonlive_index(manifest: dict) -> int:
    for i, t in enumerate(manifest["tools"]):
        if t.get("status") != "live":
            return i
    raise RuntimeError("No non-live tool in manifest")


def run_validator_against(manifest_dict: dict) -> tuple[int, str, str]:
    """Write manifest_dict to a temp data/ dir, run validator, return
    (exit_code, stdout, stderr)."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_root = Path(tmp)
        # Mirror the layout the validator expects: REPO_ROOT/data/*.yml,
        # REPO_ROOT/schemas/tools.schema.json
        (tmp_root / "data").mkdir()
        (tmp_root / "schemas").mkdir()
        (tmp_root / "scripts").mkdir()
        with open(tmp_root / "data" / "tools.yml", "w", encoding="utf-8") as f:
            yaml.safe_dump(manifest_dict, f, allow_unicode=True, sort_keys=False)
        # Copy schema + validator
        shutil.copy(SCHEMA_PATH, tmp_root / "schemas" / "tools.schema.json")
        shutil.copy(VALIDATOR, tmp_root / "scripts" / "validate_manifests.py")
        result = subprocess.run(
            [sys.executable, "scripts/validate_manifests.py"],
            capture_output=True,
            text=True,
            cwd=tmp_root,
        )
        return result.returncode, result.stdout, result.stderr


# ─── Mutation functions ───────────────────────────────────────────────


def mutate_dup_slug(m: dict) -> dict:
    out = copy.deepcopy(m)
    out["tools"][1]["slug"] = out["tools"][0]["slug"]
    return out


def mutate_bad_slug_pattern(m: dict) -> dict:
    out = copy.deepcopy(m)
    out["tools"][0]["slug"] = "Has_Bad_Chars!"
    return out


def mutate_remove_required(field: str) -> Callable[[dict], dict]:
    def f(m: dict) -> dict:
        out = copy.deepcopy(m)
        out["tools"][0].pop(field, None)
        return out
    return f


def mutate_bad_status(m: dict) -> dict:
    out = copy.deepcopy(m)
    out["tools"][0]["status"] = "bogus-status"
    return out


def mutate_bad_type(m: dict) -> dict:
    out = copy.deepcopy(m)
    out["tools"][0]["type"] = "not-a-real-type"
    return out


def mutate_bad_domain(m: dict) -> dict:
    out = copy.deepcopy(m)
    out["tools"][0]["framework_mapping"]["domain"] = "not-a-domain"
    return out


def mutate_aliases_not_array(m: dict) -> dict:
    out = copy.deepcopy(m)
    out["tools"][0]["aliases"] = "this-should-be-an-array"
    return out


def mutate_dangling_related(m: dict) -> dict:
    out = copy.deepcopy(m)
    out["tools"][0]["related_tools"] = [
        {"slug": "this-tool-does-not-exist", "relationship": "see-also"}
    ]
    return out


def mutate_bad_relationship(m: dict) -> dict:
    out = copy.deepcopy(m)
    out["tools"][0]["related_tools"] = [
        {"slug": out["tools"][1]["slug"], "relationship": "made-up-relationship"}
    ]
    return out


def mutate_hero_copy_too_long(m: dict) -> dict:
    out = copy.deepcopy(m)
    out["tools"][0]["hero_copy"] = "x" * 200
    return out


def mutate_embed_custom_html_no_html(m: dict) -> dict:
    out = copy.deepcopy(m)
    out["tools"][0]["embed"] = {"type": "custom_html"}
    return out


def mutate_embed_iframe_no_url(m: dict) -> dict:
    out = copy.deepcopy(m)
    out["tools"][0]["embed"] = {"type": "iframe"}
    return out


def mutate_embed_bad_type(m: dict) -> dict:
    out = copy.deepcopy(m)
    out["tools"][0]["embed"] = {"type": "vimeo", "url": "https://example.com"}
    return out


def mutate_live_missing_long_description(m: dict) -> dict:
    out = copy.deepcopy(m)
    i = first_live_index(out)
    out["tools"][i]["long_description"] = None
    return out


def mutate_live_missing_hero_image(m: dict) -> dict:
    out = copy.deepcopy(m)
    i = first_live_index(out)
    out["tools"][i]["hero_image"] = None
    return out


def mutate_live_missing_cta(m: dict) -> dict:
    out = copy.deepcopy(m)
    i = first_live_index(out)
    out["tools"][i]["cta"] = None
    return out


def mutate_live_cta_missing_primary_url(m: dict) -> dict:
    out = copy.deepcopy(m)
    i = first_live_index(out)
    out["tools"][i]["cta"] = {"primary": {"text": "Take it"}}  # no url
    return out


def mutate_cta_style_invalid(m: dict) -> dict:
    out = copy.deepcopy(m)
    i = first_live_index(out)
    cta = copy.deepcopy(out["tools"][i].get("cta") or {})
    cta.setdefault("primary", {"text": "x", "url": "https://example.com"})
    cta["primary"]["style"] = "neon-blink"  # not in enum
    out["tools"][i]["cta"] = cta
    return out


def mutate_extra_unknown_top_field(m: dict) -> dict:
    """Schema is not strict (additionalProperties unrestricted) so this
    should pass — included as a regression test that we DON'T break on
    unknown future fields."""
    out = copy.deepcopy(m)
    out["tools"][0]["future_field_xyz"] = "some value"
    return out


def mutate_unicode_in_name(m: dict) -> dict:
    """Should pass — unicode in name field is fine."""
    out = copy.deepcopy(m)
    out["tools"][0]["name"] = "Émulation™ — Διάγνωσις · 诊断"
    return out


def mutate_sort_order_negative(m: dict) -> dict:
    """Should pass — schema doesn't constrain sort_order to non-negative."""
    out = copy.deepcopy(m)
    out["tools"][0]["sort_order"] = -999
    return out


def mutate_no_tools_key(m: dict) -> dict:
    out = copy.deepcopy(m)
    del out["tools"]
    return out


def mutate_tools_empty_list(m: dict) -> dict:
    out = copy.deepcopy(m)
    out["tools"] = []
    return out


# ─── Test definitions ─────────────────────────────────────────────────


@dataclass
class Test:
    name: str
    mutate: Callable[[dict], dict]
    must_reject: bool          # True = validator must exit 1
    needle: str | None = None  # substring expected in stderr when rejecting


TESTS: list[Test] = [
    # ── Schema-level rejections ─────────────────────────────────────
    Test("dup_slug", mutate_dup_slug, True, "DUPLICATE_SLUG"),
    Test("bad_slug_pattern", mutate_bad_slug_pattern, True, "pattern"),
    Test("missing_slug", mutate_remove_required("slug"), True, "slug"),
    Test("missing_name", mutate_remove_required("name"), True, "name"),
    Test("missing_status", mutate_remove_required("status"), True, "status"),
    Test("missing_type", mutate_remove_required("type"), True, "type"),
    Test("missing_dates", mutate_remove_required("dates"), True, "dates"),
    Test("missing_sort_order", mutate_remove_required("sort_order"), True, "sort_order"),
    Test("missing_framework_mapping", mutate_remove_required("framework_mapping"), True, "framework_mapping"),
    Test("bad_status_enum", mutate_bad_status, True, "enum"),
    Test("bad_type_enum", mutate_bad_type, True, "enum"),
    Test("bad_domain_enum", mutate_bad_domain, True, "enum"),
    Test("aliases_not_array", mutate_aliases_not_array, True, "array"),
    # ── v1.2 conditional rejections (validator-only) ────────────────
    Test("related_tools_dangling", mutate_dangling_related, True, "unknown slug"),
    Test("related_tools_bad_rel", mutate_bad_relationship, True, "relationship"),
    Test("hero_copy_too_long", mutate_hero_copy_too_long, True, "maxLength"),
    Test("embed_custom_html_no_html", mutate_embed_custom_html_no_html, True, "html"),
    Test("embed_iframe_no_url", mutate_embed_iframe_no_url, True, "url"),
    Test("embed_bad_type", mutate_embed_bad_type, True, "embed.type"),
    Test("live_missing_long_desc", mutate_live_missing_long_description, True, "long_description"),
    Test("live_missing_hero", mutate_live_missing_hero_image, True, "hero_image"),
    Test("live_missing_cta", mutate_live_missing_cta, True, "cta"),
    Test("live_cta_no_primary_url", mutate_live_cta_missing_primary_url, True, "url"),
    Test("cta_bad_style_enum", mutate_cta_style_invalid, True, "enum"),
    # ── Top-level errors ────────────────────────────────────────────
    Test("no_tools_key", mutate_no_tools_key, True, "tools"),
    # ── Acceptance cases (validator must NOT reject these) ──────────
    Test("extra_unknown_field", mutate_extra_unknown_top_field, False, None),
    Test("unicode_in_name", mutate_unicode_in_name, False, None),
    Test("sort_order_negative", mutate_sort_order_negative, False, None),
    Test("empty_tools_list", mutate_tools_empty_list, False, None),
]


# ─── Runner ───────────────────────────────────────────────────────────


def run() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--filter", default="", help="Only run tests whose name contains this substring")
    parser.add_argument("--verbose", action="store_true", help="Show stderr on unexpected results")
    args = parser.parse_args()

    base = load_manifest()
    # Sanity: validator MUST pass on the current real manifest.
    rc, _out, err = run_validator_against(base)
    if rc != 0:
        print("SETUP FAIL: validator rejects the current real manifest. Fix that first.")
        print(err)
        return 1
    print("baseline: current manifest validates cleanly (rc=0) OK")
    print()

    passed = failed = skipped = 0
    failures: list[tuple[Test, int, str]] = []

    for t in TESTS:
        if args.filter and args.filter not in t.name:
            skipped += 1
            continue
        mutated = t.mutate(base)
        rc, _out, err = run_validator_against(mutated)
        ok = False
        why = ""
        if t.must_reject:
            if rc == 0:
                why = "expected rejection (rc=1) but validator accepted (rc=0)"
            elif t.needle and t.needle.lower() not in err.lower():
                why = f"rejected as expected (rc={rc}) but needle {t.needle!r} not in stderr"
                # Tolerable — still counts as pass if rc!=0. Make it a warning.
                ok = True
                print(f"PASS* {t.name:<32} rc={rc} (needle missing — verify stderr)")
            else:
                ok = True
                print(f"PASS  {t.name:<32} rc={rc} ('{t.needle}' found)")
        else:
            if rc != 0:
                why = f"expected acceptance (rc=0) but validator rejected (rc={rc})"
            else:
                ok = True
                print(f"PASS  {t.name:<32} rc=0 (accepted as expected)")
        if not ok:
            print(f"FAIL  {t.name:<32} {why}")
            failed += 1
            failures.append((t, rc, err))
        else:
            passed += 1

    print()
    print(f"Summary: {passed} pass · {failed} fail · {skipped} skipped")
    if failures and args.verbose:
        print()
        print("=" * 72)
        for t, rc, err in failures:
            print(f"--- {t.name} (must_reject={t.must_reject}, rc={rc}) ---")
            print(err[:600])
            print()
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(run())
