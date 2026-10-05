"""Derive O-M02 supplier solids without changing approved Revision O.
Add the specified boss edge chamfers and conventional M4 drill/entry geometry.
Threads remain tapping pilots, per JLCCNC's upload instructions.
"""
from pathlib import Path
import math, shutil, hashlib
import revision_json as json
import cadquery as cq
ROOT=Path(__file__).resolve().parents[1]
p=json.loads((ROOT/'cad/iterations/O-long-bore.json').read_text())
f=json.loads((ROOT/'cad/manufacturing/O-M02.json').read_text())
out=ROOT/'output/manufacturing/O-M02';out.mkdir(parents=True,exist_ok=True)
source=ROOT/'output/long-bore-O/cad'
body=cq.importers.importStep(str(source/'body.step'))
# Shorten only the projecting bosses; the 40 mm slab and R1 roots are preserved.
height=f['boss_height']
assert height == p['faceplate_thickness'] + f['boss_projection_above_plate']
body=body.cut(cq.Solid.makeBox(600,p['port_boss_height']-height,100,cq.Vector(-300,-p['port_boss_height'],-5)))
# Restore each G1/4 entry on the new sealing plane.
for z in p['port_rows_z']:
    for x in [-180+40*i for i in range(10)]:
        body=body.cut(cq.Solid.makeCone(6.9,5.9,1,cq.Vector(x,-height,z),cq.Vector(0,1,0)))
original_volume=body.val().Volume()
edges=[e for e in body.val().Edges() if e.geomType()=='CIRCLE' and abs(e.Center().y+height)<1e-6 and abs(e.radius()-14)<1e-6]
assert len(edges)==20
body=body.newObject(edges).chamfer(f['boss_outer_chamfer'])
removed_boss_volume=original_volume-body.val().Volume()
expected=20*math.pi*(14*.5**2-.5**3/3)
print("Boss chamfer removed / expected volume:", removed_boss_volume, expected)
assert abs(removed_boss_volume-expected)<0.02
pilot_r=p['faceplate_fastener']['tap_drill_diameter']/2
entry_r=f['m4_entry_diameter']/2
point=pilot_r/math.tan(math.radians(f['m4_drill_point_included_angle']/2))
for x,z in p['faceplate_mounts_xz']:
    body=body.cut(cq.Solid.makeCone(entry_r,pilot_r,entry_r-pilot_r,cq.Vector(x,0,z),cq.Vector(0,1,0)))
    body=body.cut(cq.Solid.makeCone(pilot_r,0,point,cq.Vector(x,14,z),cq.Vector(0,1,0)))
assert body.val().isValid() and len(body.val().Solids())==1
plate=cq.importers.importStep(str(source/'faceplate.step'))
assert body.val().intersect(plate.val()).Volume()<1e-6
networks=[cq.importers.importStep(str(source/f'fluid-network-{i}.step')).val() for i in (1,2)]
assert networks[0].intersect(networks[1]).Volume()<1e-6
# Conservative envelope: nominal M4 major diameter continued through nominal drill-tip depth.
clearance=min(cq.Solid.makeCylinder(2,14+point,cq.Vector(x,0,z),cq.Vector(0,1,0)).distance(wet) for x,z in p['faceplate_mounts_xz'] for wet in networks)
assert clearance>2
assert abs(body.val().BoundingBox().xlen-410)<1e-6
assert abs(body.val().BoundingBox().ylen-(40+height))<1e-6
assert abs(body.val().BoundingBox().zlen-87)<1e-6
cq.exporters.export(body,str(out/'RM10-O-M02-BODY.step'))
shutil.copyfile(source/'faceplate.step',out/'RM10-O-M02-FACEPLATE.step')
shutil.copyfile(source/'faceplate-flat.dxf',out/'RM10-O-M02-FACEPLATE.dxf')
# Unambiguous machining feature schedule: signed X from width midplane B, Z from bottom C.
xs=[-180+40*i for i in range(10)]
ports=[{'id':f'P{i+1:02d}','x':x,'z':z,'thread':'G 1/4 ISO 228-1','full_thread_length_min':8} for i,(z,x) in enumerate((z,x) for z in p['port_rows_z'] for x in xs)]
mounts=[dict(id=f'F{i+1}',x=x,z=z,thread='M4 x 0.7 - 6H',full_thread_length_min=10) for i,(x,z) in enumerate(p['faceplate_mounts_xz'])]
ends=[dict(id=f'E{i+1}',side=side,x=x,y=20,z=z,thread='G 1/4 ISO 228-1',full_thread_length_min=8) for i,(side,x,z) in enumerate((side,x,z) for side,x in [('LEFT',-205),('RIGHT',205)] for z in p['port_rows_z'])]
slots=[dict(id=f'R{i+1:02d}',x=x,z=z,length=10,width=7) for i,(x,z) in enumerate((x,z) for x in (-232.55,232.55) for z in p['rack_slot_centres_z'])]
schedule=dict(manufacturing_revision='O-M02',datums='A: POM mounting plane Y0 / plate POM-side plane Y0; B: width midplane X0; C: bottom Z0',front_ports=ports,body_fixings=mounts,end_ports=ends,rack_slots=slots)
(out/'feature-schedule.json').write_text(json.dumps(schedule,indent=2)+'\n')
# Worst-size root fit, with ±0.10 coordinate deviations independently in X and Z on each part.
root_max=28.1+2*1.1
coordinate_offset=math.hypot(.2,.2)
root_gap=(32-root_max)/2-coordinate_offset
assert root_gap>.5
report=dict(manufacturing_revision='O-M02',approved_source_sha256=hashlib.sha256((source/'body.step').read_bytes()).hexdigest(),
    boss_height_mm=height,boss_projection_above_plate_mm=height-3,modified_body_valid=True,body_volume_mm3=body.val().Volume(),boss_chamfers=20,m4_entry_chamfers=6,m4_drill_points=6,
    m4_total_pilot_depth_mm=14+point,conservative_M4_envelope_to_wet_network_mm=clearance,
    tapped_body_holes_total=30,front_G14=20,end_G14=4,M4=6,faceplate_tapped_holes=0,
    faceplate_windows=20,faceplate_clearance_holes=6,faceplate_countersinks=6,faceplate_rack_slots=12,
    faceplate_unchanged_from_approved_O=True,boss_nominal_radial_gap_mm=2,root_max_envelope_mm=root_max,
    root_min_radial_gap_before_location_mm=(32-root_max)/2,root_min_gap_with_stated_coordinate_stack_mm=root_gap,
    fit_scope='Coordinate stack assumes aligned A/B/C assembly frames; not thermal growth, screw-clearance registration or deformation. Assembly trial required.',
    CAD_exceptions='Thread helices not modelled. General external edge deburring not modelled. Functional boss and port-entry chamfers and M4 drill points are modelled.')
(out/'geometry-verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
