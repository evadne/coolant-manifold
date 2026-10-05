"""Accepted Q: add four rear G1/4 ports to the retained P solid.
Thread cylinders are tap pilots, never finished plain holes. Millimetres.
"""
import json, math, hashlib, shutil
from pathlib import Path
import cadquery as cq
ROOT=Path(__file__).resolve().parents[1]
p=json.loads((ROOT/'cad/iterations/Q-rear-ports.json').read_text())
base=ROOT/'output/long-bore-P/cad';out=ROOT/'output/long-bore-Q/cad';mesh=ROOT/'output/long-bore-Q/meshes'
out.mkdir(parents=True,exist_ok=True);mesh.mkdir(parents=True,exist_ok=True)
parent=json.loads((ROOT/'cad/iterations/P-long-bore.json').read_text())
W,D,H=(parent[k] for k in ('body_width','body_depth','body_height'))
assert (W,D,H)==(410,40,87)
body=cq.importers.importStep(str(base/'body.step')).val();original=body
face=cq.importers.importStep(str(base/'faceplate.step')).val()
wet=[cq.importers.importStep(str(base/f'fluid-network-{i}.step')).val() for i in (1,2)]
positions=[(x,D,z) for x in p['rear_port_columns_x_mm'] for z in parent['port_rows_z']]
R=parent['tap_drill_diameter']/2;point=R/math.tan(math.radians(parent['front_drill_point_angle']/2))
axis=cq.Vector(0,-1,0);checks=[]
for x,y,z in positions:
 idx=parent['port_rows_z'].index(z)
 bore=cq.Solid.makeCylinder(R,D-parent['gallery_axis_y'],cq.Vector(x,y,z),axis)
 tip=cq.Solid.makeCone(R,0,point,cq.Vector(x,parent['gallery_axis_y'],z),axis)
 entry=cq.Solid.makeCone(p['entry_mouth_diameter_mm']/2,R,p['entry_depth_mm'],cq.Vector(x,y,z),axis)
 void=bore.fuse(tip).fuse(entry)
 assert void.intersect(wet[idx]).Volume()>1
 assert void.intersect(wet[1-idx]).Volume()<1e-7
 # Threads must end before entering the longitudinal gallery: entry + full form.
 thread=cq.Solid.makeCylinder(parent['thread_major_diameter']/2,p['entry_depth_mm']+p['full_thread_depth_after_entry_mm'],cq.Vector(x,y,z),axis)
 gallery=cq.Solid.makeCylinder(R,W,cq.Vector(-W/2,parent['gallery_axis_y'],z),cq.Vector(1,0,0))
 assert thread.distance(gallery)>2
 assert min(W/2-abs(x),z,H-z)-p['seal_land_diameter_mm']/2>0
 body=body.cut(void);wet[idx]=wet[idx].fuse(void)
 checks.append(dict(centre_xyz_mm=[x,y,z],thread_end_to_gallery_mm=thread.distance(gallery)))
# User requested shorter M4 threads and pilots during Q manufacturing review.
# Fill only the old pilot tail, then form the new 118-degree tip at full depth 13.
F=parent['faceplate_fastener'];m4point=1.65/math.tan(math.radians(59))
new_depth=p['M4_retention']['pilot_full_diameter_depth_mm'];added=0
for x,z in parent['faceplate_mounts_xz']:
    old_tail=cq.Solid.makeCylinder(1.65,F['pilot_depth']-new_depth,cq.Vector(x,new_depth,z),cq.Vector(0,1,0)).fuse(cq.Solid.makeCone(1.65,0,m4point,cq.Vector(x,F['pilot_depth'],z),cq.Vector(0,1,0)))
    new_tip=cq.Solid.makeCone(1.65,0,m4point,cq.Vector(x,new_depth,z),cq.Vector(0,1,0))
    body=body.fuse(old_tail).cut(new_tip);added+=old_tail.Volume()-new_tip.Volume()
body=body.clean()
assert body.isValid() and len(body.Solids())==1
assert all(v.isValid() and len(v.Solids())==1 for v in wet)
assert wet[0].intersect(wet[1]).Volume()<1e-7
assert body.intersect(face).Volume()<1e-7
# Match every pre-existing opening; changes are confined to four rear drill envelopes.
assert abs(body.cut(original).Volume()-added)<1e-5
F=parent['faceplate_fastener'];m4point=1.65/math.tan(math.radians(59))
clear=min(cq.Solid.makeCylinder(2,new_depth+m4point,cq.Vector(x,0,z),cq.Vector(0,1,0)).distance(v)
          for x,z in parent['faceplate_mounts_xz'] for v in wet)
assert clear>2
cq.exporters.export(body,str(out/'body.step'));shutil.copyfile(base/'faceplate.step',out/'faceplate.step')
cq.exporters.export(body,str(mesh/'body.stl'),tolerance=.025,angularTolerance=.06)
cq.exporters.export(face,str(mesh/'faceplate.stl'),tolerance=.025,angularTolerance=.06)
for i,v in enumerate(wet,1):
 cq.exporters.export(v,str(out/f'fluid-network-{i}.step'))
 cq.exporters.export(v,str(mesh/f'fluid-network-{i}.stl'),tolerance=.04,angularTolerance=.12)
assy=cq.Assembly(name='RM10_Q_four_rear_ports');assy.add(body,name='POM_Q');assy.add(face,name='unchanged_P_faceplate');assy.export(str(out/'manifold-assembly.step'))
# Reuse P fitting envelopes only for explicit nominal clearance checks.
rear_keepouts=[cq.Solid.makeCylinder(p['rear_fitting_keepout_diameter_mm']/2,80,cq.Vector(*v),cq.Vector(0,1,0)) for v in positions]
# Existing side elbow reference solids are available in the assembly STEP.
side_assembly=cq.importers.importStep(str(base/'elbow-envelope-assembly.step')).solids().vals()
side=[s for s in side_assembly if s.BoundingBox().xlen<60]
assert len(side)==4
side_gap=min(r.distance(s) for r in rear_keepouts for s in side)
assert side_gap>0
report=dict(revision='Q',status='Operator-approved Q geometry; supplier issue Q-M01',front_ports=20,side_ports=4,rear_ports=4,total_G1_4_ports=28,
 wet_networks=2,rear_bosses=0,rear_cover=False,body_slab_depth_mm=D,overall_POM_depth_mm=D+parent['port_boss_height'],
 rear_port_details=checks,rear_full_diameter_pilot_depth_mm=D-parent['gallery_axis_y'],rear_drill_tip_Y_mm=parent['gallery_axis_y']-point,
 M4_full_thread_after_entry_mm=10,M4_pilot_full_diameter_depth_mm=new_depth,M4_reference_screw_length_mm=10,M4_drill_tip_depth_mm=new_depth+m4point,
 full_thread_depth_after_entry_mm=p['full_thread_depth_after_entry_mm'],rear_thread_envelope_depth_from_face_mm=p['entry_depth_mm']+p['full_thread_depth_after_entry_mm'],
 removed_POM_volume_mm3=original.Volume()-body.Volume(),minimum_M4_to_wet_network_mm=clear,
 rear_seal_land_edge_margin_min_mm=min(min(W/2-abs(x),z,H-z)-p['seal_land_diameter_mm']/2 for x,y,z in positions),
 rear_fitting_keepout_diameter_mm=p['rear_fitting_keepout_diameter_mm'],rear_keepout_to_side_elbow_envelope_min_mm=side_gap,
 rear_fitting_row_gap_mm=40-p['rear_fitting_keepout_diameter_mm'],plugged_equipment_width_mm=W+8,
 faceplate_identical_to_P=True,checks='PASS: valid solid; two isolated networks; four rear branches join corresponding galleries; dry M4s and seal lands; nominal fitting envelopes clear',
 scope='Accepted layout; matching Q-M01 drawings specify machining. STEP thread cylinders are tap pilots. Fitting envelopes are nominal; exact hardware, hose bends and loads not qualified.',
 source_sha256={str(path.relative_to(ROOT)):hashlib.sha256(path.read_bytes()).hexdigest() for path in [ROOT/'cad/iterations/Q-rear-ports.json',ROOT/'cad/iterations/P-long-bore.json',ROOT/'scripts/build_revision_Q.py',base/'body.step',base/'faceplate.step',base/'fluid-network-1.step',base/'fluid-network-2.step',base/'elbow-envelope-assembly.step']})
(out/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
