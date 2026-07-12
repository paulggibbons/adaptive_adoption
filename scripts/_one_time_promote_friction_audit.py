from pathlib import Path

PATH = Path("data/tools.yml")
SLUG = "  slug: ai-adoption-friction-audit\n"


def replace_once(block: str, old: str, new: str) -> str:
    if new in block:
        return block
    if old not in block:
        raise RuntimeError(f"Expected text not found: {old!r}")
    return block.replace(old, new, 1)


def main() -> None:
    text = PATH.read_text(encoding="utf-8")
    start = text.index("- supabase_id: null\n" + SLUG)
    block = text[start:]

    block = replace_once(block, "  status: in-development\n", "  status: live\n")
    block = replace_once(
        block,
        "  astro_url: null\n",
        "  astro_url: /diagnostics/ai-adoption-friction-audit\n",
    )
    block = replace_once(
        block,
        "  hero_image_alt: Adaptive Adoption framework spanning Change Agility, Leadership Delta, and Behavioral Governance\n  attribution:\n",
        "  hero_image_alt: Adaptive Adoption framework spanning Change Agility, Leadership Delta, and Behavioral Governance\n  cta:\n    primary:\n      text: Take the Audit\n      url: /diagnostics/ai-adoption-friction-audit\n      style: primary\n    secondary:\n      text: Explore Adaptive Adoption\n      url: /adaptive-adoption\n      style: secondary\n  attribution:\n",
    )
    block = replace_once(
        block,
        "  supabase:\n    table: diagnostic_responses\n    notes: Response capture disabled in the initial website release pending a versioned response schema and slug migration.\n",
        "  supabase:\n    table: null\n    notes: Version 0.1 is local-only; answers remain in browser localStorage and are not transmitted.\n",
    )
    block = replace_once(block, "    is_greyed: true\n", "    is_greyed: false\n")
    block = replace_once(
        block,
        "    greyed_pillar_label: AI ADOPTION FRICTION SUITE\n    greyed_time: In development\n",
        "    greyed_pillar_label: null\n    greyed_time: null\n",
    )
    block = replace_once(block, "    built: null\n", "    built: '2026-07-11'\n")
    block = replace_once(block, "  - in-development\n", "  - live\n")

    PATH.write_text(text[:start] + block, encoding="utf-8")
    print("Promoted AI Adoption Friction Audit to live")


if __name__ == "__main__":
    main()
