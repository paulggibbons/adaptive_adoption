# PGA Diagnostics System — Architectural Decisions

**Status:** canonical decision log
**Owner:** Paul Gibbons
**Last reviewed:** 2026-07-11

This file records the principal design decisions governing the PGA diagnostics and AI-tools system. It is not a changelog. Each entry records the context, choice, consequences, and conditions for reconsideration.

## Decision 001 — Split framework/manifest from public website

**Status:** accepted  
**Date:** 2026-05-12

**Decision:** Maintain two repositories:

- `adaptive_adoption` for framework content, the tool-registry export, publication manifest, schema, validation, and operating documentation;
- `pg-advisory-astro` for production pages, React widgets, shared layouts, API routes, and Vercel deployment.

**Consequences:** Intellectual content and production delivery remain separately governed, but cross-repository changes require explicit coordination.

**Revisit when:** A monorepo can preserve the same governance boundaries with materially less coordination cost.

---

## Decision 002 — Supabase registry plus versioned YAML publication manifest

**Status:** accepted; clarified 2026-07-11  
**Date:** 2026-05-05 to 2026-05-12

**Decision:** Use:

- Supabase `public.tools` as the editable portfolio registry;
- `adaptive_adoption/data/tools.yml` as the canonical version-controlled publication manifest;
- `scripts/seed_tools.py` to transform registry rows into the manifest;
- schema validation and pressure tests before publication.

**Consequences:** Supabase and GitHub provide different forms of authority. Registry-to-manifest drift is possible, and the current seed script is not a pure export because it includes overrides and aspirational entries.

**Revisit when:** One system can safely provide editing, release review, validation, rollback, and build reliability without increasing fragility.

---

## Decision 003 — Website consumes the manifest at build time

**Status:** accepted  
**Date:** 2026-05-11

**Decision:** `pg-advisory-astro/src/lib/manifest.ts` fetches the raw GitHub manifest during the Astro build, with a committed snapshot fallback. Thin Astro page shells bind a manifest record to a tool-specific React component through `DiagnosticPageLayout.astro`.

**Consequences:** Shared page chrome and metadata remain consistent, while tool interactions can stay bespoke. Manifest changes require a rebuild.

**Revisit when:** Runtime publication becomes essential or stable interaction patterns justify a generic renderer.

---

## Decision 004 — Correct-answer scoring remains server-side

**Status:** accepted  
**Date:** 2026-06-14

**Decision:** Store public prompts/options in `diagnostic_questions`, protected answers/insights in `diagnostic_answer_key`, and score through the `SECURITY DEFINER` RPC `score_diagnostic`.

**Consequences:** Answer keys are not directly client-readable. The database functions and their ownership/RLS configuration become a critical security boundary.

**Revisit when:** The instrument has no correct answers, is intentionally open-book, or another scoring service provides stronger governance.

---

## Decision 005 — Anonymous response collection with optional demographics

**Status:** accepted; safeguards incomplete  
**Date:** 2026-06-14

**Decision:** Permit anonymous INSERT into `diagnostic_responses`, deny anonymous row reads, and collect optional pseudonym, role, region, sector, and years leading change. Return aggregate comparisons only through controlled RPCs.

**Consequences:** Participation friction is low and population data can accumulate, but spam, low-quality data, small-cohort disclosure, and re-identification risks require controls.

**Revisit when:** Commercial deployments require authenticated cohorts, deletion rights, respondent tracking, or organization-level administration.

---

## Decision 006 — Benchmarks are descriptive, not validated norms

**Status:** accepted  
**Date:** 2026-07-11

**Decision:** Describe current comparisons as population or cohort benchmarks, not norms. Display sample size, suppress small cohorts, and separate materially different instrument versions.

**Consequences:** Claims remain proportionate to evidence. Some comparison features may remain unavailable until enough responses exist.

**Revisit when:** Reliability, validity, sampling, and norming work support stronger claims.

---

## Decision 007 — Shared shell, bespoke interaction components

**Status:** accepted  
**Date:** 2026-05-12

**Decision:** Use a shared manifest-driven page layout and demographic layer, while retaining tool-specific React components for interaction and result logic.

**Consequences:** Brand, metadata, CTA, provenance, and response capture are consistent, while each tool can use the interaction its model requires. Some repeated form and scoring logic may accumulate.

**Revisit when:** Several stable patterns justify shared engines, hooks, or schema-driven renderers.

---

## Decision 008 — Keep the two evidence scales separate

**Status:** accepted  
**Date:** 2026-07-11

### Context

The system needs to communicate both:

1. how strong the evidence is for a model, framework, diagnostic, or tool; and
2. what kind of evidence supports a claim about organizational behavior.

These are different questions.

### Decision

Use two independent scales, defined fully in [EVIDENCE-SCALES.md](EVIDENCE-SCALES.md).

**A. Tool/model epistemic strength — five levels**

1. Conceptual
2. Research-grounded
3. Face validity
4. Construct validity
5. Predictive validity

The manifest field `epistemic.level` stores this five-level scale. Levels 4 and 5 are intentionally demanding and should be rare.

**B. Behavioral evidence — three layers**

1. Anecdotal or reported evidence
2. Artifact evidence: policy, process, playbook, decision record, configuration, or another durable representation
3. Observed behavior: evidence of what people actually do

Behavioral evidence must not be stored in `epistemic.level`. If structured storage is added, it must use a separate field such as `behavioral_evidence_layer`.

### Consequences

- A scientifically strong tool may still collect only Layer 1 self-report evidence.
- A conceptually early tool may collect Layer 3 observed behavior.
- Tool polish, popularity, and commercial usefulness do not justify epistemic Levels 4 or 5.
- A written policy is evidence of an artifact, not proof of enacted behavior.

### Revisit when

A broader model-card standard replaces both fields while preserving the conceptual distinction.

---

## Decision 009 — Architecture documentation lives with implementation

**Status:** accepted  
**Date:** 2026-07-11

**Decision:** Make `adaptive_adoption/docs/SYSTEM-OVERVIEW.md` the master map and `docs/README.md` the documentation index. Keep specialist canonical documents in the repository. External notes may link to them but should not maintain competing copies.

**Consequences:** Architecture changes must include documentation changes. Private credentials and secrets remain outside the repository.

**Revisit when:** A dedicated internal documentation system can preserve version coupling, access control, and discoverability better than repository documentation.

---

## Proposed decisions requiring review

These are not yet accepted:

1. Replace the hard-coded response-slug CHECK constraint with a foreign-keyed diagnostics registry.
2. Move all Supabase schema and RPC definitions into version-controlled migrations.
3. Automate registry-to-manifest export and drift detection in CI.
4. Establish a minimum sample threshold for benchmark display.
5. Add mandatory instrument/scoring version fields to response records.
6. Consolidate duplicate `/api/query` implementations.
7. Add a structured `behavioral_evidence_layer` field only after its storage scope and use are specified.