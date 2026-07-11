# PGA Diagnostics System — Master Overview

**Status:** canonical master map
**Owner:** Paul Gibbons
**Last reviewed:** 2026-07-11

## Purpose

This document is the front door for the PGA diagnostics and AI-tools system. It explains what the system is, where each kind of truth lives, how information moves, and where an operator or agent should make changes.

Read the linked specialist documents for full implementation detail. Do not duplicate them here.

## System boundary

The production system spans two repositories and one Supabase project:

| Layer | Location | Responsibility |
|---|---|---|
| Framework and publication manifest | `paulggibbons/adaptive_adoption` | Tool portfolio, versioned publication manifest, schema, validation, framework documentation |
| Public website and interactive applications | `paulggibbons/pg-advisory-astro` | Astro pages, React diagnostic widgets, shared layouts, API routes, Vercel deployment |
| Database and population layer | Supabase `Jarvis_paulg` (`dgzulkjyevijzznvfipi`) | Editable tool registry, question banks, protected answer keys, responses, demographics, benchmarks, PaulGPT corpus |

The separate Supabase project `polymath-poker` is outside this system.

## Systems of record

The word “canonical” applies at different layers. Use these distinctions:

| Information | System of record |
|---|---|
| Tool portfolio/catalogue as edited operationally | Supabase `public.tools` |
| Versioned publication manifest consumed by builds | `adaptive_adoption/data/tools.yml` |
| Manifest contract | `adaptive_adoption/schemas/tools.schema.json` |
| Tool-specific UI and scoring/application code | `pg-advisory-astro` |
| Scored diagnostic questions | Supabase `diagnostic_questions` |
| Protected correct answers and scoring insights | Supabase `diagnostic_answer_key` |
| Completed responses and demographics | Supabase `diagnostic_responses` |
| Population and cohort comparisons | Supabase RPC `get_diagnostic_benchmarks` |
| Public framework prose and provenance | `adaptive_adoption` Markdown |

### Authority statement

Supabase `tools` is the editable portfolio registry. `data/tools.yml` is the canonical, version-controlled publication manifest generated from that registry and enriched for release. The website consumes the manifest at build time. Supabase separately stores questions, protected scoring logic, responses, and population data.

Do not casually edit the same field in both Supabase and YAML. The normal direction of travel is:

```text
Supabase tools registry
        ↓ export/transform
versioned tools.yml manifest
        ↓ validation + commit
Astro/Vercel build
        ↓
public diagnostic pages
```

The export is not currently pure: `scripts/seed_tools.py` contains overrides and several aspirational entries that are not in Supabase. Treat those as explicit release-enrichment logic until they are migrated or removed.

## Core data flows

### 1. Tool catalogue and publication

```text
Edit Supabase tools row
  ↓
Run scripts/seed_tools.py
  ↓
Review generated data/tools.yml
  ↓
Run manifest validation and pressure tests
  ↓
Commit to adaptive_adoption/main
  ↓
GitHub webhook triggers Vercel
  ↓
pg-advisory-astro fetches tools.yml at build time
  ↓
public site updates
```

The site falls back to `pg-advisory-astro/src/data/tools.snapshot.yml` if the raw GitHub manifest cannot be fetched.

### 2. Scored diagnostic

```text
React widget fetches public questions
  ↓
user submits answers
  ↓
score_diagnostic SECURITY DEFINER RPC
  ↓
server-side answer key returns score, band, gaps, and insights
  ↓
response and optional demographics insert into diagnostic_responses
  ↓
get_diagnostic_benchmarks returns eligible comparisons
  ↓
results render
```

The protected answer key must never be shipped to browser code.

### 3. Self-scored diagnostic or assessment

Questions and scoring logic may live in the React component. The shared demographic capture layer can still submit answers and score dimensions to `diagnostic_responses`, and the benchmark RPC can still provide comparisons.

### 4. Interactive tool, canvas, or generator

The application may be entirely browser-local, may save a structured output, or may write a response record. Its data policy must be explicit in the manifest copy and the page itself.

## Shared website architecture

Key files in `pg-advisory-astro`:

- `src/lib/manifest.ts` — build-time manifest loader
- `src/components/DiagnosticPageLayout.astro` — shared page chrome, metadata, attribution, CTAs, demographic capture
- `src/components/DemographicCapture.astro` — optional pseudonym/demographic capture and response insert
- `src/components/diagnostics/*` — tool-specific React components
- `src/pages/diagnostics/*.astro` — thin page shells binding manifest records to components

The current site is manifest-driven at the page/chrome level, but most tool interactions remain tool-specific React implementations rather than one fully generic diagnostic renderer.

## Tool lifecycle

Use these states:

1. `SPECULATIVE` — idea only
2. `PLANNED` — accepted into the portfolio
3. `BUILD NEXT` — prioritized and sufficiently specified
4. `IN DEVELOPMENT` — implementation underway
5. `LIVE` — publicly available and monitored
6. `ARCHIVED` — retained for history or redirect, no longer active

A tool is not live merely because a row exists in Supabase. It must have a valid publication manifest entry, implemented route/component where required, database permissions and constraints, tested response flow, and production verification.

## Security boundaries

- Anonymous users may read public tools and diagnostic questions.
- Anonymous users may insert diagnostic responses but may not read response rows.
- The diagnostic answer key has no client-readable RLS policy.
- Correct-answer scoring occurs through `SECURITY DEFINER` RPCs.
- Browser code must use the public/anon Supabase key only.
- Service-role keys must never appear in client bundles or committed files.
- Small demographic cohorts must not be exposed through benchmark results.

## Population and validity rules

Population results are descriptive benchmarks, not validated norms, until sufficient evidence supports stronger language.

Every diagnostic should record or preserve:

- diagnostic slug
- instrument version
- scoring version where distinct
- completion timestamp
- score dimensions
- optional demographic filters

Material instrument changes must not silently pool responses across versions. Benchmark displays should define a minimum sample threshold and suppress small cohorts.

## How to add a tool

Start with [TOOL-BUILD-PROTOCOL.md](TOOL-BUILD-PROTOCOL.md). Then use:

- [SUPABASE-SCHEMA.md](SUPABASE-SCHEMA.md) for database details
- [OPERATIONS.md](OPERATIONS.md) for publication and rollback
- [ARCHITECTURE.md](ARCHITECTURE.md) for build/deployment flow
- [DECISIONS.md](DECISIONS.md) before changing a locked design choice

## Open hygiene issues

1. Decide whether `scripts/seed_tools.py` remains the official registry-to-manifest path and make that path reproducible in CI.
2. Move Supabase schema, constraints, RLS policies, and RPC definitions into version-controlled migrations.
3. Replace the hard-coded `diagnostic_responses.diagnostic_slug` CHECK list with a registry or controlled insert mechanism.
4. Define and enforce benchmark minimum sample sizes and version separation.
5. Resolve the duplicate `/api/query` implementations in root `api/query.js` and `src/pages/api/query.ts`.
6. Reconcile schema-version references: manifest files and documentation currently refer to both v1.1 and v1.2.
7. Refresh the committed website manifest snapshot after major releases.

## Documentation maintenance rule

Architecture changes are incomplete until their documentation changes are included in the same pull request. When implementation and documentation disagree, implementation describes current behavior, but the discrepancy is a defect to be resolved—not a reason to leave the documentation stale.