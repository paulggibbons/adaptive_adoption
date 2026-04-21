# Tools

This directory contains the **operational toolkits** of Adaptive Adoption — the “what to do Monday morning” layer.

If `docs/` is the narrative method, `tools/` is the **craft**: templates, rituals, checklists, and playbooks that practitioners can run without a consultant in the room.

---

## How to use tools

Each tool should be runnable in **30–90 minutes** and produce a concrete artifact (a template filled out, a decision recorded, a score produced, a ritual completed).

**Tool format (standard):**
1. **Problem it solves**
2. **When to use / when not to use**
3. **Inputs** (what you need)
4. **Steps** (time-boxed)
5. **Outputs / artifacts**
6. **Failure modes**
7. **Evidence / references** (optional but preferred)
8. **Links** (to pillars + diagnostics)

---

## Tool index (initial)

### Master the Craft (Pillar 1)
- **Prompt Recipe Card** (capture “wins” and reuse)
- **Glitch Log / Hallucination Hunter** (make failure teachable)
- **Weekly Show-and-Tell** (ritual for peer learning)
- **Micro-learning Clips** (1–3 minute “how I did it” patterns)

### Embrace Complexity (Pillar 2)
- **Complexity Triage** (simple vs complex vs chaotic)
- **Safe-to-Fail Experiment Canvas**
- **Constraint Mapping** (where the system pushes back)

### Consciously Manage Trust (Pillar 3)
- **Trust Spectrum Check** (undertrust ↔ calibrated ↔ overtrust)
- **“Show Your Work” Template** (sources, assumptions, confidence)
- **Escalation Rules** (when humans must review)

### Put People First™ (Pillar 4)
- **Augment-before-Automate Sequencing Tool**
- **Role Impact Map** (where value is created vs displaced)
- **Work Redesign Conversation Guide** (manager + team)

### Design and Prototype (Pillar 5)
- **Sprint Template** (Build → Measure → Learn)
- **Experiment Designer** (hypothesis, measures, guardrails)
- **Value Capture Tracker** (time saved, quality improved, risk reduced)

### Prioritize Behavior (Pillar 6)
- **Habit Loop Installer** (cue → routine → reward)
- **Friction Audit** (what blocks practice in the workflow)
- **Behavior Scorecard** (actions, not attitudes)

### Manage Ethics Always (Pillar 7)
- **Ethical Pre-Mortem** (structured harm + misuse review)
- **Stakeholder Harm Map**
- **Red-Team Prompt Pack** (misuse discovery)

---

## AI Mastery Diagnostic (v0.5 for comment)

AI Mastery Diagnostic — a 12-question CLI self-assessment that places users on a 4-level AI mastery scale (User → Practitioner → Builder → Architect) across three dimensions (Know, Do, Build). Run with `python ai_mastery_diagnostic.py`. Generates an HTML report. Part of the Adaptive Adoption™ Framework.

---

## Where tools live

Tools should sit in dedicated subfolders, e.g.:

```text
tools/
├── README.md
├── prompt-recipe-card/
│   ├── README.md
│   └── template.md
├── glitch-log/
│   ├── README.md
│   └── template.md
└── ethical-pre-mortem/
    ├── README.md
    └── template.md
