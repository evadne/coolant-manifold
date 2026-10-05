"""Derive Q-M01 supplier solids/schedules and independently inspect critical geometry."""
from pathlib import Path
import shutil, hashlib, math
import json
import cadquery as cq
from OCP.BRepAdaptor import BRepAdaptor_Surface
import ezdxf
R=Path(__file__).resolve().parents[1];S=R/'output/long-bore-Q/cad';O=R/'output/manufacturing/Q-M01';O.mkdir(parents=True,exist_ok=True)
P=json.loads((R/'cad/iterations/P-long-bore.json').read_text());M=json.loads((R/'cad/manufacturing/Q-M01.json').read_text());Q=json.loads((R/'cad/iterations/Q-rear-ports.json').read_text())
r=json.loads((S/'verification.json').read_text())
for f,h in r['source_sha256'].items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h,f
assert r['M4_pilot_full_diameter_depth_mm']==M['M4_pilot_full_diameter_depth_mm']==13
features=[]
def add(group,points,**kwargs):
 for i,point in enumerate(points,1):features.append(dict(id=f'{group}{i:02}',group=group,xyz_mm=point,**kwargs))
front=[(x,-3,z) for z in P['port_rows_z'] for x in range(-180,181,40)]
mount=[(x,0,z) for x,z in P['faceplate_mounts_xz']]
side=[(x,20,z) for x in (-205,205) for z in P['port_rows_z']]
rear=[(x,40,z) for z in P['port_rows_z'] for x in (-180,180)]
add('P',front,thread='G 1/4 ISO 228-1',full_thread_after_entry=8,pilot_full_depth=23,entry_depth=1)
add('E',side,thread='G 1/4 ISO 228-1',full_thread_after_entry=8,pilot_full_depth='THROUGH gallery',entry_depth=1)
add('B',rear,thread='G 1/4 ISO 228-1',full_thread_after_entry=8,pilot_full_depth=20,entry_depth=1)
add('F',mount,thread='M4 x 0.7 - 6H',full_thread_after_entry=10,pilot_full_depth=13,entry_depth=.55)
add('W',[(x,0,z) for x,y,z in front],diameter=32)
add('H',mount,diameter=4.5)
add('R',[(x,0,z) for x in (-232.55,232.55) for z in P['rack_slot_centres_z']],length=10,width=7)
(O/'feature-schedule.json').write_text(json.dumps({'manufacturing_revision':'Q-M01','datum':'A POM front Y0; B width midplane X0; C bottom Z0; rear view reverses X on page','features':features},indent=2)+'\n')
for part in ('body','faceplate'):
 dest=O/f'RM10-Q-M01-{part.upper()}.step';shutil.copyfile(S/f'{part}.step',dest)
 shape=cq.importers.importStep(str(dest)).val();assert shape.isValid() and len(shape.Solids())==1
 assert dest.read_bytes()==(S/f'{part}.step').read_bytes()
body=cq.importers.importStep(str(S/'body.step')).val();plate=cq.importers.importStep(str(S/'faceplate.step')).val()
assert abs(body.BoundingBox().xlen-410)<1e-6 and abs(body.BoundingBox().ylen-43)<1e-6 and abs(body.BoundingBox().zlen-87)<1e-6
# Test each of the actual shorter holes and the restored material behind its point.
for x,y,z in mount:
 for depth in (1,6,12.99):assert not body.isInside(cq.Vector(x,depth,z))
 assert body.isInside(cq.Vector(x,14.1,z))
 assert body.isInside(cq.Vector(x+2.1,6,z))
for points in (front,side,rear):
 for x,y,z in points:
  v=cq.Vector(0,1,0) if y<0 else cq.Vector(0,-1,0) if y==40 else cq.Vector(1 if x<0 else -1,0,0)
  assert not body.isInside(cq.Vector(x,y,z)+v*5)
  test=cq.Vector(x,y,z)+v*.2+(cq.Vector(0,0,9) if y==20 else cq.Vector(9,0,0))
  assert body.isInside(test)
assert not any(f.geomType()=='CONE' for f in plate.Faces())
cs=[]
for f in plate.Faces():
 if f.geomType()=='CYLINDER':
  c=BRepAdaptor_Surface(f.wrapped).Cylinder();v=c.Location();cs.append((v.X(),v.Z(),c.Radius()))
for group,radius in [('W',16),('H',2.25)]:
 rows=[f for f in features if f['group']==group];actual=[c for c in cs if abs(c[2]-radius)<1e-6];assert len(actual)==len(rows)
 for row in rows:
  x,y,z=row['xyz_mm'];assert any(math.hypot(x-a,z-b)<1e-6 for a,b,c in actual)
shutil.copyfile(R/'output/long-bore-P/cad/faceplate-flat.dxf',O/'RM10-Q-M01-FACEPLATE.dxf')
dxf=ezdxf.readfile(O/'RM10-Q-M01-FACEPLATE.dxf');assert not dxf.audit().has_errors
cir=list(dxf.modelspace().query('CIRCLE'));assert len(cir)==32
assert not list(dxf.modelspace().query('TEXT MTEXT DIMENSION'))
for f in features:
 if f['group'] in ('W','H'):
  x,y,z=f['xyz_mm'];assert any(math.hypot(c.dxf.center.x-x,c.dxf.center.y-z)<1e-6 and abs(c.dxf.radius-f['diameter']/2)<1e-6 for c in cir)
# Reference assembly only: shorten the prior ISO button screw shank to 10 mm.
AOUT=R/'output/assembly/Q';AOUT.mkdir(parents=True,exist_ok=True)
screw=cq.importers.importStep(str(R/'output/long-bore-P/cad/REFERENCE-M4x16-ISO7380.step')).val()
screw=screw.cut(cq.Solid.makeBox(30,20,30,cq.Vector(-15,10,-15)))
cq.exporters.export(screw,str(AOUT/'REFERENCE-M4x10-ISO7380.step'))
assy=cq.Assembly(name='Q_M01_REFERENCE_not_a_supplier_part');assy.add(body,name='POM');assy.add(plate,name='faceplate')
for i,(x,y,z) in enumerate(mount):
 s=screw.translate(cq.Vector(x,-2,z));assert s.intersect(body).Volume()<1e-6 and s.intersect(plate).Volume()<1e-6;assy.add(s,name=f'REFERENCE_M4x10_{i+1}')
assy.export(str(AOUT/'REFERENCE-assembled-with-screws.step'))
report=dict(manufacturing_revision='Q-M01',checks='PASS',body_solid_count=1,plate_solid_count=1,G1_4_ports=28,M4_threads=12,plate_windows=20,plate_retention_holes=12,optional_rack_slots=12,
 body_extent_mm=[410,43,87],plate_extent_mm=[482.6,2,87],body_volume_mm3=body.Volume(),plate_volume_mm3=plate.Volume(),plate_mass_kg=plate.Volume()*7.9e-6,
 M4_pilot_full_diameter_mm=13,M4_total_drilled_depth_mm=13+1.65/math.tan(math.radians(59)),M4_full_thread_after_entry_mm=10,M4_reference_screw_length_mm=10,M4_tip_to_full_pilot_bottom_mm=5,
 M4_nominal_screw_to_hole_radial_clearance_mm=.25,M4_worst_coordinate_fit_margin_mm=.25-math.hypot(.1,.1),
 boss_window_nominal_radial_clearance_mm=2,root_window_worst_size_and_coordinate_clearance_mm=(32-(28.1+2*1.1))/2-math.hypot(.2,.2),
 boss_projection_size_stack_mm=[2.95-2.1,3.05-1.9],projection_note='Size-only stack before flatness and assembled distortion',
 geometry=r,source_sha256={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [R/'cad/manufacturing/Q-M01.json',R/'scripts/prepare_Q_production.py',S/'body.step',S/'faceplate.step']})
assert report['root_window_worst_size_and_coordinate_clearance_mm']>.5
(O/'geometry-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='geometry'},indent=2))
