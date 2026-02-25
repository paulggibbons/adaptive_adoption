# Adaptive Adoption
### The first change framework built in code — not living in PDFs, but in a repository.

**Adaptive Adoption** is a code-native, open change method for adopting AI in organizations — built to evolve as fast as the technology.

Most change frameworks live as static PDFs and certification decks. Adaptive Adoption ships as a **repository**:

- **Docs**: the narrative method (pillars + theory)
- **Diagnostics**: assessment instruments (inputs → scores → recommendations)
- **Tools**: operational playbooks and templates ("what to do Monday morning")
- **Industry modules**: forkable extensions (healthcare, government, financial services, etc.)
- **Agent**: automation that monitors staleness and drafts updates

> *"We are all apprentices in a craft where no one ever becomes a master."* — Ernest Hemingway

---

## Why this exists

AI adoption is not a one-time "change program." It's a permanent capability shift — organizations must learn, prototype, and govern in a world where the tools and risks shift quarterly.

Traditional change management was built for projects. It implicitly assumes a clear end state, a defined timeline, a stable technology, and a workforce that just needs to be "brought along." None of those assumptions hold for AI.

**Adaptive Adoption reframes change management for the AI era:**

| Old model | Adaptive Adoption |
|-----------|-------------------|
| Plans | Practice |
| Communication | Behavior |
| Compliance | Frontline judgment |
| Static frameworks | Living systems |
| Project completion | Capability regime |

The evidence for why this matters is stark: 72% of organizations score high on organizational AI maturity. Only 6% score high on operational maturity. Every existing framework is measuring the 72% and calling it success. This one measures the 6%.

---

## The Seven Pillars

### 1. Master the Craft
Capability is built through practice, not curriculum. L&D's model — predict skills, design curriculum, deliver training — fails when the skill landscape shifts quarterly. Craft is built through doing, sharing, failing loudly, and iterating. The unit of learning is the community of practice, not the training course.

### 2. Embrace Complexity
AI adoption is emergence, not rollout. Design for nonlinear systems: probe-sense-respond rather than plan-execute-review. The organizations that scale are the ones that stopped trying to predict the destination and started building the capacity to navigate whatever comes next.

### 3. Consciously Manage Trust
Trust is the change resistance anti-venom — and it can fail in both directions. **Overtrust** (blind acceptance of AI outputs, automation bias) and **undertrust** (blanket refusal, performative skepticism) are both failure modes. No other change framework treats both as risks requiring different interventions. This one does.

### 4. Put People First™
Augment before automate. This is both an ethical stance and a strategic sequence: start with AI as a bicycle for the mind, build trust and craft capability, then pursue efficiency. *"You get to the efficiency gains faster by not starting with them."*

### 5. Design and Prototype
We don't plan our way to the future; we prototype our way there. Sprints and experimentation replace fixed future states. The change initiative itself is designed with the same build-measure-learn logic as the AI products it deploys.

### 6. Prioritize Behavior
Awareness, desire, and knowledge do not add up to action. This is the direct, evidence-based dismantling of ADKAR's core logic using the intention-action gap from behavioral science. Change the environment and the behaviors; the mindsets catch up. Not the other way around.

### 7. Manage Ethics Always
Ethics isn't a brake — it's the steering that allows speed. Compliance frameworks didn't stop VW, Enron, Wells Fargo, or Boeing. Every catastrophic ethics failure happened inside organizations with ethics codes and governance dashboards. Ethics must be a practiced frontline capability: ethical reasoning as a skill, psychological safety as ethics infrastructure, ethics embedded in every sprint.

---

## The Adaptive Adoption Maturity Index (AAMI)

The AAMI is the first AI adoption maturity model grounded in behavioral science rather than technical or process capability.

Every existing model — MITRE, IBM, Gartner, Prosci, AWS, CMMI — measures **espoused capability**: "has the organization established processes for X?" None measure **enacted behavior**: "does anyone actually do X?"

The AAMI asks: **"How ready are your humans for AI?"** — measured by what people demonstrably do, not what policies say exist.

**Five levels. Seven pillars. Three assessment layers** (self-report, evidence, behavioral indicators). The primary output is not a score — it's a Gap Score: the distance between what the organization claims and what an observer would see.

→ See [`diagnostics/AA_MI/`](diagnostics/AA_MI/) for the full specification.

---

## Repo Structure

```
adaptive-adoption/
├── README.md                        # This file
├── LICENSE
├── CONTRIBUTING.md
├── docs/
│   ├── pillars/                     # The seven pillars (narrative + operational)
│   │   ├── 00-toolkit-7x5.md        # Master reference: all 7 pillars × 5 categories
│   │   ├── 01-master-the-craft.md
│   │   ├── 02-embrace-complexity.md
│   │   ├── 03-consciously-manage-trust.md
│   │   ├── 04-put-people-first.md
│   │   ├── 05-design-and-prototype.md
│   │   ├── 06-prioritize-behavior.md
│   │   └── 07-manage-ethics-always.md
│   └── theory/                      # Intellectual foundations
│       ├── intellectual-lineage.md  # Canonical texts + where AA departs
│       ├── two-tier-framework.md    # Board governance model (5 dials + 7×5)
│       └── session-2026-02-19-founding.md
├── diagnostics/
│   └── AA_MI/                       # Adaptive Adoption Maturity Index
│       ├── AA_MI_structure.md       # Canonical structure (levels, pillars, scoring)
│       ├── AA_MI_trust03_calibration.md  # Pillar 3 proof-of-concept
│       └── research/
│           └── notebooklm_enacted_gap_evidence.md
├── tools/                           # Operational playbooks and templates
├── industry-modules/                # Forkable industry extensions
└── agent/                           # Maintenance automation
```

---

## How to Use This Repo

**If you're an executive** looking to understand where your organization is: start with [`diagnostics/AA_MI/AA_MI_structure.md`](diagnostics/AA_MI/AA_MI_structure.md).

**If you're a practitioner** implementing AI adoption: start with [`docs/pillars/00-toolkit-7x5.md`](docs/pillars/00-toolkit-7x5.md) — it gives you the full operational system in one view.

**If you're a researcher or skeptic**: start with [`docs/theory/intellectual-lineage.md`](docs/theory/intellectual-lineage.md) — it maps every claim to its academic foundation and states explicitly where Adaptive Adoption departs from the literature.

**If you want to fork for your industry**: see [`industry-modules/`](industry-modules/) for existing extensions and contribution guidelines.

---

## Why Open Source

Proprietary change frameworks need change management to be static — their revenue depends on controlling it. Prosci charges $4,500/seat for certifications that update every few years. That model cannot survive a world where the technology shifts quarterly.

Adaptive Adoption is the opposite: open, evolving, forkable. The framework is free. Implementation is where the value is created — in the hands of practitioners who know their industry, their organization, and their people.

The meta-positioning is intentional: **a framework for AI adoption that uses AI to maintain itself** is a live demonstration of what it teaches.

---

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for guidelines.

Industry module contributions are especially welcome. If you're adapting Adaptive Adoption for healthcare, financial services, government, or manufacturing — fork it, build it, and contribute back.

---

## Author

**Paul Gibbons** — strategist, author, and keynote speaker on AI adoption, organizational change, and leadership.

- [paulgibbonsadvisory.com](https://paulgibbonsadvisory.com)
- Substack: [Think Bigger Think Better](https://paulgibbons.substack.com)
- Author of *Adopting AI* and seven other books on organizational change

---

> *"This is not a new change management framework. This is the end of change management as a static, proprietary discipline — and the beginning of something that evolves as fast as the technology it's designed to adopt."*
