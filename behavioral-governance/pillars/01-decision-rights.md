!!! warning "v0.8 — Working Draft"
    This page is under active development. Content is directionally accurate but subject to revision.
    [Suggest an edit →](https://github.com/paulggibbons/adaptive_adoption/issues)

# Decision Rights

**Focus:** Who decides what, with what authority, under what constraints.

## The Argument

Most organizations claim to have clear decision rights for AI. Few actually do. The gap between documented authority and enacted authority — who *really* decides whether to deploy a model, escalate a risk, or override an AI recommendation — is where governance fails silently.

Decision rights in AI contexts are categorically harder than in traditional IT governance for three reasons. First, the decision surface is vast: AI systems generate recommendations across functions, and each recommendation implies a human decision about whether to accept, modify, or reject it. Second, the pace of model iteration compresses decision timelines beyond what committee-based governance can handle. Third, the expertise asymmetry between technical teams and business decision-makers creates de facto authority that rarely matches de jure authority — the people who understand the model often make the real decisions, regardless of what the RACI chart says.

Behavioral Governance demands that decision rights be observable, not merely documented. A decision-rights framework that exists only in a policy document is not governance; it is aspiration. The relevant question is not "Does your organization have a decision-rights matrix?" but "Can you show me, in the last three decisions about AI deployment, who decided, on what basis, and with what oversight?"

This dimension draws on organizational design literature (Galbraith, 2014), the concept of "decision architecture" from behavioral economics (Thaler & Sunstein, 2008), and the practical failures catalogued in enterprise AI post-mortems where ambiguous authority led to either reckless deployment or paralytic caution.

Decision rights must address at minimum: model deployment authorization, override authority (when humans override AI and vice versa), escalation triggers, and sunset decisions (who decides to decommission an AI system that is underperforming or creating risk).

## Three-Layer Assessment

| Layer | Method | Example |
|---|---|---|
| **Self-Report** | Survey / interview | "We have a clear RACI for AI deployment decisions." |
| **Evidence** | Document and artifact review | Decision logs showing named decision-makers, approval timestamps, and documented rationale for the last five AI deployment decisions. |
| **Behavioral Observation** | Observed practice | In a live deployment review, observe whether the designated decision-maker actually makes the call, or whether a senior technical lead overrides the process without formal authority. |

## Key Questions

1. For your last three AI deployment decisions, can you name the decision-maker, the alternatives considered, and the constraints applied?
2. When a model recommendation conflicts with human judgment, who has final authority — and is that authority exercised consistently?
3. Are decision rights revisited as AI systems mature, or do they remain static from initial deployment?
4. How do you handle decision rights for AI agents that operate autonomously between human review cycles?

---

← [Back to Behavioral Governance Overview](../)
