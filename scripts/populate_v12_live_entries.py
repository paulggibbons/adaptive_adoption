#!/usr/bin/env python3
"""
One-shot migration: populate v1.2 renderer fields on the 13 status: live
entries in data/tools.yml. Content was extracted verbatim from
pg-advisory-astro/src/pages/diagnostics/<slug>.astro on 2026-05-11.

Mirrors seed_tools.py's dumper config so the file diff stays minimal.

Usage:
  python scripts/populate_v12_live_entries.py

Idempotent — re-running on a populated manifest produces a no-op diff.
"""

import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).parent.parent
MANIFEST_PATH = REPO_ROOT / "data" / "tools.yml"

CHANGE_AGILITY_IMG = "/images/change-agility-diagram.png"
CHANGE_AGILITY_ALT = (
    "Change Agility framework — seven pillars from Master the Craft "
    "through Manage Ethics Always"
)
LEADERSHIP_DELTA_IMG = "/images/leadership-delta-diagram.png"
LEADERSHIP_DELTA_ALT = (
    "Leadership Delta framework — seven dimensions of AI leadership posture"
)
BG_IMG = "/images/behavioral-governance-diagram.png"
BG_ALT = (
    "Behavioral Governance framework — six dimensions including Decision "
    "Rights and Governance Intelligence"
)
CROSS_IMG = "/images/aa-triptych.png"
CROSS_ALT = (
    "Adaptive Adoption triptych — Change Agility, Leadership Delta, and "
    "Behavioral Governance"
)

MAILTO = "mailto:paul@paulgibbonsadvisory.com"

PATCHES: dict[str, dict] = {
    "adaptive-adoption-behavioral-index": {
        "hero_copy": "How mature is your organisation's AI adoption — really?",
        "hero_image": CROSS_IMG,
        "hero_image_alt": CROSS_ALT,
        "long_description": (
            "Twenty pillars across three domains: Change Agility, Leadership "
            "Delta, and Behavioral Governance. For each pillar, select the "
            "description that best matches your organisation today — not "
            "aspirationally, but as enacted behaviour you can actually "
            "observe. Takes around 15–20 minutes. Results include a full "
            "radar profile, domain breakdown, and your highest-leverage "
            "intervention target."
        ),
        "cta": {
            "primary": {"text": "Discuss your results with Paul", "url": MAILTO, "style": "primary"},
            "secondary": {"text": "All AI Tools", "url": "/diagnostics", "style": "secondary"},
        },
        "attribution": [
            "Original framework © Paul Gibbons · Adaptive Adoption™",
            "Layer 1 self-report · Not a validated psychometric · v0.1",
        ],
    },
    "ai-knowledge-quick-quiz": {
        "hero_copy": "Where do you stand on AI adoption? 12 questions, four levels.",
        "hero_image": CHANGE_AGILITY_IMG,
        "hero_image_alt": CHANGE_AGILITY_ALT,
        "long_description": (
            "12 questions across four mastery levels — User, Practitioner, "
            "Builder, Architect — each assessed on three dimensions: Know, "
            "Do, Build. Brutally honest answers only. Results appear after "
            "all 12 questions are answered."
        ),
        # NOTE: source page has placeholder href="#" primary; mailto from
        # "Want this for your team?" used until MkDocs Master the Craft
        # pillar URL is filled in.
        "cta": {
            "primary": {"text": "Want this for your team?", "url": MAILTO, "style": "primary"},
        },
        "attribution": [
            "Original framework — Gibbons (2026)",
            "Adaptive Adoption™ — Pillar 1: Master the Craft · v0.5",
        ],
    },
    "cynefin-domain-diagnostic": {
        "hero_copy": "Is your system complex?",
        "hero_image": CHANGE_AGILITY_IMG,
        "hero_image_alt": CHANGE_AGILITY_ALT,
        "long_description": (
            "Seven questions to diagnose which Cynefin domain your problem "
            "lives in — then a live reading that shifts with external "
            "turbulence. Based on Snowden & Boone's widely-cited framework "
            "for navigating complexity."
        ),
        "cta": {
            "primary": {"text": "Discuss this with Paul", "url": MAILTO, "style": "primary"},
            "secondary": {"text": "All AI Tools", "url": "/diagnostics", "style": "secondary"},
        },
        "attribution": [
            "Framework — Snowden & Boone (2007)",
            "Items original — Gibbons · v0.5",
        ],
    },
    "human-flourishing-at-work": {
        "hero_copy": "Are you flourishing at work?",
        "hero_image": LEADERSHIP_DELTA_IMG,
        "hero_image_alt": LEADERSHIP_DELTA_ALT,
        "long_description": (
            "Fifteen statements across five dimensions — Meaning, Engagement, "
            "Relationships, Excellence, and Positive Affect. Rate each 1–5. "
            "Takes about four minutes. Results are instant, private, and "
            "never stored."
        ),
        "cta": {
            "primary": {"text": "Discuss this with Paul", "url": MAILTO, "style": "primary"},
            "secondary": {"text": "All AI Tools", "url": "/diagnostics", "style": "secondary"},
        },
        "attribution": [
            "Framework — Seligman PERMA (2011)",
            "Items © Paul Gibbons · Not a clinical instrument",
        ],
    },
    "ikigai-diagnostic": {
        "hero_copy": "What is your reason for being?",
        "hero_image": CHANGE_AGILITY_IMG,
        "hero_image_alt": CHANGE_AGILITY_ALT,
        "long_description": (
            "Twelve scored statements across four dimensions — what you Love, "
            "what you're Good At, what the World Needs, and what you can be "
            "Paid For. Where all four converge is your *ikigai*. Takes about "
            "three minutes."
        ),
        "cta": {
            "primary": {"text": "Discuss this with Paul", "url": MAILTO, "style": "primary"},
            "secondary": {"text": "All AI Tools", "url": "/diagnostics", "style": "secondary"},
        },
        "attribution": [
            "Traditional framework — Japanese ikigai tradition",
            "Items © Paul Gibbons (Spirituality of Work and Leadership) · Reflective, not normative",
        ],
    },
    "ai-mastery-assessment": {
        "hero_copy": "AI literacy was 2025. Where are you on the path to AI Mastery?",
        "hero_image": CHANGE_AGILITY_IMG,
        "hero_image_alt": CHANGE_AGILITY_ALT,
        "long_description": (
            "A 21-question behavioral self-assessment across 7 dimensions of "
            "AI mastery — from Civics and Ethics to Creativity and "
            "Orchestration. Each question describes four levels of practice. "
            "Choose the one that most honestly reflects how you actually "
            "work, not how you aspire to work. The output is a scored "
            "mastery profile with radar chart, dimension-by-dimension "
            "breakdown, and a downloadable development brief."
        ),
        "cta": {
            "primary": {"text": "Discuss your mastery profile with Paul", "url": MAILTO, "style": "primary"},
            "secondary": {"text": "All AI Tools", "url": "/diagnostics", "style": "secondary"},
        },
        "attribution": [
            "Structured self-assessment · AI Mastery Framework",
            "Original — Gibbons (2026) · v0.1",
        ],
    },
    "personal-context-passport": {
        "hero_copy": "Stop re-explaining yourself to every AI.",
        "hero_image": LEADERSHIP_DELTA_IMG,
        "hero_image_alt": LEADERSHIP_DELTA_ALT,
        "long_description": (
            "A guided interview across 8 sections — identity, work, ideas, "
            "goals, voice, tools, agent instructions, and privacy. The "
            "output is a portable context artifact: a Markdown file, a JSON "
            "file, and a compact agent brief you can paste into any AI "
            "system. Nothing is stored. Everything downloads to you."
        ),
        "cta": {
            "primary": {"text": "Discuss this with Paul", "url": MAILTO, "style": "primary"},
            "secondary": {"text": "All AI Tools", "url": "/diagnostics", "style": "secondary"},
        },
        "attribution": [
            "Structured self-authored artifact · Not psychometric",
            "Original — Gibbons (2026) · v0.1",
        ],
    },
    "creative-climate-diagnostic": {
        "hero_copy": "Assess your organization's creative climate across 10 dimensions.",
        "hero_image": LEADERSHIP_DELTA_IMG,
        "hero_image_alt": LEADERSHIP_DELTA_ALT,
        "long_description": (
            "Ten dimensions of organizational climate that predict creative "
            "performance — nine positively correlated, one (Conflict) "
            "negatively. Rate each question on a 1–5 frequency scale. All "
            "questions are behavioral: they ask what you *do* or observe, "
            "not what you think or believe."
        ),
        # NOTE: source page has placeholder href="#" primary; mailto used
        # until MkDocs Creative Cultivation pillar URL is filled in.
        "cta": {
            "primary": {"text": "Want this for your team?", "url": MAILTO, "style": "primary"},
        },
        "attribution": [
            "Based on Ekvall, G. (1996). Organizational climate for creativity and innovation. European Journal of Work and Organizational Psychology, 5(1), 105–123.",
            "Questions adapted for behavioral framing · © Paul Gibbons Advisory · v0.3",
        ],
    },
    "rist-trust-diagnostic": {
        "hero_copy": "Four dimensions of trust that predict successful AI adoption.",
        "hero_image": CHANGE_AGILITY_IMG,
        "hero_image_alt": CHANGE_AGILITY_ALT,
        "long_description": (
            "Four dimensions of trust that predict successful AI adoption — "
            "all require calibration, not maximization. Trust exists on a "
            "spectrum: undertrust and overtrust are both failure modes. Rate "
            "each question on a 1–5 frequency scale. All questions are "
            "behavioral: they ask what you *do* or observe, not what you "
            "think or believe."
        ),
        # NOTE: source page has placeholder href="#" primary; mailto used
        # until MkDocs Trust Calibration pillar URL is filled in.
        "cta": {
            "primary": {"text": "Want this for your team?", "url": MAILTO, "style": "primary"},
        },
        "attribution": [
            "Gibbons, P. (2025). RIST Framework™, in Adopting AI.",
            "Original operationalization · Construct validation planned · v0.3",
        ],
    },
    "causal-loop-diagram-builder": {
        "hero_copy": "Map feedback loops. Reinforcing and Balancing loops detected automatically.",
        "hero_image": LEADERSHIP_DELTA_IMG,
        "hero_image_alt": LEADERSHIP_DELTA_ALT,
        "long_description": (
            "Map feedback loops in your change system. Add variables, "
            "connect them, toggle polarity — Reinforcing (R) and Balancing "
            "(B) loops detected automatically."
        ),
        "cta": {
            "primary": {"text": "Discuss this with Paul", "url": MAILTO, "style": "primary"},
            "secondary": {"text": "All AI Tools", "url": "/diagnostics", "style": "secondary"},
        },
        "attribution": [
            "Systems thinking tool — Meadows (2008)",
            "Educational / exploratory · Not a psychometric",
        ],
    },
    "leadership-delta-scoresheet": {
        "hero_copy": "Score your leadership team's AI posture across 7 dimensions. Compare up to 4 teams.",
        "hero_image": LEADERSHIP_DELTA_IMG,
        "hero_image_alt": LEADERSHIP_DELTA_ALT,
        "long_description": (
            "A consultant-grade diagnostic built on the Leadership Delta "
            "framework. Each of the 7 dimensions has 3 observable indicators "
            "scored 1–5. Total score out of 105. Designed for CAIOs, "
            "transformation leads, and advisors assessing one or multiple "
            "leadership teams side by side. Produces a radar chart "
            "comparison and downloadable reports per team and cross-team."
        ),
        "cta": {
            "primary": {"text": "Discuss this with Paul", "url": MAILTO, "style": "primary"},
            "secondary": {"text": "AI Mastery Assessment", "url": "/diagnostics/ai-mastery-assessment", "style": "secondary"},
        },
        "attribution": [
            "Consultant-grade diagnostic · AI Leadership Delta™",
            "Original — Gibbons (2026) · v0.1",
        ],
    },
    "ai-governance-gap-finder": {
        "hero_copy": "Where are the gaps between your governance policies and practice?",
        "hero_image": BG_IMG,
        "hero_image_alt": BG_ALT,
        "long_description": (
            "A 6-dimension diagnostic built on the Three-Layer Assessment "
            "Protocol — Self-Report, Evidence, and Behavioral Observation. "
            "The gap between layers 1 and 3 is the Enacted Gap: the "
            "governance maturity signal that lives in behavior, not in "
            "binders."
        ),
        "cta": {
            "primary": {"text": "Discuss this with Paul", "url": MAILTO, "style": "primary"},
            "secondary": {"text": "All AI Tools", "url": "/diagnostics", "style": "secondary"},
        },
        "attribution": [
            "Structured self-assessment artifact · Three-Layer Protocol",
            "Original — Gibbons (2026) · v0.1",
        ],
    },
    "decision-rights-quick-map": {
        "hero_copy": "Who can say yes to AI in your organization? Map it in 5 minutes.",
        "hero_image": BG_IMG,
        "hero_image_alt": BG_ALT,
        "long_description": (
            "Eight questions about AI decision authority. The output is a "
            "structured Decision Rights Map — showing who has authority over "
            "what, your Decision Velocity score, and your Shadow AI Risk "
            "rating. If the approval path takes longer than a sprint cycle, "
            "people will build in the dark."
        ),
        "cta": {
            "primary": {"text": "Discuss this with Paul", "url": MAILTO, "style": "primary"},
            "secondary": {"text": "Full Gap Finder", "url": "/diagnostics/governance-gap-finder", "style": "secondary"},
        },
        "attribution": [
            "Structured self-assessment artifact · Decision Rights dimension",
            "Original — Gibbons (2026) · v0.1",
        ],
    },
}


class LiteralStr(str):
    """Tag a string to force YAML literal-block (|) representation."""


class _ManifestDumper(yaml.SafeDumper):
    pass


def _literal_str_representer(dumper, data):
    return dumper.represent_scalar("tag:yaml.org,2002:str", str(data), style="|")


_ManifestDumper.add_representer(LiteralStr, _literal_str_representer)


def patch_entry(entry: dict, patch: dict) -> dict:
    """Rebuild entry preserving key order, inserting v1.2 fields after astro_url."""
    rebuilt: dict = {}
    new_keys = ("hero_copy", "hero_image", "hero_image_alt", "cta", "attribution")
    for key, value in entry.items():
        # Overwrite long_description in its existing slot
        if key == "long_description" and "long_description" in patch:
            rebuilt[key] = patch["long_description"]
        else:
            rebuilt[key] = value
        # After astro_url, insert renderer fields
        if key == "astro_url":
            for new_key in new_keys:
                if new_key in patch:
                    rebuilt[new_key] = patch[new_key]
    return rebuilt


def main() -> int:
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        manifest = yaml.safe_load(f)

    patched_count = 0
    for i, entry in enumerate(manifest["tools"]):
        slug = entry.get("slug")
        if slug not in PATCHES:
            continue
        if entry.get("status") != "live":
            print(f"SKIP {slug}: not status=live (status={entry.get('status')!r})", file=sys.stderr)
            continue
        patch = dict(PATCHES[slug])
        if "long_description" in patch:
            patch["long_description"] = LiteralStr(patch["long_description"])
        manifest["tools"][i] = patch_entry(entry, patch)
        patched_count += 1

    print(f"Patched {patched_count} live entries (expected 13)", file=sys.stderr)
    if patched_count != 13:
        print(f"ERROR expected 13, got {patched_count}", file=sys.stderr)
        return 1

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        yaml.dump(
            manifest,
            f,
            Dumper=_ManifestDumper,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
            width=120,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
