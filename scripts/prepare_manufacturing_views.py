"""Tessellate the issued supplier STEP files for O-M02 review, preserving O."""
from pathlib import Path
import hashlib
import json
import shutil
import cadquery as cq

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/manufacturing/O-M02'
MESH = ROOT / 'tmp/mesh-O-M02'
MESH.mkdir(parents=True, exist_ok=True)
body = cq.importers.importStep(str(OUT / 'RM10-O-M02-BODY.step'))
plate = cq.importers.importStep(str(OUT / 'RM10-O-M02-FACEPLATE.step'))
assert body.val().isValid() and plate.val().isValid()
assert abs(body.val().BoundingBox().ymin + 4) < 1e-6
assert abs(body.val().BoundingBox().ymax - 40) < 1e-6
for name, part in [('body', body), ('faceplate', plate)]:
    cq.exporters.export(part, str(MESH / f'{name}.stl'), tolerance=.04, angularTolerance=.10)
section = body.cut(cq.Solid.makeBox(412, 21, 89, cq.Vector(-206, 20, -1)))
cq.exporters.export(section, str(MESH / 'body-section.stl'), tolerance=.04, angularTolerance=.10)
for i in (1, 2):
    wet = cq.importers.importStep(str(ROOT / f'output/long-bore-O/cad/fluid-network-{i}.step'))
    wet = wet.cut(cq.Solid.makeBox(500, 3, 100, cq.Vector(-250, -7, -5)))
    assert abs(wet.val().BoundingBox().ymin + 4) < 1e-6
    cq.exporters.export(wet, str(MESH / f'fluid-network-{i}.stl'), tolerance=.04, angularTolerance=.10)
for pattern in ('side_plug_*.stl', 'elbow-reference-*.stl'):
    for path in (ROOT / 'tmp/mesh-long-bore-O').glob(pattern):
        shutil.copyfile(path, MESH / path.name)
assert len(list(MESH.glob('*.stl'))) == 13
report = {
    'issue': 'O-M02', 'source': 'Issued manufacturing STEP solids',
    'boss_height_mm': 4, 'slab_depth_mm': 40, 'boss_projection_mm': 1,
    'body_depth_mm': 44, 'body_valid': True, 'plate_valid': True,
    'source_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in sorted(OUT.glob('*.step'))},
    'fluid_highlight': 'Diagnostic voids trimmed to the new Y=-4 sealing plane',
    'references': 'Unchanged O side plugs and elbows; not supplier fitting CAD',
}
(OUT / 'render-geometry-verification.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
