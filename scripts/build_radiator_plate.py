"""Build R1 plate, export matching STEP/DXF/STL and check geometry and loads.

CAD axes: X horizontal; Y upwards from bottom edge; Z plate thickness (0..3).
Run with the project's CadQuery .venv. Supplier radiator mesh is read-only evidence.
"""
from pathlib import Path
import json, math, hashlib, argparse
import cadquery as cq
import ezdxf
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--revision',choices=['R1','R2'],default='R1')
REV=parser.parse_args().revision
P = json.loads((ROOT/f'cad/radiator/{REV}.json').read_text())
OUT = ROOT/f'output/radiator-{REV}'
OUT.mkdir(parents=True, exist_ok=True)
W,H,T = (P[k] for k in ('width','height','thickness'))
mounts = [(x,H/2+y) for x in P['radiator_mount_x'] for y in P['radiator_mount_y_from_centre']]
slots = [(x,y) for x in P['rack_mount_x'] for y in P['rack_mount_y']]
windows = [(x,H/2+y) for x in P['aperture_centres_x'] for y in P['aperture_centres_y_from_centre']]

def rounded(x,y,w,h,r,depth):
    return cq.Workplane('XY').center(x,y).rect(w,h).extrude(depth).edges('|Z').fillet(r)

plate = rounded(0,H/2,W,H,P['outer_radius'],T)
for x,y in windows:
    plate = plate.cut(rounded(x,y,P['aperture_width'],P['aperture_height'],P['aperture_radius'],T))
for x,y in mounts:
    plate = plate.cut(cq.Workplane('XY').center(x,y).circle(P['radiator_clearance_diameter']/2).extrude(T))
for x,y in slots:
    plate = plate.cut(cq.Workplane('XY').center(x,y).slot2D(P['rack_slot_length'],P['rack_slot_width']).extrude(T))
solid=plate.val()
assert solid.isValid() and len(solid.Solids())==1
for ext in ('step','stl'):
    cq.exporters.export(plate,str(OUT/f'rack-plate-{REV}.{ext}'))

# Exact arcs and closed cut contours, rather than a tessellated DXF.
doc=ezdxf.new('R2010'); doc.units=4; doc.layers.new('CUT'); ms=doc.modelspace()
def rr(x,y,w,h,r):
    l,b=x-w/2,y-h/2; rt,tp=x+w/2,y+h/2; q=math.tan(math.pi/8)
    pts=[(l+r,b,0),(rt-r,b,q),(rt,b+r,0),(rt,tp-r,q),
         (rt-r,tp,0),(l+r,tp,q),(l,tp-r,0),(l,b+r,q)]
    ms.add_lwpolyline(pts,format='xyb',close=True,dxfattribs={'layer':'CUT'})
rr(0,H/2,W,H,P['outer_radius'])
for x,y in windows: rr(x,y,P['aperture_width'],P['aperture_height'],P['aperture_radius'])
for x,y in mounts: ms.add_circle((x,y),P['radiator_clearance_diameter']/2,dxfattribs={'layer':'CUT'})
for x,y in slots:
    r=P['rack_slot_width']/2; a=(P['rack_slot_length']-P['rack_slot_width'])/2
    ms.add_lwpolyline([(x-a,y-r,0),(x+a,y-r,1),(x+a,y+r,0),(x-a,y+r,1)],format='xyb',close=True,dxfattribs={'layer':'CUT'})
doc.saveas(OUT/f'rack-plate-{REV}.dxf')
dx=ezdxf.readfile(OUT/f'rack-plate-{REV}.dxf'); assert not dx.audit().has_errors
assert len(dx.modelspace().query('CIRCLE'))==12
assert len(dx.modelspace().query('LWPOLYLINE'))==5+len(slots)
assert all(e.closed for e in dx.modelspace().query('LWPOLYLINE'))

def area_rr(w,h,r): return w*h-(4-math.pi)*r*r
aperture_area=4*area_rr(P['aperture_width'],P['aperture_height'],P['aperture_radius'])
area=area_rr(W,H,P['outer_radius'])-aperture_area
area-=len(mounts)*math.pi*(P['radiator_clearance_diameter']/2)**2
area-=len(slots)*((P['rack_slot_length']-P['rack_slot_width'])*P['rack_slot_width']+math.pi*(P['rack_slot_width']/2)**2)
assert abs(solid.Volume()-area*T)<1e-4
reloaded=cq.importers.importStep(str(OUT/f'rack-plate-{REV}.step')).val()
assert reloaded.isValid() and abs(reloaded.Volume()-area*T)<1e-4
assert np.allclose([reloaded.BoundingBox().xlen,reloaded.BoundingBox().ylen,reloaded.BoundingBox().zlen],[W,H,T])
for x,y in mounts:
    assert solid.isInside((x+P['radiator_clearance_diameter']/2+.05,y,T/2))
    assert not solid.isInside((x,y,T/2))
    for wx,wy in windows:
        dx=max(abs(x-wx)-P['aperture_width']/2,0)
        dy=max(abs(y-wy)-P['aperture_height']/2,0)
        assert math.hypot(dx,dy)-P['radiator_clearance_diameter']/2 >= 7.69

# Verify all 12 structural attachment pilots in supplier mesh at the plate seat.
reference=ROOT/'docs/references/alphacool-14351-manufacturer.stl'
raw=reference.read_bytes()
tri=np.frombuffer(raw,np.dtype([('n','<f4',3),('v','<f4',(3,3)),('a','<u2')]),offset=84)['v']
v=tri.reshape(-1,3); pilot_evidence=[]
for x,y in mounts:
    z=y-H/2+212 # supplier mesh uses z=212 as radiator centre
    nearby=v[(abs(v[:,1]+22.5)<.002)&(abs(v[:,0]-x)<1.3)&(abs(v[:,2]-z)<1.3)]
    radius=np.sqrt((nearby[:,0]-x)**2+(nearby[:,2]-z)**2)
    assert np.count_nonzero(abs(radius-1.23)<.015)>=12,(x,z)
    pilot_evidence.append([x,z])

if REV=='R2':
    assert abs(H/44.45-10)<1e-9 and len(slots)==40
    assert all(any(abs((y%44.45)-o)<1e-7 for o in [6.35,38.1]) for x,y in slots)

mass=solid.Volume()*P['density_kg_m3']/1e9
payload=P['radiator_mass_kg']+P['additional_load_kg']; total=payload+mass
g=9.80665; moment=payload*g*P['assumed_load_cg_behind_plate_mm']/1000
span=max(P['rack_mount_y'])-min(P['rack_mount_y'])
report={
 'revision':REV,'geometry_checks':'PASS', 'plate_volume_mm3':solid.Volume(),
 'plate_mass_kg':mass,'radiator_plus_allowance_kg':payload,'total_rack_mass_kg':total,
 'payload_force_N':payload*g,'total_rack_force_N':total*g,
 'airflow_aperture_area_mm2':aperture_area,'open_fraction_of_400mm_square':aperture_area/160000,
 'minimum_mount_hole_to_aperture_ligament_mm':7.7,
 'rack_slot_outer_edge_ligament_mm':W/2-max(P['rack_mount_x'])-P['rack_slot_length']/2,
 'radiator_mount_count':len(mounts),'rack_slot_count':len(slots),
 'manufacturer_pilot_centres_xz':pilot_evidence,'manufacturer_mesh_sha256':hashlib.sha256(raw).hexdigest(),
 'statics_assumptions':f'Stationary vertical rack; payload CG {P["assumed_load_cg_behind_plate_mm"]} mm behind plate; symmetric load sharing; no shock or hose loads.',
 'eccentric_payload_moment_Nm':moment,
 'four_corner_rack_screws_average_shear_N':total*g/4,
 'four_corner_rack_screws_top_pair_total_tension_N':moment/(span/1000),
 'twelve_radiator_screws_average_shear_N':payload*g/12,
 'same_profile_bending_stiffness_ratio_to_1p5mm':(T/1.5)**3,
 'limits':'Statics and CAD checks only. No assembly stiffness, screw pull-out, vibration or load rating qualification.'}
(OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
