"""Verify the selected radiator revision and derive a single-part production issue without changing its solid."""
from pathlib import Path
import json,shutil,hashlib,math,argparse
import cadquery as cq
import ezdxf
from OCP.BRepAdaptor import BRepAdaptor_Surface
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--issue',default='R6-M02',choices=['R4-M01','R5-M01','R6-M01','R6-M02','R6-M03','R7-M01'])
ISSUE=parser.parse_args().issue
M=json.loads((ROOT/f'cad/manufacturing/{ISSUE}.json').read_text());REV=M['geometry_revision']
P=json.loads((ROOT/f'cad/radiator/{REV}.json').read_text())
OUT=ROOT/f'output/manufacturing/{ISSUE}';OUT.mkdir(parents=True,exist_ok=True)
source=ROOT/f'output/radiator-{REV}';stem=M['part_number'];H=P['height'];notched=bool(P.get('cable_notch'))
build_report=json.loads((source/'verification.json').read_text())
assert build_report['revision']==REV and build_report['geometry_checks']=='PASS'
assert P['fan_mount_style']=='clearance' and P['fan_thread'] is None
for ext in ('step','dxf'):
 shutil.copyfile(source/f'rack-plate-{REV}.{ext}',OUT/f'{stem}.{ext}')
rows=[]
def add(group,points,kind,**dims):
 for i,(x,y) in enumerate(points,1):rows.append(dict(id=f'{group}{i:02}',group=group,kind=kind,x=round(x,5),y=round(y,5),**dims))
a=sorted([(x+dx,H/2+y+dy) for x in P['aperture_centres_x'] for y in P['aperture_centres_y_from_centre'] for dx in (-85,85) for dy in (-85,85)],key=lambda p:(p[1],p[0]))
b=sorted([(x,H/2+y) for x in P['radiator_mount_x'] for y in P['radiator_mount_y_from_centre']],key=lambda p:(p[1],p[0]))
c=[(x,y) for x in P['rack_mount_x'] for y in P['rack_mount_y']]
d=sorted([(x,H/2+y) for x in P['aperture_centres_x'] for y in P['aperture_centres_y_from_centre']],key=lambda p:(p[1],p[0]))
add('A',a,'round_hole',diameter=4.5);add('B',b,'round_hole',diameter=3.6)
add('C',c,'slot',length=10,width=7,end_radius=3.5)
add('D',d,'aperture',width=188,height=188,corner_radius=50)
if notched:add('E',[(0,H)],'edge_notch',**P['cable_notch'])
assert len(rows)==72+int(notched) and len({r['id'] for r in rows})==len(rows)
solid=cq.importers.importStep(str(OUT/f'{stem}.step')).val();bb=solid.BoundingBox()
assert abs(solid.Volume()-build_report['plate_volume_mm3'])<1e-4
assert solid.isValid() and len(solid.Solids())==1
assert max(abs(bb.xlen-482.6),abs(bb.ylen-444.5),abs(bb.zlen-2))<1e-6
faces=[f for f in solid.Faces() if abs(f.Center().z)<1e-6 and f.geomType()=='PLANE']
front=max(faces,key=lambda f:f.Area());assert len(front.Wires())==73
cyl=[]
for f in solid.Faces():
 if f.geomType()=='CYLINDER':
  cc=BRepAdaptor_Surface(f.wrapped).Cylinder();pt=cc.Location();axis=cc.Axis().Direction()
  assert abs(abs(axis.Z())-1)<1e-7
  cyl.append((pt.X(),pt.Y(),cc.Radius()))
for group,radius,points in [('A',2.25,a),('B',1.8,b)]:
 actual=[(x,y) for x,y,r in cyl if abs(r-radius)<1e-6]
 assert len(actual)==len(points)
 for x,y in points:assert any(math.hypot(x-xx,y-yy)<1e-6 for xx,yy in actual)
for x,y in c:
 for xx in (x-1.5,x+1.5):assert any(abs(r-3.5)<1e-6 and math.hypot(px-xx,py-y)<1e-6 for px,py,r in cyl)
assert sum(abs(r-3.5)<1e-6 for x,y,r in cyl)==80
assert sum(abs(r-50)<1e-6 for x,y,r in cyl)==16
# Four outer R2 corners plus the four parameterised notch arcs.
cr=P['outer_radius']
expected_arcs=[(-P['width']/2+cr,cr,cr),(P['width']/2-cr,cr,cr),
               (-P['width']/2+cr,H-cr,cr),(P['width']/2-cr,H-cr,cr)]
if notched:
 n=P['cable_notch'];a=n['mouth_width']/2;u=n['mouth_radius'];b=n['bottom_radius'];d=n['depth']
 expected_arcs += [(a,H-u,u),(-a,H-u,u),(a-u-b,H-d+b,b),(-a+u+b,H-d+b,b)]
for x,y,r in expected_arcs:
 assert any(math.hypot(x-xx,y-yy)<1e-6 and abs(rr-r)<1e-6 for xx,yy,rr in cyl)
assert len(cyl)==128+4*int(notched)
# Independently verify the two circular DXF groups and all closed profile loops.
dxf=ezdxf.readfile(OUT/f'{stem}.dxf');assert not dxf.audit().has_errors
circles=list(dxf.modelspace().query('CIRCLE'));loops=list(dxf.modelspace().query('LWPOLYLINE'))
assert len(circles)==28 and len(loops)==45 and all(l.closed for l in loops)
assert not list(dxf.modelspace().query('TEXT MTEXT DIMENSION'))
for r in rows:
 if r['kind']=='round_hole':assert any(math.hypot(e.dxf.center.x-r['x'],e.dxf.center.y-r['y'])<1e-6 and abs(e.dxf.radius-r['diameter']/2)<1e-6 for e in circles)
(OUT/'feature-schedule.json').write_text(json.dumps({'part_number':stem,'origin':'X centreline; Y bottom straight edge; Z=0 at one broad face; solid spans Z0..2','features':rows},indent=2)+'\n')
report={'part_number':stem,'source_revision':REV,'checks':'PASS','solid_count':1,'extent_mm':[bb.xlen,bb.ylen,bb.zlen],
 'volume_mm3':solid.Volume(),'net_mass_kg_at_7900_kg_m3':solid.Volume()*7.9e-6,
 'plain_fan_holes':16,'plain_radiator_holes':12,'rack_slots':40,'air_apertures':4,'front_face_boundary_wires':73,'through_wall_cylinders':len(cyl),'edge_notches':int(notched),
 'drawing_has_unmodelled_edge_breaks':True,'nominal_geometry_unchanged':True,'outer_corner_radius_mm':P['outer_radius'],'geometry_comparison_basis':'Production issue matches selected geometry revision',
 'source_step_sha256':hashlib.sha256((source/f'rack-plate-{REV}.step').read_bytes()).hexdigest(),
 'production_step_sha256':hashlib.sha256((OUT/f'{stem}.step').read_bytes()).hexdigest(),
 'DFM':'Flatness and specified edge finishes require supplier acceptance; size/position tolerances follow the selected issue drawing.'}
assert report['source_step_sha256']==report['production_step_sha256']
(OUT/'geometry-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
