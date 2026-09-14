"""Re-import supplier solids and compare machined features with the drawing schedule."""
from pathlib import Path
import json, math
import cadquery as cq
import ezdxf
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/manufacturing/O-M01'
schedule = json.loads((OUT / 'feature-schedule.json').read_text())
body = cq.importers.importStep(str(OUT / 'RM10-O-M01-BODY.step')).val()
plate = cq.importers.importStep(str(OUT / 'RM10-O-M01-FACEPLATE.step')).val()
def near(a, b): return abs(a-b) < 1e-5
def centres(faces): return {(round(f.Center().x, 4), round(f.Center().z, 4)) for f in faces}
def expected(key): return {(v['x'], v['z']) for v in schedule[key]}
def conical(shape, diameter, ymin, ymax):
    return [f for f in shape.Faces() if f.geomType() == 'CONE'
            and near(f.BoundingBox().xlen, diameter)
            and near(f.BoundingBox().ymin, ymin) and near(f.BoundingBox().ymax, ymax)]
for shape in (body, plate):
    assert shape.isValid() and len(shape.Solids()) == 1
assert body.intersect(plate).Volume() < 1e-6
for shape, dims in [(body, (410, 46, 87)), (plate, (482.6, 3, 87))]:
    b = shape.BoundingBox()
    assert all(near(a, v) for a, v in zip((b.xlen, b.ylen, b.zlen), dims))
for faces, key in [(conical(body, 28, -6, -5.5), 'front_ports'),
                   (conical(body, 13.8, -6, -5), 'front_ports'),
                   (conical(body, 4.4, 0, .55), 'body_fixings'),
                   (conical(body, 3.3, 14, 14+1.65/math.tan(math.radians(59))), 'body_fixings'),
                   (conical(plate, 8, -3, -1.25), 'body_fixings')]:
    assert len(faces) == len(schedule[key]) and centres(faces) == expected(key)
end_cones = [f for f in body.Faces() if f.geomType() == 'CONE' and near(f.BoundingBox().xlen, 1)]
assert len(end_cones) == 4
for port in schedule['end_ports']:
    assert any(near(f.Center().y, port['y']) and near(f.Center().z, port['z'])
               and near(f.BoundingBox().xmin if port['x'] < 0 else f.BoundingBox().xmax, port['x']) for f in end_cones)
for diameter, key in [(32, 'front_ports'), (4.5, 'body_fixings')]:
    faces = [f for f in plate.Faces() if f.geomType() == 'CYLINDER'
             and near(f.BoundingBox().xlen, diameter) and near(f.BoundingBox().zlen, diameter)]
    assert len(faces) == len(schedule[key]) and centres(faces) == expected(key)
# DXF is a through-cut profile: countersink mouths must not become through holes.
doc = ezdxf.readfile(OUT / 'RM10-O-M01-FACEPLATE.dxf')
entities = list(doc.modelspace())
circles = [e for e in entities if e.dxftype() == 'CIRCLE']
assert len(circles) == 26
for radius, key in [(16, 'front_ports'), (2.25, 'body_fixings')]:
    found = {(round(e.dxf.center.x, 4), round(e.dxf.center.y, 4)) for e in circles if near(e.dxf.radius, radius)}
    assert found == expected(key)
polys = [e for e in entities if e.dxftype() == 'LWPOLYLINE']
assert len(polys) == 13 and all(e.closed for e in polys)
from ezdxf import bbox
extents = [bbox.extents([e]) for e in polys]
for slot in schedule['rack_slots']:
    assert any(near(b.center.x, slot['x']) and near(b.center.y, slot['z'])
               and near(b.size.x, 10) and near(b.size.y, 7) for b in extents)
report = {'issue': 'O-M01', 'status': 'PASS', 'method': 'Independent STEP re-import and DXF entity inspection',
          'checks': ['valid single solids and overall sizes', 'no nominal body/plate overlap',
                     '20 boss lips and 20 front port entries at scheduled positions',
                     'four side port entries', 'six M4 entries and drill points',
                     '20 plate windows and six clearance holes', 'six 90-degree plate countersinks',
                     'DXF through-cut diameters and all 12 slot locations/sizes'],
          'limits': 'Checks nominal model features only; threads are pilot representations, and physical machining capability is unverified.'}
(OUT / 'export-verification.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
