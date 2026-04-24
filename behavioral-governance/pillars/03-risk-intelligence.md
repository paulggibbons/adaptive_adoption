!!! warning "v0.8 — Working Draft"
    This page is under active development. Content is directionally accurate but subject to revision.
    [Suggest an edit →](https://github.com/paulggibbons/adaptive_adoption/issues)

# Risk Intelligence

**Focus:** Dynamic risk sensing, not static risk registers.

## The Argument

Enterprise risk management for AI typically begins and ends with a risk register — a static document listing identified risks, likelihood ratings, impact scores, and named owners. This is necessary but deeply insufficient. Risk registers capture known risks at a point in time. AI risk is characterized by emergence, interaction effects, and rapid evolution. A risk register for AI is like a weather forecast carved in stone: accurate briefly, misleading thereafter.

Risk Intelligence, as a Behavioral Governance dimension, demands a shift from risk documentation to risk sensing — the organizational capacity to detect, interpret, and respond to risk signals in something closer to real time. This draws on Taleb's distinction between fragile and antifragile systems (Taleb, 2012) and on high-reliability organization (HRO) theory, which emphasizes "preoccupation with failure" as an operational discipline, not merely a risk management aspiration (Weick & Sutcliffe, 2015).

The specific characteristics of AI risk that demand dynamic sensing include: model drift (performance degradation that emerges gradually), adversarial exposure (attack surfaces that shift as models are deployed to new contexts), regulatory flux (compliance requirements that change faster than annual review cycles can accommodate), and cascade risk (failures in one AI system propagating through interconnected processes).

Risk Intelligence requires three capabilities. First, leading indicators: metrics that signal emerging risk before it materializes (e.g., rising override rates, expanding confidence intervals, unusual input distributions). Second, sense-making routines: regular, structured forums where risk signals are interpreted by people with both technical and domain expertise. Third, response readiness: pre-defined playbooks for risk scenarios that have been tested, not merely written.

The behavioral assessment asks whether the organization actually practices dynamic risk sensing or merely claims to. Many organizations have sophisticated risk frameworks that are, in practice, annual compliance exercises disconnected from operational reality.

## Three-Layer Assessment

| Layer | Method | Example |
|---|---|---|
| **Self-Report** | Survey / interview | "We continuously monitor AI risk using real-time dashboards." |
| **Evidence** | Artifact and data review | Risk signal logs showing detection events, timestamps, escalation actions, and resolution records from the past 90 days — demonstrating active monitoring, not dormant dashboards. |
| **Behavioral Observation** | Observed practice | Inject a simulated anomaly (e.g., a sudden shift in model input distribution) and observe whether the risk sensing process detects, escalates, and responds within the organization's stated SLA. |

## Key Questions

1. Beyond your risk register, what leading indicators do you actively monitor for AI-specific risk?
2. When was the last time a risk signal led to a material change in an AI system's deployment or configuration?
3. How frequently do technical and business stakeholders jointly review AI risk signals — and can you show evidence of the last session?
4. Have your risk response playbooks been tested under simulated conditions in the past twelve months?

---

← [Back to Behavioral Governance Overview](../)
