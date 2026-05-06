#!/usr/bin/env python3
"""
Generate MkDocs pages from data/tools.yml.

Reads the canonical tool manifest, renders Jinja2 templates, writes generated
markdown into content/ before mkdocs build.

Outputs:
  content/change-agility/tools/index.md
  content/leadership-delta/tools/index.md
  content/behavioral-governance/tools/index.md
  content/tools/index.md
  content/tools/long-list.md
  content/tools/archive.md

Idempotent. Safe to re-run. All output files carry an AUTO-GENERATED header.
"""

import logging
import sys
from collections import defaultdict
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

# ── Configuration ─────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "data" / "tools.yml"
TEMPLATE_DIR = REPO_ROOT / "scripts" / "templates"
CONTENT_DIR = REPO_ROOT / "content"
ASTRO_BASE = "https://paulgibbonsadvisory.com"

DOMAIN_DISPLAY_NAMES = {
    "change-agility":        "Change Agility",
    "leadership-delta":      "Leadership Delta",
    "behavioral-governance": "Behavioral Governance",
    "cross-cutting":         "Cross-cutting",
}

DOMAIN_INTROS = {
    "change-agility": (
        "Practitioner tools across the seven Change Agility pillars. Each tool "
        "produces actionable output — a decision, a diagnosis, or a design input "
        "— not a report for its own sake."
    ),
    "leadership-delta": (
        "Tools for closing the Leadership Delta — the gap between current "
        "leadership capability and what AI-era leadership demands. Most assess "
        "the conditions that enable leadership behavior change, not the "
        "leader in isolation."
    ),
    "behavioral-governance": (
        "Governance tools for adoption rather than prevention. These instruments "
        "make decision rights, agent authority, and risk intelligence "
        "operational — not just declared."
    ),
    "cross-cutting": (
        "Tools that span multiple pillars or sit above the framework's "
        "three-discipline split."
    ),
}

# Render order within domain pages
STATUS_DISPLAY_ORDER = [
    "live", "build-next", "in-development", "planned", "speculative", "archived",
]

# Domains that get their own page (cross-cutting surfaces only in All Tools)
DOMAIN_PAGES = ["change-agility", "leadership-delta", "behavioral-governance"]

# ── Logging ───────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    stream=sys.stderr,
)
log = logging.getLogger(__name__)


# ── Manifest loading ──────────────────────────────────────────────────────────

def load_manifest() -> list:
    """Load manifest and return the tools list."""
    if not MANIFEST_PATH.exists():
        log.error("Manifest not found at %s", MANIFEST_PATH)
        sys.exit(1)
    with MANIFEST_PATH.open(encoding="utf-8") as f:
        manifest = yaml.safe_load(f)
    if "tools" not in manifest:
        log.error("Manifest missing 'tools' key")
        sys.exit(1)
    tools = manifest["tools"]
    log.info("Loaded %d tools from %s", len(tools), MANIFEST_PATH)
    return tools


# ── Grouping helpers ──────────────────────────────────────────────────────────

def group_by_domain(tools: list) -> dict:
    """Return dict domain → sorted tool list."""
    by_domain: dict = defaultdict(list)
    for t in tools:
        by_domain[t["framework_mapping"]["domain"]].append(t)
    for domain in by_domain:
        by_domain[domain].sort(key=lambda t: (t.get("sort_order") or 9999))
    return dict(by_domain)


def group_by_status(tools: list) -> dict:
    """Return dict status → sorted tool list, ordered by STATUS_DISPLAY_ORDER."""
    grouped: dict = defaultdict(list)
    for t in tools:
        grouped[t["status"]].append(t)
    for status in grouped:
        grouped[status].sort(key=lambda t: (t.get("sort_order") or 9999))
    # Return with all status keys present (empty lists for missing)
    return {s: grouped.get(s, []) for s in STATUS_DISPLAY_ORDER}


# ── Rendering ─────────────────────────────────────────────────────────────────

def make_env() -> Environment:
    return Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=select_autoescape(disabled_extensions=("md", "j2")),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )


def render_domain_pages(env: Environment, tools_by_domain: dict) -> int:
    """Render per-domain tool index pages. Returns count of files written."""
    template = env.get_template("domain_tools_index.md.j2")
    written = 0
    for domain in DOMAIN_PAGES:
        domain_tools = tools_by_domain.get(domain, [])
        if not domain_tools:
            log.warning("No tools found for domain %r — page will be empty", domain)
        out_path = CONTENT_DIR / domain / "tools" / "index.md"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        rendered = template.render(
            domain_slug=domain,
            domain_display_name=DOMAIN_DISPLAY_NAMES[domain],
            domain_intro=DOMAIN_INTROS[domain],
            tools_by_status=group_by_status(domain_tools),
            astro_base=ASTRO_BASE,
        )
        out_path.write_text(rendered, encoding="utf-8")
        log.info("Wrote %s (%d tools)", out_path.relative_to(REPO_ROOT), len(domain_tools))
        written += 1
    return written


def render_all_tools(env: Environment, tools: list, tools_by_domain: dict) -> None:
    """Render the master All Tools page."""
    out_path = CONTENT_DIR / "tools" / "index.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    template = env.get_template("all_tools.md.j2")
    rendered = template.render(
        tools=tools,
        tools_by_domain=tools_by_domain,
        domain_display_names=DOMAIN_DISPLAY_NAMES,
        domain_count=len(tools_by_domain),
        status_count=len({t["status"] for t in tools}),
        astro_base=ASTRO_BASE,
    )
    out_path.write_text(rendered, encoding="utf-8")
    log.info("Wrote %s (%d tools)", out_path.relative_to(REPO_ROOT), len(tools))


def render_long_list(env: Environment, tools: list) -> None:
    """Render the Long List page (build-next + in-dev + planned + speculative)."""
    long_list_tools = [
        t for t in tools
        if t["status"] in ("build-next", "in-development", "planned", "speculative")
    ]
    out_path = CONTENT_DIR / "tools" / "long-list.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    template = env.get_template("long_list.md.j2")
    rendered = template.render(
        long_list_tools=long_list_tools,
        tools_by_status=group_by_status(long_list_tools),
        domain_display_names=DOMAIN_DISPLAY_NAMES,
    )
    out_path.write_text(rendered, encoding="utf-8")
    log.info("Wrote %s (%d tools)", out_path.relative_to(REPO_ROOT), len(long_list_tools))


def render_archive(env: Environment, tools: list) -> None:
    """Render the Archive page."""
    archive_tools = [t for t in tools if t["status"] == "archived"]
    out_path = CONTENT_DIR / "tools" / "archive.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    template = env.get_template("archive.md.j2")
    rendered = template.render(
        tools_by_status={"archived": archive_tools},
    )
    out_path.write_text(rendered, encoding="utf-8")
    log.info("Wrote %s (%d archived tools)", out_path.relative_to(REPO_ROOT), len(archive_tools))


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> int:
    log.info("=== generate_tool_pages.py start ===")

    tools = load_manifest()
    tools_by_domain = group_by_domain(tools)
    env = make_env()

    domain_pages_written = render_domain_pages(env, tools_by_domain)
    render_all_tools(env, tools, tools_by_domain)
    render_long_list(env, tools)
    render_archive(env, tools)

    total = domain_pages_written + 3  # 3 = all_tools + long_list + archive
    log.info("=== Done: %d files written ===", total)

    if total != 6:
        log.error("Expected 6 generated files, got %d — check domain grouping", total)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
