# Contributing to Adaptive Adoption™

Use it, study it, challenge it, improve it. Contributions can be conceptual, empirical, or practical; coding is not required.

## Suggest a correction or challenge

[Open an issue](https://github.com/paulggibbons/adaptive_adoption/issues/new) with the page or tool, the specific claim or problem, your proposed change, and supporting evidence. Distinguish a research finding from a practitioner observation or an illustrative example.

## Propose a change

Create a branch and open a pull request. Explain the problem, what changes, the source of any revised framework wording, and how you checked it. Preserve existing attribution and make the status of new tools explicit. Do not describe a planned instrument as live or a conceptual instrument as validated.

The [canonical source notes](docs/CANONICAL-SOURCES.md) govern the published wording. Bring apparent conflicts with the website into the pull request rather than silently creating another version. For diagnostic claims, use the [evidence scales](docs/EVIDENCE-SCALES.md).

## Technical validation

Install `scripts/requirements.txt` and run the manifest validator and its existing pressure tests when changing the manifest. Run `python scripts/assemble_content.py` followed by `python -m mkdocs build` when changing the documentation. Pull requests build the documentation before publication.

Contact: paul@paulgibbonsadvisory.com.
