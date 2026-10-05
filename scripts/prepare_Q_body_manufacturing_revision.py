"""Derive Q-M04 with twelve C0.5 perimeter chamfers; preserve submitted Q-M01."""
from pathlib import Path
import hashlib, math
import json
import cadquery as cq
R=Path(__file__).resolve().parents[1];manufacturing_revision='Q-M04';out=R/f'output/manufacturing/{manufacturing_revision}';out.mkdir(parents=True,exist_ok=True)
M=json.loads((R/f'cad/manufacturing/{manufacturing_revision}.json').read_text())
source=R/'output/manufacturing/Q-M01/RM10-Q-M01-BODY.step'
old=cq.importers.importStep(str(source)).val()
def perimeter(e):
 p=e.Center()
 return e.geomType()=='LINE' and sum([abs(abs(p.x)-205)<1e-6,min(abs(p.y),abs(p.y-40))<1e-6,min(abs(p.z),abs(p.z-87))<1e-6])>=2
edges=[e for e in old.Edges() if perimeter(e)];assert len(edges)==12
body=cq.Workplane(obj=old).newObject(edges).chamfer(M['perimeter_chamfer_mm']).val()
assert body.isValid() and len(body.Solids())==1 and body.cut(old).Volume()<1e-6
removed=old.cut(body)
# All change confined to the twelve exterior edges of the slab.
blank=cq.Workplane('XY').box(410,40,87,centered=False).translate((-205,0,0))
expected=blank.val().cut(blank.edges().chamfer(.5).val())
assert removed.cut(expected).Volume()<1e-5 and expected.cut(removed).Volume()<1e-5
S=json.loads((R/'output/manufacturing/Q-M01/feature-schedule.json').read_text())
for f in S['features']:
 if f['group'] not in 'PEBF':continue
 x,y,z=f['xyz_mm'];axis=(0,1,0) if f['group'] in 'PF' else (0,-1,0) if f['group']=='B' else (1 if x<0 else -1,0,0)
 radius=14 if f['group'] in 'PB' else 11 if f['group']=='E' else 3.8
 zone=cq.Solid.makeCylinder(radius,1,cq.Vector(x,y,z),cq.Vector(*axis))
 assert removed.intersect(zone).Volume()<1e-6,f['id']
# Retain every curved face: bores, boss roots/lips and hole entries.
def curved(shape):
 return sorted((f.geomType(),round(f.Area(),5),tuple(round(v,5) for v in f.Center().toTuple())) for f in shape.Faces() if f.geomType()!='PLANE')
assert curved(old)==curved(body)
planes=[f for f in body.Faces() if f.geomType()=='PLANE' and max(abs(v) for v in f.normalAt().toTuple())<.999]
edge_planes=[f for f in planes if sum(abs(v)>1e-6 for v in f.normalAt().toTuple())==2]
corner_planes=[f for f in planes if sum(abs(v)>1e-6 for v in f.normalAt().toTuple())==3]
assert len(edge_planes)==12 and len(corner_planes)==8
stem=f'RM10-{manufacturing_revision}-BODY';cq.exporters.export(body,str(out/f'{stem}.step'));cq.exporters.export(body,str(out/f'{stem}.stl'),tolerance=.025,angularTolerance=.06)
S['manufacturing_revision']=manufacturing_revision;(out/'feature-schedule.json').write_text(json.dumps(S,indent=2)+'\n')
face=cq.importers.importStep(str(R/'output/manufacturing/Q-M03/RM10-Q-M03-FACEPLATE.step')).val()
assert body.intersect(face).Volume()<1e-6
screw=cq.importers.importStep(str(R/'output/assembly/Q/REFERENCE-M4x10-ISO7380.step')).val()
a=cq.Assembly(name='Q_M04_body_Q_M03_faceplate');a.add(body,name='POM_Q_M04');a.add(face,name='faceplate_Q_M03')
for f in S['features']:
 if f['group']=='F':
  x,y,z=f['xyz_mm'];a.add(screw.translate((x,-2,z)),name='M4_'+f['id'])
a.export(str(R/'output/assembly/Q/REFERENCE-assembled-with-screws.step'))
prior=json.loads((R/'output/manufacturing/Q-M01/geometry-verification.json').read_text())
report={k:v for k,v in prior.items() if k!='source_sha256'}
report.update(manufacturing_revision=manufacturing_revision,body_volume_mm3=body.Volume(),perimeter_chamfer_mm=.5,perimeter_chamfer_angle_degrees=45,perimeter_edges=12,removed_volume_mm3=removed.Volume(),curved_faces_unchanged=True,sealing_lands_and_M4_bearing_areas_unchanged=True,geometry_change='Only twelve main-slab outside edges chamfered C0.5 x45 degrees; intersecting corners meet as modelled',source_sha256={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [source,R/f'cad/manufacturing/{manufacturing_revision}.json',R/'scripts/prepare_Q_body_manufacturing_revision.py',R/'output/manufacturing/Q-M01/geometry-verification.json']})
(out/'geometry-verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['manufacturing_revision','checks','perimeter_edges','removed_volume_mm3','curved_faces_unchanged','sealing_lands_and_M4_bearing_areas_unchanged']},indent=2))
