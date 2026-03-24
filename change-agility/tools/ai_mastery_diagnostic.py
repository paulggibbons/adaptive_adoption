#!/usr/bin/env python3
"""
AI Mastery Diagnostic Tool
(c) Paul Gibbons Advisory — Adaptive Adoption Framework

A 12-question self-assessment that measures AI mastery across four levels:
  Level 1: User         — Basic prompting, ad hoc use
  Level 2: Practitioner — Structured workflows, custom agents
  Level 3: Builder      — Agent literacy, code tools, shipped apps
  Level 4: Architect    — Human-AI systems design, governance

Each level is assessed on three dimensions:
  - Know (conceptual understanding)
  - Do (frequency of practice)
  - Build (what you've actually made)

Output: An HTML report with level breakdown bars and summary banner.

v0.5 for comment
"""

import os
import datetime
import webbrowser

# ─────────────────────────────────────────────
# QUESTIONS: 4 levels × 3 dimensions = 12 questions
# Each question has a prompt and scoring options (0-4)
# ─────────────────────────────────────────────

QUESTIONS = [
    # ── Level 1: User ──
    {
        "level": "User",
        "dimension": "Know",
        "question": "Can you explain the difference between a prompt and a conversation with AI? (e.g., context window, system instructions, temperature)",
        "options": [
            (0, "No idea what those terms mean"),
            (1, "I've heard of them but couldn't explain them"),
            (2, "I could give a rough explanation"),
            (3, "I understand them well and could teach someone"),
            (4, "I understand these deeply and know when each matters"),
        ],
    },
    {
        "level": "User",
        "dimension": "Do",
        "question": "How often do you use AI for ad hoc tasks — drafting, summarizing, research, brainstorming?",
        "options": [
            (0, "Never or almost never"),
            (1, "A few times a month"),
            (2, "A few times a week"),
            (3, "Daily"),
            (4, "Multiple times per day — it's my default first move"),
        ],
    },
    {
        "level": "User",
        "dimension": "Build",
        "question": "Have you saved and reused a prompt template or created a structured prompt with specific formatting instructions?",
        "options": [
            (0, "No — I type fresh each time"),
            (1, "I've copy-pasted a good prompt before"),
            (2, "I have a few saved prompts I return to"),
            (3, "I have a personal library of structured prompts"),
            (4, "I maintain and iterate on prompt templates regularly"),
        ],
    },

    # ── Level 2: Practitioner ──
    {
        "level": "Practitioner",
        "dimension": "Know",
        "question": "Can you explain what a Custom GPT, Gem, or Claude Project is, and when you'd use one over a raw conversation?",
        "options": [
            (0, "I don't know what those are"),
            (1, "I've heard of them but haven't explored"),
            (2, "I've tried one but couldn't explain the differences"),
            (3, "I understand the distinctions and have preferences"),
            (4, "I know exactly when each is the right tool and why"),
        ],
    },
    {
        "level": "Practitioner",
        "dimension": "Do",
        "question": "How often do you use AI for structured workflow tasks — meeting prep, stakeholder analysis, communication plans, document synthesis?",
        "options": [
            (0, "Never"),
            (1, "Occasionally, when someone shows me how"),
            (2, "Regularly for one or two workflow types"),
            (3, "It's embedded in most of my recurring workflows"),
            (4, "I can't imagine doing these tasks without AI"),
        ],
    },
    {
        "level": "Practitioner",
        "dimension": "Build",
        "question": "Have you created a custom agent (Custom GPT, Claude Project, Cowork skill) loaded with your own context or methodology?",
        "options": [
            (0, "No"),
            (1, "I've thought about it but haven't tried"),
            (2, "I've created one basic custom agent"),
            (3, "I've built several, each with specific instructions and context"),
            (4, "I build and iterate on custom agents as a core part of my work"),
        ],
    },

    # ── Level 3: Builder ──
    {
        "level": "Builder",
        "dimension": "Know",
        "question": "Can you describe at least 3 types of AI agents (e.g., reflex, goal-based, learning, conversational, retrieval, autonomous)?",
        "options": [
            (0, "I don't know what an AI agent is"),
            (1, "I know the term but couldn't name types"),
            (2, "I could name 1-2 types with rough descriptions"),
            (3, "I can describe 3-4 types and give examples"),
            (4, "I understand agent taxonomies and their design trade-offs"),
        ],
    },
    {
        "level": "Builder",
        "dimension": "Do",
        "question": "How often do you use code-capable AI tools (Claude Code, Copilot, Code Interpreter) to automate tasks or build prototypes?",
        "options": [
            (0, "Never — I don't use code tools"),
            (1, "I've tried once or twice"),
            (2, "Occasionally, for specific tasks"),
            (3, "Regularly — it's part of how I build things"),
            (4, "Daily — I ship working code with AI assistance"),
        ],
    },
    {
        "level": "Builder",
        "dimension": "Build",
        "question": "Have you built a working application, automated workflow, or multi-step pipeline using AI? (e.g., 'read email → draft response → schedule follow-up')",
        "options": [
            (0, "No"),
            (1, "I've thought about it or seen demos"),
            (2, "I've built one simple automation"),
            (3, "I've built several working pipelines or applications"),
            (4, "I've shipped applications that other people use"),
        ],
    },

    # ── Level 4: Architect ──
    {
        "level": "Architect",
        "dimension": "Know",
        "question": "Can you explain what 'human-in-the-loop' means and describe when autonomous AI should and shouldn't operate without oversight?",
        "options": [
            (0, "Not familiar with the concept"),
            (1, "I've heard the phrase but couldn't explain it"),
            (2, "I understand the basic idea"),
            (3, "I can articulate specific criteria for when autonomy is appropriate"),
            (4, "I can design governance frameworks that balance autonomy with oversight"),
        ],
    },
    {
        "level": "Architect",
        "dimension": "Do",
        "question": "How often do you design or govern AI workflows for a team or organization — not just your own productivity?",
        "options": [
            (0, "Never — I only use AI for myself"),
            (1, "I've advised others informally"),
            (2, "I've helped design team-level AI workflows"),
            (3, "I regularly design AI adoption strategies for groups"),
            (4, "I lead organizational AI governance and adoption programs"),
        ],
    },
    {
        "level": "Architect",
        "dimension": "Build",
        "question": "Have you designed a multi-agent system, governance framework, or organizational AI adoption strategy?",
        "options": [
            (0, "No"),
            (1, "I've thought about what one might look like"),
            (2, "I've drafted a basic framework or strategy"),
            (3, "I've built and implemented one in a real organization"),
            (4, "I've designed enterprise-scale AI governance systems"),
        ],
    },
]

LEVELS = ["User", "Practitioner", "Builder", "Architect"]
DIMENSIONS = ["Know", "Do", "Build"]

LEVEL_DESCRIPTIONS = {
    "User": {
        "title": "Level 1: The User",
        "subtitle": "Basic Prompting & Ad Hoc Use",
        "description": "You're using AI as a smarter search engine or junior intern. The opportunity ahead: build muscle memory so AI becomes your default first move, not an occasional experiment.",
    },
    "Practitioner": {
        "title": "Level 2: The Practitioner",
        "subtitle": "Structured Workflows & Custom Agents",
        "description": "You've moved from 'asking' to 'architecting' at the prompt level. AI is embedded in your daily workflows. The next frontier: understanding agent typology and building reusable tools.",
    },
    "Builder": {
        "title": "Level 3: The Builder",
        "subtitle": "Agent Literacy & Shipped Applications",
        "description": "You understand how different types of agents work and you've built things that run. You're not just using AI — you're engineering with it. Next: designing systems for teams, not just yourself.",
    },
    "Architect": {
        "title": "Level 4: The Architect",
        "subtitle": "Human-AI Systems Design & Governance",
        "description": "You design how humans and AI systems work together at organizational scale. You think about governance, autonomy boundaries, cultural readiness, and emergent behavior in multi-agent systems.",
    },
}


def run_assessment():
    """Run the interactive CLI assessment."""
    print("\n" + "=" * 64)
    print("  AI MASTERY DIAGNOSTIC")
    print("  Adaptive Adoption Framework — Paul Gibbons Advisory")
    print("=" * 64)
    print("\n  12 questions. ~5 minutes. Brutally honest answers only.\n")

    # Collect optional name
    name = input("  Your name (optional, press Enter to skip): ").strip()
    if not name:
        name = "Anonymous"

    scores = {}  # {level: {dimension: score}}
    for level in LEVELS:
        scores[level] = {}

    for i, q in enumerate(QUESTIONS, 1):
        print(f"\n{'─' * 64}")
        print(f"  Question {i}/12 — {q['level']} / {q['dimension']}")
        print(f"{'─' * 64}")
        print(f"\n  {q['question']}\n")

        for score, label in q["options"]:
            print(f"    [{score}] {label}")

        while True:
            try:
                answer = int(input(f"\n  Your answer (0-4): ").strip())
                if 0 <= answer <= 4:
                    break
                print("  Please enter a number between 0 and 4.")
            except ValueError:
                print("  Please enter a number between 0 and 4.")

        scores[q["level"]][q["dimension"]] = answer

    return name, scores


def calculate_results(scores):
    """Calculate level scores, overall level, and dimension profiles."""
    # Level scores (sum of 3 dimensions, max 12 per level)
    level_scores = {}
    for level in LEVELS:
        level_scores[level] = sum(scores[level].values())

    # Dimension scores across all levels (max 16 per dimension)
    dimension_scores = {}
    for dim in DIMENSIONS:
        dimension_scores[dim] = sum(scores[level][dim] for level in LEVELS)

    # Overall level determination
    # You "own" a level if you score >= 8/12 (67%)
    # Your level is the highest level you own
    overall_level = "User"  # default
    for level in LEVELS:
        if level_scores[level] >= 8:
            overall_level = level

    # Total score
    total = sum(level_scores.values())
    max_total = len(QUESTIONS) * 4  # 48

    return {
        "level_scores": level_scores,
        "dimension_scores": dimension_scores,
        "overall_level": overall_level,
        "total": total,
        "max_total": max_total,
        "percentage": round((total / max_total) * 100),
    }


def generate_html_report(name, scores, results):
    """Generate a polished HTML report with level breakdown bars and summary banner."""

    overall = LEVEL_DESCRIPTIONS[results["overall_level"]]
    timestamp = datetime.datetime.now().strftime("%B %d, %Y")

    # Color mapping for levels
    level_colors = {
        "User": "#4A90D9",
        "Practitioner": "#50B86C",
        "Builder": "#E8913A",
        "Architect": "#D94A6E",
    }

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Mastery Diagnostic — {name}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

  :root {{
    --bg: #0a0e17;
    --surface: #131825;
    --surface-2: #1a2030;
    --border: #2a3040;
    --text: #e2e8f0;
    --text-muted: #8892a4;
    --accent-user: #4A90D9;
    --accent-practitioner: #50B86C;
    --accent-builder: #E8913A;
    --accent-architect: #D94A6E;
    --accent-know: #7C6FE0;
    --accent-do: #4ABFD9;
    --accent-build: #D9A04A;
  }}

  * {{ margin: 0; padding: 0; box-sizing: border-box; }}

  body {{
    font-family: 'IBM Plex Sans', sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
    padding: 40px 20px;
  }}

  .container {{
    max-width: 900px;
    margin: 0 auto;
  }}

  .header {{
    text-align: center;
    padding: 48px 0 40px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 40px;
  }}

  .header h1 {{
    font-size: 2rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-bottom: 8px;
  }}

  .header .subtitle {{
    font-size: 0.95rem;
    color: var(--text-muted);
    font-weight: 300;
  }}

  .header .date {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.8rem;
    color: var(--text-muted);
    margin-top: 16px;
  }}

  .result-banner {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 40px;
    margin-bottom: 32px;
    text-align: center;
  }}

  .result-banner .level-label {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-muted);
    margin-bottom: 8px;
  }}

  .result-banner .level-title {{
    font-size: 1.8rem;
    font-weight: 700;
    color: {level_colors[results['overall_level']]};
    margin-bottom: 4px;
  }}

  .result-banner .level-subtitle {{
    font-size: 1rem;
    color: var(--text-muted);
    margin-bottom: 20px;
  }}

  .result-banner .level-description {{
    font-size: 0.95rem;
    line-height: 1.7;
    max-width: 640px;
    margin: 0 auto;
    color: var(--text);
  }}

  .score-strip {{
    display: flex;
    justify-content: center;
    gap: 32px;
    margin-top: 24px;
    padding-top: 24px;
    border-top: 1px solid var(--border);
  }}

  .score-strip .score-item {{
    text-align: center;
  }}

  .score-strip .score-value {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.5rem;
    font-weight: 600;
  }}

  .score-strip .score-label {{
    font-size: 0.75rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }}

  .level-breakdown {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 28px;
    margin-bottom: 32px;
  }}

  .level-breakdown h3 {{
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--text-muted);
    margin-bottom: 20px;
  }}

  .level-row {{
    display: flex;
    align-items: center;
    padding: 16px 0;
    border-bottom: 1px solid var(--border);
  }}

  .level-row:last-child {{
    border-bottom: none;
  }}

  .level-row .level-name {{
    width: 140px;
    font-weight: 600;
    font-size: 0.9rem;
  }}

  .level-row .bar-container {{
    flex: 1;
    height: 28px;
    background: var(--surface-2);
    border-radius: 6px;
    overflow: hidden;
    margin: 0 16px;
  }}

  .level-row .bar-fill {{
    height: 100%;
    border-radius: 6px;
    transition: width 0.6s ease;
    display: flex;
    align-items: center;
    padding-left: 12px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    font-weight: 500;
    color: rgba(255,255,255,0.9);
  }}

  .level-row .bar-score {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.85rem;
    color: var(--text-muted);
    width: 50px;
    text-align: right;
  }}

  .footer {{
    text-align: center;
    padding: 32px 0;
    border-top: 1px solid var(--border);
    margin-top: 16px;
  }}

  .footer p {{
    font-size: 0.8rem;
    color: var(--text-muted);
  }}

  .footer a {{
    color: var(--accent-user);
    text-decoration: none;
  }}

  @media (max-width: 768px) {{
    .score-strip {{
      gap: 20px;
    }}
  }}
</style>
</head>
<body>
<div class="container">

  <div class="header">
    <h1>AI Mastery Diagnostic</h1>
    <div class="subtitle">Adaptive Adoption Framework — Paul Gibbons Advisory</div>
    <div class="date">{name} · {timestamp}</div>
  </div>

  <div class="result-banner">
    <div class="level-label">Your Current Level</div>
    <div class="level-title">{overall['title']}</div>
    <div class="level-subtitle">{overall['subtitle']}</div>
    <div class="level-description">{overall['description']}</div>
    <div class="score-strip">
      <div class="score-item">
        <div class="score-value">{results['total']}</div>
        <div class="score-label">Total Score</div>
      </div>
      <div class="score-item">
        <div class="score-value">{results['percentage']}%</div>
        <div class="score-label">Overall</div>
      </div>
      <div class="score-item">
        <div class="score-value">{results['dimension_scores']['Know']}</div>
        <div class="score-label">Know (of 16)</div>
      </div>
      <div class="score-item">
        <div class="score-value">{results['dimension_scores']['Do']}</div>
        <div class="score-label">Do (of 16)</div>
      </div>
      <div class="score-item">
        <div class="score-value">{results['dimension_scores']['Build']}</div>
        <div class="score-label">Build (of 16)</div>
      </div>
    </div>
  </div>

  <div class="level-breakdown">
    <h3>Level Breakdown</h3>
    <div class="level-row">
      <div class="level-name" style="color: var(--accent-user);">User</div>
      <div class="bar-container">
        <div class="bar-fill" style="width: {results['level_scores']['User']/12*100}%; background: var(--accent-user);">
          {results['level_scores']['User']}/12
        </div>
      </div>
      <div class="bar-score">{'✓ Owned' if results['level_scores']['User'] >= 8 else '—'}</div>
    </div>
    <div class="level-row">
      <div class="level-name" style="color: var(--accent-practitioner);">Practitioner</div>
      <div class="bar-container">
        <div class="bar-fill" style="width: {results['level_scores']['Practitioner']/12*100}%; background: var(--accent-practitioner);">
          {results['level_scores']['Practitioner']}/12
        </div>
      </div>
      <div class="bar-score">{'✓ Owned' if results['level_scores']['Practitioner'] >= 8 else '—'}</div>
    </div>
    <div class="level-row">
      <div class="level-name" style="color: var(--accent-builder);">Builder</div>
      <div class="bar-container">
        <div class="bar-fill" style="width: {results['level_scores']['Builder']/12*100}%; background: var(--accent-builder);">
          {results['level_scores']['Builder']}/12
        </div>
      </div>
      <div class="bar-score">{'✓ Owned' if results['level_scores']['Builder'] >= 8 else '—'}</div>
    </div>
    <div class="level-row">
      <div class="level-name" style="color: var(--accent-architect);">Architect</div>
      <div class="bar-container">
        <div class="bar-fill" style="width: {results['level_scores']['Architect']/12*100}%; background: var(--accent-architect);">
          {results['level_scores']['Architect']}/12
        </div>
      </div>
      <div class="bar-score">{'✓ Owned' if results['level_scores']['Architect'] >= 8 else '—'}</div>
    </div>
  </div>

  <div class="footer">
    <p>AI Mastery Diagnostic v0.5 · Adaptive Adoption™ Framework</p>
    <p>(c) Paul Gibbons Advisory · <a href="https://github.com/paulggibbons/adaptive_adoption">github.com/paulggibbons/adaptive_adoption</a></p>
  </div>

</div>

</body>
</html>"""

    return html


def main():
    """Main entry point."""
    name, scores = run_assessment()
    results = calculate_results(scores)
    html = generate_html_report(name, scores, results)

    # Write the report
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, f"ai_mastery_report_{name.lower().replace(' ', '_')}.html")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n{'=' * 64}")
    print(f"  RESULTS: {LEVEL_DESCRIPTIONS[results['overall_level']]['title']}")
    print(f"  Score: {results['total']}/{results['max_total']} ({results['percentage']}%)")
    print(f"{'=' * 64}")
    print(f"\n  Report saved to: {output_path}")

    # Try to open in browser
    try:
        webbrowser.open(f"file://{output_path}")
        print("  Opening in browser...")
    except Exception:
        print("  Open the HTML file in your browser to see the full report.")

    print()


if __name__ == "__main__":
    main()
