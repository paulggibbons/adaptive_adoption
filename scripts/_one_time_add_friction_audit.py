from pathlib import Path

MANIFEST = Path("data/tools.yml")
SLUG_MARKER = "\n  slug: ai-adoption-friction-audit\n"

ENTRY = r'''- supabase_id: null
  slug: ai-adoption-friction-audit
  name: AI Adoption Friction Audit
  aliases:
  - Adaptive Adoption Friction Audit
  type: diagnostic
  status: in-development
  version: '0.1'
  short_description: Diagnose why one specific AI initiative is stuck and identify the friction that matters most.
  long_description: |-
    A structured diagnostic for one named AI initiative, deployment, or human–AI workflow. Assess eight domains of adoption friction, separate severity from evidence confidence, identify the three highest-priority constraints, and generate focused next steps. This is a decision-support framework, not a validated psychometric instrument or a company-wide AI maturity score.
  framework_mapping:
    domain: cross-cutting
    pillar: null
    pillar_num: 0
    pillar_name: AI Adoption Friction Suite
  astro_url: null
  hero_copy: Diagnose what is blocking one AI initiative from producing real organisational value.
  hero_image: /images/aa-triptych.png
  hero_image_alt: Adaptive Adoption framework spanning Change Agility, Leadership Delta, and Behavioral Governance
  attribution:
  - Original framework © Paul Gibbons · Adaptive Adoption™
  - Epistemic Level 1 conceptual tool · Behavioral evidence Layer 1 self-report · v0.1
  supabase:
    table: diagnostic_responses
    notes: Response capture disabled in the initial website release pending a versioned response schema and slug migration.
  source: Original — Gibbons 2026
  epistemic:
    level: 1
    label: Original conceptual tool · Not psychometrically validated · v0.1
  card_display:
    pillar_label: AI ADOPTION FRICTION SUITE
    time: 12–15 min
    is_greyed: true
    greyed_pillar_label: AI ADOPTION FRICTION SUITE
    greyed_time: In development
  related_tools:
  - slug: adoption-friction-mapper
    relationship: successor
    label: AI Adoption Friction Mapper
  dates:
    created: '2026-07-11'
    last_updated: '2026-07-11'
    built: null
    archived: null
  archived_reason: null
  aspirational_notes: First tool in the AI Adoption Friction Suite; Mapper and 90-Day Intervention Planner follow.
  sort_order: 2
  tags:
  - cross-cutting
  - in-development
  - diagnostic
  - ai-adoption
  - friction-suite
'''


def main() -> None:
    text = MANIFEST.read_text(encoding="utf-8")
    if SLUG_MARKER in text:
        print("ai-adoption-friction-audit already exists; no change")
        return
    MANIFEST.write_text(text.rstrip() + "\n" + ENTRY, encoding="utf-8")
    print("appended ai-adoption-friction-audit to data/tools.yml")


if __name__ == "__main__":
    main()
