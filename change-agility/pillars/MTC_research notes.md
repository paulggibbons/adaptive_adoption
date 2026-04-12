---
title: "Pillar 1 — Master the Craft: Research Notes & Supporting Material"
date: 2026-02-19
updated: 2026-02-25
type: research-notes
project: adaptive-adoption
parent: "[[01-master-the-craft]]"
tags: [adaptive-adoption, pillar1, craft, deliberate-practice, communities-of-practice, measurement]
---

# Pillar 1: Master the Craft
## Research Notes, Quotes, Dashboard Spec & Citations

---

## Craft Quotes

> "Being a craftsman is knowing how to work. Being an artist is knowing when to stop."
> — Ben Affleck

> "For the things we have to learn before we can do them, we learn by doing them."
> — Aristotle (4th c. BCE)

> "If people knew how hard I worked to get my mastery, it wouldn't seem so wonderful at all."
> — Michelangelo

> "We are all apprentices in a craft where no one ever becomes a master."
> — Ernest Hemingway

> "Either the foot is pointed or it is not."
> — Martha Graham (high-art precision, no self-deception)

> "Kendrick had to work hard to perfect his craft…"
> — on Kendrick Lamar (craft as disciplined refinement)

---

## Dashboard Spec: Pillar 1 Measurement (Beta)

One board-ready + operator-ready view. Five tiles — enough to launch without pretending measurement is solved.

| # | Tile | What It Measures | Signal Type |
|---|------|-----------------|-------------|
| 1 | **Access** | Sandbox + tool availability (friction) | Leading |
| 2 | **Participation** | Peer learning intensity (CoP health) | Leading |
| 3 | **Artifacts** | Reusable craft production + reuse (prompt libraries, templates) | Leading |
| 4 | **Practice** | Deliberate practice signals (repeat attempts + feedback loops) | Leading |
| 5 | **Outcomes** | Time saved / quality improvement / adoption stability | Lagging |

### Design Principles
- Tiles 1–4 are leading indicators — they tell you if the conditions for craft-building exist
- Tile 5 is the lagging outcome — don't optimize for it directly; optimize for 1–4 and 5 follows
- Launch with imperfect measurement rather than waiting for perfect measurement
- Each tile should have one primary metric and one secondary metric maximum

---

## Canonical Academic Sources

The six intellectual backbone citations for Pillar 1:

### Tier 1: Essential

**Lave & Wenger (1991)** — *Situated Learning: Legitimate Peripheral Participation*
Learning is fundamentally social; newcomers learn via participation, not instruction. The origin of legitimate peripheral participation — the idea that you learn a craft by doing real work at the edges of a community, not in a classroom. Foundation for why prompt libraries, working out loud, and peer learning are not optional features of AI craft-building.

**Wenger (1998)** — *Communities of Practice: Learning, Meaning, and Identity*
Practice communities as the unit of learning. Extends Lave & Wenger into full organizational theory. The CoP is the organizational structure that Pillar 1 instantiates. Wenger's three dimensions — mutual engagement, joint enterprise, shared repertoire — map directly to what a functioning AI craft community looks like.

**Ericsson, Krampe & Tesch-Römer (1993)** — *The Role of Deliberate Practice in the Acquisition of Expert Performance*
Expertise comes from structured practice with feedback, not passive exposure or raw time-on-task. The empirical foundation for why "use AI more" is not a craft strategy. Deliberate practice requires: defined skill target, immediate feedback, repetition at the edge of current ability. All three are designable organizational conditions.

### Tier 2: Supporting

**Bandura (1977)** — *Self-Efficacy: Toward a Unifying Theory of Behavioral Change*
Confidence in capability predicts persistence and behavior change. Critical for AI craft-building because the learning curve is steep and failure is frequent. Low self-efficacy = people stop at the first failure. Pillar 1 interventions must build self-efficacy alongside skill, not just skill.

**Edmondson (1999)** — *Psychological Safety and Learning Behavior in Work Teams*
Teams learn when it's safe to admit errors and uncertainty. Directly underpins the "fail loudly (safely)" norm in Pillar 1. Without psychological safety, craft learning goes underground — people hide failures instead of learning from them. Cross-reference: Pillar 2 (Psychological Safety pillar in AAMI).

**Argyris & Schön (1978)** — *Organizational Learning: A Theory of Action Perspective*
Organizations improve when they detect and correct underlying governing assumptions (double-loop learning), not just errors (single-loop). Pillar 1 requires double-loop learning: not just "that prompt didn't work" but "our assumption about how to use AI for this task was wrong."

### Tier 3: Adjacent (Worth Citing)

**Nonaka & Takeuchi (1995)** — *The Knowledge-Creating Company*
How tacit knowledge becomes shareable organizational knowledge. Highly aligned with prompt libraries and working out loud as organizational practices. The SECI model (Socialization → Externalization → Combination → Internalization) is a useful frame for how individual AI craft becomes organizational AI capability.

---

## Connection to AAMI

Pillar 1 (Master the Craft) maps to **AAMI Pillar 5: Learning Velocity** — does the organization systematically learn from AI use, failure, and near-misses?

The dashboard tiles above are proto-behavioral indicators for AAMI Level 3 (Practicing) and Level 4 (Integrating):
- Level 3: Artifacts tile shows output; Participation tile shows sharing
- Level 4: Practice tile shows deliberate improvement cycles; Outcomes tile shows measurable impact

---

## Open Questions

- [ ] What is the minimum viable CoP structure for an organization of 50-200 people?
- [ ] How do you measure "prompt library reuse" in practice — usage logs, survey, or artifact count?
- [ ] Is there a deliberate practice protocol specifically for LLM prompting? (Likely not yet — opportunity)
- [ ] Bandura's self-efficacy interventions — which translate to AI craft contexts?

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1 | 2026-02-19 | Initial notes from session |
| 0.2 | 2026-02-25 | Formatted for repo, added AAMI connections |
