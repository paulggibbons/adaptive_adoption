!!! warning "v0.8 — Working Draft"
    This page is under active development. Content is directionally accurate but subject to revision.
    [Suggest an edit →](https://github.com/paulggibbons/adaptive_adoption/issues)

# Agent Authority

**Focus:** How autonomous AI agents are authorized, bounded, and supervised.

## The Argument

The emergence of agentic AI — systems that plan, execute multi-step tasks, use tools, and operate with degrees of autonomy — creates a governance challenge that has no precedent in enterprise technology. Agent authority is not a variant of decision rights; it is a distinct dimension because agents act without real-time human oversight, making the *pre-authorization* framework the primary governance mechanism.

Traditional software authorization follows a permission model: a system is granted access to data and functions, and humans initiate actions. Agentic systems invert this. The agent initiates actions within a bounded mandate, and governance must define the boundaries *before* the agent acts. This is closer to how organizations govern delegated authority in human hierarchies — a regional manager has spending authority up to a threshold, escalation rules for exceptions, and audit requirements — than to how they govern software.

The critical governance failures in agent authority are predictable. Scope creep: agents authorized for narrow tasks gradually operating across wider domains without re-authorization. Supervision gaps: no defined cadence or method for reviewing agent actions after the fact. Composition risk: multiple agents, each individually authorized, interacting in ways that no single authorization anticipated (Shavit et al., 2023).

Behavioral Governance requires that agent authority be specified in terms of action boundaries (what the agent may do), resource boundaries (what data and tools it may access), escalation triggers (conditions under which the agent must pause and seek human input), and audit trails (machine-readable logs of every action taken). The assessment is whether these boundaries exist on paper, whether they are technically enforced, and whether they hold under observation.

This dimension will grow in importance as multi-agent architectures become standard. Organizations that defer agent authority governance until after deployment are building technical debt that compounds with each agent added.

## Three-Layer Assessment

| Layer | Method | Example |
|---|---|---|
| **Self-Report** | Survey / interview | "All AI agents operate within defined guardrails reviewed quarterly." |
| **Evidence** | Technical artifact review | Agent configuration files showing explicit action boundaries, escalation triggers, and resource access scopes — plus change logs showing when boundaries were last updated. |
| **Behavioral Observation** | Observed practice | Trigger an edge case (e.g., an agent encountering ambiguous input near its authority boundary) and observe whether the agent escalates as specified or proceeds without escalation. |

## Key Questions

1. Can you enumerate every AI agent operating in your environment, its authorized scope, and the date its authority was last reviewed?
2. What happens when an agent encounters a situation outside its defined boundaries — is the fail-safe mode documented and tested?
3. How do you govern the interactions between multiple agents, particularly when their combined actions exceed any single agent's authorization?
4. Who is accountable when an agent causes harm within its authorized scope?

---

← [Back to Behavioral Governance Overview](../)
