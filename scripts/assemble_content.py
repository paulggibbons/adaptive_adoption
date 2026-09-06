"""Assemble the public documentation without flattening or overwriting source files."""
from pathlib import Path
import re
import shutil
import subprocess
import sys
from urllib.parse import quote, unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'content'
REPO_URL = 'https://github.com/paulggibbons/adaptive_adoption'

def main():
    # The content directory is generated; its six committed tool pages regenerate below.
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    mapping = {}
    def add(source, target=None):
        source = ROOT / source
        assert source.is_file(), f'Missing publication source: {source}'
        target = OUT / (target or source.relative_to(ROOT))
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        mapping[source.resolve()] = target

    for name in ['README.md', 'what-is-adaptive-adoption.md', 'why-adaptive-adoption-matters.md',
                 'how-this-repo-works.md', 'CONTRIBUTING.md']:
        add(name, 'index.md' if name == 'README.md' else name)
    add('tools/README.md', 'tools/live.md')
    add('publications/README.md', 'publications/index.md')
    add('docs/CANONICAL-SOURCES.md', 'canonical-sources.md')
    for folder in ['why-change-must-change', 'provenance', 'maturity-model']:
        for p in (ROOT/folder).glob('*.md'):
            if not p.stat().st_size: continue
            dest = p.relative_to(ROOT)
            if folder == 'why-change-must-change': dest = Path('foundations')/p.name
            if p.name.lower() == 'readme.md':dest=dest.with_name('index.md')
            add(p.relative_to(ROOT), dest)
    for domain in ['change-agility','leadership-delta','behavioral-governance']:
        add(f'{domain}/readme.md', f'{domain}/index.md')
        add(f'{domain}/99_PROVENANCE.md')
        for p in (ROOT/domain/'pillars').glob('0[1-7]-*.md'):add(p.relative_to(ROOT))
    for source,target in [
        ('change-agility/theory/philosophical-foundations.md',None),
        ('change-agility/diagnostics/AA_MI/AA_MI_structure.md','change-agility/diagnostics/AA_MI_structure.md'),
        ('leadership-delta/pillars/01-strategic-imagination/conditions-audit.md','leadership-delta/tools/conditions-audit.md'),
        ('behavioral-governance/pillars/governance-framework.md','behavioral-governance/theory/governance-framework.md'),
        ('behavioral-governance/dashboard/governance-dashboard.md','behavioral-governance/tools/governance-dashboard.md')]:add(source,target)
    for p in (ROOT/'visuals-and-presentations').rglob('*'):
        if p.is_file() and p.stat().st_size:add(p.relative_to(ROOT))
    add('assets/extra.css','extra.css')
    add('googleacea638aeb4140cf.html')
    subprocess.run([sys.executable, str(ROOT/'scripts/generate_tool_pages.py')], check=True)

    # Rewrite repo-relative Markdown links for the assembled layout. Supporting
    # research outside this curated site remains accessible in its GitHub location.
    for source,dest in mapping.items():
        if dest.suffix != '.md':continue
        def rewrite(match):
            href=match.group(1)
            if not href or href.startswith(('#','http:','https:','mailto:')):return match.group(0)
            parts=urlsplit(href)
            candidate=(source.parent/unquote(parts.path)).resolve()
            assert candidate.is_relative_to(ROOT), (source,href)
            if candidate.is_dir():
                candidate=next((candidate/n for n in ['README.md','readme.md','index.md'] if (candidate/n).is_file()),candidate)
            if candidate in mapping:
                import os
                target=Path(os.path.relpath(mapping[candidate],dest.parent)).as_posix()
                if parts.fragment:target+='#'+parts.fragment
                return ']('+target+')'
            if candidate.exists():
                kind='tree' if candidate.is_dir() else 'blob'
                target=f'{REPO_URL}/{kind}/main/{quote(candidate.relative_to(ROOT).as_posix())}'
                if parts.fragment:target+='#'+parts.fragment
                return ']('+target+')'
            return match.group(0)
        dest.write_text(re.sub(r'\]\(([^\s)]+)\)',rewrite,dest.read_text()))
    print(f'Assembled {len(mapping)} source files plus generated tool pages.')

if __name__ == '__main__':main()
