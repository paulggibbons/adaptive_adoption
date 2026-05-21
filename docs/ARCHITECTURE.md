# Adaptive Adoption — Architecture

**Status:** as of 2026-05-12, post Phase 3 completion.
**Audience:** future Claude sessions + Paul, when something breaks and we need to know how the pieces fit.

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

---

## Repositories

### `paulggibbons/adaptive_adoption`

The framework + manifest source. Three things live here:

1. **`data/tools.yml`** — the manifest. Schema v1.2 (see `schemas/tools.schema.json`). 92 tools, of which 13 are `status: live` and render on the public site.
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

- **Operations playbooks:** [docs/OPERATIONS.md](./OPERATIONS.md) — add/edit/deprecate a tool, debug a failed deploy, roll back
- **Troubleshooting:** [docs/TROUBLESHOOTING.md](./TROUBLESHOOTING.md) — common failure modes and fixes
- **Phase 3 session traces:** in the Obsidian vault at `999_session_traces/2026-05-{05,06,10,11,12}-phase-*`
