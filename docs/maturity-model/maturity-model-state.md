---
title: Adaptive Adoption Maturity Model — Working State
date: 2026-02-19
updated: 2026-02-21
type: working-doc
project: adaptive-adoption
status: build-ready
parent: "[[adaptive-adoption-framework]]"
related:
  - "[[session-2026-02-19]]"
  - "[[session-2026-02-21]]"
  - "[[notebooklm-enacted-gap-evidence]]"
  - "[[notebooklm-competitive-landscape]]"
  - "[[notebooklm-trust-behavioral-indicators]]"
  - "[[trust-session-export-2026-02-21]]"
  - "[[canonical-lineage]]"
  - "[[framework-comparison]]"
tags: #adaptive-adoption, #maturity-model, #research, #behavioral-science, #implementation-science, #safety-culture, #enacted-behavior, #espoused-vs-enacted, #three-layer-assessment
---

# Adaptive Adoption Maturity Model — Working State

> **Status:** Research phase complete. All structural decisions resolved. Ready to build.

---

## The Core Insight

Every existing AI maturity model (MITRE, IBM, Gartner, Prosci, AWS, Microsoft, CMMI, Accenture, Deloitte, McKinsey, PwC, IDC, EY, Forrester) measures **espoused capability** — "has the organization established processes for X?" None measure **enacted behavior** — "does anyone actually do X?"

The AA maturity model asks: **"How ready are your humans for AI?"** — measured by what they demonstrably do, not what policies exist.

This is Pillar 6 (Prioritize Behavior) applied to the assessment instrument itself.

**The 72/6 finding is the model's entire justification in one number.** Accenture found 72% of companies score high on organizational maturity but only 6% on operational maturity. Every existing model measures the 72%. AA measures inside the 6%.

---

## Behavioral Science Foundation — COM-B Adapted

The 7 pillars are the practical operationalization of a COM-B derived framework with one significant theoretical addition: **Trust as a distinct fourth quadrant.**

Original COM-B: Capability / Opportunity / Motivation → Behavior
AA Adaptation: Capability / Opportunity / Motivation / **Trust** → Behavior

The addition of Trust as a standalone quadrant is the theoretical contribution to the COM-B literature. In AI adoption, trust failure is the primary adoption barrier and operates independently of the other three. Full capability + strong motivation + no friction ≠ adoption if trust is absent.

**Quadrant → Pillar mapping:**

| Quadrant | Question | Pillars |
|---|---|---|
| Capability ("Can I?") | Internal skill & judgment | Pillar 1: Master the Craft |
| Motivation ("Why should I?") | Desire, identity & incentives | Pillar 4: Put People First + Pillar 6: Prioritize Behavior |
| Trust ("Should I?") | Confidence, legitimacy & safety | Pillar 3: Consciously Manage Trust |
| Opportunity/Friction ("Am I enabled or blocked?") | Environment & systems | Pillar 2: Embrace Complexity + Pillar 5: Design and Prototype |
| Ethics (governing constraint) | Spans all quadrants | Pillar 7: Manage Ethics Always |

**Visual asset:** COM-B Behavioral Science Framework — complete, branded, publication-ready.

---

## Confirmed Structure

| Element | Decision | Rationale |
|---|---|---|
| **Pillars (dimensions)** | 7 | Stable — see below |
| **Assessment layers** | 3 | Self-report / Evidence / Behavioral indicators |
| **Levels** | 6 (0–5) | Level 0 added; Level 5 aspirational |
| **Level labels** | Behavioral — see below | Not process language (CMMI) or archetype language (EY) |
| **Scoring** | Radar chart per pillar + summary | Drill-down sub-dimensions per pillar |
| **Competitive position** | First human-centered AI adoption maturity model with behavioral observation methodology | Differentiated from all 12 reviewed models |

---

## Level Architecture (0–5)

Labels name **behavioral patterns** — what an observer would characterize — not process stages or identity archetypes.

| Level | Label | Behavioral Reality |
|---|---|---|
| **0** | **Unexamined** | Activity without pattern; no enacted behavior to assess. Shadow AI and tool abandonment coexist untracked. Well-populated in practice. |
| **1** | **Performing** | Visible activity; inconsistent; no feedback loop. Compliance theater. |
| **2** | **Acknowledging** | The gap between espoused and enacted is visible and being tracked. Leading indicator: measurement begins. |
| **3** | **Aligning** | Self-report and evidence beginning to converge; behavioral change is intentional. Leading indicator: role-modeling and rituals appear. |
| **4** | **Embedding** | Consistent enacted behavior evidenced across the pillar. Dynamic governance. |
| **5** | **Adapting** | Behavioral patterns are self-correcting; organization learns from its own enacted gaps. Aspirational — few organizations reach this on all pillars simultaneously. |

**Key principle — the Level 2/3 boundary:** Across all 7 pillars, this boundary is the same structural move: the organization becomes aware of its own gap and starts measuring it. Level 2 has a consistent behavioral definition: *"The gap between espoused and enacted is visible and being tracked."*

---

## The Three-Layer Assessment Structure

| Layer | What It Measures | Method |
|---|---|---|
| **1. Self-report** | What do you believe you do? | Surveys, questionnaires |
| **2. Evidence** | Show me artifacts that prove it | Documents, outputs, usage logs, governance records |
| **3. Behavioral indicators** | What would an observer see? | Direct observation, behavioral sampling, leading indicators |

High scores on Layer 1 with low Layer 2/3 scores = the 72% problem.

**Academic foundations:**
- Implementation science (Proctor et al., 2011) — fidelity measurement; only 25-50% of adopted programs achieve sufficient implementation fidelity
- Safety culture research — Bradley's safety culture ladder measures observed behaviors, not survey responses
- Behavioral safety auditing (BBS) — direct observation and behavioral sampling
- Argyris — "espoused theory" vs "theory-in-use"

---

## The People-First Flywheel — Core Theoretical Claim

> **Hypothesis:** Organizations that develop people-first use cases — AI applications that demonstrably make working lives better (flourishing, not just productivity) — will generate faster, deeper, and more durable adoption than organizations that lead with efficiency or strategic mandates. Specifically, people-first use cases causally improve performance on Pillars 1, 3, and 6 beyond what structural readiness would predict.

**The mechanism:**
- **Trust (Pillar 3)** activates because the AI is visibly serving workers, not surveilling or replacing them — relational trust (layer 3 of the Three Trusts) is addressed directly
- **Skill pull (Pillar 1)** activates because motivation to learn is intrinsic when the tool solves *your* problem — workers pull learning toward themselves rather than having training pushed at them
- **Psychological safety (Pillar 6)** activates because experimentation feels safe when stakes are "this might make my work better" not "this might make me redundant"

**The conventional adoption sequence is backwards:** Strategy → governance → tools → training → change management puts the cart before the horse. People-first use cases first; the other pillars activate with less friction.

**For the model — Pillar 4 level descriptors assess** *whose interests the use cases serve*, not just whether use cases exist:
- Level 0: No people-first use cases; AI deployed for org efficiency only
- Level 5: Use cases co-designed with workers; flourishing measured alongside productivity

**Cross-pillar interaction effect:** Organizations scoring high on Pillar 4 will tend to score higher on Pillars 1, 3, and 6 than structural readiness predicts. If captured empirically across assessments, this is a publishable finding and a book chapter.

**Status:** Hypothesis — to be validated empirically. **Named concept:** *The People-First Flywheel*

---

## The 7 Pillars — Integrated Research Findings

### Pillar 1: Master the Craft — Prompt Quality and AI Skill
*Foundation: EY latent class analysis (n=665); BCG software developer survey*

**Enacted behavior measured:** Do people use AI with skill, iteration, and structured methodology — or treat it as a search engine?

**Observable behaviors:**
- *Low (0-2):* Employees use AI for "information assistance" only; abandon tool after poor result rather than iterating
- *High (4-5):* "Semiautonomous collaboration" — structured methodologies (few-shot, chain of thought), custom agents, AI as thought partner

**Leading behavioral indicator:** Team-based rituals — weekly prompt swaps, agent showcases, GenAI retrospectives. The Level 3 inflection point: individual skill becoming collective capability.

**Key concept:** *Semiautonomous collaboration* (EY)

---

### Pillar 2: Embrace Complexity — Navigating Ambiguity and System Effects
*Foundation: HBS/BCG field experiment on knowledge worker productivity*

**Enacted behavior measured:** Do people know where AI competence ends and theirs begins — and design work accordingly?

**Observable behaviors:**
- *Low (0-2):* Blindly apply AI to complex tasks; AI bolted onto existing linear processes; rework negates gains
- *High (4-5):* "Human-AI Sandwich" — human frames complex task → AI handles well-defined sub-tasks → human reviews and handles ambiguity

**Leading behavioral indicator:** Fundamental workflow redesign. High-performing teams are 2.8x more likely to dismantle and rebuild processes rather than layer AI on top.

**Key concepts:** *Jagged technological frontier* (BCG); *Human-AI Sandwich*

---

### Pillar 3: Consciously Manage Trust — Calibrated Reliance on AI Outputs
*Foundation: Nature Human Behaviour studies; McKinsey Rewired; Dietvorst et al. 2015/2018; Kim, Kim & Lee 2025; Hoffman et al. 2025 (GitHub Copilot); Capital One dynamic decision rights*

**Enacted behavior measured:** Do people interact with AI with calibrated judgment — neither abandoning nor uncritically following?

**Trust is three-headed:**
1. **Task trust (micro):** "Can I trust this model to do X?"
2. **Institutional trust (macro):** "Do I trust the technology ecosystem — labs, incentives, governance?"
3. **Relational trust (social):** "Do I trust leadership that adoption won't harm my livelihood?"

*Most existing models only assess Task trust. AA assesses all three.*

**Observable behaviors:**
- *Low (0-2):* Polarization — "blind trust" generating "AI slop," OR "algorithmic aversion" (tool abandoned after single error); knowledge hiding present
- *High (4-5):* Calibrated trust; formal consequence-bucketing; demand for "contrastive explanations"

**Leading behavioral indicator:** Demand for contrastive explanations — users interrogating AI logic: why this output and not another?

**Level anchors:**

| Level | Behavioral Profile |
|---|---|
| 0 | Shadow AI high and untracked; tool abandonment unmonitored; no psychological safety |
| 1 | Knowledge hiding present; overtrust or undertrust dominates; no error feedback loop |
| 2 | Organisation recognises undertrust/overtrust as distinct problems; tracking begins |
| 3 | Psychological safety sufficient for error disclosure; sanctioned tools; Trust Calibration Protocol in use |
| 4 | Dynamic decision rights thresholds — human oversight calibrated to demonstrated AI reliability |
| 5 | Trust calibration self-correcting; organisation learns from both overtrust and undertrust events |

**Critical findings:**
- *Kim, Kim & Lee (2025):* AI adoption → lower psychological safety → depressive symptoms. Trust pillar is not optional — skipping it potentially harms people.
- *Hoffman et al. (2025) GitHub Copilot:* Lower-ability developers benefited *more* from AI in psychologically safe environments. Psychological safety determines who captures the productivity gains.
- *"AI slop":* outputs that look convincing but collapse under expert scrutiny — the overtrust failure mode named.

**Tool:** `tools/trust-calibration-protocol/`
**Visual asset:** Three Trusts of AI Adoption — complete, branded, publication-ready.

---

### Pillar 4: Put People First — Human-Centered Use Case Design
*Foundation: People-First Flywheel hypothesis; COM-B Motivation quadrant; flourishing research*

**Enacted behavior measured:** Are AI use cases designed to serve the people doing the work — or purely to extract organizational efficiency?

**Observable behaviors:**
- *Low (0-2):* AI deployed for cost reduction or compliance; workers are objects of change, not participants; use cases designed by leadership without worker input
- *High (4-5):* Use cases co-designed with workers; flourishing measured alongside productivity; People-First Flywheel operating — trust and skill pull are self-reinforcing

**Leading behavioral indicator:** Workers proactively request or design their own AI use cases without mandate.

**Note:** This pillar is the adoption flywheel. Organizations scoring high here systematically outperform on Pillars 1, 3, and 6. See People-First Flywheel section above.

---

### Pillar 5: Design and Prototype — Moving from Pilot to Scale
*Foundation: "Peeling the Onion" framework (n=847 hotel implementations); MIT organizational experiments*

**Enacted behavior measured:** Do organizations design AI initiatives with current-state rigor before procurement?

**Observable behaviors:**
- *Low (0-2):* "Tool-first procurement"; AI bought before baseline metrics; "pilot purgatory" (88% claim adoption, 74% can't scale)
- *High (4-5):* Organizational experiments using control groups and randomized rollouts

**Leading behavioral indicator:** "Current-State Primacy" documentation — systematic mapping of current processes before any tool is procured. The Level 2 gate: organizations that skip this are structurally incapable of scaling.

**Key concept:** *Pilot purgatory* — a craft problem (Pillar 1) + complexity problem (Pillar 2).

---

### Pillar 6: Prioritize Behavior — Closing the Intention-Action Gap
*Foundation: Transformation Design Framework (TDF); Knowledge Behavior Gap (KBG) models; BCG employee-centric AI adoption research; COM-B*

**Enacted behavior measured:** Do organizations close the gap between stated intention and actual behavioral change?

**Observable behaviors:**
- *Low (0-2):* Top-down mandates → performative compliance or shadow AI; fear of replacement
- *High (4-5):* "Habit Stacking" — attaching small AI actions to existing routines

**Leading behavioral indicator:** Visible managerial vulnerability and role-modeling. The Level 3 signal — predicts whether top-down adoption will stick.

**Behavior change arc:** Mandate (L1) → Role-modeling (L3) → Habit integration (L4) → Self-sustaining culture (L5)

**ADKAR critique:** Awareness + Desire + Knowledge ≠ Action. AA corrects this with behavioral science methodology.

---

### Pillar 7: Manage Ethics Always — Consequence Reasoning and Responsible Use
*Foundation: Accenture/Stanford Responsible AI Survey (n=1,000); GenAI Cognitive Dissonance studies*

**Enacted behavior measured:** Is ethics embedded in design and deployment — or applied as a compliance checklist after the fact?

**Observable behaviors:**
- *Low (0-2):* Ethics as post-development compliance checklist; cognitive dissonance (convenience over integrity)
- *High (4-5):* "Ethics by design" — bias testing, explainability, accuracy checks embedded in pipeline; active red-teaming

**Leading behavioral indicator:** Cross-functional "control tower" with *authority to pause* AI projects. Advisory bodies = Level 3. Authority to pause = Level 5 differentiator.

**Note:** Pillar 7 spans all four COM-B quadrants as the governing ethical constraint.

---

## Visual Assets Inventory

| Asset | Status | Notes |
|---|---|---|
| Three Trusts of AI Adoption | ✅ Complete | Publication-ready, branded |
| COM-B Behavioral Science Framework | ✅ Complete | Publication-ready, branded |
| 7-pillar × 6-level matrix | ❌ Not built | Priority for March 15th |
| Three-layer assessment diagram | ❌ Not built | Self-report / evidence / behavioral |
| Trust spectrum diagnostic visual | ❌ Not built | Tech debt |
| Practitioner matrices (7×5) | 🟡 Draft exists | ~30 slides in working pptx; full audit needed |

*~30 visual assets exist across working drafts — full audit required before March 15th release.*

---

## Tech Debt

### Trust Diagnostic — `diagnostics/trust-spectrum/`
Standalone diagnostic mapping organizations on undertrust ↔ calibrated ↔ overtrust per trust layer (Task / Institutional / Relational). Distinct from Pillar 3 rubric — lightweight, standalone, market entry product.

Components needed: `README.md`, `instrument.md`, `scoring.md`

**Priority:** Build after Pillar 3 rubric. The rubric generates the content; diagnostic extracts it.

### Leadership/Governance Meta-Layer
Sits above the 7 pillars as enabling context — prerequisite condition, not a pillar. Prototype developed. To be integrated before v0.1 release.

### Visual Assets Audit
~30 visual assets in working drafts. Full audit needed before March 15th release.

---

## Competitive Landscape Summary

| Model | Measures | AA Differentiation |
|---|---|---|
| MITRE AI MM | Technical capability, data, governance | Zero behavioral science, zero trust |
| IBM GenAI | Infrastructure, model hosting | Humans don't appear |
| Gartner | Technology readiness, culture survey | Culture = survey dimension, no behavioral observation |
| Accenture Responsible AI | Identifies org vs operational maturity gap | Identifies the gap; AA measures inside it |
| EY | Behavioral archetypes; emotional journey | Archetypes descriptive not diagnostic |
| IDC | Tracks shadow AI progression | Metric only, not root cause |
| McKinsey | Workflow redesign, agentic org | No behavioral observation methodology |
| Healthcare (Filipovic) | Adds people/org to technical models | 86% of models over-index on Technology/Data |
| AIMAA | Weighted data-driven scoring | Requires high-quality enterprise data |
| **AA Maturity Model** | **Enacted behavior — 3-layer instrument** | **First model with behavioral observation methodology from implementation science + safety culture + behavioral auditing** |

---

## Empirical Foundation — Key Numbers

| Finding | Source | Pillar | Use |
|---|---|---|---|
| 72% org maturity / 6% operational | Accenture | All | Model's core justification |
| 88% claim adoption, 74% can't scale | Accenture | Pillar 5 | Pilot purgatory |
| 54% using AI without authorization | Industry survey | Pillar 3 | Shadow AI as trust indicator |
| 2.8x more likely to redesign workflows | BCG | Pillar 2 | Level 4-5 behavioral separator |
| 25-50% implementation fidelity | Implementation science | Methodology | Three-layer instrument justification |
| 86% of AI models over-index on Tech/Data | Filipovic et al. | Competitive | Field knows the problem; AA is the solution |
| n=847 hotel implementations | Peeling the Onion | Pillar 5 | Current-State Primacy validation |
| n=665 user latent class analysis | EY | Pillar 1 | Semiautonomous collaboration evidence |
| AI adoption → lower psych safety → depression | Kim, Kim & Lee (2025) | Pillar 3 | Trust pillar is not optional |
| Lower-ability devs benefit more w/ psych safety | Hoffman et al. (2025) | Pillar 3 | Psych safety determines who captures gains |

---

## Glossary — Named Concepts

| Term | Pillar | Definition |
|---|---|---|
| Semiautonomous collaboration | 1 | High-maturity craft: structured methodology, custom agents, AI as thought partner |
| Jagged technological frontier | 2 | The boundary between what AI can and cannot do competently |
| Human-AI Sandwich | 2 | Human frames → AI executes sub-tasks → human reviews; Level 4-5 workflow |
| Super Productivity Paradox | 4 | Individual AI speed outpaces org review capacity; bottleneck just moves |
| Pilot purgatory | 5 | 88% claim adoption; 74% can't scale |
| Current-State Primacy | 5 | Mapping actual processes before tool procurement; Level 2 gate |
| Habit Stacking | 6 | Attaching AI actions to existing routines; Level 4 behavior change mechanism |
| AI slop | 3 | Outputs that look convincing but collapse under expert scrutiny |
| Contrastive explanations | 3 | Users interrogating AI logic: why this output and not another |
| Control tower | 7 | Cross-functional AI governance body with authority to pause; Level 5 differentiator |
| Knowledge hiding | 3 | Withholding expertise to protect relevance; Level 1 trust indicator |
| Algorithm aversion | 3 | Tool abandoned after single error; undertrust behavioral indicator |
| Three Trusts | 3 | Task trust + Institutional trust + Relational trust |
| People-First Flywheel | 4 | People-first use cases catalyze trust, skill pull, and psychological safety |
| COM-B (AA adaptation) | All | Capability + Motivation + Trust + Opportunity → Behavior |

---

## Key Quotes

- "Behavioral — enacted capability, not 'we could, in some world, do this' — demonstrated capability" — Paul
- "Awareness, desire, and knowledge do not add up to action" — Pillar 6 / ADKAR critique
- "You get to the efficiency gains faster by not starting with them" — Pillar 4
- "Vanishingly few walk the walk" — intention-action gap empirical finding
- "Zero trust assumes breach. Human zero trust assumes fallibility — and builds conditions where learning and safety can coexist." — Trust session
- "If an org develops people-first use cases, stuff that makes working lives better, then that patches some of the trust and skills issues — they will trust it because it serves them, and they will pull learning toward them." — Paul

---

## Repo Placement Map

```
docs/
  maturity-model/
    maturity-model-state.md          ← this file
    methodology.md                   ← to build
    competitive-landscape.md         ← to build
    empirical-foundation.md          ← to build
  pillars/
    01-master-the-craft.md
    02-embrace-complexity.md
    03-consciously-manage-trust.md
    04-put-people-first.md
    05-design-and-prototype.md
    06-prioritize-behavior.md
    07-manage-ethics-always.md

diagnostics/
  maturity-model/
    pillar-rubrics/
      03-trust-rubric.md             ← build first (draft complete)
      06-behavior-change-rubric.md   ← build second
      [01,02,04,05,07]-rubrics       ← build after
    trust-spectrum/                  ← tech debt

tools/
  trust-calibration-protocol/
    README.md
    template.md
```

---

## Build Order — March 15th Sprint

| Week | Deliverable | Status |
|---|---|---|
| **Week 1 (by Feb 28)** | Pillar 3 Trust rubric | Draft exists — 1 session |
| | Pillar 6 Behavior Change rubric | Research complete — 1 session |
| | White paper outline + methodology section | 1 session |
| | Trust spectrum visual | Concept clear — 1 session |
| **Week 2 (by Mar 7)** | Remaining 5 pillar rubrics | 1 session each |
| | 7×6 level matrix visual | 1 session |
| | White paper pillars section | Derives from rubrics |
| **Week 3 (by Mar 15)** | White paper complete + committed | — |
| | Substack launch post | Derives from white paper |
| | PDF diagnostic beta (1-2 pillars) | — |
| | GitHub Release tagged v0.1 | — |

*v0.1 = credible, defensible, honest about what is beta. Not v1.0.*

---

*Last updated: 2026-02-21 | Sessions: 2026-02-19, 2026-02-21*
*© Paul Gibbons — Adaptive Adoption (working notes)*
