"""Audit PDF essentials and bundle matching supplier files, with no assemblies or notes in ZIPs."""
from pathlib import Path
import hashlib, json, zipfile
from pypdf import PdfReader
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/manufacturing/O-M01'
PDF = ROOT / 'output/pdf'
checks = {}
for part, pages in [('BODY', 3), ('FACEPLATE', 2), ('DFM', 2)]:
    path = PDF / f'RM10-O-M01-{part}.pdf'
    reader = PdfReader(path)
    assert len(reader.pages) == pages
    text = '\n'.join(p.extract_text() for p in reader.pages)
    assert '\ufffd' not in text and 'O-M01' in text
    if part == 'BODY':
        for phrase in ['INTERNAL EDGE DEBURRING IS NOT REQUIRED', 'POM-C or POM-H accepted', 'G 1/4', 'M4', 'external edges']:
            assert phrase in text, phrase
    elif part == 'FACEPLATE':
        assert 'NO TAPPED HOLES IN THIS PLATE' in text
        assert '90°' in text and 'Ø32' in text
    checks[path.name] = {'pages': pages, 'required_notes': 'PASS'}
for part, extensions in [('BODY', ['step']), ('FACEPLATE', ['step', 'dxf'])]:
    stem = f'RM10-O-M01-{part}'
    paths = [OUT / (stem+'.'+ext) for ext in extensions] + [PDF / (stem+'.pdf')]
    archive = OUT / (stem+'.zip')
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
        for path in paths:
            z.write(path, path.name)
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        assert set(z.namelist()) == {p.name for p in paths}
        for path in paths:
            assert z.read(path.name) == path.read_bytes()
    checks[archive.name] = {'members': [p.name for p in paths], 'integrity': 'PASS'}
(OUT / 'package-verification.json').write_text(json.dumps(checks, indent=2)+'\n')
paths = sorted([p for p in OUT.iterdir() if p.is_file() and p.name != 'SHA256SUMS.txt'] + list(PDF.glob('RM10-O-M01-*.pdf')))
(OUT / 'SHA256SUMS.txt').write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(ROOT)}\n' for p in paths))
print(json.dumps(checks, indent=2))
