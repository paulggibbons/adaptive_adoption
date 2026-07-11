# PGA Diagnostics — Evidence Scales

**Status:** canonical definitions
**Owner:** Paul Gibbons
**Last reviewed:** 2026-07-11

The diagnostics system uses two different evidence scales. They measure different things and must never share one field.

## 1. Epistemic strength of a model or tool — five levels

This scale evaluates the evidential strength of the **model, framework, diagnostic, or tool itself**.

| Level | Name | Meaning |
|---:|---|---|
| 1 | Conceptual | A reasoned proposition, synthesis, or prototype whose usefulness is plausible but not yet established empirically. |
| 2 | Research-grounded | Built from relevant research, established theory, or documented evidence, but the particular tool has not itself been validated. |
| 3 | Face validity | Qualified users or experts judge that the tool appears to represent the intended construct and is credible for its stated purpose. |
| 4 | Construct validity | Evidence shows that the tool measures the construct it claims to measure and behaves appropriately relative to related constructs. |
| 5 | Predictive validity | Evidence shows that the tool predicts meaningful later outcomes or performance with adequate reliability. |

Levels 4 and 5 are intentionally demanding and should be rare. They must not be awarded because a tool is polished, popular, commercially useful, or based on a respected source.

The structured manifest field `epistemic.level` stores this five-level scale.

## 2. Behavioral evidence layer — three levels

This scale evaluates the **kind of evidence available about organizational behavior or adoption**. It does not evaluate the scientific validity of the tool collecting that evidence.

| Layer | Name | Meaning |
|---:|---|---|
| 1 | Anecdotal or reported evidence | What people say, recall, believe, intend, or report in interviews, surveys, conversations, or self-assessments. |
| 2 | Artifact evidence | Something durable has been written, configured, recorded, or institutionalized: a policy, process, playbook, decision record, workflow specification, system setting, or similar artifact. |
| 3 | Observed behavior | Evidence of what people actually do in practice, through direct observation, reliable traces, enacted workflow, or repeated behavior. |

An artifact is stronger than an anecdote but does not prove that the documented practice is enacted. Observed behavior is the strongest layer in this behavioral-evidence scale.

## 3. The scales are independent

A tool can have high epistemic strength while collecting only anecdotal/self-report data. Conversely, a conceptually early tool may capture genuine observed behavior.

Examples:

- A validated questionnaire completed by one executive: high tool epistemic strength, Layer 1 behavioral evidence.
- An early workflow-observation method applied to system logs and direct observation: low tool epistemic strength, Layer 3 behavioral evidence.
- A written AI policy: Layer 2 behavioral evidence, regardless of the epistemic strength of the framework used to analyze it.

Never infer one scale from the other.

## 4. Data-model rule

- `epistemic.level` = five-level epistemic strength of the model/tool.
- Behavioral evidence must use a separate field or explicit label, such as `behavioral_evidence_layer`.
- Labels such as `Layer 1 self-report`, `Layer 2 artifact`, or `Layer 3 observed behavior` must not be encoded as epistemic levels.

The current system often records behavioral evidence only in human-readable labels. A future schema change may add a structured behavioral-evidence field, but that decision should be explicit and migration-backed.

## 5. Use in the AI Adoption Friction Suite

The Friction Suite should distinguish:

- how strong the Friction Audit model is as a tool;
- what evidence supports each friction finding.

A respondent's perception may identify a plausible friction at behavioral-evidence Layer 1. A policy, role description, workflow document, or governance artifact may raise confidence to Layer 2. Observation of real work, system traces, recurring workarounds, or enacted decisions may support Layer 3.

The Suite should not pretend that a self-report answer is observed behavior, and it should not treat a sophisticated interface as scientific validation.