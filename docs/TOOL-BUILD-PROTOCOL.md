# PGA Diagnostics — Tool Build Protocol

**Status:** canonical operating procedure
**Owner:** Paul Gibbons
**Last reviewed:** 2026-07-11

Use this document to add a new diagnostic, assessment, AI tool, canvas, generator, or scorecard to the PGA system.

Read [SYSTEM-OVERVIEW.md](SYSTEM-OVERVIEW.md) first. Use [OPERATIONS.md](OPERATIONS.md) for publication, validation, rollback, and deployment details.

## 1. Classify the tool before building

Choose the closest implementation class.

### A. Scored diagnostic with correct answers

Use when questions have defensible right/wrong answers and the answer key must remain hidden.

Examples: knowledge or judgement tests.

Requires:

- `tools` registry entry;
- `diagnostic_questions` rows;
- `diagnostic_answer_key` rows;
- `score_diagnostic` RPC compatibility;
- response slug registration;
- React widget and Astro page;
- response capture and optional benchmarks.

### B. Self-scored diagnostic or assessment

Use when responses measure conditions, perceptions, maturity, friction, trust, readiness, or behavior rather than correctness.

Examples: AI Adoption Friction Audit, RIST Trust, Creative Climate.

Usually requires:

- `tools` registry entry;
- questions and scoring either in Supabase or the React component;
- dimension scoring in browser code or a dedicated RPC;
- response slug registration;
- response capture and optional benchmarks;
- clear validity and epistemic language.

### C. Interactive tool

Use when the user manipulates a model, creates a map, or explores relationships rather than receives a diagnostic score.

Examples: causal-loop builder, decision-rights map.

May remain browser-local or save structured outputs. State the data policy explicitly.

### D. Canvas, template, or generator

Use when the primary output is a plan, worksheet, structured artifact, or downloadable result.

May be implemented as an interactive form, downloadable resource, or browser-local generator.

### E. Scorecard or dashboard

Use when multiple measures are aggregated into a continuing or executive-level view. Define data refresh, ownership, and interpretation rules before development.

## 2. Product contract

Before coding, write a short contract covering:

- tool name and slug;
- target user;
- unit of analysis;
- problem addressed;
- promised output;
- what the tool does not claim;
- implementation class;
- framework/domain mapping;
- data captured;
- validity/epistemic status;
- likely follow-on tool or service.

A diagnostic should assess one clearly bounded object. Avoid mixing individual capability, team conditions, enterprise maturity, and project performance in one score unless the model explicitly justifies it.

## 3. Add the portfolio record

### 3.1 Create or update the Supabase `tools` row

Start with `PLANNED`, `BUILD NEXT`, or `IN DEVELOPMENT`.

Populate:

- domain;
- pillar and pillar number where applicable;
- tool display name;
- type;
- status;
- source/provenance;
- route if known;
- card metadata;
- epistemic level and label;
- notes.

Use a greyed card only when exposing the upcoming tool is strategically useful.

### 3.2 Regenerate the publication manifest

Run:

```bash
python scripts/seed_tools.py
```

Then review `data/tools.yml` rather than committing blindly.

The script currently adds overrides and aspirational entries. Confirm that your new tool is not being duplicated or transformed incorrectly.

### 3.3 Complete release-only manifest fields

For a live tool, ensure the YAML entry contains the fields required by the manifest schema and validator, including:

- stable slug;
- `astro_url`;
- long and short descriptions;
- hero copy and imagery;
- CTA fields;
- attribution;
- source;
- epistemic label;
- related tools;
- dates;
- status and tags.

## 4. Choose the question and scoring architecture

### 4.1 Correct-answer diagnostic

1. Insert public prompts and options into `diagnostic_questions`.
2. Insert correct indexes and post-score insights into `diagnostic_answer_key`.
3. Confirm answer-key RLS remains closed.
4. Confirm `score_diagnostic` supports the slug and intended banding.
5. Never include correct answers in browser source.

### 4.2 Self-scored assessment

Choose one of two patterns.

**Supabase question-bank pattern**

Use when questions should be editable without rebuilding the site or shared across variants.

**Component-owned pattern**

Use when the instrument is tightly coupled to a bespoke UI or still changing rapidly.

Whichever pattern is chosen, document:

- item wording;
- scale anchors;
- reverse-scored items;
- missing-answer behavior;
- dimension formulas;
- weighting;
- interpretation bands;
- cross-domain pattern rules;
- instrument version.

Do not call a self-report score a validated measure without evidence.

## 5. Update response storage

Before production:

1. permit the diagnostic slug in the current response validation mechanism;
2. define the `answers` JSON shape;
3. define the `scores` JSON shape;
4. include instrument version in the payload or schema;
5. confirm anonymous insert succeeds;
6. confirm anonymous read fails;
7. confirm malformed payloads fail safely.

The present hard-coded slug CHECK constraint is temporary architecture debt. Prefer a migration-backed registry design when changed.

## 6. Build the website implementation

In `pg-advisory-astro`:

### React component

Create:

```text
src/components/diagnostics/<ToolName>.tsx
```

The component should:

- present the tool accessibly;
- save in-progress state locally when useful;
- calculate or request scores;
- call the shared demographic flow where applicable;
- handle network failure without losing the user's result;
- render clear, bounded interpretations;
- avoid exposing protected logic;
- work on mobile;
- include restart/reset behavior;
- include tests for scoring logic where feasible.

### Astro page shell

Create:

```text
src/pages/diagnostics/<route>.astro
```

Use the shared manifest consumer:

```astro
---
import DiagnosticPageLayout from '../../components/DiagnosticPageLayout.astro';
import MyTool from '../../components/diagnostics/MyTool.tsx';
import { getTool } from '../../lib/manifest';
const tool = await getTool('my-tool-slug');
---

<DiagnosticPageLayout tool={tool} responseSlug="my-response-slug">
  <MyTool client:load />
</DiagnosticPageLayout>
```

Use `responseSlug` when the publication slug and database slug differ. Prefer eliminating such differences rather than perpetuating them.

## 7. Benchmark protocol

Before displaying comparisons:

- confirm the benchmark RPC can read the score dimensions;
- define the minimum sample size;
- suppress small demographic cohorts;
- distinguish population, role, and filtered cohort comparisons;
- label comparisons as descriptive benchmarks rather than norms;
- prevent pooling materially different instrument versions;
- display sample size alongside averages.

A benchmark feature may ship disabled until sufficient responses exist.

## 8. Privacy and epistemic review

Every live tool must state:

- what is stored;
- what remains browser-local;
- whether demographics are optional;
- whether results are anonymous or pseudonymous;
- whether the instrument is conceptual, research-grounded, reliable, or validated;
- whether organizational decisions should rely on the result alone.

Do not imply individual confidentiality when team administrators can inspect identifiable data.

## 9. Validate before publication

In `adaptive_adoption`:

```bash
python scripts/validate_manifests.py
python scripts/check_live_urls.py
python scripts/pressure_test_manifest.py
```

In `pg-advisory-astro`:

```bash
npm run build
```

Also test:

- desktop and mobile;
- keyboard navigation;
- incomplete answers;
- restart/reset;
- Supabase unavailable;
- response insert success;
- response insert rejection for malformed data;
- benchmark suppression;
- print/download where promised.

## 10. Promote to live

Only promote when:

- registry row is complete;
- manifest entry validates;
- route and component exist;
- database changes are deployed;
- security boundaries are confirmed;
- production build succeeds;
- response flow is verified;
- copy and epistemic labels are accurate;
- related-tool links are correct.

Then update status to `LIVE`, regenerate/review the manifest, commit, deploy, and verify production.

## 11. Required documentation changes

The same pull request should update, as applicable:

- this protocol;
- `SUPABASE-SCHEMA.md`;
- `ARCHITECTURE.md`;
- `DECISIONS.md`;
- schema and migrations;
- the tool's framework/provenance documentation.

## 12. Friction Audit classification

The proposed **AI Adoption Friction Audit** is a self-scored, cross-cutting diagnostic.

Recommended characteristics:

- unit of analysis: one named AI initiative or workflow;
- no correct-answer key;
- eight dimension scores;
- separate consequence and evidence-confidence measures;
- structured interpretation rather than one maturity score;
- anonymous response storage for population benchmarking;
- complementary relationship to the planned process-level `adoption-friction-mapper`.