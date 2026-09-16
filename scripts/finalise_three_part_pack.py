"""Verify current fabrication bundles and reviewed presentations; create a local index."""
from pathlib import Path
import hashlib
import json
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/submission/current-three-parts'
OUT.mkdir(parents=True, exist_ok=True)

def read(path):
    return json.loads((ROOT / path).read_text())

def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()

def check_sources(record):
    for path, expected in record.get('source_sha256', {}).items():
        assert sha(path) == expected, f'Stale source: {path}'

q = read('output/manufacturing/Q-M04/geometry-verification.json')
r = read('output/manufacturing/R7-M01/geometry-verification.json')
face = read('output/manufacturing/Q-M03/geometry-verification.json')
assert face['checks'] == 'PASS' and face['outer_corner_radius_mm'] == 5
assert face['minimum_opening_to_outer_profile_mm'] > 1.89
check_sources(face)
assert q['checks'] == r['checks'] == 'PASS'
check_sources(q)
check_sources(q['geometry'])
assert q['perimeter_edges'] == 12 and q['perimeter_chamfer_mm'] == 0.5
assert q['curved_faces_unchanged'] and q['sealing_lands_and_M4_bearing_areas_unchanged']
assert q['G1_4_ports'] == 28 and q['M4_threads'] == 12
assert q['M4_full_thread_after_entry_mm'] == 10
assert q['M4_pilot_full_diameter_mm'] == 13
assert q['geometry']['wet_networks'] == 2
# Q-M01's positive fit calculation is historical; Q-M03 records the accepted capability.
assert face['linear_and_coordinate_tolerance_mm'] == 0.1
assert q['root_window_worst_size_and_coordinate_clearance_mm'] > 0
assert r['nominal_geometry_unchanged'] and r['solid_count'] == 1
assert sha('output/radiator-R7/rack-plate-R7.step') == r['source_step_sha256']

# Superseded index copies are disposable; canonical submitted archives remain intact.
for old_name in ['RM10-Q-M01-BODY.zip', 'RM10-Q-M01-FACEPLATE.zip', 'SN1260-R6-M02-PLATE.zip', 'RM10-Q-M02-FACEPLATE.zip', 'SN1260-R6-M03-PLATE.zip']:
    (OUT/old_name).unlink(missing_ok=True)

parts = []
for issue, stem, pages in [
    ('Q-M04', 'RM10-Q-M04-BODY', 3),
    ('Q-M03', 'RM10-Q-M03-FACEPLATE', 2),
    ('R7-M01', 'SN1260-R7-M01-PLATE', 3),
]:
    directory = Path('output/submission') / issue
    verification = read(directory / 'package-verification.json')
    assert verification['checks'] == 'PASS'
    if issue == 'Q-M01':
        # Preserve historical generator hashes: verify the untouched body bundle against
        # its actual submission record instead of requiring old scripts to remain frozen.
        original = read('output/submission/jlc-quotation-2026-09-15.json')
        sent = next(p for p in original['parts'] if p['part'] == stem)
        assert sha(sent['archive']) == sent['sha256']
    else:
        check_sources(verification)
    for line in (ROOT / directory / 'SHA256SUMS.txt').read_text().splitlines():
        digest, name = line.split('  ', 1)
        assert sha(directory / name) == digest, f'Stale package: {name}'
    extensions = ['step', 'pdf'] + ([] if stem.endswith('BODY') else ['dxf'])
    bundle = directory / f'{stem}.zip'
    with zipfile.ZipFile(ROOT / bundle) as archive:
        assert archive.testzip() is None
        assert set(archive.namelist()) == {f'{stem}.{ext}' for ext in extensions}
        for ext in extensions:
            origin = Path('output/pdf') if ext == 'pdf' else Path('output/manufacturing') / issue
            assert archive.read(f'{stem}.{ext}') == (ROOT / origin / f'{stem}.{ext}').read_bytes()
    shutil.copyfile(ROOT / bundle, OUT / bundle.name)
    parts.append({'part': stem, 'zip': bundle.name, 'sha256': sha(bundle),
                  'pdf_sheets': pages, 'contents': extensions})

product = read('output/long-bore-Q/product-views/render-manifest.json')
context = read('output/context-25U/layout.json')
studio = read('output/long-bore-Q/photorealistic/render-notes.json')
assert product['revision'] == studio['revision'] == context['manifold_revision'] == 'Q'
assert context['radiator_plate_revision'] == 'R7'
assert product['body_issue'] == studio['body_issue'] == context['manifold_body_issue'] == 'Q-M04'
assert product['faceplate_issue'] == studio['faceplate_issue'] == context['manifold_faceplate_issue'] == 'Q-M03'
assert r['outer_corner_radius_mm'] == product['outer_corner_radius_mm'] == context['outer_corner_radius_mm'] == 5
check_sources(product)
check_sources(context)
assert len(product['views']) == 12 and len(context['view_files']) == 9
assert not read('output/context-25U/scene-verification.json')['tube_equipment_intersections']
# Earlier render paths have intentionally been refreshed; their old hashes are historical.
visual = read('output/review/Q-M04-visual-review.json')
check_sources(visual)
assert visual['pdf_sheets_reviewed'] == 3 and visual['unchanged_steel_sheets_inherited'] == 5
assert visual['presentation_images_reviewed'] == 25 and visual['unchanged_radiator_images_inherited'] == 7

submission_path = ROOT / 'output/submission/jlc-order-2026-09-16.json'
submission = json.loads(submission_path.read_text())
submitted = bool(submission.get('submitted') and len(submission['parts']) == len(parts) and all(
    any(p['part'] == sent['part'] and p['sha256'] == sent.get('sha256') for p in parts)
    for sent in submission['parts']))

manifest = {
    'checks': 'PASS', 'parts': parts,
    'release_status': read('output/submission/jlc-order-2026-09-16.json')['status'],
    'operator_disposition': 'Complete set accepted and separately submitted for file review with operator-confirmed UPS shipping. Preserve original orders. No payment authorised.',
    'fabrication_scope': 'Each ZIP contains only one custom part STEP and its fabrication drawing/profile.',
    'assembly_guide': 'docs/assembly-Q.md',
    'assembly_parameters': 'cad/assembly/Q.json',
    'geometry_and_coordinate_checks': 'PASS',
    'current_context_sources': 'PASS',
    'visual_review_record': 'output/review/Q-M04-visual-review.json',
    'faceplate_worst_case_fit': face['fit_status'],
    'faceplate_M4_radial_margin_mm': face['worst_case_M4_radial_margin_mm'],
    'historical_submission_record': 'output/submission/jlc-quotation-2026-09-15.json',
    'supplier_submission_performed': submitted,
    'submission_record': 'output/submission/jlc-order-2026-09-16.json' if submitted else None,
    'remaining_supplier_review': ['POM stock grade', 'Deep-gallery drilling process',
                                   'Specified tolerances, flatness and surface finishes'],
    'source_sha256': {str(p): sha(p) for p in [
        Path('scripts/finalise_three_part_pack.py'),
        Path('output/review/Q-M04-visual-review.json'),
        Path('scripts/draw_radiator_production.py'),
        Path('scripts/package_radiator_production.py'),
        Path('cad/manufacturing/R7-M01.json'),
    ]},
}
(OUT / 'verification.json').write_text(json.dumps(manifest, indent=2) + '\n')
(OUT / 'README.md').write_text('''# Current three-part fabrication pack

Accepted new-order pack: Q-M04 body with C0.5 slab-edge chamfers and eight corner flats, Q-M03 faceplate and R7-M01 radiator. A separate new order was submitted for file review after the operator confirmed UPS, the cheapest quoted shipping option. Preserve the original supplier orders and files. [New-order status](../../../docs/jlc-order-2026-09-16.md) records UI progress separately from these local packaging checks. No payment is performed by these scripts.

| Part | Fabrication bundle | Process |
|---|---|---|
| Q POM body | [RM10-Q-M04-BODY.zip](RM10-Q-M04-BODY.zip) | CNC milling, drilling and tapping; black unfilled declared POM-C or POM-H |
| Q faceplate | [RM10-Q-M03-FACEPLATE.zip](RM10-Q-M03-FACEPLATE.zip) | 2 mm 304 flat sheet; plain holes and raw sheet finish on both faces |
| R7 radiator plate | [SN1260-R7-M01-PLATE.zip](SN1260-R7-M01-PLATE.zip) | 2 mm 304 flat sheet; plain holes and raw sheet finish on both faces |

Each ZIP contains a same-name single-part STEP and PDF; the steel parts also have a DXF cut profile. The drawings define finished geometry, threads, tolerances, surface finish and inspection. STEP thread cylinders represent tapping pilots. There are eight drawing sheets across the three parts. Both steel drawings specify four R5 outside corners and ±0.10 mm cut dimensions and coordinates. Other cut profiles and fixing positions are retained. Separate flatness limits remain 0.30/0.50 mm; faceplate uses standard deburring, radiator retains its specified cable-contact edge finish.

[Supplier requirements and open fabrication questions](../../../docs/jlc-final-review.md) cover the POM stock, long-gallery drilling and specified tolerances/finishes. [Verification](verification.json) records bundle integrity and consistency with the reviewed Q/R7 outputs.

[Manifold assembly instructions](../../../docs/assembly-Q.md), [radiator assembly instructions](../../../docs/radiator-rack-plate.md) and engineering assessments are separate project documents, outside these fabrication ZIPs. The current [product views](../../../docs/product-views.md) and [rack scene](../../../docs/context-25U.md) are review references.
''')
files = sorted(p for p in OUT.iterdir() if p.is_file() and p.name != 'SHA256SUMS.txt')
(OUT / 'SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.name}\n' for p in files))
print(json.dumps({'checks': 'PASS', 'parts': len(parts), 'drawing_sheets': 8,
                  'new_pdf_sheets_reviewed': 3, 'presentation_images_reviewed': 25, 'inherited_radiator_images': 7, 'supplier_submission_performed': submitted}, indent=2))
