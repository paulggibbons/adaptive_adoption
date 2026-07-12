# AI Adoption Friction Audit — Production Specification

**Version:** 0.1
**Status:** in development
**Owner:** Paul Gibbons

## Purpose

Diagnose the friction preventing one named AI initiative, deployment, or human–AI workflow from producing reliable changed work and organizational value.

## Unit of analysis

One specific initiative. The user must not answer for “AI across the company.”

## Eight domains

1. Value and strategic fit
2. Workflow fit
3. Technology and data fit
4. Capability and learning
5. Trust and legitimacy
6. Incentives, power, and professional identity
7. Leadership and governance
8. Measurement and adaptation

## Item model

- 32 items total
- four items per domain
- response options: 1–5 plus Unable to assess
- higher item scores indicate healthier enabling conditions and therefore lower friction
- a domain requires at least two answered items

## Domain friction score

```text
condition_score = mean(answered item scores)
friction_score = ((5 - condition_score) / 4) × 100
```

Working communication bands:

| Score | Interpretation |
|---:|---|
| 0–19 | Minimal visible friction |
| 20–39 | Manageable friction |
| 40–59 | Material friction |
| 60–79 | Severe friction |
| 80–100 | Critical friction |

These thresholds are interpretive aids, not validated cut points.

## Consequence

Each domain receives a consequence rating from 1 to 5:

1. limited local consequence
2. modest consequence
3. material consequence
4. high consequence
5. very high or potentially initiative-threatening consequence

## Behavioral evidence layer

Each domain receives a separate evidence-layer rating:

1. anecdotal or reported evidence
2. artifact evidence
3. observed behavior

This is not the five-level epistemic-strength scale of the tool itself.

## Priority score

For v0.1:

```text
priority_score = friction_score × (consequence / 5) × evidence_multiplier
```

Working evidence multipliers:

- Layer 1: 0.60
- Layer 2: 0.80
- Layer 3: 1.00

The priority score is a decision aid, not a scientifically validated ranking.

A consequence of 5 with Layer 1 evidence triggers an **urgent evidence gap** flag rather than being allowed to disappear behind the multiplier.

## Missing information

- one missing item: note evidence gap
- two missing items: score with caution
- three or four missing items: insufficient evidence; do not rank normally

Unable to assess is missing information, not a neutral score.

## Cross-domain hypotheses

Pattern rules generate hypotheses, not diagnoses.

Initial rules:

- value + workflow: solution–problem mismatch
- workflow + technology: deployment debt
- capability + trust: unsafe or defensive use
- incentives + governance: structural resistance mislabeled as communication failure
- value + measurement: no learning contract
- trust + governance: legitimacy gap

## Initial intervention prompts

Each domain includes one first-move prompt. Recommendations must be linked to the diagnosed mechanism and should not default to communication or training.

## Website behavior

- fully responsive React component inside the existing Astro diagnostic shell
- one wizard step for initiative definition, followed by one step per domain
- autosave to localStorage
- explicit local-only privacy statement
- printable results
- no server transmission in the initial release
- no account or email requirement
- direct CTA to the future Friction Mapper

## Output

- initiative summary
- eight-domain friction profile
- top three priority domains
- evidence-layer and missing-information flags
- cross-domain hypotheses
- first-move recommendations
- 90-day planning questions

## Epistemic position

Version 0.1 is a **Level 1 conceptual tool**, informed by research and practice but not psychometrically validated.

## Non-claims

The Audit does not:

- prove causality;
- certify readiness or maturity;
- assess legal compliance, cybersecurity, or model risk;
- measure individual resistance or personality;
- replace interviews, workflow observation, system data, or performance evidence;
- provide a company-wide AI maturity score.