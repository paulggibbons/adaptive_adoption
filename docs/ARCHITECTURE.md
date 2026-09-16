# Adaptive Adoption — Architecture

**Status:** current as of 2026-09-16. Refreshed after the June 2026 Supabase scoring rework and the September 2026 canonical-website sync.
**Scope:** the two-repository manifest pipeline and the build/deploy/render path that turns `data/tools.yml` into public pages. This is the "how the build fits together" document.
**Audience:** future Claude sessions + Paul, when something breaks and we need to know how the pieces fit.

> **Where this fits.** This is one document in a set. Start at **[SYSTEM-OVERVIEW.md](./SYSTEM-OVERVIEW.md)** for the master map (system boundaries, systems of record, security, end-to-end flows across both repos *and* Supabase). This file zooms in on the manifest + deployment mechanics only, and deliberately does **not** re-describe the Supabase database, the scoring RPCs, the tool lifecycle, or the evidence scales — those have their own docs, linked under [Cross-references](#cross-references). See **[docs/README.md](./README.md)** for the full index and the documentation-update rule.

## TL;DR

Two repos, one Supabase project. One manifest. One live site. The manifest is the publication contract.

```
paulggibbons/adaptive_adoption       paulggibbons/pg-advisory-astro       Supabase Jarvis_paulg
─────────────────────────────────    ──────────────────────────────      ─────────────────────
data/tools.yml (publication          consumes manifest at build time      editable tool registry,
  manifest, version-controlled)       renders diagnostic pages             question banks, answer
schemas/tools.schema.json (v1.2)      Vercel auto-deploys main branch        keys, responses,
scripts/ (validate, seed, sync)       paulgibbonsadvisory.com                benchmarks, PaulGPT
MkDocs docs site (GitHub Pages)                                            server-side scoring RPCs
```

Push to `adaptive_adoption/main` → GitHub webhook → Vercel deploy hook → `pg-advisory-astro` rebuilds → fresh `tools.yml` fetched at build time → live in ~30–60s. The **scoring layer** (Supabase) is a separate runtime path invoked by the widgets at use time, not at build time — see [The Supabase scoring layer](#the-supabase-scoring-layer).

---

## Repositories

### `paulggibbons/adaptive_adoption` (this repo)

The framework + manifest source. Four things live here:

1. **`data/tools.yml`** — the publication manifest. Validated against `schemas/tools.schema.json` (schema **v1.2**; see [Schema](#schema-v12--quick-reference)). **97 tool entries**, of which **17 are `status: live`** and render on the public site. This file is the version-controlled release metadata; the editable portfolio registry of record is Supabase `public.tools` (see [SYSTEM-OVERVIEW.md](./SYSTEM-OVERVIEW.md) → *Systems of record*).
2. **Framework MkDocs site** at `paulggibbons.github.io/adaptive_adoption/` — long-form framework documentation across `change-agility/`, `leadership-delta/`, `behavioral-governance/`, and the foundations pages. As of the September 2026 refresh the discipline pages are **synced from the canonical website** (`paulgibbonsadvisory.com`) by `scripts/sync_framework_pages.py`; the website's public pages govern current framework wording. See [CANONICAL-SOURCES.md](./CANONICAL-SOURCES.md).
3. **Tool index pages** — auto-generated from `tools.yml` by `scripts/generate_tool_pages.py`, invoked by `scripts/assemble_content.py` during the CI build. The manifest is the single source for what appears in the tool listings.
4. **Validation infrastructure** — `scripts/validate_manifests.py` (schema + conditional live rules), `scripts/pressure_test_manifest.py` (29 stress tests over the validator), `scripts/check_live_urls.py` (non-blocking URL health). Wired into the `validate-manifests` CI job on every PR and every push to main.

### `paulggibbons/pg-advisory-astro`

The public-facing advisory site at `paulgibbonsadvisory.com`. Astro framework, Vercel-deployed. It **consumes** the manifest; it is not edited from here.

Key files for the manifest integration:

- `src/lib/manifest.ts` — fetches `tools.yml` at build time. Primary source: raw GitHub URL. Fallback: committed snapshot at `src/data/tools.snapshot.yml`. Cached per-build.
- `src/components/DiagnosticPageLayout.astro` — shared layout that renders page chrome (breadcrumb, hero, CTAs, attribution, demographic capture) from a `tool` object.
- `src/components/DemographicCapture.astro` — optional pseudonym/demographic capture that inserts into Supabase `diagnostic_responses`.
- `src/styles/diagnostic-chrome.css` — shared chrome styles imported by the layout.
- `src/components/diagnostics/*.{tsx,jsx}` — tool-specific React widget components.
- `src/pages/diagnostics/<slug>.astro` — thin page shells: import widget, `getTool(slug)`, mount inside `<DiagnosticPageLayout>`, plus tool-specific `<style is:global>`.

The site is manifest-driven at the page/chrome level, but most tool interactions are still tool-specific React implementations rather than one fully generic renderer.

---

## Data flow (build → publish)

```
┌─ Author edits ────────────────────────────────────────────────────┐
│ git commit on adaptive_adoption/main: data/tools.yml change        │
│ (normally regenerated from the Supabase registry via seed_tools.py │
│  and reviewed — see SYSTEM-OVERVIEW.md for the registry→manifest   │
│  direction of travel)                                              │
└──────────────────────────────┬────────────────────────────────────┘
                               │
                               ▼
┌─ adaptive_adoption CI (.github/workflows/mkdocs.yml) ──────────────┐
│ 1. validate-manifests job (every PR + push):                       │
│    - validate_manifests.py (schema + conditional live rules)       │
│    - pressure_test_manifest.py (29 validator stress tests)         │
│    - check_live_urls.py (non-blocking, warns on failure)           │
│ 2. build job (needs validate-manifests):                           │
│    - assemble_content.py → runs generate_tool_pages.py, assembles  │
│      framework markdown into the MkDocs tree                       │
│    - mkdocs build → _site/                                         │
│ 3. deploy job: GitHub Pages → paulggibbons.github.io/adaptive_…    │
└──────────────────────────────┬────────────────────────────────────┘
                               │ (parallel to CI)
                               ▼
┌─ GitHub webhook on adaptive_adoption ──────────────────────────────┐
│ POST to the Vercel deploy hook URL (webhook configured 2026-05-12).│
│ To fire manually or debug a stale site, see OPERATIONS.md.         │
└──────────────────────────────┬────────────────────────────────────┘
                               │
                               ▼
┌─ Vercel build of pg-advisory-astro ────────────────────────────────┐
│ astro build:                                                       │
│ 1. src/lib/manifest.ts fetches raw tools.yml from main             │
│    (falls back to src/data/tools.snapshot.yml on network failure)  │
│ 2. fetches the tools.yml commit SHA for the manifest-version meta  │
│ 3. each diagnostics/<slug>.astro renders via DiagnosticPageLayout  │
│ 4. React widgets hydrate on client:load                            │
└──────────────────────────────┬────────────────────────────────────┘
                               │
                               ▼
       paulgibbonsadvisory.com/diagnostics/<slug>
       (live ~30–60s after push to adaptive_adoption/main)
```

This is the **build-time** path. It does not touch Supabase — the manifest is static YAML consumed at build. Scored diagnostics reach Supabase separately, at **use time**, from the browser widget (next section).

---

## The Supabase scoring layer

Some live tools are scored server-side. This is a **runtime** flow orthogonal to the manifest pipeline above; it is summarized here only so the manifest architecture doesn't read as the whole system. The authoritative specification is **[SUPABASE-SCHEMA.md](./SUPABASE-SCHEMA.md)**, and the end-to-end flow is in [SYSTEM-OVERVIEW.md](./SYSTEM-OVERVIEW.md) → *Core data flows → Scored diagnostic*.

In one paragraph: the browser widget fetches public questions, the user submits answers, and a `score_diagnostic` `SECURITY DEFINER` RPC grades them server-side against `diagnostic_answer_key` (which has **no** client-readable RLS policy) and returns score, band, gaps, and insights. The response and optional demographics insert into `diagnostic_responses`; `get_diagnostic_benchmarks` returns eligible population/cohort comparisons. **The answer key never reaches browser code.** Not every live tool is scored — self-scored assessments and browser-local canvases/generators may never call these RPCs.

---

## Live tools — how routing works

The set of live tools changes; do not hard-code it here. As of 2026-09-16 there are **17 `status: live`** entries. The canonical lists are:

- **`data/tools.yml`** — filter `status: live`; the `astro_url` field is the source of truth for each tool's public route.
- **`tools/README.md`** — the human-readable public tool index, grouped by discipline.
- **`paulgibbonsadvisory.com/diagnostics/`** — the live site.

Two rules that trip people up:

1. **The page filename ≠ the manifest slug.** The route is whatever `astro_url` says; the widget filename is whatever the developer named it. Only `astro_url` is authoritative.
2. **Deprecated slugs are preserved.** When a tool is renamed (e.g. the flagship's rename to *AI Workforce Readiness Assessment* in the Sept 2026 refresh), the old name becomes an `alias` and the slug is kept unchanged, to preserve `diagnostic_responses` continuity. See [CANONICAL-SOURCES.md](./CANONICAL-SOURCES.md).

---

## Schema (v1.2) — quick reference

Full schema: `schemas/tools.schema.json`. Highlights:

**Required fields** (always): `slug` (lowercase-with-hyphens), `name`, `type` (enum), `status` (enum), `framework_mapping.domain` (enum), `dates.created`, `dates.last_updated`, `sort_order`.

**Required for `status: live`** (enforced by `validate_manifests.py`, not the JSON Schema — so non-live entries can carry partial data): `long_description`, `hero_image`, `hero_image_alt`, `cta.primary.text`, `cta.primary.url`, `astro_url`, `dates.built`.

**Enums:**
- `status`: `live | build-next | in-development | planned | speculative | archived`
- `type`: `diagnostic | assessment | canvas | quick-diagnostic | ai-tool | interactive-tool | template | checklist | tracker | workshop-tool | scorecard`
- `framework_mapping.domain`: `change-agility | leadership-delta | behavioral-governance | cross-cutting`
- `related_tools[*].relationship`: `predecessor | successor | complementary | see-also`
- `embed.type`: `iframe | typeform | google_form | custom_html`

**v1.2 renderer fields** (all optional, conditionally required for live): `hero_copy` (≤140 chars), `hero_image`, `hero_image_alt`, `cta` (with primary/secondary), `embed`, `attribution` (string array). `related_tools` changed from `string[]` to `object[]` in v1.2.

**Epistemic level.** `epistemic.level` uses a **5-level scale** (`1` conceptual → `5` predictive validity), with `null` for unrated tools. The schema enum is `[null, 1, 2, 3, 4, 5]`, matching Supabase `public.tools.epistemic_level`. The scale is defined in **[EVIDENCE-SCALES.md](./EVIDENCE-SCALES.md)** (which also covers the separate three-layer behavioral-evidence scale).

### ⚠️ Known version discrepancy

The JSON Schema document **self-describes as v1.2** in its `description` (and this is the contract `validate_manifests.py` enforces), but `data/tools.yml`'s top-level `schema_version` field still reads **`1.1.0`**. Treat **v1.2** as the current contract. The stale `schema_version` string is a documented hygiene item ([SYSTEM-OVERVIEW.md](./SYSTEM-OVERVIEW.md) → *Open hygiene issues* #6); it is not read by the validator, so it does not affect builds. Do not "fix" one to match the other without checking what consumes it — the site's `manifest-version` meta uses the commit SHA, not this field.

---

## Backup / rollback layers

| Layer | Where | What it restores |
|---|---|---|
| Vercel instant rollback | Vercel dashboard → pg-advisory-astro → Deployments → "…" → Instant Rollback | Last known-good production deploy. ~30s. Non-destructive. |
| Snapshot fallback | `pg-advisory-astro/src/data/tools.snapshot.yml` | Manifest content if the raw GitHub fetch fails at build time. Refresh manually after major manifest releases (hygiene item — see SYSTEM-OVERVIEW). |
| Git history | both repos | Framework prose, manifest, and schema are all version-controlled; revert a bad manifest commit and let the webhook rebuild (see OPERATIONS.md). |
| Historical backup tags | `pre-phase-3b-pr-b-backup-2026-05-12` (pg-advisory-astro), `pre-phase-3c-backup-2026-05-12` (adaptive_adoption) | Repo state before the May 2026 Phase 3 rendering work. Retained for audit; not part of routine rollback. |

For the operational how-to (fire the webhook manually, diagnose a stale site, verify the deployed manifest SHA), see [OPERATIONS.md](./OPERATIONS.md).

---

## Cross-references

- **Master map (start here):** [docs/SYSTEM-OVERVIEW.md](./SYSTEM-OVERVIEW.md) — system boundaries, systems of record, security boundaries, all data flows across both repos and Supabase.
- **Database + scoring:** [docs/SUPABASE-SCHEMA.md](./SUPABASE-SCHEMA.md) — tables, RLS, scoring/benchmark RPCs, diagnostic flow.
- **Evidence scales:** [docs/EVIDENCE-SCALES.md](./EVIDENCE-SCALES.md) — the 5-level epistemic scale and the 3-layer behavioral-evidence scale.
- **Adding a tool:** [docs/TOOL-BUILD-PROTOCOL.md](./TOOL-BUILD-PROTOCOL.md) — protocol by tool type.
- **Website/framework sync:** [docs/CANONICAL-SOURCES.md](./CANONICAL-SOURCES.md) — how framework pages, the tool index, and publications track the canonical website.
- **Operations playbooks:** [docs/OPERATIONS.md](./OPERATIONS.md) — add/edit/deprecate a tool, debug a failed deploy, roll back.
- **Troubleshooting:** [docs/TROUBLESHOOTING.md](./TROUBLESHOOTING.md) — common failure modes and fixes.
- **Locked decisions:** [docs/DECISIONS.md](./DECISIONS.md) — read before changing a locked design choice.
- **Doc index + update rule:** [docs/README.md](./README.md).
