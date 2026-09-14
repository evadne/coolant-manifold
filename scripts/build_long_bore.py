"""Separate revision H: two through-drilled galleries, four G1/4 end plugs.

Preserves revision G files. Threads are pilot/envelope call-outs, not helices.
"""
from pathlib import Path
import json
import math
import shutil
import cadquery as cq
ROOT=Path(__file__).resolve().parents[1]
P=json.loads((ROOT/'cad/iterations/H-long-bore.json').read_text())
OUT=ROOT/'output/long-bore-H/cad';OUT.mkdir(parents=True,exist_ok=True)
MESH=ROOT/'tmp/mesh-long-bore-H';MESH.mkdir(parents=True,exist_ok=True)
W,D,H=P['body_width'],P['body_depth'],P['body_height']
T=P['faceplate_thickness'];BH=P['port_boss_height'];F=P['faceplate_fastener']
R=P['gallery_diameter']/2;Y=P['gallery_axis_y'];rows=P['port_rows_z']
xs=[(i-P['branch_count']/2)*P['port_pitch'] for i in range(P['branch_count']+1)]

def box(w,d,h,x=0,y=0,z=0):
 return cq.Workplane('XY').box(w,d,h,centered=(True,False,False)).translate((x,y,z))
def cyl(r,l,pos,axis):
 return cq.Workplane(obj=cq.Solid.makeCylinder(r,l,cq.Vector(*pos),cq.Vector(*axis)))
def vol(s):return sum(v.Volume() for v in s.solids().vals())

body=box(W,D,H)
for z in rows:
 for x in xs:body=body.union(cyl(P['port_boss_diameter']/2,BH,(x,-BH,z),(0,1,0)))
roots=[e for e in body.val().Edges() if e.geomType()=='CIRCLE' and abs(e.Center().y)<1e-6]
assert len(roots)==18
body=body.newObject(roots).fillet(P['port_boss_root_radius'])
fluids=[];channels=[];side_ports=[]
point_length=P['tap_drill_diameter']/2/math.tan(math.radians(P['front_drill_point_angle']/2))
for z in rows:
 gallery=cyl(R,W,(-W/2,Y,z),(1,0,0));channels.append(gallery)
 fluid=gallery
 for x in xs:
  length=P['front_drill_cylinder_end_y']+BH
  bore=cyl(P['tap_drill_diameter']/2,length,(x,-BH,z),(0,1,0))
  tip=cq.Workplane(obj=cq.Solid.makeCone(P['tap_drill_diameter']/2,0,point_length,cq.Vector(x,P['front_drill_cylinder_end_y'],z),cq.Vector(0,1,0)))
  mouth=cq.Workplane(obj=cq.Solid.makeCone(6.9,P['tap_drill_diameter']/2,1,cq.Vector(x,-BH,z),cq.Vector(0,1,0)))
  fluid=fluid.union(bore).union(tip).union(mouth)
 for sign in (-1,1):
  start=(sign*W/2,Y,z);axis=(-sign,0,0)
  entry=cq.Workplane(obj=cq.Solid.makeCone(P['side_entry_mouth_diameter']/2,R,P['side_entry_chamfer_depth'],cq.Vector(*start),cq.Vector(*axis)))
  fluid=fluid.union(entry);side_ports.append((sign*W/2,Y,z))
 body=body.cut(fluid);fluids.append(fluid)

face=box(P['rack_width'],T,H,y=-T)
for z in rows:
 for x in xs:face=face.cut(cyl(P['faceplate_port_clearance']/2,T+.2,(x,-T-.1,z),(0,1,0)))
rack_z=[6.35-(88.9-H)/2,82.55-(88.9-H)/2]
for sign in (-1,1):
 for z in rack_z:
  face=face.cut(cq.Workplane('XZ',origin=(sign*P['rack_hole_pitch']/2,.1,z)).slot2D(P['rack_slot_length'],P['rack_slot_width']).extrude(T+.2))
for x,z in P['faceplate_mounts_xz']:
 face=face.cut(cyl(F['clearance_diameter']/2,T+.1,(x,-T,z),(0,1,0)))
 face=face.cut(cq.Solid.makeCone(F['countersink_diameter']/2,F['clearance_diameter']/2,(F['countersink_diameter']-F['clearance_diameter'])/2,cq.Vector(x,-T,z),cq.Vector(0,1,0)))
 body=body.cut(cyl(F['tap_drill_diameter']/2,F['pilot_depth'],(x,0,z),(0,1,0)))

plug_spec=P['side_plug_reference'];plugs=[]
for x,y,z in side_ports:
 sign=1 if x>0 else -1
 head=cyl(plug_spec['head_diameter']/2,plug_spec['head_projection'],(x,y,z),(sign,0,0))
 # Clearance-sized shank only: avoids false interference with pilot-model female threads.
 shank=cyl(R,plug_spec['thread_length'],(x,y,z),(-sign,0,0))
 plug=head.union(shank)
 socket=(cq.Workplane('YZ',origin=(x+sign*(plug_spec['head_projection']+.1),y,z))
         .polygon(6,2*plug_spec['socket_across_flats']/math.sqrt(3)).extrude(-sign*2.1))
 plug=plug.cut(socket)
 assert plug.val().isValid()
 plugs.append(plug)

# Manufacturing solids and connected fluid topology.
assert all(s.val().isValid() and len(s.solids().vals())==1 for s in [body,face]+fluids)
assert vol(fluids[0].intersect(fluids[1]))<1e-6
assert vol(body.intersect(face))<1e-6
assert P['gallery_diameter']<=P['tap_drill_diameter']
assert P['side_thread_full_depth']>plug_spec['thread_length']
assert Y+R<D and Y-R>F['pilot_depth']
assert min(rows[0]-R,H-rows[1]-R)>0
assert rows[1]-rows[0]>2*R
assert BH-T==3 and len(side_ports)==4
# Every branch opens to its intended continuous gallery, without requiring a group jumper.
for z,gallery,fluid in zip(rows,channels,fluids):
 for x in xs:
  bore=cyl(P['tap_drill_diameter']/2,P['front_drill_cylinder_end_y']+BH,(x,-BH,z),(0,1,0))
  assert vol(bore.intersect(gallery))>1
  usable=cyl(P['thread_major_diameter']/2,P['thread_full_depth'],(x,-BH,z),(0,1,0))
  assert vol(usable.intersect(gallery))<1e-6
  keepout=cyl(P['port_hardware_keepout_diameter']/2,12,(x,-BH,z),(0,-1,0))
  assert vol(keepout.intersect(face))<1e-6
mount_clearance=min(cyl(F['nominal_diameter']/2,F['pilot_depth'],(x,0,z),(0,1,0)).val().distance(fluid.val()) for x,z in P['faceplate_mounts_xz'] for fluid in fluids)
assert mount_clearance>2
for i,plug in enumerate(plugs):
 assert vol(plug.intersect(body))<1e-5
 assert vol(plug.intersect(face))<1e-5
 for other in plugs[i+1:]:assert vol(plug.intersect(other))<1e-6
# Entire flat side seal land fits the POM side, clear of front/rear edges.
assert P['side_seal_land_diameter']/2<min(Y,D-Y,rows[0],H-rows[-1])
# Conservative plug-thread envelope stays clear of the first front branch on each end.
plug_to_branch=(W/2-max(abs(x) for x in xs))-plug_spec['thread_length']-P['thread_major_diameter']/2
assert plug_to_branch>20

assy=cq.Assembly(name='RM8_2U_revision_H_long_bore')
for name,part,col in [('body',body,(.025,.03,.035)),('faceplate',face,(.5,.53,.56))]:
 cq.exporters.export(part,str(OUT/f'{name}.step'))
 cq.exporters.export(part,str(MESH/f'{name}.stl'),tolerance=.06,angularTolerance=.12)
 assy.add(part,name=name,color=cq.Color(*col))
for i,plug in enumerate(plugs):
 cq.exporters.export(plug,str(MESH/f'side_plug_{i}.stl'),tolerance=.04,angularTolerance=.12)
 assy.add(plug,name=f'REFERENCE_side_plug_{i+1}',color=cq.Color(.6,.62,.64))
assy.export(str(OUT/'manifold-assembly.step'))
# Separate technical cutaway, explicitly a section rather than a milled pocket design.
cutaway=body.cut(box(W+2,D-Y+1,H+2,y=Y,z=-1))
assert cutaway.val().isValid()
cq.exporters.export(cutaway,str(MESH/'body-section.stl'),tolerance=.06,angularTolerance=.12)
for i,v in enumerate(fluids):cq.exporters.export(v,str(OUT/f'fluid-network-{i+1}.step'))
# The unchanged dry front plate is checked against G before reusing its cut profile.
gface=cq.importers.importStep(str(ROOT/'output/cad/faceplate.step'))
assert vol(face.cut(gface))+vol(gface.cut(face))<1e-5
shutil.copyfile(ROOT/'output/cad/faceplate-flat.dxf',OUT/'faceplate-flat.dxf')
area=math.pi*R*R;old_area=16*24
report={'revision':'H','parent_tag':P['parent_tag'],'wet_networks':2,'front_G1_4_ports':18,'side_G1_4_ports':4,'initial_side_plugs':4,
 'manufactured_parts':2,'rear_plate':False,'large_gallery_O_rings':0,'plug_face_seals_required':4,'front_mount_screws_M4':8,'rear_screws':0,
 'body_envelope_mm':[W,D,H],'rack_assembly_envelope_without_front_QDs_mm':[P['rack_width'],D+BH,H],
 'gallery_diameter_mm':2*R,'gallery_axis_y_mm':Y,'gallery_length_mm':W,'gallery_area_mm2':area,'previous_gallery_area_mm2':old_area,
 'same_local_flow_velocity_ratio_H_to_G':old_area/area,'nominal_full_bore_L_over_D':W/(2*R),
 'opposed_drill_nominal_reach_with_overlap_mm':(W+P['opposed_drill_overlap'])/2,
 'opposed_drill_L_over_D':(W+P['opposed_drill_overlap'])/(4*R),
 'front_wall_to_gallery_mm':Y-R,'rear_wall_mm':D-Y-R,'inter_gallery_web_mm':rows[1]-rows[0]-2*R,
 'front_drill_tip_y_mm':P['front_drill_cylinder_end_y']+point_length,'M4_thread_envelope_to_wet_network_min_mm':mount_clearance,
 'side_plug_to_nearest_front_thread_envelope_mm':plug_to_branch,'body_volume_mm3':vol(body),
 'checks':['valid connected solids','two separated uninterrupted fluid networks','all eighteen front ports intersect intended gallery','four side mouths and plug positions','front usable threads precede gallery breakthrough','M4 mounts clear wet networks','no overlap of plugs with pilot-represented body or faceplate','side seal lands within POM face','front plate geometrically identical to G','raised port fitting keep-outs clear steel'],
 'limitations':['Deep drilling exceeds ordinary 10D guidance even from both ends; manual vendor DFM required','Nominal straight cylinder does not simulate drill wander or opposed-bore mismatch','Plugs are provisional envelopes; seal footprint and thread length need confirmation','No pressure, thermal, creep or hydraulic qualification','BSPP thread helices and plug face seals not modelled']}
(OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
(ROOT/'tmp/scene-long-bore-H.json').write_text(json.dumps({'parameters':dict(P,mounting='faceplate'),'ports_x':xs,'cover_bolts':[],'faceplate_mounts':P['faceplate_mounts_xz'],'side_plugs':side_ports},indent=2)+'\n')
print(json.dumps(report,indent=2))
