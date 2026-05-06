"""Identify Supabase rows where pillar_num doesn't match the canonical mkdocs.yml slug prefix."""
import yaml, re, sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent

with open(REPO_ROOT / "data" / "tools.yml", encoding="utf-8") as f:
    manifest = yaml.safe_load(f)

corrections = []
for entry in manifest["tools"]:
    if not entry.get("supabase_id"):
        continue
    fm = entry.get("framework_mapping", {})
    pillar_slug = fm.get("pillar")
    pillar_num = fm.get("pillar_num")
    if pillar_slug and pillar_num is not None:
        m = re.match(r"^(\d+)-", pillar_slug)
        if m:
            canonical_num = int(m.group(1))
            if canonical_num != pillar_num:
                corrections.append({
                    "id": entry["supabase_id"],
                    "name": entry["name"],
                    "domain": fm.get("domain"),
                    "pillar_name": fm.get("pillar_name"),
                    "pillar_slug": pillar_slug,
                    "canonical_num": canonical_num,
                    "supabase_pillar_num": pillar_num,
                })

print(f"Found {len(corrections)} stale pillar_num rows")
for c in corrections:
    print(
        f"  id={c['id']:<4} supabase_num={c['supabase_pillar_num']} "
        f"canonical={c['canonical_num']} slug={c['pillar_slug']:<40} "
        f"name={c['name']!r}"
    )

# Write JSON for corrections doc generation
import json
print("\nJSON:")
print(json.dumps(corrections, indent=2))
