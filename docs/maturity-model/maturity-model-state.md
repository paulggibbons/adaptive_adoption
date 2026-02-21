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

**Key principle — the Level 2/3 boundary:** Across all 7 pillars, this boundary is the same structural move: the organization becomes aware of its own gap and starts measuring it. Level 2 has a consistent behavioral definition: *"The gap between espoused and enacted is visible and being tracked."* This makes the assessment diagnostic rather than merely descriptive.

---

## The Three-Layer Assessment Structure

| Layer | What It Measures | Method |
|---|---|---|
| **1. Self-report** | What do you believe you do? | Surveys, questionnaires |
| **2. Evidence** | Show me artifacts that prove it | Documents, outputs, usage logs, governance records |
| **3. Behavioral indicators** | What would an observer see? | Direct observation, behavioral sampling, leading indicators |

High scores on Layer 1 with low Layer 2/3 scores = the 72% problem. This is the instrument's core diagnostic move.

**Academic foundations:**
- Implementation science (Proctor et al., 2011) — fidelity measurement; only 25-50% of adopted programs achieve sufficient implementation fidelity
- Safety culture research — Bradley's safety culture ladder measures observed behaviors, not survey responses
- Behavioral safety auditing (BBS) — direct observation and behavioral sampling
- Argyris — "espoused theory" vs "theory-in-use"

---

## The 7 Pillars — Integrated Research Findings

### Pillar 1: Craft — Prompt Quality and AI Skill
*Foundation: EY latent class analysis (n=665); BCG software developer survey*

**Enacted behavior measured:** Do people use AI with skill, iteration, and structured methodology — or treat it as a search engine?

**Observable behaviors:**
- *Low (0-2):* Employees use AI for "information assistance" only; abandon tool after poor result rather than iterating
- *High (4-5):* "Semiautonomous collaboration" — structured methodologies (few-shot, chain of thought), custom agents, AI as thought partner

**Leading behavioral indicator:** Team-based rituals — weekly prompt swaps, agent showcases, GenAI retrospectives. This is the Level 3 inflection point: individual skill becoming collective capability.

**Key concept:** *Semiautonomous collaboration* (EY) — the named high-maturity craft behavior.

---

### Pillar 2: Complexity — Navigating Ambiguity and System Effects
*Foundation: HBS/BCG field experiment on knowledge worker productivity*

**Enacted behavior measured:** Do people know where the AI's competence ends and theirs begins — and do they design work accordingly?

**Observable behaviors:**
- *Low (0-2):* Blindly apply AI to complex tasks; AI bolted onto existing linear processes; rework negates gains
- *High (4-5):* "Human-AI Sandwich" — human frames complex task → AI handles well-defined sub-tasks → human reviews and handles ambiguity

**Leading behavioral indicator:** Fundamental workflow redesign. High-performing teams are 2.8x more likely to dismantle and rebuild processes rather than layer AI on top.

**Key concepts:**
- *Jagged technological frontier* (BCG) — the boundary between what AI can and cannot do competently
- *Human-AI Sandwich* — the observable workflow pattern at Level 4-5

---

### Pillar 3: Trust — Calibrated Reliance on AI Outputs
*Foundation: Nature Human Behaviour studies; McKinsey Rewired; Dietvorst et al. 2015/2018; Kim, Kim & Lee 2025; Hoffman et al. 2025 (GitHub Copilot); Capital One dynamic decision rights*

**Enacted behavior measured:** Do people interact with AI with calibrated judgment — neither abandoning nor uncritically following — and does the organization create conditions where that calibration is possible?

**Trust is three-headed (critical structural point):**
1. **Task trust (micro):** "Can I trust this model to do X?" — observable through verification behavior, output review, error reporting
2. **Institutional trust (macro):** "Do I trust the technology ecosystem — labs, incentives, governance?" — observable through vendor scrutiny, governance engagement, policy co-creation
3. **Relational trust (social):** "Do I trust leadership that adoption won't harm my livelihood?" — observable through disclosure, knowledge sharing vs hiding, experimentation willingness

*Most existing models only assess Task trust. AA assesses all three.*

**Observable behaviors:**
- *Low (0-2):* Polarization — "blind trust" generating unchecked "AI slop," OR "algorithmic aversion" (tool abandoned after single error); knowledge hiding (withholding expertise to protect relevance — Arias-Pérez & Vélez-Jaramillo, 2022)
- *High (4-5):* Calibrated trust — formal consequence-bucketing processes; demand for "contrastive explanations" (users interrogate AI logic: why this output and not another?)

**Leading behavioral indicator:** Demand for contrastive explanations (Nature Human Behaviour).

**Level anchors:**
| Level | Behavioral Profile |
|---|---|
| 0 | Shadow AI high and untracked; tool abandonment unmonitored; no psychological safety to disclose use |
| 1 | Knowledge hiding present; overtrust or undertrust dominates; no feedback loop on AI errors |
| 2 | Organisation recognises undertrust/overtrust as distinct problems; tracking begins |
| 3 | Psychological safety sufficient for error disclosure; sanctioned tools exist; escalation protocols defined; Trust Calibration Protocol in use |
| 4 | Dynamic decision rights thresholds (Capital One model) — human oversight calibrated to demonstrated AI reliability |
| 5 | Trust calibration is self-correcting; organisation learns from both overtrust and undertrust events and updates governance |

**Key findings to preserve:**
- *"AI slop"* — outputs that look convincing but collapse under expert scrutiny (overtrust failure mode named)
- Kim, Kim & Lee (2025): AI adoption lowers psychological safety → depressive symptoms. Trust pillar is not optional — skipping it potentially harms people.
- Hoffman et al. (2025) GitHub Copilot: lower-ability developers benefited *more* from AI in psychologically safe environments. Psychological safety determines who captures the productivity gains.
- The Trust Calibration Protocol (tool): Low stakes → trust + spot-check; Medium stakes → source-check + human review; High stakes → mandatory review + evidence trail

**Tool:** `tools/trust-calibration-protocol/`
**Narrative:** `docs/pillars/03-consciously-manage-trust.md`

---

### Pillar 4: Efficiency — Realizing Actual Productivity Gains
*Foundation: PwC AI Jobs Barometer; Asana AI Super Productivity Paradox research*

**Enacted behavior measured:** Are organizations tracking and capturing real productivity gains — or measuring activity and calling it efficiency?

**Observable behaviors:**
- *Low (0-2):* Vanity metrics (login counts, prompt counts); "Super Productivity Paradox" — individual AI speed outpaces org review capacity, bottleneck just shifts to human approval chains
- *High (4-5):* Operational flow metrics (cycle time, merge frequency, output quality, direct time saved); dynamic decision rights

**Leading behavioral indicator:** Redesigning approval rights — dynamic decision authority shifting between humans and algorithms based on confidence scores and risk tiers. (Note: this indicator spans Pillars 3 and 4 — efficiency without trust calibration produces the Super Productivity Paradox.)

**Key concept:** *Super Productivity Paradox* (Asana) — individual speed gains are real; organizational throughput doesn't improve because the bottleneck moves.

---

### Pillar 5: Design and Prototype — Moving from Pilot to Scale
*Foundation: "Peeling the Onion" framework (n=847 hotel implementations); MIT organizational experiments approach*

**Enacted behavior measured:** Do organizations design AI initiatives with current-state rigor before procurement — or buy tools first and discover problems during pilot?

**Observable behaviors:**
- *Low (0-2):* "Tool-first procurement" — AI purchased before baseline metrics or current-state documentation; "pilot purgatory" (88% claim adoption, 74% can't scale)
- *High (4-5):* Organizational experiments using control groups and randomized rollouts to isolate causal effects

**Leading behavioral indicator:** "Current-State Primacy" documentation — systematic mapping of current manual processes (5 W's and H) to identify pain points and establish baselines *before* any tool is procured or prompt is written. This is the Level 2 gate: organizations that skip it are structurally incapable of scaling regardless of pilot success.

**Key concept:** *Pilot purgatory* — the failure mode where 88% claim adoption but 74% can't scale. A craft problem (Pillar 1) + complexity problem (Pillar 2): pilots succeed in contained conditions; scaling requires navigating complexity they don't have the capability for.

---

### Pillar 6: Behavior Change — Closing the Intention-Action Gap
*Foundation: Transformation Design Framework (TDF); Knowledge Behavior Gap (KBG) models; BCG employee-centric AI adoption research*

**Enacted behavior measured:** Do organizations close the gap between stated intention and actual behavioral change — or generate compliance theater?

**Observable behaviors:**
- *Low (0-2):* Top-down mandates → performative compliance or shadow AI usage; no psychological safety; fear of replacement
- *High (4-5):* "Habit Stacking" — attaching small AI actions to existing routines (e.g., "After I open a client file, I will spend 2 minutes asking AI to analyze recent industry news")

**Leading behavioral indicator:** Visible managerial vulnerability and role-modeling. Adoption velocity spikes when leaders visibly experiment with AI, publicly share failures, and integrate AI learning into existing team rhythms. This is the Level 3 signal — the behavioral marker that predicts whether top-down adoption will stick.

**Behavior change arc:**
- Level 1: Mandate
- Level 3: Role-modeling (leading indicator)
- Level 4: Habit integration (mechanism)
- Level 5: Self-sustaining behavioral culture

**ADKAR critique:** Awareness, Desire, and Knowledge do not add up to Action. ADKAR's empirical blind spot — organizations that score high on A, D, K but fail at Ability and Reinforcement because behavioral science was never part of the model. AA corrects this.

---

### Pillar 7: Ethics — Consequence Reasoning and Responsible Use
*Foundation: Accenture/Stanford Responsible AI Survey (n=1,000 companies); GenAI-induced Cognitive Dissonance studies*

**Enacted behavior measured:** Is ethics embedded in the design and deployment process — or applied as a compliance checklist after the fact?

**Observable behaviors:**
- *Low (0-2):* Ethics as abstract compliance checklist applied *after* development; cognitive dissonance (convenience prioritized over integrity)
- *High (4-5):* "Ethics by design" — bias testing, explainability, accuracy checks embedded in self-service tooling and data pipeline; continuous post-deployment monitoring; active red-teaming (simulating failure scenarios)

**Leading behavioral indicator:** Presence of a cross-functional "control tower" — an AI Governance body that monitors risk in real-time, conducts pre-mortems before sprints, and has *authority to pause or alter AI projects*. Advisory bodies exist at Level 3; authority to pause is the Level 5 differentiator.

**Level anchors:**
- Level 1: Ethics checklist exists, applied post-development
- Level 3: Cross-functional ethics body exists — advisory role
- Level 4: Ethics embedded in tooling and pipeline; red-teaming practice
- Level 5: Control tower with genuine authority; pre-mortems standard practice

---

## Competitive Landscape Summary

| Model | Measures | AA Differentiation |
|---|---|---|
| MITRE AI MM | Technical capability, data, governance | Zero behavioral science, zero trust |
| IBM GenAI | Infrastructure, model hosting, tuning | Humans don't appear |
| Gartner | Technology readiness, people/culture survey | Culture is a survey dimension — no behavioral observation |
| Accenture Responsible AI | Identifies org vs operational maturity gap | Identifies the gap; AA measures inside it with behavioral instruments |
| EY | Behavioral archetypes; emotional journey | Archetypes descriptive not diagnostic; no behavioral observation layer |
| IDC | Tracks shadow AI → legitimate use | Tracks as metric, not as trust indicator with root cause |
| McKinsey | Workflow redesign, agentic org | No behavioral observation methodology |
| PwC | KPIs, outcome monitoring | Still artifact-based |
| Deloitte | Human capital, workforce analyzers | Infers behavior from org artifacts |
| Healthcare (Filipovic) | Adds regulations, people, organization to technical models | Academic validation: 86% of models over-index on Technology/Data |
| AIMAA | Weighted data-driven scoring | Requires high-quality enterprise data; still infrastructure story |
| **AA Maturity Model** | **Enacted behavior — 3-layer instrument** | **First model with behavioral observation methodology derived from implementation science, safety culture research, and behavioral auditing** |

---

## Empirical Foundation — Key Numbers

| Finding | Source | Pillar | Use |
|---|---|---|---|
| 72% org maturity / 6% operational maturity | Accenture | All | Model's core justification |
| 88% claim adoption, 74% can't scale | Accenture | Pillar 5 | Pilot purgatory definition |
| 54% using AI without authorization | Industry survey | Pillar 3 | Shadow AI as trust indicator |
| 2.8x more likely to redesign workflows | BCG | Pillar 2 | Level 4-5 behavioral separator |
| 25-50% implementation fidelity | Implementation science | Methodology | Three-layer instrument justification |
| 86% of AI models over-index on Technology/Data | Filipovic et al. | Competitive | Field knows the problem; AA is the solution |
| n=847 hotel implementations | Peeling the Onion | Pillar 5 | Current-State Primacy validation |
| n=665 user latent class analysis | EY | Pillar 1 | Semiautonomous collaboration evidence |
| AI adoption → lower psych safety → depression | Kim, Kim & Lee (2025) | Pillar 3 | Trust pillar is not optional |

---

## Glossary — Named Concepts

| Term | Pillar | Definition |
|---|---|---|
| Semiautonomous collaboration | 1 | High-maturity craft: structured methodology, custom agents, AI as thought partner |
| Jagged technological frontier | 2 | The boundary between what AI can and cannot do competently |
| Human-AI Sandwich | 2 | Human frames → AI executes sub-tasks → human reviews; Level 4-5 workflow pattern |
| Super Productivity Paradox | 4 | Individual AI speed outpaces org review capacity; bottleneck just moves |
| Pilot purgatory | 5 | 88% claim adoption; 74% can't scale |
| Current-State Primacy | 5 | Mapping actual processes before tool procurement; Level 2 gate |
| Habit Stacking | 6 | Attaching AI actions to existing routines; Level 4 behavior change mechanism |
| AI slop | 3 | Outputs that look convincing but collapse under expert scrutiny; overtrust failure mode |
| Contrastive explanations | 3 | Users interrogating AI logic: why this output and not another; leading trust indicator |
| Control tower | 7 | Cross-functional AI governance body with authority to pause; Level 5 ethics indicator |
| Knowledge hiding | 3 | Withholding expertise to protect relevance when psychological safety is absent; Level 1 trust indicator |
| Algorithm aversion | 3 | Tool abandoned after single error; undertrust behavioral indicator |
| Automation bias / Cognitive offloading | 3 | Accepting AI output without review; overtrust behavioral indicator |
| Three Trusts | 3 | Task trust + Institutional trust + Relational trust — must assess all three |

---

## Key Quotes

- "Behavioral — enacted capability, not 'we could, in some world, do this' — but this is demonstrated capability" — Paul
- "Awareness, desire, and knowledge do not add up to action" — Pillar 6 / ADKAR critique
- "You get to the efficiency gains faster by not starting with them" — Pillar 4
- "Vanishingly few walk the walk" — Intention-action gap empirical finding
- "Zero trust assumes breach. Human zero trust assumes fallibility — and builds conditions where learning and safety can coexist." — Trust session

---

## Repo Placement Map

```
docs/
  pillars/
    01-craft.md
    02-complexity.md
    03-consciously-manage-trust.md
    04-efficiency.md
    05-design-and-prototype.md
    06-prioritize-behavior.md
    07-manage-ethics-always.md
  maturity-model/
    maturity-model-state.md          ← this file
    methodology.md                   ← to build
    competitive-landscape.md         ← to build
    empirical-foundation.md          ← to build

diagnostics/
  maturity-model/
    pillar-rubrics/
      01-craft-rubric.md             ← to build
      02-complexity-rubric.md
      03-trust-rubric.md             ← draft complete (session 2026-02-21)
      04-efficiency-rubric.md
      05-design-prototype-rubric.md
      06-behavior-change-rubric.md
      07-ethics-rubric.md
    trust-spectrum/                  ← future: undertrust ↔ calibrated ↔ overtrust diagnostic

tools/
  trust-calibration-protocol/
    README.md
    template.md

research/
  notebooklm-enacted-gap-evidence.md
  notebooklm-competitive-landscape.md
  notebooklm-trust-behavioral-indicators.md
```

---

## What Comes Next (Build Order)

1. [ ] Build Pillar 3 (Trust) rubric — full three-layer assessment instrument (draft in session 2026-02-21)
2. [ ] Build Pillar 6 (Behavior Change) rubric — strongest ADKAR critique foundation
3. [ ] Extend to remaining 5 pillars
4. [ ] Build `methodology.md` — three-layer instrument methodology + academic foundations
5. [ ] Build `competitive-landscape.md` — full positioning against 12 reviewed models
6. [ ] Build radar chart diagnostic tool
7. [ ] Write `empirical-foundation.md` — the "why this model exists" chapter

---

*Last updated: 2026-02-21 | Session: trust + behavioral indicators NLM outputs integrated*
*© Paul Gibbons — Adaptive Adoption (working notes)*
