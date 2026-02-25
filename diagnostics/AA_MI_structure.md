---
title: Adaptive Adoption Maturity Index — Canonical Structure
date: 2026-02-25
version: 0.1
status: draft
type: canonical-doc
project: adaptive-adoption
parent: "[[adaptive-adoption-framework]]"
related:
  - "[[aami-working-state]]"
  - "[[framework-comparison]]"
  - "[[canonical-lineage]]"
tags: #adaptive-adoption, #maturity-model, #aami, #behavioral-science, #enacted-behavior
---

# Adaptive Adoption Maturity Index (AAMI)
## Canonical Structure v0.1

---

## Why This Model Exists

Every existing AI maturity model — MITRE, IBM, Gartner, Prosci, AWS, Microsoft, CMMI — measures **espoused capability**: "has the organization established processes for X?"

None measure **enacted behavior**: "does anyone actually do X?"

The AAMI asks a different question: **"How ready are your humans for AI?"** — measured by what people demonstrably do, not what policies say exist.

This is the first AI adoption maturity model grounded in behavioral science rather than technical or process capability.

---

## Academic Foundations

The espoused-vs-enacted distinction is not new. The AAMI draws on established bodies of research:

- **Argyris (1970s)**: "espoused theory" vs "theory-in-use" — organizations routinely act contrary to their stated values
- **Schein**: artifacts and espoused values are surface; basic underlying assumptions drive actual behavior
- **Implementation science (Proctor et al., 2011)**: only 25–50% of adopted programs achieve sufficient implementation fidelity — the gap between adoption decision and enacted practice is the norm, not the exception
- **Safety culture research (Bradley's Ladder)**: distinguishes "safety climate" (what people say) from "safety behavior" (what people do), measured through observed behavioral indicators across a maturity scale
- **Behavioral safety auditing (BBS)**: uses direct observation and behavioral sampling rather than surveys

---

## The Three-Layer Assessment Structure

What makes the AAMI instrument genuinely different from all competitors is how it gathers evidence. Three layers are used for each pillar at each level:

### Layer 1: Self-Report
What does the organization believe it does?
- Surveys and questionnaires completed by leaders, managers, and practitioners
- Captures the espoused position
- Necessary but insufficient on its own

### Layer 2: Evidence
What artifacts prove it?
- Documents, outputs, usage logs, training records, meeting notes, workflow examples
- Closes the gap between claim and demonstration
- Each maturity level has defined evidence requirements

### Layer 3: Behavioral Indicators
What would an independent observer actually see?
- Direct observation, behavioral sampling, shadow sessions
- The acid test of enacted capability
- Drawn from behavioral auditing methodology

> The diagnostic value of the AAMI comes from the **gap pattern**: where does Layer 1 (espoused) systematically exceed Layers 2 and 3 (enacted)? This gap, not the score, is the intervention target.

---

## The Five Maturity Levels

Level labels use behavioral descriptors — what you would observe — not process descriptors. CMMI language (Initial / Managed / Defined / Quantitatively Managed / Optimizing) is explicitly avoided.

| Level | Label | Behavioral Signature |
|-------|-------|----------------------|
| 1 | **Unaware** | AI use is absent, accidental, or actively avoided. No deliberate engagement with AI tools or their implications. |
| 2 | **Experimenting** | Individuals or teams try AI tools on their own initiative. Use is ad hoc, undirected, and not shared. The organization does not yet learn from these experiments. |
| 3 | **Practicing** | Deliberate, consistent use of AI in defined workflows. Teams share what works. Failures are discussed. Trust is calibrated through experience rather than assumption. |
| 4 | **Integrating** | AI use is embedded in how work gets done. Human judgment and AI capability are consciously orchestrated. The organization actively closes its espoused-enacted gap. |
| 5 | **Adaptive** | The organization learns faster than the technology changes. Behavior evolves in response to new capabilities, failure signals, and emerging risks. AI governance is behavioral, not just procedural. |

### Level Progression Logic

Movement between levels is not automatic with time or investment. Each transition requires a specific behavioral shift:

- **1→2**: From avoidance to curiosity — someone starts experimenting
- **2→3**: From individual to collective — the organization starts learning from experiments
- **3→4**: From use to orchestration — deliberate integration of human and AI judgment
- **4→5**: From integration to adaptation — the system learns faster than it fossilizes

---

## The Seven Pillars

The AAMI assesses across seven pillars, each representing a distinct dimension of human readiness for AI. Scores are produced per-pillar and displayed as a radar chart, enabling diagnostic specificity rather than a single headline number.

| # | Pillar | Core Question |
|---|--------|---------------|
| 1 | **Strategic Alignment** | Do leaders make AI decisions that serve organizational purpose, not technology enthusiasm? |
| 2 | **Psychological Safety** | Can people admit AI failures, ask basic questions, and resist AI outputs without fear? |
| 3 | **Trust Calibration** | Is trust in AI commensurate with demonstrated reliability — neither overtrusting nor undertrusting? |
| 4 | **Workflow Integration** | Is AI embedded in how work actually gets done, not kept in a separate "AI projects" category? |
| 5 | **Learning Velocity** | Does the organization systematically learn from AI use, failure, and near-misses? |
| 6 | **Behavioral Consistency** | Do people act in alignment with stated AI principles when it is costly or inconvenient to do so? |
| 7 | **Governance Enactment** | Are AI policies and guidelines actually followed, or do they exist only as documents? |

---

## Scoring Architecture

### Pillar Scores
Each pillar is scored 1–5, corresponding to the maturity levels above. The score is determined by the **lowest** of the three layers (self-report, evidence, behavioral indicators) — the enacted floor, not the espoused ceiling.

### Sub-Dimension Scores
Each pillar has 3–5 sub-dimensions with their own 1–5 scores, enabling drill-down diagnosis. Pillar score = mean of sub-dimension scores, rounded to nearest 0.5.

### Composite Index
The AAMI Composite Score = mean of all 7 pillar scores. This single number is useful for benchmarking and tracking over time, but the radar chart is the primary diagnostic output.

### The Gap Score
For each pillar, the Gap Score = Layer 1 (self-report mean) − Layer 3 (behavioral indicator score). A positive gap indicates espoused-enacted divergence. High gap scores are the primary intervention signal.

```
Gap Score interpretation:
  0.0–0.5  : Aligned — organization knows what it does
  0.5–1.5  : Moderate gap — awareness exceeds practice
  1.5+     : Significant gap — policy theatre; intervention required
```

---

## Competitive Differentiation

| Model | Measures | Humans Appear? | Behavioral Science? | Gap Diagnostic? |
|-------|----------|----------------|---------------------|-----------------|
| MITRE AI MM | Technical capability, data, governance | No | No | No |
| IBM GenAI | Infrastructure, model hosting, tuning | No | No | No |
| Gartner | Technology readiness | Acknowledged, not measured | No | No |
| Microsoft/AWS CAF | Platform adoption maturity | No | No | No |
| Prosci CM Maturity | Adoption of Prosci's methodology | Partially | No | No |
| CMMI | Process maturity | No | No | No |
| **AAMI** | **Enacted human behavior** | **Central** | **Core methodology** | **Primary output** |

---

## What Comes Next

### Immediate (v0.2)
- [ ] Define sub-dimensions for each of the 7 pillars (3–5 per pillar)
- [ ] Build behavioral indicators at each level for Pillar 3 (Trust Calibration) as proof-of-concept
- [ ] Draft evidence requirements for Pillar 3 at each level
- [ ] Write self-report questions for Pillar 3

### Near-term (v0.3)
- [ ] Extend behavioral indicators, evidence requirements, and questions to all 7 pillars
- [ ] Design the radar chart output format
- [ ] Build the scoring calculator (CSV input → scores + gap analysis)

### Longer-term
- [ ] Field test with 3–5 organizations
- [ ] Calibrate level boundaries based on empirical distribution
- [ ] Develop industry-specific variants (professional services, financial services, healthcare)
- [ ] Pursue academic validation partnership

---

## Key Quotes to Preserve

> "Behavioral — enacted capability, not 'we could, in some world, do this' — but this is demonstrated capability." — Paul Gibbons

> "Awareness, desire, and knowledge do not add up to action." — AAMI critique of ADKAR

> "The gap, not the score, is the intervention target." — Diagnostic principle

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1 | 2026-02-25 | Initial canonical structure — levels, labels, pillars, scoring architecture |
