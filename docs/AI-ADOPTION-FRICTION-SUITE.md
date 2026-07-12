# AI Adoption Friction Suite

**Status:** product architecture v0.1
**Owner:** Paul Gibbons
**Last reviewed:** 2026-07-11

## Product thesis

Most AI adoption work misdiagnoses failure as a generic resistance, capability, or communication problem. The AI Adoption Friction Suite treats adoption failure as a patterned interaction among the initiative, the workflow, the organization, and the people expected to use or govern it.

The Suite is a connected family of tools sharing one friction taxonomy, one evidence language, and one intervention logic.

## The three tools

### 1. AI Adoption Friction Audit

**Question:** What kinds of friction are preventing one named AI initiative or workflow from achieving adoption and value?

**Unit of analysis:** one specific AI initiative, deployment, workflow, or use case.

**Primary output:** a friction profile identifying the highest-priority domains, consequences, confidence in the evidence, and immediate investigative priorities.

**Target completion time:** 10–15 minutes.

### 2. AI Adoption Friction Mapper

**Question:** Where is the friction concentrated, between which groups, and where does it propagate through the work?

**Unit of analysis:** the organizational system surrounding the same initiative.

**Primary output:** a heatmap across functions, teams, roles, workflow handoffs, or adoption stages; ownership gaps; cross-functional dependencies; and bottleneck relationships.

**Target completion time:** 20–30 minutes.

The Mapper is not a second survey that averages the Audit by department. It captures structural and relational information: who experiences the friction, who produces or amplifies it, who can resolve it, and where one group’s workaround becomes another group’s burden.

### 3. 90-Day Intervention Planner

**Question:** What should be done next, by whom, and in what sequence?

**Unit of analysis:** the priority friction pattern produced by the Audit and Mapper.

**Primary output:** a sequenced 90-day plan with intervention owners, milestones, evidence requirements, and adaptation checkpoints.

**Target completion time:** 15–20 minutes.

## Shared friction taxonomy

The provisional eight domains are:

1. Value and strategic fit
2. Workflow fit
3. Technology and data fit
4. Capability and learning
5. Trust and legitimacy
6. Incentives, power, and professional identity
7. Leadership and governance
8. Measurement and adaptation

The taxonomy may evolve during instrument development, but all three tools must use the same domain keys and definitions.

## Shared evidence model

Every friction claim should separate:

- **severity or consequence** — how much the friction matters;
- **evidence confidence** — how confident the user should be in the finding;
- **behavioral evidence layer** — anecdotal/reported, artifact, or observed behavior;
- **tool epistemic strength** — the independent five-level strength of the instrument itself.

See [EVIDENCE-SCALES.md](EVIDENCE-SCALES.md).

## Product sequence

### Phase 1 — Audit MVP

Ship the Audit first as a public, self-scored, cross-cutting diagnostic.

Required outputs:

- initiative definition;
- friction-domain profile;
- top three priority domains;
- consequence and evidence-confidence ratings;
- interpretation narrative;
- next evidence to gather;
- initial interventions;
- CTA to map the friction across the organization.

### Phase 2 — Mapper

The Mapper should consume the Audit result rather than force users to re-enter it.

Provide two views:

- **organizational view:** function/team/role × friction domain;
- **journey view:** adoption stage/workflow step × friction domain.

Do not force a three-dimensional team × stage × domain interface in v1.

### Phase 3 — Planner

Generate a bounded 90-day response using the priority frictions and ownership map.

The Planner must distinguish:

- action;
- responsible owner;
- affected groups;
- evidence required;
- dependency;
- timing;
- adaptation checkpoint;
- expected behavioral signal.

## Audit design principles

- One initiative per completion.
- No claim of company-wide maturity.
- No objectively correct answer key.
- No single grand maturity score unless empirical work later supports one.
- Preserve domain-level patterns and tensions.
- Make uncertainty visible.
- Treat self-report as behavioral-evidence Layer 1.
- Provide practical next steps without implying scientific validation.

## Provisional Audit structure

Four items per domain, 32 items total.

Each item should capture a clearly observable condition, using a response scale that distinguishes absence, inconsistency, and reliable presence.

Recommended response fields:

- condition rating;
- consequence rating;
- evidence source/layer;
- optional note.

The initial public version may simplify the interface by collecting consequence and evidence confidence at domain level rather than for every item.

## Mapper design principles

The Mapper must reveal relationships rather than merely display departmental scores.

It should capture:

- where friction is experienced;
- where it originates;
- where it is amplified;
- who owns the decision;
- who absorbs the cost;
- where handoffs fail;
- where workarounds emerge;
- where evidence is missing.

## Planner design principles

Interventions should be selected because they address a diagnosed friction mechanism, not because they are standard change-management activities.

Every recommendation should state:

- which friction it addresses;
- why it should work;
- what behavior should change;
- what evidence would confirm progress;
- when to adapt or stop.

## Product ladder

1. Public Friction Audit
2. Friction Mapper
3. 90-Day Intervention Planner
4. Fully asynchronous practitioner course
5. Organizational/team edition
6. Portfolio or advisory application

## Relationship to the course

The Suite is the reusable intellectual product. The course teaches practitioners how to apply it responsibly.

The course should not be required to understand the public Audit. It should deepen:

- diagnosis;
- evidence quality;
- pattern interpretation;
- mapping across organizational boundaries;
- intervention selection;
- adaptation over time.

## Data architecture

The Suite should use shared identifiers for:

- suite version;
- instrument version;
- scoring version;
- initiative/session identifier;
- friction-domain keys;
- evidence layer;
- function/team/role;
- workflow/adoption stage;
- intervention identifiers.

Audit, Mapper, and Planner records must be linkable without requiring personally identifiable information.

## Initial epistemic position

The Audit begins as a **Level 1 conceptual tool informed by research and practice**. It should move to Level 2 only when the item set and model are explicitly traceable to relevant research and documented evidence. Levels 3–5 require distinct validation work and must not be inferred from usage volume or favorable feedback.

## Immediate build decision

Build the Audit first. Design the shared data model so the Mapper and Planner can consume its output, but do not delay the Audit by attempting to build the full Suite at once.