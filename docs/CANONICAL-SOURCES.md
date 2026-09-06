# Canonical sources and synchronization

Reviewed: **6 September 2026**. Scope: the homepage’s framework, AI Tools, and Publications destinations.

## Source map

| Website source | Repository destination | Reconciliation |
|---|---|---|
| [Change Agility](https://paulgibbonsadvisory.com/change-agility/) | `change-agility/readme.md` and 7 numbered pillar pages | Published descriptions and four practice columns copied into readable Markdown |
| [Leadership Delta](https://paulgibbonsadvisory.com/leadership-delta/) | `leadership-delta/readme.md` and 7 numbered dimension pages | Published claims and self / others / systems practices |
| [Behavioral Governance](https://paulgibbonsadvisory.com/behavioral-governance/) | `behavioral-governance/readme.md` and 6 numbered dimension pages | Published enacted standards and three-layer assessment content |
| [AI Tools](https://paulgibbonsadvisory.com/diagnostics/) | `tools/README.md`, `data/tools.yml` | 17 live tools indexed; flagship renamed AI Workforce Readiness Assessment and current route restored |
| [Publications](https://paulgibbonsadvisory.com/publications/) | `publications/README.md` | Seven canonical web/PDF pairs, books, and Corpus |
| Three framework page diagrams | `visuals-and-presentations/*/canonical-framework.png` | Published PNGs copied unchanged |

The main website’s public pages govern current framework wording for this synchronization. The manifest remains the version-controlled publication metadata used by the website build. The retired flagship name is retained as an alias and its slug is unchanged to preserve response continuity.

## Earlier material

Earlier draft arguments, research, nested descriptions, historical model cards, and presentation PDFs are not newly validated by this refresh. Current entry points identify their status. No unsupported case-study claims from the previous pillar pages have been carried into the synchronized pages. Their history remains available through Git.

The website’s tool long list includes some pillar labels that differ from its framework matrices. This refresh follows the matrices for the framework and does not silently renumber the entire tool registry. The new public tools index groups applications by discipline without reproducing inconsistent pillar numbers.

## Repeat the synchronization

`python scripts/sync_framework_pages.py` downloads the three public framework pages, validates the 7 + 7 + 6 page mappings, and updates their Markdown. HTML hashes and retrieval dates are recorded in `data/canonical-website.json`. Review the diff before publishing; this command does not assert that the source’s empirical claims have been independently validated.

Separately check live tool names, URLs, statuses, publication links, and the three diagram files against the website. Update the indexes and this receipt. Preserve deprecated diagnostic identifiers unless a migration is explicitly intended.

Run the manifest checks, assemble the documentation, and build MkDocs. Keep research drafts clearly labelled and publication links pointed at the website’s current editions.
