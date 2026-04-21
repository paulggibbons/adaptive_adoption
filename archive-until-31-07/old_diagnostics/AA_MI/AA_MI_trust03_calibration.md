---
title: AAMI Pillar 3 — Trust Calibration (Proof of Concept)
date: 2026-02-25
version: 0.1
status: draft
type: pillar-spec
project: adaptive-adoption
parent: "[[aami-structure]]"
tags: #adaptive-adoption, #aami, #trust, #calibration, #behavioral-indicators, #three-layer-assessment
---

# AAMI Pillar 3: Trust Calibration
## Proof-of-Concept Specification

---

## Pillar Definition

**Core Question**: Is trust in AI commensurate with demonstrated reliability — neither overtrusting nor undertrusting?

**Why Trust Calibration?**  
Trust calibration is the most behaviorally measurable of the seven pillars, and the most consequential. Miscalibrated trust is the proximate cause of most AI failures in organizations:

- **Overtrust**: accepting AI outputs without appropriate scrutiny; automation bias; surrendering judgment to the system
- **Undertrust**: refusing to use AI tools that would genuinely help; requiring human re-verification of every AI output regardless of stakes; performative skepticism

Both failure modes are observable. Both have defined behavioral signatures at each maturity level. Neither is captured by any existing AI maturity model.

**Academic grounding**:
- Lee & See (2004): trust in automation as a function of performance, process, and purpose
- Parasuraman & Riley (1997): misuse (overtrust) and disuse (undertrust) as dual failure modes
- Mayer, Davis & Schoorman (1995): trust as ability, benevolence, integrity — applies directly to AI systems
- Kahneman (2011): System 1 automation bias — the default tendency to accept machine outputs

---

## Sub-Dimensions

Pillar 3 is assessed across four sub-dimensions:

| # | Sub-Dimension | What It Measures |
|---|---------------|-----------------|
| 3a | **Verification behavior** | Do people check AI outputs in proportion to the stakes? |
| 3b | **Error recognition** | Can people identify when AI is confidently wrong? |
| 3c | **Overtrust signals** | Are there observable patterns of uncritical acceptance? |
| 3d | **Undertrust signals** | Are there observable patterns of blanket rejection or performative skepticism? |

---

## Maturity Level Specifications

### Level 1 — Unaware

**Behavioral Signature**: Trust is entirely uncalibrated. Either wholesale adoption without scrutiny or wholesale rejection without engagement. No distinction made between high-stakes and low-stakes AI use.

**3a — Verification behavior**  
What you observe: AI outputs used without any verification. Copy-paste from AI to final output is standard practice. OR: AI tools not used at all, so no verification question arises.  
Evidence: No review checkpoints exist in any AI-assisted workflows.  
Self-report question: *"How does your team decide when to verify an AI output before acting on it?"* (Expected answer: no systematic approach; verification is individual and arbitrary, or not considered)

**3b — Error recognition**  
What you observe: People cannot articulate how they would know if an AI was wrong. Confidence in AI is indistinguishable from confidence in an expert colleague.  
Evidence: No examples of AI error identification in team records, post-mortems, or shared channels.  
Self-report question: *"Can you give an example of catching an AI error in the last month?"*

**3c — Overtrust signals**  
What you observe: AI-generated content submitted to clients, leadership, or public channels without review. Hallucinated facts or fabricated citations appear in outputs.  
Evidence: Incidents or near-misses attributable to unchecked AI output.  
Self-report question: *"Has your team ever caught an AI error before it caused a problem?"*

**3d — Undertrust signals**  
What you observe: Explicit refusal to use AI tools despite demonstrated utility. Requiring all AI-assisted work to be redone by humans before use.  
Evidence: Formal or informal policies restricting AI use beyond what risk warrants.  
Self-report question: *"Are there areas where your team could use AI but chooses not to? Why?"*

---

### Level 2 — Experimenting

**Behavioral Signature**: Some individuals have developed personal heuristics for when to trust AI. These are intuitive and not shared. The organization as a whole has no calibration framework. Overtrust and undertrust coexist in different individuals or teams.

**3a — Verification behavior**  
What you observe: Individual variation — some people check outputs, others don't. Verification is stakes-blind (same scrutiny applied to a tweet as to a regulatory submission).  
Evidence: No organizational standard; individual approaches undocumented.  
Self-report question: *"Do different people on your team have different approaches to checking AI work? Who decides?"*

**3b — Error recognition**  
What you observe: Individuals who use AI heavily can sometimes identify when outputs "feel off." Cannot always articulate why. Catching errors is accidental rather than systematic.  
Evidence: Anecdotal examples exist but are not captured or shared.  
Self-report question: *"When you catch an AI error, what does that process look like? Do you share it with others?"*

**3c — Overtrust signals**  
What you observe: Occasional incidents where AI errors reach downstream. Treated as one-off mistakes rather than systemic signals.  
Evidence: Incidents occur but are not analyzed.  
Self-report question: *"Has the team had any situations where an AI output turned out to be wrong after it had been used?"*

**3d — Undertrust signals**  
What you observe: Pockets of resistance. Some team members consistently avoid AI tools their colleagues use effectively.  
Evidence: Usage data shows high variance across team members without correlation to role or task type.  
Self-report question: *"Are there team members who are skeptical of AI? How does that play out in practice?"*

---

### Level 3 — Practicing

**Behavioral Signature**: The team has developed shared, explicit heuristics for when and how to verify AI outputs. Stakes-proportionate verification is the norm. Errors are caught and discussed. Overtrust and undertrust are recognized as failure modes rather than positions.

**3a — Verification behavior**  
What you observe: Team applies different scrutiny to AI outputs based on stakes. High-stakes use (client deliverables, financial decisions, public statements) has defined verification steps. Low-stakes use (internal drafts, brainstorming) has lighter touch.  
Evidence: Documented workflow checkpoints for AI-assisted work. Review steps visible in project management tools or shared templates.  
Self-report question: *"Walk me through how your team decides how much to check an AI output. Does it vary by task?"*

**3b — Error recognition**  
What you observe: Team members can articulate common AI failure modes relevant to their work (hallucination, outdated knowledge, overconfident tone, loss of nuance). When an error is caught, it is shared.  
Evidence: Team retros, Slack channels, or shared docs contain examples of caught AI errors.  
Self-report question: *"What are the most common ways AI gets things wrong in your type of work? How did you learn that?"*

**3c — Overtrust signals**  
What you observe: Overtrust incidents are rare and when they occur, are treated as learning events. No pattern of unchecked AI-to-output pipelines.  
Evidence: Review checkpoints exist and are used.  
Self-report question: *"When was the last time an AI error made it into a final output? What happened?"*

**3d — Undertrust signals**  
What you observe: Skepticism about AI is expressed as specific, evidence-based concern ("this model is unreliable for X type of task") rather than blanket refusal.  
Evidence: Decisions not to use AI are documented with rationale.  
Self-report question: *"Can you give an example of deciding not to use AI for something? What drove that decision?"*

---

### Level 4 — Integrating

**Behavioral Signature**: Trust calibration is organizational rather than individual. The team actively tracks AI reliability by task type, learns from near-misses, and updates its calibration accordingly. The espoused-enacted gap on trust is narrow and closing.

**3a — Verification behavior**  
What you observe: Verification protocols are embedded in workflows and consistently applied. Different task categories have different verification standards, documented and followed.  
Evidence: Workflow documentation specifies verification steps by task type. Usage logs or review records show compliance.  
Self-report question: *"Do you have different verification standards for different types of AI-assisted work? Are they written down?"*

**3b — Error recognition**  
What you observe: Team maintains an informal or formal record of AI failure modes encountered. New failure modes are added as discovered. Onboarding includes calibration training.  
Evidence: Failure mode library or equivalent. Onboarding materials address AI trust calibration.  
Self-report question: *"How do new team members learn when to trust AI outputs in your context?"*

**3c — Overtrust signals**  
What you observe: No pattern of overtrust incidents. Near-misses are captured as data and used to update verification standards.  
Evidence: Near-miss capture process exists. Review cadence for verification standards.  
Self-report question: *"How do you update your verification approach when you discover a new way AI can fail?"*

**3d — Undertrust signals**  
What you observe: No blanket AI avoidance. When AI is not used, the rationale is specific and revisited as capabilities evolve.  
Evidence: Regular review of AI non-use decisions.  
Self-report question: *"Are there areas where you decided not to use AI in the past that you've since reconsidered?"*

---

### Level 5 — Adaptive

**Behavioral Signature**: Trust calibration keeps pace with changing AI capabilities. The organization updates its calibration proactively as models improve, degrade, or new failure modes are discovered. Trust calibration is institutionalized as an ongoing process, not a one-time assessment.

**3a — Verification behavior**  
What you observe: Verification standards are reviewed on a defined cadence and updated as model capabilities change. The organization does not continue applying 2023 verification standards to 2026 models.  
Evidence: Version-controlled verification standards with revision history. Review cadence documented.  
Self-report question: *"How have your verification practices changed as AI capabilities have improved? What triggered those changes?"*

**3b — Error recognition**  
What you observe: Team actively monitors for new AI failure modes as models update. Emerging failure modes (e.g., sycophancy, prompt injection risks, capability regression after model updates) are tracked.  
Evidence: Active monitoring process for AI reliability changes. Communication to team when verification standards change.  
Self-report question: *"How do you find out when an AI model's reliability changes? Who is responsible for tracking that?"*

**3c — Overtrust signals**  
What you observe: None. The calibration system catches drift before it becomes incident.  
Evidence: Audit trail of near-miss captures and verification standard updates.  
Self-report question: *"Has your verification approach ever been too lenient? How did you find out, and what changed?"*

**3d — Undertrust signals**  
What you observe: None. The team expands AI use proactively as reliability is demonstrated, rather than waiting for policy permission.  
Evidence: Examples of AI use expanding into new task categories with documented rationale and new verification standards.  
Self-report question: *"Can you give an example of expanding AI use in the last year as you became more confident in reliability? What convinced you?"*

---

## Scoring This Pillar

### Calculating the Sub-Dimension Score

For each sub-dimension (3a, 3b, 3c, 3d):
1. Administer the self-report question(s) — score 1–5 based on response quality and specificity
2. Request evidence artifacts — score 1–5 based on existence, specificity, and currency
3. Conduct behavioral observation or behavioral sampling — score 1–5 based on what you observe

**Sub-dimension score** = lowest of the three layer scores (enacted floor, not espoused ceiling)

### Calculating the Pillar 3 Score

**Pillar 3 score** = mean of (3a score, 3b score, 3c score, 3d score), rounded to nearest 0.5

### Calculating the Trust Calibration Gap Score

**Gap Score** = Layer 1 mean (self-report across sub-dimensions) − Layer 3 mean (behavioral observation across sub-dimensions)

```
Gap Score interpretation:
  0.0–0.5  : Calibrated — organization practices what it believes
  0.5–1.5  : Awareness gap — knows it should verify but doesn't consistently
  1.5+     : Theatre — stated trust calibration has no behavioral reality
```

---

## Diagnostic Patterns

### Common Gap Patterns in Trust Calibration

**"We have a process" gap**: High self-report on 3a (claims verification is standard), low behavioral observation (verification rarely happens). Gap Score 1.5+. Intervention: process redesign + behavioral accountability.

**"Stars and stragglers" gap**: High individual variance on 3b and 3c. Some team members are well-calibrated; most are not. Gap Score moderate (0.5–1.5). Intervention: peer learning + shared failure mode library.

**"Policy theater" gap**: Evidence layer shows verification protocols exist; behavioral layer shows they are ignored. Gap Score high on 3a specifically. Intervention: workflow integration (make verification impossible to skip, not just mandatory).

**"Legacy undertrust" gap**: High 3d scores (undertrust) in organizations with previous AI failures. Low willingness to re-engage even as capabilities improve. Intervention: controlled trust-building experiments with explicit learning review.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1 | 2026-02-25 | Initial proof-of-concept — all five levels, four sub-dimensions, three-layer assessment, scoring, gap patterns |
