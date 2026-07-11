# Adaptive Adoption — Architecture

**Status:** as of 2026-05-12, post Phase 3 completion. **Partially superseded** by the June 2026 Supabase scoring rework — see the note below.
**Audience:** future Claude sessions + Paul, when something breaks and we need to know how the pieces fit.

> **⚠️ Partially superseded (July 2026).** This document was written for the two-repo manifest + static-render architecture and remains the authority for that scope (the two-repo split, the manifest pipeline, and site rendering). It **predates** the June 2026 server-side scoring rework, which added a third layer: a Supabase database with server-side scoring RPCs, question banks, and protected answer keys. For the full current picture, read:
> - **[SYSTEM-OVERVIEW.md](./SYSTEM-OVERVIEW.md)** — the master system map and source-of-truth split across both repos and Supabase.
> - **[SUPABASE-SCHEMA.md](./SUPABASE-SCHEMA.md)** — the live database schema, RLS policies, RPCs, and diagnostic scoring flow.
>
> This file now cross-references the scoring layer (see [The Supabase scoring layer](#the-supabase-scoring-layer)) but deliberately does not duplicate those documents.

## TL;DR

Two repos. One manifest. One live site. The manifest is the OS.

```
paulggibbons/adaptive_adoption       paulggibbons/pg-advisory-astro
─────────────────────────────────    ──────────────────────────────
data/tools.yml (source of truth)     consumes manifest at build time
schemas/tools.schema.json            renders 13 diagnostic pages
scripts/ (validate, seed, etc.)      Vercel auto-deploys main branch
.github/workflows/mkdocs.yml         paulgibbonsadvisory.com
GitHub Pages docs site
```

Push to `adaptive_adoption/main` → GitHub webhook → Vercel deploy hook → `pg-advisory-astro` rebuilds → fresh tools.yml fetched at build time → live in ~30–60s.

Since June 2026 there is also a **third layer** not shown above: a Supabase project (`Jarvis_paulg`) that holds the scored diagnostic question banks, protected answer keys, anonymous responses, and the server-side scoring/benchmark RPCs. The manifest pipeline described here is unchanged by it; the scoring layer is summarized under [The Supabase scoring layer](#the-supabase-scoring-layer) and specified in full in [SUPABASE-SCHEMA.md](./SUPABASE-SCHEMA.md).

---

## Repositories

### `paulggibbons/adaptive_adoption`

The framework + manifest source. Three things live here:

1. **`data/tools.yml`** — the manifest. Validated against `schemas/tools.schema.json`, which self-describes as **schema v1.2**. Note the version discrepancy called out under [Schema version](#schema-version) below: the manifest's own `schema_version` field still reads `1.1.0`. 92 tools, of which 13 are `status: live` and render on the public site.
2. **Open-source MkDocs site** at `paulggibbons.github.io/adaptive_adoption/` — long-form framework documentation. Built by `.github/workflows/mkdocs.yml` from markdown files in `change-agility/`, `leadership-delta/`, `behavioral-governance/`, `foundations/`. **Tool listing pages are auto-generated from `tools.yml`** by `scripts/generate_tool_pages.py` during the CI build.
3. **Validation infrastructure** — `scripts/validate_manifests.py`, `scripts/check_live_urls.py`, `scripts/pressure_test_manifest.py`. Wired into the `validate-manifests` job that runs on every PR and every push to main.

### `paulggibbons/pg-advisory-astro`

The public-facing advisory site at `paulgibbonsadvisory.com`. Astro framework, Vercel-deployed.

Key files for the manifest integration:

- `src/lib/manifest.ts` — fetches `tools.yml` at build time. Primary source: raw GitHub URL. Fallback: committed snapshot at `src/data/tools.snapshot.yml`. Cached per-build.
- `src/components/DiagnosticPageLayout.astro` — shared layout that renders chrome (breadcrumb, hero, CTAs, attribution) from a `tool` object.
- `src/styles/diagnostic-chrome.css` — shared `.perspective-bar` / `.persp-*` / `.bm-*` styles imported by the layout.
- `src/components/diagnostics/*.{tsx,jsx}` — 13 React widget components, one per diagnostic.
- `src/pages/diagnostics/<slug>.astro` — 13 thin page shells, one per tool. Each: import widget, `getTool(slug)`, mount widget inside `<DiagnosticPageLayout>`. Plus tool-specific `<style is:global>` block for widget CSS.

---

## Data flow

```
┌─ Author edits ────────────────────────────────────────────────────┐
│ git commit on adaptive_adoption/main: data/tools.yml change      │
└──────────────────────────────┬────────────────────────────────────┘
                               │
                               ▼
┌─ adaptive_adoption CI (.github/workflows/mkdocs.yml) ─────────────┐
│ 1. validate-manifests job:                                        │
│    - validate_manifests.py (schema + v1.2 conditional rules)      │
│    - check_live_urls.py (non-blocking, warn on failure)           │
│ 2. build job (only on push to main, not PRs):                     │
│    - assemble content/ from framework markdown                    │
│    - generate_tool_pages.py renders tool index pages              │
│    - mkdocs build → _site/                                        │
│ 3. deploy job: GitHub Pages → paulggibbons.github.io/adaptive_…   │
└──────────────────────────────┬────────────────────────────────────┘
                               │ (parallel to CI)
                               ▼
┌─ GitHub webhook on adaptive_adoption ─────────────────────────────┐
│ POST to Vercel deploy hook URL                                    │
│   https://api.vercel.com/v1/integrations/deploy/prj_…/…           │
│ Webhook ID 622310725 (configured 2026-05-12)                      │
└──────────────────────────────┬────────────────────────────────────┘
                               │
                               ▼
┌─ Vercel build of pg-advisory-astro ───────────────────────────────┐
│ astro build:                                                      │
│ 1. src/lib/manifest.ts fetches raw tools.yml from main           │
│    (falls back to src/data/tools.snapshot.yml on network failure) │
│ 2. fetches commit SHA for tools.yml from GitHub commits API       │
│    (used for <meta name="manifest-version"> on each page)         │
│ 3. each src/pages/diagnostics/<slug>.astro renders via            │
│    <DiagnosticPageLayout tool={await getTool(slug)}>              │
│ 4. React widgets hydrate on client:load                           │
└──────────────────────────────┬────────────────────────────────────┘
                               │
                               ▼
       paulgibbonsadvisory.com/diagnostics/<slug>
       (live ~30–60s after push to adaptive_adoption/main)
```

---

## The 13 live tools

| Slug | URL | Widget | Domain |
|---|---|---|---|
| `adaptive-adoption-behavioral-index` | `/diagnostics/aabi` | `AABIDiagnostic.jsx` | cross-cutting |
| `ai-knowledge-quick-quiz` | `/diagnostics/ai-mastery` | `AIKnowledgeQuickQuiz.tsx` | change-agility |
| `cynefin-domain-diagnostic` | `/diagnostics/cynefin` | `CynefinDiagnostic.tsx` | change-agility |
| `human-flourishing-at-work` | `/diagnostics/human-flourishing` | `HumanFlourishingDiagnostic.jsx` | leadership-delta |
| `ikigai-diagnostic` | `/diagnostics/ikigai` | `IkigaiDiagnostic.jsx` | change-agility |
| `ai-mastery-assessment` | `/diagnostics/ai-mastery-assessment` | `AIMasteryAssessment.tsx` | change-agility |
| `personal-context-passport` | `/diagnostics/personal-context-passport` | `PersonalContextPassport.tsx` | leadership-delta |
| `creative-climate-diagnostic` | `/diagnostics/creative-climate` | `CreativeClimateDiagnostic.tsx` | leadership-delta |
| `rist-trust-diagnostic` | `/diagnostics/rist-trust` | `RISTTrustDiagnostic.tsx` | change-agility |
| `causal-loop-diagram-builder` | `/diagnostics/causal-loop` | `CausalLoopDiagram.jsx` | leadership-delta |
| `leadership-delta-scoresheet` | `/diagnostics/leadership-delta-scoresheet` | `LeadershipDeltaScoresheet.tsx` | leadership-delta |
| `ai-governance-gap-finder` | `/diagnostics/governance-gap-finder` | `GovernanceGapFinder.tsx` | behavioral-governance |
| `decision-rights-quick-map` | `/diagnostics/decision-rights-map` | `DecisionRightsMap.tsx` | behavioral-governance |

**The page filename does not always equal the manifest slug.** The manifest's `astro_url` field is the source of truth for the route. The widget filename is whatever the developer named it.

---

## The Supabase scoring layer

Added in the **June 2026 server-side scoring rework**, after this document's original Phase 3 scope. It is summarized here so the manifest architecture doesn't read as the whole system; the authoritative specification is **[SUPABASE-SCHEMA.md](./SUPABASE-SCHEMA.md)**.

Not every live tool is scored. Several diagnostics (`ai-mastery`, `creative-climate`, `rist-trust`, and the three `leadership-delta-*` instruments) submit answers to Supabase and receive a computed score and benchmarks back. The manifest pipeline above is unaffected — this layer is orthogonal to how tools are catalogued and rendered.

**Project:** Supabase `Jarvis_paulg` (`dgzulkjyevijzznvfipi`).

**Tables (scoring-relevant):**

- `diagnostic_questions` — the scored question banks (prompt, options, topic, order). RLS: anon + authenticated `SELECT`.
- `diagnostic_answer_key` — correct option index + insight per question. **RLS: no anonymous or authenticated read policy.** This is the key security boundary: the answer key must never reach the browser.
- `diagnostic_responses` — anonymous completions (answers, scores, optional demographics). RLS: anonymous `INSERT` only, no anonymous readback.

**Scoring RPCs (both `SECURITY DEFINER`):**

- `score_diagnostic(p_slug, p_answers)` — grades a submission and returns total, score, band (`frontier`/`practising`/`exposed`), gap topics, and per-question correctness + insight. It runs as `SECURITY DEFINER` precisely so it can read `diagnostic_answer_key` server-side **without** granting the client any direct access to that table.
- `get_diagnostic_benchmarks(p_slug, p_role, p_region, p_sector, p_years)` — returns population, role, and cohort averages/sample counts computed from `diagnostic_responses.scores`. Also `SECURITY DEFINER`. (Open hygiene item: enforce a minimum cohort sample size before exposing comparisons.)

**Data flow — answer keys never reach the browser:**

```
Browser widget                  Supabase (SECURITY DEFINER)
──────────────                  ───────────────────────────
submit answers  ──rpc──▶ score_diagnostic(slug, answers)
                                 │ reads diagnostic_answer_key
                                 │ (client has NO read access)
                                 ▼
   score + band + insights ◀── returns graded result only
                                 (answer key stays server-side)

request benchmarks ─rpc─▶ get_diagnostic_benchmarks(...)
                                 │ aggregates diagnostic_responses
                                 ▼
   population / cohort averages ◀── returns descriptive stats only
```

The browser only ever sees questions (public), its own submitted answers, and the graded result. Correct answers and insights are joined in server-side by the `SECURITY DEFINER` function. See [SUPABASE-SCHEMA.md](./SUPABASE-SCHEMA.md) for the full column-level schema, RLS policies, and the `epistemic_level` scale on `public.tools`.

---

## Schema (v1.2) — quick reference

Full schema: `schemas/tools.schema.json`. Highlights:

### Schema version

There are currently **two version references that disagree**, and the JSON Schema document is the authoritative one:

- `schemas/tools.schema.json` — self-describes as **v1.2** in its `description` (adds the renderer fields and the `object[]` shape for `related_tools`). This is what `validate_manifests.py` enforces.
- `data/tools.yml` — its top-level `schema_version` field still reads **`1.1.0`**.

Treat **v1.2** (the schema document) as the current contract. The stale `schema_version: 1.1.0` in the manifest is a known-hygiene item to be bumped to `1.2.0` in a future edit; it is not read by the validator, so it does not affect builds today. Do not "fix" one to match the other without also updating whatever downstream expects it (e.g. the `<meta name="manifest-version">` rendering in `pg-advisory-astro`, which uses the commit SHA, not this field).

**Required fields** (always): `slug` (lowercase-with-hyphens), `name`, `type` (enum), `status` (enum), `framework_mapping.domain` (enum), `dates.created`, `dates.last_updated`, `sort_order`.

**Required for `status: live`** (enforced by `validate_manifests.py`, not the JSON Schema — so non-live entries can carry partial data): `long_description`, `hero_image`, `hero_image_alt`, `cta.primary.text`, `cta.primary.url`, `astro_url`, `dates.built`.

**Enums:**
- `status`: `live | build-next | in-development | planned | speculative | archived`
- `type`: `diagnostic | assessment | canvas | quick-diagnostic | ai-tool | interactive-tool | template | checklist | tracker | workshop-tool | scorecard`
- `framework_mapping.domain`: `change-agility | leadership-delta | behavioral-governance | cross-cutting`
- `related_tools[*].relationship`: `predecessor | successor | complementary | see-also`
- `embed.type`: `iframe | typeform | google_form | custom_html`

**v1.2 renderer fields** (all optional, conditionally required for live): `hero_copy` (≤140 chars), `hero_image`, `hero_image_alt`, `cta` (with primary/secondary), `embed`, `attribution` (string array). `related_tools` changed from `string[]` to `object[]` in v1.2.

**Epistemic level.** `epistemic.level` uses a **5-level scale** (`1` conceptual → `5` predictive validity), with `null` for unrated tools. The manifest schema previously capped the enum at `[null, 1, 2, 3]`; it has been widened to `[null, 1, 2, 3, 4, 5]` to match the operational scale carried by Supabase `public.tools.epistemic_level`. The 5-level scale is the canonical scale — see [SUPABASE-SCHEMA.md](./SUPABASE-SCHEMA.md) §2.1. (Today's manifest entries only populate `1`–`3` and `null`, but the schema no longer rejects `4`/`5`.)

---

## Backup / rollback layers

| Layer | Where | What it restores |
|---|---|---|
| Git tags | `pre-phase-3b-pr-b-backup-2026-05-12` on pg-advisory-astro; `pre-phase-3c-backup-2026-05-12` on adaptive_adoption | Repo state before Phase 3 rendering work |
| Vercel instant rollback | Vercel dashboard → pg-advisory-astro → Deployments → "..." → Instant Rollback | Last known-good production deploy. ~30s. Non-destructive. |
| Snapshot fallback | `pg-advisory-astro/src/data/tools.snapshot.yml` | Manifest content if raw GitHub fetch fails at build time. Refreshed manually as part of major manifest releases. |
| WIP backup | `Paul Master Vault REBUILT/999_session_traces/2026-05-12-pg-advisory-astro-WIP-backup/` | Paul's pre-Frameworks-PR uncommitted edits (obsoleted by PR-4 merge but kept as audit) |

---

## Cross-references

- **Master system map:** [docs/SYSTEM-OVERVIEW.md](./SYSTEM-OVERVIEW.md) — the front door: source-of-truth split across both repos and Supabase. Read this first for the full current picture.
- **Database + scoring:** [docs/SUPABASE-SCHEMA.md](./SUPABASE-SCHEMA.md) — live schema, RLS, scoring/benchmark RPCs, diagnostic flow.
- **Operations playbooks:** [docs/OPERATIONS.md](./OPERATIONS.md) — add/edit/deprecate a tool, debug a failed deploy, roll back
- **Troubleshooting:** [docs/TROUBLESHOOTING.md](./TROUBLESHOOTING.md) — common failure modes and fixes
- **Phase 3 session traces:** in the Obsidian vault at `999_session_traces/2026-05-{05,06,10,11,12}-phase-*`
