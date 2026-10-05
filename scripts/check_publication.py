"""Read-only check of canonical downloads and public documentation navigation.

Uses only Python's standard library. This checks file integrity and local link
existence, not manufacturability, render appearance, licences or external URLs.
"""
from pathlib import Path
import hashlib
import json
import re
import zipfile
from check_retained_inputs import check as check_inputs
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check():
    release = json.loads((ROOT / 'cad/current-release.json').read_text())
    require(len(release['parts']) == 3, 'Expected three selected parts')
    names = set()
    for part in release['parts']:
        require(part['part'] not in names, 'Duplicate selected part')
        names.add(part['part'])
        for field in ('source', 'bundle', 'issue_bundle', 'drawing', 'step'):
            require((ROOT / part[field]).is_file(), f'Missing {field}: {part[field]}')
        for field in ('bundle', 'issue_bundle'):
            require(digest(ROOT / part[field]) == part['sha256'], f'Hash mismatch: {part[field]}')
        originals = {'step': ROOT / part['step'], 'pdf': ROOT / part['drawing']}
        if part['dxf']:
            originals['dxf'] = ROOT / part['dxf']
        with zipfile.ZipFile(ROOT / part['bundle']) as archive:
            require(archive.testzip() is None, f'ZIP corruption: {part["bundle"]}')
            require(set(archive.namelist()) == {part['part'] + '.' + ext for ext in originals},
                    f'Unexpected ZIP contents: {part["bundle"]}')
            for ext, original in originals.items():
                require(archive.read(part['part'] + '.' + ext) == original.read_bytes(),
                        f'ZIP differs from current {ext}: {part["part"]}')
    index = ROOT / 'output/submission/current-three-parts'
    for line in (index / 'SHA256SUMS.txt').read_text().splitlines():
        expected, name = line.split('  ', 1)
        require(digest(index / name) == expected, f'Stale index checksum: {name}')
    verification = json.loads((index / 'verification.json').read_text())
    require(verification['checks'] == 'PASS', 'Index verification is not PASS')
    for path, expected in verification['source_sha256'].items():
        require(digest(ROOT / path) == expected, f'Stale index source: {path}')

    # Deliberately check maintained entry points, not every snapshot's old links.
    docs = ['README.md', 'AGENTS.md', 'LICENSING.md', 'output/README.md',
            'output/submission/current-three-parts/README.md', 'docs/README.md',
            'docs/order-from-jlc.md', 'docs/jlc-first-article.md', 'docs/manufacturing.md',
            'docs/design.md', 'docs/iterations.md',
            'docs/three-part-recap.md', 'docs/rebuild.md', 'docs/new-revision.md',
            'docs/publication-review.md', 'docs/astra-commentary.md',
            'docs/archive/working-notes-2026-09-16.md',
            'docs/archive/manufacturing-status-through-2026-10-05.md']
    links = 0
    for name in docs:
        document = ROOT / name
        require(document.is_file(), f'Missing navigation document: {name}')
        content = re.sub(r'```.*?```', '', document.read_text(), flags=re.S)
        for match in re.finditer(r'!?\[[^\]]*\]\(([^)]+)\)', content):
            target = match.group(1).strip('<>')
            url = urlsplit(target)
            if url.scheme or not url.path:
                continue
            path = (document.parent / unquote(url.path)).resolve()
            require(path.is_relative_to(ROOT), f'Non-portable link in {name}: {target}')
            require(path.exists(), f'Broken local link in {name}: {target}')
            links += 1
    return {'checks': 'PASS', 'canonical_parts': len(names), 'navigation_documents': len(docs),
            'local_links_checked': links,
            'retained_inputs': check_inputs(),
            'scope': 'Bundle/member hashes, index checksums/source hashes, local link targets; read-only'}


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
