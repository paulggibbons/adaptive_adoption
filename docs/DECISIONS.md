# PGA Diagnostics System — Architectural Decisions

**Status:** canonical decision log
**Owner:** Paul Gibbons
**Last reviewed:** 2026-07-11

This file records the principal design decisions governing the PGA diagnostics and AI-tools system. It is not a changelog. Each entry explains the context, choice, consequences, and conditions under which the decision should be revisited.

## Decision 001 — Split framework/manifest from public website

**Status:** accepted
**Date:** 2026-05-12

### Context

The Adaptive Adoption framework, provenance, tool portfolio, and long-form documentation evolve differently from the production advisory website.

### Decision

Maintain two repositories:

- `adaptive_adoption` for framework content, tool registry export, publication manifest, schema, validation, and documentation;
- `pg-advisory-astro` for production pages, React widgets, shared layouts, API routes, and Vercel deployment.

### Consequences

- Intellectual content can remain openly documented and versioned.
- Production code remains focused on delivery.
- Cross-repository changes require coordination.
- Documentation must clearly identify which repository owns each concern.

### Revisit when

The coordination cost materially exceeds the separation benefit, or a monorepo can preserve the same governance boundaries more simply.

---

## Decision 002 — Supabase registry plus versioned YAML publication manifest

**Status:** accepted, clarification added 2026-07-11
**Date:** 2026-05-05 to 2026-05-12

### Context

The tool portfolio needs an editable operational registry, while production builds need a reviewable and versioned release artifact.

### Decision

Use:

- Supabase `public.tools` as the editable portfolio registry;
- `adaptive_adoption/data/tools.yml` as the canonical version-controlled publication manifest;
- `scripts/seed_tools.py` to transform registry rows into the manifest;
- schema and pressure tests before publication.

### Consequences

- Supabase and GitHub serve different kinds of authority.
- The website can build deterministically from a committed artifact.
- Registry-to-manifest drift is possible.
- The seed script's overrides and aspirational entries mean the export is not currently pure.

### Revisit when

A single source can safely provide editing, version history, validation, rollback, release review, and build reliability without increasing fragility.

---

## Decision 003 — Website consumes manifest at build time

**Status:** accepted
**Date:** 2026-05-11

### Context

Tool descriptions, routes, CTAs, attribution, epistemic labels, and card metadata should not be duplicated across website pages.

### Decision

`pg-advisory-astro/src/lib/manifest.ts` fetches the raw GitHub manifest during the Astro build, with a committed snapshot fallback. Thin Astro page shells bind a manifest record to a tool-specific React component through `DiagnosticPageLayout.astro`.

### Consequences

- Shared page chrome updates consistently.
- Manifest changes trigger site rebuilds rather than runtime database reads.
- Builds remain available when GitHub is temporarily unavailable through the snapshot.
- Interactive implementations remain tool-specific.

### Revisit when

Runtime publication without rebuild becomes essential, or a generic renderer can represent most tool interaction patterns without flattening them.

---

## Decision 004 — Correct-answer scoring remains server-side

**Status:** accepted
**Date:** 2026-06-14

### Context

Knowledge and judgement diagnostics need correct answers and explanatory insights, but shipping an answer key to browser code makes the instrument trivial to inspect and undermines data quality.

### Decision

Store public prompts/options in `diagnostic_questions`, protected answers/insights in `diagnostic_answer_key`, and score through the `SECURITY DEFINER` RPC `score_diagnostic`.

### Consequences

- The answer key is not directly client-readable.
- Server-side functions become a critical security and availability dependency.
- RLS and function ownership must be reviewed carefully.
- Self-scored instruments do not need this architecture.

### Revisit when

The diagnostic is intentionally open-book, has no correct answers, or an alternative secure scoring service materially improves governance.

---

## Decision 005 — Anonymous response collection with optional demographics

**Status:** accepted, safeguards incomplete
**Date:** 2026-06-14

### Context

The tools should produce population learning without requiring accounts or email capture.

### Decision

Allow anonymous INSERT into `diagnostic_responses`; deny anonymous row reads. Collect optional pseudonym, role, region, sector, and years leading change. Return aggregate comparisons through a controlled RPC.

### Consequences

- Participation friction is low.
- Population data can accumulate across tools.
- Anonymous submission can attract spam or low-quality data.
- Small cohort disclosure and re-identification risks must be managed.

### Revisit when

Commercial team deployments require authenticated cohorts, deletion rights, respondent tracking, or organization-level administration.

---

## Decision 006 — Benchmarks are descriptive, not validated norms

**Status:** accepted
**Date:** 2026-07-11 clarification

### Context

Population averages can be useful early, but the sample is self-selected and most instruments have not been psychometrically validated.

### Decision

Describe current comparisons as population or cohort benchmarks. Do not call them norms. Display sample size, suppress small cohorts, and separate materially different instrument versions.

### Consequences

- Claims remain proportionate to evidence.
- Benchmark features may remain unavailable until sufficient responses exist.
- Instrument versioning must become part of response governance.

### Revisit when

Sampling, reliability, validity, and norming work supports stronger claims.

---

## Decision 007 — Tools use a shared shell but bespoke interaction components

**Status:** accepted
**Date:** 2026-05-12

### Context

The portfolio includes quizzes, multidimensional diagnostics, canvases, maps, generators, and interactive models. One generic form renderer would simplify maintenance but may flatten the user experience.

### Decision

Use a shared manifest-driven page layout and demographic layer, while retaining tool-specific React components for interaction and result logic.

### Consequences

- Brand, metadata, CTA, provenance, and data capture are consistent.
- Each tool can use the interaction best suited to its model.
- Repeated scoring and form logic may accumulate across components.

### Revisit when

Several stable patterns emerge that justify shared diagnostic engines, hooks, or schema-driven renderers.

---

## Decision 008 — Tool epistemic status is a first-class field

**Status:** accepted
**Date:** 2026-05-05

### Context

The portfolio mixes original conceptual tools, research-grounded adaptations, established frameworks, and potentially validated instruments.

### Decision

Store and display an epistemic level and human-readable label for each tool. Claims must match the evidence behind the instrument.

### Consequences

- Users can distinguish a prototype from an established measure.
- The current Supabase 1–5 scale and manifest schema 1–3 enum appear inconsistent and require reconciliation.

### Revisit when

A single documented model-card standard replaces the current field pair.

---

## Decision 009 — Architecture documentation lives with implementation

**Status:** accepted
**Date:** 2026-07-11

### Context

Relevant knowledge was fragmented across GitHub, Supabase, Drive, Obsidian, and session traces, creating ambiguity about the current system.

### Decision

Make `adaptive_adoption/docs/SYSTEM-OVERVIEW.md` the master map and `docs/README.md` the documentation index. Keep specialist canonical documents in the repository. External notes may link to them but should not maintain competing copies.

### Consequences

- Future agents and collaborators have one starting point.
- Architecture changes must include documentation updates.
- Private operational secrets must still remain outside the repository.

### Revisit when

A dedicated internal documentation system can preserve version coupling, access control, and discoverability better than repository documentation.

---

## Proposed decisions requiring review

These are not yet accepted:

1. Replace the hard-coded response-slug CHECK constraint with a foreign-keyed diagnostics registry.
2. Move all Supabase schema and RPC definitions into version-controlled migrations.
3. Automate registry-to-manifest export and drift detection in CI.
4. Establish a minimum sample threshold for benchmark display.
5. Add mandatory instrument/scoring version fields to response records.
6. Consolidate duplicate `/api/query` implementations.
7. Reconcile the epistemic-level scales used by Supabase and the YAML schema.