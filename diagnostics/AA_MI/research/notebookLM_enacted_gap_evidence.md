---
title: Empirical Evidence — The Enacted-Behavior Gap
date: 2026-02-25
type: research
status: canonical
project: adaptive-adoption
parent: "[[aami-structure]]"
related:
  - "[[aami-pillar3-trust-calibration]]"
  - "[[framework-comparison]]"
tags: #adaptive-adoption, #aami, #research, #evidence, #enacted-behavior, #espoused-vs-enacted
source: NotebookLM synthesis — 48-source adoption research corpus
---

# Empirical Evidence: The Enacted-Behavior Gap
## Why the AAMI Measures What Others Don't

---

## The Core Finding

This document collects the empirical evidence base validating the AAMI's central claim: that measuring **espoused organizational capability** (what all existing maturity models do) systematically misrepresents the state of AI adoption, and that **enacted behavior** is the only measurement that matters.

These findings are not edge cases. They are the mainstream finding across independent research streams. Every data point below is a nail in the coffin of capability-based maturity models.

---

## Finding 1: The 72% vs 6% Chasm

**Source**: Accenture

**Data**: 72% of organizations score high on organizational AI maturity. Only 6% score high on operational AI maturity.

**What this means for the AAMI**:

This is not a gap. It is a chasm — a 66-point divergence between what organizations claim and what they can actually do. Every maturity model that measures organizational capability (which is all of them — MITRE, IBM, Gartner, Prosci, AWS, CMMI) is telling 72% of companies they are doing fine. Only 6% actually are.

The AAMI is the first model designed to measure the 6%, not the 72%.

**Pillar relevance**: All pillars, but especially Pillar 7 (Governance Enactment) and Pillar 6 (Behavioral Consistency). The 66-point gap is the espoused-enacted gap made quantitative.

**Quote to use**: *"72% score high on organizational maturity but only 6% on operational maturity. Every existing model is measuring the 72% and calling it success."*

---

## Finding 2: Pilot Purgatory — 88% Claim Adoption, 74% Can't Scale

**Source**: Research corpus (multiple sources)

**Data**: 88% of organizations claim AI adoption. 74% cannot scale beyond pilot.

**What this means for the AAMI**:

"Pilot purgatory" is the name for this failure mode. Organizations can run a pilot because pilots are contained — small teams, defined scope, sympathetic sponsors, minimal integration requirements. They cannot scale because scaling requires navigating organizational complexity, and they lack the capability.

This is not primarily an adoption problem. It is:
- A **craft problem** (Pillar 1: Strategic Alignment — leaders chose pilots that couldn't scale by design)
- A **complexity problem** (Pillar 4: Workflow Integration — integration into existing systems was never solved)
- A **behavioral problem** (Pillar 5: Learning Velocity — the organization didn't learn from the pilot what scaling would require)

Claiming 88% adoption while 74% are stuck in purgatory is the organizational equivalent of saying you've learned to swim because you can float with a life jacket.

**Pillar relevance**: Pillar 1 (Strategic Alignment), Pillar 4 (Workflow Integration), Pillar 5 (Learning Velocity).

**Quote to use**: *"88% claim adoption. 74% can't scale. That's not an adoption problem — that's a behavioral capability problem that no existing model measures."*

---

## Finding 3: Shadow AI — The Trust Failure in Both Directions

**Source**: Research corpus

**Data**: 54% of employees use AI tools without organizational authorization.

**What this means for the AAMI**:

Shadow AI is Pillar 3 (Trust Calibration) made visible. Leadership is in "contemplation phase" while the workforce has already moved. This is a trust failure operating simultaneously in two directions:

- **Leadership doesn't trust the workforce** enough to enable them — so policy is restriction, not enablement
- **The workforce doesn't trust leadership** enough to wait — so they route around policy entirely

The result is unauthorized AI use at scale, with no organizational learning, no failure capture, no calibration. The worst possible outcome: the enacted behavior is happening, but invisibly, so the organization cannot improve.

An espoused-capability model would score this organization's AI governance as "in progress" (policy under development). The AAMI would score it as Level 1 on Pillar 7 (Governance Enactment) — because governance that 54% of employees are actively circumventing is not governance.

**Pillar relevance**: Pillar 3 (Trust Calibration), Pillar 7 (Governance Enactment), Pillar 2 (Psychological Safety — employees don't feel safe declaring their actual AI use).

**Quote to use**: *"54% using AI without authorization. Leadership in contemplation while the workforce has already moved. That's a trust failure in both directions — and no existing model diagnoses it."*

---

## Finding 4: The Intention-Action Gap — "Vanishingly Few Walk the Walk"

**Source**: Research corpus

**Data**: Organizations that score high on AI adoption intention, strategy, and awareness consistently fail to convert to behavioral change. Researchers used the phrase "vanishingly few walk the walk."

**What this means for the AAMI**:

This is Pillar 6 (Behavioral Consistency) validated by name, and it is ADKAR's empirical indictment. ADKAR measures Awareness, Desire, Knowledge, Ability, Reinforcement. The research finds that organizations achieve the first three (Awareness, Desire, Knowledge) and fail at the last two (Ability, Reinforcement) — because behavioral science was never part of the model. You cannot reinforce behavior you haven't defined as a behavioral target.

The intention-action gap is not a motivation problem. It is a measurement problem: if you measure intention, you will optimize for intention. The AAMI measures action.

**Pillar relevance**: Pillar 6 (Behavioral Consistency) directly. Also Pillar 5 (Learning Velocity) — organizations that don't learn from the intention-action gap repeat it.

**Quote to use**: *"'Vanishingly few walk the walk.' They literally found ADKAR's blind spot empirically — awareness and desire don't produce behavior. The AAMI measures behavior."*

---

## Synthesis: What These Findings Prove

Together, these four findings establish three claims that underpin the entire AAMI:

### Claim 1: Existing models are measuring the wrong thing
The 72% vs 6% finding is definitive. When 72% pass the test and only 6% can actually do the thing, the test is wrong. All existing models share this flaw — they measure organizational capability (processes, policies, platforms) not enacted behavior.

### Claim 2: The gap is not random — it is systematic and predictable
Pilot purgatory, shadow AI, and the intention-action gap are not idiosyncratic organizational failures. They are the predictable consequences of measuring espoused capability and ignoring the behavioral conditions required to enact it. The AAMI's seven pillars are defined to target exactly the behavioral conditions that these failure modes violate.

### Claim 3: The gap is diagnosable and therefore closable
The AAMI's three-layer assessment (self-report, evidence, behavioral indicators) is designed to surface the gap explicitly — as a number (the Gap Score), not just a qualitative observation. What is measured can be managed. The Gap Score is the intervention target.

---

## Uses for This Document

### In the AAMI repo
This is the research foundation for the `diagnostics/aami/` directory. It should be linked from:
- `aami-structure.md` (the "Why This Model Exists" section)
- `README.md` (the repo's empirical credibility section)
- Each pillar specification (in the academic grounding section)

### In Book 8 (Adopting AI)
This becomes the empirical foundation chapter — the section that proves the problem before introducing the solution. The four findings build a prosecutorial case against existing models before the AAMI is introduced.

### In speaking/advisory materials
The 72% vs 6% number is the opening provocation for any board or executive audience. One slide. One number. "Every model you've seen is measuring the 72% and calling it done."

### In the AAMI positioning doc / white paper
The "why this model exists" section opens with these four findings. They are the demand-side case; the AAMI is the supply-side response.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1 | 2026-02-25 | Initial synthesis from NotebookLM 48-source corpus and Paul's analysis |
