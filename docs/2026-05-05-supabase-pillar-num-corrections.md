# Supabase `pillar_num` Corrections Needed

**Generated:** 2026-05-05  
**Phase:** 1 (tools.yml seed) — read-only; Supabase not modified  
**Pick up in:** Phase 6 (Supabase deprecation / data cleanup)

---

## Summary

13 rows in `public.tools` have a `pillar_num` value that no longer matches the canonical
pillar ordering in `mkdocs.yml`. All 13 are in the **behavioral-governance** domain.

This happened because BG pillar numbering was reordered at some point between when those
rows were entered and the current mkdocs.yml. The `pillar_num` field is preserved in
`data/tools.yml` as-is (it is a legacy decoration, not load-bearing — see schema v1.1).
The `framework_mapping.pillar` slug is correct in all cases.

**No action required before Phase 2.** The canonical slug is what drives URLs.
Clean up Supabase `pillar_num` in Phase 6 before dropping the table.

---

## Old vs canonical BG pillar numbering

| Old `pillar_num` | Pillar name | Canonical `pillar_num` (mkdocs.yml) | Canonical slug |
|---|---|---|---|
| 1 | Strategic Coherence | **6** | `06-strategic-coherence` |
| 2 | Decision Rights | **1** | `01-decision-rights` |
| 4 | Agent Authority | **2** | `02-agent-authority` |
| 6 | Governance Intelligence | **4** | `04-governance-intelligence` |

The reordering placed Decision Rights first and Agent Authority second, reflecting the
framework's final published structure. Strategic Coherence moved from position 1 to 6.

---

## Affected rows (13)

| Supabase id | Tool name | Pillar name | Supabase `pillar_num` | Canonical `pillar_num` |
|---|---|---|---|---|
| 51 | AI-Strategy Alignment Audit | Strategic Coherence | 1 | 6 |
| 52 | Portfolio Rationalization Matrix | Strategic Coherence | 1 | 6 |
| 53 | Initiative Coherence Scorecard | Strategic Coherence | 1 | 6 |
| 54 | AI Decision Rights Mapper (RACI+) | Decision Rights | 2 | 1 |
| 55 | Authority Escalation Matrix | Decision Rights | 2 | 1 |
| 56 | Decision Velocity Diagnostic | Decision Rights | 2 | 1 |
| 60 | Agentic Trust Level | Agent Authority | 4 | 2 |
| 61 | Human-in-the-Loop Decision Tree | Agent Authority | 4 | 2 |
| 62 | Agent Guardrails Template | Agent Authority | 4 | 2 |
| 66 | Governance Maturity Assessment | Governance Intelligence | 6 | 4 |
| 67 | Policy Effectiveness Tracker | Governance Intelligence | 6 | 4 |
| 68 | Governance Learning Loop Audit | Governance Intelligence | 6 | 4 |
| 81 | Double-Loop Learning Assessment | Governance Intelligence | 6 | 4 |

---

## Recommended Phase 6 SQL

Run after Supabase table deprecation plan is confirmed. Do NOT run before then.

```sql
-- Strategic Coherence: old 1 → canonical 6
UPDATE public.tools SET pillar_num = 6
WHERE domain = 'BG' AND pillar = 'Strategic Coherence' AND pillar_num = 1;

-- Decision Rights: old 2 → canonical 1
UPDATE public.tools SET pillar_num = 1
WHERE domain = 'BG' AND pillar = 'Decision Rights' AND pillar_num = 2;

-- Agent Authority: old 4 → canonical 2
UPDATE public.tools SET pillar_num = 2
WHERE domain = 'BG' AND pillar = 'Agent Authority' AND pillar_num = 4;

-- Governance Intelligence: old 6 → canonical 4
UPDATE public.tools SET pillar_num = 4
WHERE domain = 'BG' AND pillar = 'Governance Intelligence' AND pillar_num = 6;
```

Verify with:
```sql
SELECT id, tool, pillar, pillar_num FROM public.tools
WHERE domain = 'BG'
ORDER BY pillar_num, id;
```

---

## Non-BG domains

No stale `pillar_num` values detected in change-agility or leadership-delta domains.
