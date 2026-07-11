# PGA Site — Supabase Schema and Diagnostics Protocol

**Status:** canonical database reference
**Owner:** Paul Gibbons
**Project:** `Jarvis_paulg` (`dgzulkjyevijzznvfipi`)
**Region:** `us-east-2`
**Postgres:** `17.6.1`
**Last live verification:** 2026-07-11 via Supabase MCP

This document records the current live database shape and diagnostic protocol. It complements [ARCHITECTURE.md](ARCHITECTURE.md), which predates the June 2026 server-side scoring rework.

## 1. Database role in the wider system

Supabase provides:

- the editable tool portfolio registry;
- public diagnostic question banks;
- protected answer keys;
- anonymous response storage;
- demographic attributes;
- server-side scoring;
- population and cohort benchmarks;
- the PaulGPT corpus.

The versioned publication manifest remains `data/tools.yml`; see [SYSTEM-OVERVIEW.md](SYSTEM-OVERVIEW.md) for the authority split.

## 2. Tables

### 2.1 `tools`

Current row count at last verification: **92**.

| Column | Type | Notes |
|---|---|---|
| `id` | `int4` PK | Registry identifier |
| `domain` | `text` | CHECK: `CA`, `LD`, `BG`, `ALL` |
| `pillar` | `text` | Pillar/dimension label |
| `pillar_num` | `int4` | Position within domain |
| `tool` | `text` | Display name |
| `type` | `text` | Diagnostic, AI Tool, Interactive tool, etc. |
| `status` | `text` | CHECK: `LIVE`, `BUILD NEXT`, `IN DEVELOPMENT`, `PLANNED`, `SPECULATIVE` |
| `source` | `text` | Attribution/provenance |
| `notes` | `text` nullable | Operational notes |
| `url` | `text` nullable | PGA route |
| `sort_order` | `int4` | Ordering within pillar/domain |
| `is_greyed_card` | `bool` | Placeholder-card flag |
| `greyed_pillar_label` | `text` nullable | Placeholder label override |
| `greyed_time` | `text` nullable | Placeholder time override |
| `card_pillar_label` | `text` nullable | Live card label override |
| `card_time` | `text` nullable | e.g. `5 min`, `Interactive` |
| `epistemic_level` | `int4` nullable | Current operational scale: 1 conceptual → 5 predictive validity |
| `epistemic_label` | `text` nullable | Human-readable epistemic statement |
| `updated_at` | `timestamptz` | Auto-updated |

**RLS:** anonymous SELECT only. No client write access.

### 2.2 `diagnostic_questions`

Current row count at last verification: **18**.

| Column | Type | Notes |
|---|---|---|
| `id` | `int8` PK, serial | Referenced by answer key |
| `diagnostic_slug` | `text` | Instrument identifier |
| `sort_order` | `int4` | Question order |
| `topic` | `text` | e.g. Moat, Scaling, Trust |
| `prompt` | `text` | Question text |
| `options` | `jsonb` | Answer choices |
| `created_at` | `timestamptz` | Creation time |

**RLS:** anon and authenticated SELECT.

Current slugs:

- `leadership-delta-self`
- `leadership-delta-team`
- `leadership-delta-org`

### 2.3 `diagnostic_answer_key`

Current row count at last verification: **18**.

| Column | Type | Notes |
|---|---|---|
| `question_id` | `int8` PK, FK | References `diagnostic_questions.id` |
| `correct_index` | `int4` | Correct option index |
| `insight` | `text` | Explanation returned after scoring |

**RLS:** no anonymous or authenticated read policy.

This is a critical security boundary. Browser code must never receive the answer key directly.

### 2.4 `diagnostic_responses`

Current row count at last verification: **28**.

| Column | Type | Notes |
|---|---|---|
| `id` | `uuid` PK | `gen_random_uuid()` |
| `created_at` | `timestamptz` | Completion time |
| `diagnostic_slug` | `text` | Currently constrained to an explicit slug list |
| `role` | `text` nullable | executive, director/VP, manager, IC, consultant/L&D, other |
| `answers` | `jsonb` | User answers |
| `scores` | `jsonb` | Named score dimensions |
| `pseudonym` | `text` nullable | Optional user-chosen label |
| `region` | `text` nullable | Six-region controlled vocabulary |
| `sector` | `text` nullable | Nine-sector controlled vocabulary |
| `years_leading_change` | `text` nullable | `0-2`, `3-5`, `6-10`, `11-20`, `20+` |

**RLS:** anonymous INSERT only; no anonymous row readback.

Current allowed slugs at last verification:

- `ai-mastery`
- `creative-climate`
- `rist-trust`
- `leadership-delta-self`
- `leadership-delta-team`
- `leadership-delta-org`

The hard-coded slug CHECK is an acknowledged scaling problem. Prefer a foreign-keyed diagnostic registry or controlled insert RPC in a future migration.

### 2.5 `paulgpt_chunks`

Current row count at last verification: **1,865**.

Stores vector-embedded book and corpus chunks for PaulGPT semantic search. Key fields include source identity, chapter, text, summary, rhetorical function, concept tags, frameworks, vector embedding, token count, and validation metadata.

**RLS:** public read plus service-role write.

## 3. RPC functions

### 3.1 `score_diagnostic(p_slug text, p_answers jsonb)`

Returns a JSON result containing:

- total questions;
- score;
- band (`frontier`, `practising`, `exposed`);
- gap topics;
- per-question correctness and insight.

The function runs as `SECURITY DEFINER` so it can read `diagnostic_answer_key` without granting clients direct access.

### 3.2 `get_diagnostic_benchmarks(p_slug, p_role, p_region, p_sector, p_years)`

Returns descriptive comparison data from `diagnostic_responses.scores`, including:

- overall population averages and sample counts;
- role-based averages and sample counts;
- filtered cohort averages and sample counts.

This function also runs as `SECURITY DEFINER`.

**Required hygiene:** define and enforce a minimum sample threshold before exposing cohort comparisons. Small demographic cohorts must be suppressed.

### 3.3 `match_paulgpt_chunks(...)`

Uses pgvector cosine similarity to retrieve relevant corpus chunks for PaulGPT.

## 4. End-to-end scored diagnostic flow

```text
User opens diagnostic page
  ↓
React widget fetches diagnostic_questions through anon SELECT
  ↓
User answers all questions
  ↓
Client calls score_diagnostic(slug, answers)
  ↓
SECURITY DEFINER function reads protected answer key
  ↓
Function returns score, band, gaps, and insights
  ↓
Client optionally calls get_diagnostic_benchmarks
  ↓
Client inserts answers, scores, pseudonym, and optional demographics
  ↓
Results render
```

## 5. RLS summary

| Table | Policy | Roles | Permission |
|---|---|---|---|
| `tools` | `public_read` | anon | SELECT |
| `diagnostic_questions` | `read questions` | anon, authenticated | SELECT |
| `diagnostic_answer_key` | none | none | No client access |
| `diagnostic_responses` | `anon_insert` | anon | INSERT only |
| `paulgpt_chunks` | `public read` | public | SELECT |
| `paulgpt_chunks` | `service role write` | service role | INSERT/update pipeline |

## 6. Schema-change protocol

Any database change must eventually be represented in version-controlled SQL migrations.

At minimum, a change should include:

1. migration SQL;
2. rollback or reversal notes;
3. RLS review;
4. client-impact review;
5. documentation updates;
6. production verification date.

Until migrations are fully established, record the exact SQL and live verification in the pull request.

## 7. Open database hygiene issues

1. Version-control the live schema and RPC definitions.
2. Replace the diagnostic slug CHECK list with a registry/foreign-key design or controlled insert RPC.
3. Add explicit instrument and scoring versions to response records.
4. Define benchmark suppression thresholds and version-aware pooling.
5. Review whether public read access to the full PaulGPT corpus is intentionally broad.
6. Confirm that no service-role credential is exposed through Astro client bundles.
7. Keep this document synchronized with live Supabase after migrations.