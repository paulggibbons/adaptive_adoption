"""Refresh public framework pages from the canonical website (explicit invocation only).

Usage: python scripts/sync_framework_pages.py [--source-dir DIRECTORY]
Requires beautifulsoup4 and markdownify. A source directory may contain previously
downloaded change-agility.html, leadership-delta.html, behavioral-governance.html.
Validates all 20 dimensions before writing. Existing research is left in place.
"""
import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen

from bs4 import BeautifulSoup
from markdownify import markdownify

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://paulgibbonsadvisory.com'
DOMAINS = [('change-agility', 'ca', 'Change Agility™', 7, 'The Flywheel'),
           ('leadership-delta', 'ld', 'Leadership Delta™', 7, 'The Torque'),
           ('behavioral-governance', 'bg', 'Behavioral Governance™', 6, 'The Guardrails')]

def md(element):
    if element is None:
        return ''
    return markdownify(str(element), heading_style='ATX', bullets='-').strip()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-dir', type=Path)
    args = parser.parse_args()
    date = datetime.now(timezone.utc).date().isoformat()
    writes, records = {}, []
    for domain, prefix, title, expected, metaphor in DOMAINS:
        url = f'{BASE}/{domain}/'
        raw = ((args.source_dir / f'{domain}.html').read_bytes() if args.source_dir
               else urlopen(url, timeout=30).read())
        soup = BeautifulSoup(raw, 'html.parser')
        row_class = 'pillar-row' if prefix == 'ca' else 'dimension-row'
        rows = soup.select(f'.{prefix}-{row_class}')
        files = sorted((ROOT / domain / 'pillars').glob('0[1-7]-*.md'))
        assert len(rows) == len(files) == expected, (domain, len(rows), len(files))
        note = f'> Synchronized from the [canonical website]({url}) on {date}.\n'
        overview = f'# {title} — {metaphor}\n\n'
        overview += f'![{title} framework](../visuals-and-presentations/{domain}/canonical-framework.png)\n\n'
        overview += note + '\n'
        overview += '\n\n'.join(md(x) for x in soup.select(f'.{prefix}-subtitle')) + '\n\n'
        overview += '## Explore the framework\n\n| # | Pillar / dimension |\n|---|---|\n'
        for index, (row, path) in enumerate(zip(rows, files), 1):
            name_node = row.select_one(f'.{prefix}-pillar-name, .{prefix}-dim-name')
            assert name_node is not None
            name = name_node.get_text(' ', strip=True)
            expected_slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
            # The stable repository path spells out "first"; the website uses "1st".
            expected_slug = expected_slug.replace('1st-', 'first-')
            assert path.stem[3:] == expected_slug, (path, name)
            overview += f'| {index} | [{name}](pillars/{path.name}) |\n'
            content = f'# {"Pillar" if prefix == "ca" else "Dimension"} {index}: {name}\n\n{note}\n'
            for suffix in ['pillar-tagline', 'pillar-desc', 'dim-claim', 'dim-archetype', 'dim-condition']:
                for element in row.select(f'.{prefix}-{suffix}'):
                    content += md(element) + '\n\n'
            cells = row.select(f'.{prefix}-cell')
            assert len(cells) == (4 if prefix == 'ca' else 3 if prefix == 'ld' else 2)
            for cell in cells:
                content += '## ' + cell.select_one(f'.{prefix}-cell-label').get_text(' ', strip=True) + '\n\n'
                for item in cell.select(f'.{prefix}-cell-item'):
                    content += '### ' + item.select_one(f'.{prefix}-item-name').get_text(' ', strip=True) + '\n\n'
                    content += md(item.select_one(f'.{prefix}-item-desc')) + '\n\n'
            if prefix == 'ca' and index == 6:
                content += 'SHIFT Method © Robert Meza, *Aim for Behaviour*.\n\n'
            content += f'[Back to {title}](../readme.md) · [Live AI tools]({BASE}/diagnostics/)\n'
            writes[path] = content
        for box in soup.select(f'.{prefix}-context-box'):
            clone = BeautifulSoup(str(box), 'html.parser')
            for label in clone.select(f'.{prefix}-box-num'):
                label.decompose()
            overview += '\n' + md(clone) + '\n'
        overview += '\n## Tools, publications, and provenance\n\n'
        overview += '- [Live tools and assessments](../tools/README.md)\n- [Publications and whitepapers](../publications/README.md)\n- [Intellectual provenance](99_PROVENANCE.md)\n'
        overview += '\nOlder research notes and supporting drafts remain available in this directory. The numbered Markdown pages linked above carry the current website wording.\n'
        writes[ROOT / domain / 'readme.md'] = overview
        records.append({'url': url, 'retrieved': date, 'sha256': hashlib.sha256(raw).hexdigest(), 'dimensions': expected})
    for path, content in writes.items():
        path.write_text(content)
    (ROOT / 'data' / 'canonical-website.json').write_text(json.dumps({'sources': records}, indent=2) + '\n')
    print(f'Synchronized {len(writes)} pages; validated 20 pillar/dimension mappings.')

if __name__ == '__main__':
    main()
